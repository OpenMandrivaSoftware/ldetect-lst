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
    "ata_generic", #- prefer "generic" non-libata module or full implementation
    "intelfb", "savagefb", "tdfxfb", qr/_agp$/,
    qr/_rng$/,
);
my @preferred_modules = (
    "ahci", #- prefer over ata_piix (install will still try both), depends on BIOS settins
            #- do not prefer ata_piix, since it would override piix choice
    "bcm43xx", #- prefer over b43, b43legacy and ssb
    "dpt_i2o", #- prefer over i2o_core
    "dmfe", #- prefer over tulip, it only lists supported devices
    "c4", #- subvendors listed in c4 driver seems not to be supported by DAC960
    "i2c_viapro", #- prefer over via686a
    "ipr", #- subvendors listed in ipr driver seems not to be supported by DAC960
    "mxser_new", #- experimental clone of mxser
    "pata_netcell", "pata_ns87410", #- no non-libata implementation, prefer over generic module
    "prism54", #- prefer over p54pci
    "rt2400", "rt2500", "rt2570", "rt61", "rt73", #- prefer legacy Ralink drivers
    "skge", #- prefer over sk98lin
    qr/^snd_/, #- prefer alsa drivers
    "sx", #- prefer over specialix (sx matches subvendors)
);
my @depreciated_modules = (
    "generic", #- prefer full implementation
    "gspca", #- kernel hackers value it as poorly coded
    "ir_usb", #- false positive because of pattern
    qr/^pata_/, #- don't use libata drivers for now
    "usb_storage", #- false positive because we don't use subvendors/subdevices
);
my @preferred_categories = (
    "disk/ide",
    "disk/scsi",
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
    @modules > 1 or return;

    my @non_ignored = grep_non_matching(\@modules, \@ignored_modules);
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
