#!/usr/bin/perl

use MDK::Common;


@ignored_modules = (
qw(alsa ignore),
qw(tr bcm5700), # redhat have this, ignore it
);

if ($0 =~ /merge2pcitable/) 
{
    $ARGV[0] eq '-f' and $force = shift;
    $ARGV[0] eq '-a' and $all = shift;

    my $formats = join '|', grep {$_} map { /^read_(.*)/ ? $1 : '' } keys %main::;

    @ARGV == 3 or die "usage: $0 [-f] [-a] $formats <in_file> <mdk_pcitable>\n";

    ($format, $in, $pcitable) = @ARGV;

    my $read = $main::{"read_$format"} or die "unknown format $format (must be one of $formats)\n";
    my $d_pci = read_pcitable($pcitable);
    my $d_in = $read->($in);
    merge($d_pci, $d_in);
    cleanup_subids($d_pci);
    write_pcitable($d_pci);
} else { 1 }

sub dummy_module { 
    my ($m) = @_;
    $m =~ s/"(.*)"/$1/;
    member($m, @ignored_modules);
}

sub to_string {
    my ($id, $driver) = @_;
    my ($module, $text) = map { qq("$_") } @$driver;
    my ($id1, $id2, $subid1, $subid2) = map { "0x$_" } ($id =~ /(....)/g);
    join "\t", $id1, $id2, "$subid1 $subid2" ne "0xffff 0xffff" ? ($subid1, $subid2) : (), $module, $text;
}

