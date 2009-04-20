#!/usr/bin/perl

use lib qw(/usr/lib/libDrakX);
use File::FnMatch;
use MDK::Common;
use list_modules;
use modalias;

#- known bugs:
#- o does not match subvendors, they have to be handled on a case-by-case basis
#- o does not match PCI class (thus ahci won't match jmicron devices)

my @ignored_modules = (
    "intelfb", "savagefb", "tdfxfb", qr/_agp$/,
    qr/_rng$/,
);
my @preferred_modules = (
    "pata_marvell", #- prefer over ahci since ahci need marvel_enabled=1 to make it work (#43975)
    "bcm43xx", #- prefer over b43, b43legacy and ssb
    "dpt_i2o", #- prefer over i2o_core
    "dmfe", #- prefer over tulip, it only lists supported devices
    "c4", #- subvendors listed in c4 driver seems not to be supported by DAC960
    "i2c_viapro", #- prefer over via686a
    "ipr", #- subvendors listed in ipr driver seems not to be supported by DAC960
    "mxser_new", #- experimental clone of mxser
    "prism54", #- prefer over p54pci
    "ipw3945", #- prefer over iwl3945, which has some stability/performance issues
    "rt2400", "rt2500", "rt2570", "rt61", "rt73", #- prefer legacy Ralink drivers
    "skge", #- prefer over sk98lin
    qr/^snd_/, #- prefer alsa drivers
    "sx", #- prefer over specialix (sx matches subvendors)
);
my @depreciated_modules = (
    #- defer *piix over ahci (install will still try both ahci and ata_piix), depends on BIOS settings
    #-   do it without explicitely listing ahci in preferred modules,
    #-   to allow ahci to be overriden by pata_marvell
    #- ata_piix will still be preferred over piix, because ata_piix is in the disk/sata preferred category
    "ata_piix", "piix",
    "gspca", #- kernel hackers value it as poorly coded
    "ir_usb", #- false positive because of pattern
    "usb_storage", #- false positive because we don't use subvendors/subdevices
    "snd_usb_audio", #- prefer video camera drivers if any
);
my @preferred_categories = (
    "disk/sata",
    "disk/scsi",
);
#- For the following categories, the deferred modules are ignored, and
#- an explicit alias is set even if only one module match exactly.
#- This allows to workaround modules having class wildcards, which isn't supported.
my %category_deferred_modules = (
    #- prefer full implementation or "generic" libata module, not old IDE generic module
    "disk/ide" => [ "ide_pci_generic" ],
    "disk/sata" => [ "ata_generic", "pata_acpi" ],
    "input/tablet" => [ "usbmouse" ],
);

sub build_modalias {
    my ($class, $vendor, $device) = @_;
    {
        pci => "pci:v0000${vendor}d0000${device}sv*sd*bc*i*",
        usb => "usb:v${vendor}p${device}d*dc*dsc*dp*ic*isc*ip*",
    }->{$class};
}

sub match_module {
    my ($module, $pattern) = @_;
    ref $pattern eq 'Regexp' ? $module =~ $pattern : $module eq $pattern;
}

sub grep_non_matching {
    my ($modules, $list) = @_;
    grep {
        my $m = $_->[1];
        every { !match_module($m, $_) } @$list;
    } @$modules;
}

sub grep_matching {
    my ($modules, $list) = @_;
    grep {
        my $m = $_->[1];
        grep { match_module($m, $_) } @$list;
    } @$modules;
}

sub print_module {
    my ($modalias, $aliases, $class_other) = @_;
    my @aliases = group_by2(@$aliases);
    my @other = grep { File::FnMatch::fnmatch($_->[0], $modalias) } @$class_other;
    my @modules = uniq_ { $_->[1] } @aliases, @other;

    @modules or return;

    my @category_deferred_modules;
    foreach (map { list_modules::module2category($_->[1]) } @modules) {
        push @category_deferred_modules, @{$category_deferred_modules{$_} || []}
    }

    @modules > 1 || @category_deferred_modules or return;

    my @non_ignored = grep_non_matching(\@modules, [ @ignored_modules ]);
    if (@non_ignored == 1) {
        print "alias $modalias $non_ignored[0][1]\n";
        return;
    } elsif (@non_ignored == 0) {
        print "alias $modalias off\n";
        return;
    }

    @modules = @non_ignored;
    my @non_depreciated = grep_non_matching(\@modules, \@depreciated_modules);
    if (@non_depreciated == 1) {
        print "alias $modalias $non_depreciated[0][1]\n";
        return;
    }

    @modules = @non_depreciated if @non_depreciated > 1;
    my @preferred = grep_matching(\@modules, \@preferred_modules);
    @preferred or @preferred = grep { member(module2category($_->[1]), @preferred_categories) } @modules;
    if (@preferred == 1) {
        print "alias $modalias $preferred[0][1]\n";
        return;
    } else {
        my @non_deferred = grep_non_matching(\@modules, [ @category_deferred_modules ]);
        if (@non_deferred == 1) {
            print "alias $modalias $non_deferred[0][1]\n";
            return;
        }
    }

    print STDERR "unable to choose for $modalias " . join(" ", map { $_->[1] } @modules) . "\n";
}

my $alias_group = {};
modalias::parse_path($alias_group, "../lst/fallback-modules.alias");

foreach my $class (qw(pci pcmcia usb)) {
    my @class_other = group_by2(@{$alias_group->{$class}{other}});
    foreach my $vendor (sort(keys(%{$alias_group->{$class}}))) {
        $vendor eq "other" and next;
        foreach my $device (sort(keys(%{$alias_group->{$class}{$vendor}}))) {
            my $modalias = build_modalias($class, $vendor, $device);
            print_module($modalias, $alias_group->{$class}{$vendor}{$device}, \@class_other);
        }
    }
}