# works for RedHat's pcitable old and new format, + mdk format (alike RedHat's old one)
# (the new format has ending .o's and double quotes are removed)
sub read_pcitable {
    my ($f) = @_;
    my %drivers;
    my $rm_quote = sub { s/^"//; s/"$//; $_ };
    my $line = 0;
    foreach (cat_($f)) {
	chomp; $line++;
	next if /^#/ || /^\s*$/;
	if (my ($id1, $id2, @l) = split /\t+/) {
	    my ($subid1, $subid2) = ('ffff', 'ffff');
	    ($subid1, $subid2, @l) = @l if @l == 4;
	    @l == 2 or die "$f $line: bad number of fields " . (int @l) . " (in $_)\n";
	    my ($module, $text) = @l;

	    my $class = $text =~ /(.*?)|/;
	    my $id1_ = $rm_quote->($id1);
	    if ($class{$id1_}) {
		print STDERR "$f $line: class $id1_ named both $class and $class{$id1_}, taking $class{$id1_}\n";
		$class{$id1_} ||= $1;
		$text =~ s/(.*?)|/$class{$id1_}|/;
	    }

	    $module =~ s/\.o$//;
	    $module = "unknown" if dummy_module($module);
	    $module = "unknown" if $id1 == 0x1011 && (0x0024 <= $id2 && $id2 <= 0x0025); 
	      # known errors in redhat's pcitable
	      # these are pci to pci bridge
	    $module = "yenta_socket" if $module =~ /i82365/;
	    my $id = join '', map { s/^0x//; $_ } $id1, $id2, $subid1, $subid2;
	    $drivers{$id} and print STDERR "$f $line: multiple entry for $id (skipping $module $text)\n";
	    $drivers{$id} ||= [ map &$rm_quote, $module, $text ];
	}
    }
    \%drivers;
}

sub read_kernel_pcimap {
    my ($f) = @_;
    my %drivers;
    foreach (cat_($f)) {
	chomp;
	next if /^#/ || /^\s*$/;
	my ($module, $id1, $id2, $subid1, $subid2) = split;
	($subid1, $subid2) = ("ffff", "ffff") if $subid1 == 0 && $subid2 == 0;
	$drivers{join '', map { /(....)$/ } $id1, $id2, $subid1, $subid2} = [ $module, '' ];
    }
    \%drivers;
}

sub read_kernel_usbmap {
    my ($f) = @_;
    my %drivers;
    foreach (cat_($f)) {
	chomp;
	next if /^#/ || /^\s*$/;
	my ($module, $flag, $id1, $id2) = split;
	hex($flag) == 3 or next;
	$drivers{join '', map { /(....)$/ } $id1, $id2, "ffff", "ffff"} = [ $module, '' ];
    }
    \%drivers;
}

sub read_pciids {
    my ($f) = @_;
    my %drivers;
    my ($id1, $id2, $class, $line, $text);
    foreach (cat_($f)) {
	chomp; $line++;
	next if /^#/ || /^;/ || /^\s*$/;
	if (/^C\s/) {
	    last;
	} elsif (my ($subid1, $subid2, $text) = /^\t\t(\S+)\s+(\S+)\s+(.*)/) {
	    $text =~ s/\t/ /g;
	    $id1 && $id2 or die "$f $line: unexpected device\n";
	    $drivers{lc "$id1$id2$subid1$subid2"} = [ "unknown", "$class|$text" ];
	} elsif (/^\t(\S+)\s+(.*)/) {
	    ($id2, $text) = ($1, $2);
	    $text =~ s/\t/ /g;
	    $id1 && $id2 or die "$f $line: unexpected device\n";
	    $drivers{lc "$id1${id2}ffffffff"} = [ "unknown", "$class|$text" ];
	} elsif (/^(\S+)\s+(.*)/) {
	    $id1 = $1;
	    $class = $class{$2} || $2;
	} else {
	    die "bad line: $_\n";
	}
    }
    \%drivers;
}

sub read_pcilst {
    my ($f) = @_;
    my %drivers;
    my ($id, $class, $line, $text);
    foreach (cat_($f)) {
	chomp; $line++;
	next if /^#/ || /^;/ || /^\s*$/;
	if (/^\t\S/) {
	    my ($id, undef, $module, $text) = split ' ', $_, 4 or die "bad line: $_\n";
	    $text =~ s/\t/ /g;
	    $module = "unknown" if dummy_module($module);
	    $drivers{"${id}ffffffff"} = [ $module, "$class|$text" ];
	} elsif (/^(\S+)\s+(.*)/) {
	    $class = $class{$2} || $2;
	} else {
	    die "bad line: $_\n";
	}
    }
    \%drivers;
}

sub read_pcitablepm {
    my ($f) = @_;
    eval cat_($f);

    %pci_probing::pcitable::ids or die;
    while (my ($k, $v) = each %pci_probing::pcitable::ids) {
	$drivers{sprintf qq(%08xffffffff), $k >> 32} = [ $v->[1], $v->[0] ];
    }
    \%drivers;
}

sub read_hwd {
    my ($f) = @_;
    my %drivers;
    foreach (cat_($f)) {
	next if /^\s*#/;
	chomp;
	my ($id1, $id2, $class, $module, $undef, $descr) = /(....):(....)\s+(\S+)\s+(\S+)(\s+(.*))/ or next;
	$drivers{"$id1${id2}ffffffff"} = [ $module, $descr ];
    }
    \%drivers;
}

# write in RedHat's pcitable old format (mdk one)
sub write_pcitable {
    my ($drivers) = @_;
    foreach (sort keys %$drivers) {
	print to_string($_, $drivers->{$_}), "\n";
    }
}

sub merge {
    my ($drivers, $new) = @_;

    foreach (keys %$new) {
	next if $new->{$_}[0] =~ /parport_pc|i810_ng/;
	if ($drivers->{$_}) {
	    if ($new->{$_}[0] ne "unknown") {
		if ($drivers->{$_}[0] eq "unknown" || $force) {
		    $drivers->{$_}[0] = $new->{$_}[0];
		} elsif ($drivers->{$_}[0] ne $new->{$_}[0]) {
		    my $different = 1;
		    $different = 0 if $new->{$_}[0] =~ /fb/;
		    $different = 0 if $drivers->{$_}[0] =~ /^(Card|Server):/;
		    $different = 0 if $drivers->{$_}[0] =~ /^ISDN:([^,]+)/ && $new->{$_}[0] eq $1;
		    print STDERR "different($drivers->{$_}[0] $new->{$_}[0]): ", to_string($_, $drivers->{$_}), "\n" if $different;
		}
	    }
	} else {
	    $drivers->{$_} = $new->{$_} 
	      # don't keep sub-entries with unknown drivers
	      if $all || /ffffffff$/ || $new->{$_}[0] ne "unknown";
	}	
    }
}

sub cleanup_subids {
    my ($drivers) = @_;
    my (%l, %m);
    foreach (sort keys %$drivers) {
	my ($id, $subid) = /(........)(........)/;
	if ($l{$id}) {
	    push @{$m{$id}}, $l{$id}, $subid;
	} else {
	    $l{$id} = $subid;
	}
    }
    foreach my $id (keys %m) {
	my %modules;
	my $text;
	foreach my $subid (@{$m{$id}}) {
	    my $e = $drivers->{"$id$subid"};
	    $modules{$e->[0]} = 1;
	    $text = $e->[1] if length($e->[1]) > length($text);
	}
	if (keys(%modules) == 1) {
	    my ($module, undef) = %modules;
	    			
	    # remove others
	    foreach my $subid (@{$m{$id}}) {
		delete $drivers->{"$id$subid"};		
	    }
	    # add a main one
	    $drivers->{$id . 'ffffffff'} = [ $module, $text ];
	} else {
#	    print STDERR "keeping subids for $id ($text) because of ", join(", ", keys %modules), "\n";
	}
    }
}
