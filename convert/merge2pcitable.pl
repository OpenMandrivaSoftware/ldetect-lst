#!/usr/bin/perl

use MDK::Common;


my @ignored_modules = (
qw(alsa ignore),
);

my ($force, @force_modules, $all, $keep_subids, $wildcards, $use_description);

if ($0 =~ /merge2pcitable/) 
{
    if ($ARGV[0] =~ /^-f=?(.*)$/) {
        shift;
        @force_modules = split(/,/, $1);
        $force = !@force_modules;
    }
    $ARGV[0] eq '-a' and $all = shift;
    $ARGV[0] eq '--keep-subids' and $keep_subids = shift;
    $ARGV[0] eq '--handle-wildcards' and $wildcards = shift;
    $ARGV[0] eq '--old' and $use_description = shift;

    my $formats = join '|', grep { $_ } map { /^read_(.*)/ ? $1 : '' } keys %main::;

    @ARGV == 3 or die "usage: $0 [-f[=module1,...]] [-a] [--old] $formats <in_file> <mdk_pcitable>\n";

    my ($format, $in, $pcitable) = @ARGV;

    my $read = $main::{"read_$format"} or die "unknown format $format (must be one of $formats)\n";
    my $d_pci = read_pcitable($pcitable, 'strict');
    my ($d_in, $classes) = $read->($in);
    merge($d_pci, $d_in, $classes);
    exit 1 if our $error;
    cleanup_subids($d_pci) if !$keep_subids;
    write_pcitable($d_pci);
} else { 1 }

sub dummy_module { 
    my ($m) = @_;
    $m =~ s/"(.*)"/$1/;
    member($m, @ignored_modules);
}

sub to_string {
    my ($id, $driver) = @_;
    @$driver >= 1 or error("error: to_string $id");
    my ($module, $text) = map { defined($_) && qq("$_") } @$driver;
    my ($id1, $id2, $subid1, $subid2) = map { "0x$_" } ($id =~ /(....)/g);
    join "\t", $id1, $id2, if_("$subid1 $subid2" ne "0xffff 0xffff", $subid1, $subid2), $module, if_($use_description && $text, $text);
}

sub read_rhpcitable {
    my ($f, $strict) = @_;
    read_pcitable($f, $strict, 1);
}

# works for RedHat's pcitable old and new format, + mdk format (alike RedHat's old one)
# (the new format has ending .o's and double quotes are removed)
sub read_pcitable {
    my ($f, $strict, $newer_rh_format) = @_;
    my %drivers;
    my %class;
    my $line = 0;
    my $rm_quote_silent = sub { local ($_) = @_; s/^"//; s/"$//; $_ };
    my $rm_quote = sub {
	    local ($_) = @_; 
	    s/^"// or error("$f:$line: missing left quote");
            s/"$// or error("$f:$line: missing right quote");
	    /"/ && $strict and error("$f:$line: bad double quote");
	    $_;
    };
    foreach (eval { catMaybeCompressed($f) }) {
	chomp; $line++;
	next if /^#/ || /^\s*$/;

	if (!$strict) {
	    #- help poor written pcitable's like redhat's :)
	    s/(\S+)\s+(\S+)\s+(.*)/$1\t$2\t$3/;
	}

	if (my ($id1, $id2, @l) = split /\t+/) {
	    push @l, '""' if $newer_rh_format;
	    my ($subid1, $subid2) = ('ffff', 'ffff');
	    ($subid1, $subid2, @l) = @l if @l > 2;
	    @l == 1 || @l == 2 or die "$f:$line: bad number of fields " . (int @l) . " (in $_)\n";
	    my ($module, $text) = @l;

	    my $class = $text =~ /(.*?)|/;
	    my $id1_ = $rm_quote_silent->($id1);
	    if (defined $text && $class{$id1_}) {
		print STDERR "$f:$line: class $id1_ named both $class and $class{$id1_}, taking $class{$id1_}\n";
		$class{$id1_} ||= $1;
		$text =~ s/(.*?)|/$class{$id1_}|/;
	    }

	    $module =~ s/\.o$//;
	    $module = '"unknown"' if dummy_module($module);
	    $module = '"unknown"' if $id1 eq '0x1011' && $id2 eq '0x0004';
	      # known errors in redhat's pcitable
	      # these are pci to pci bridge
	    $module = '"yenta_socket"' if $module =~ /i82365/;
	    my $id = join '', map { 
		s/^0x//;
		length == 4 or error("$f:$line: bad number $_");
		lc($_);
	    } $id1, $id2, $subid1, $subid2;
	    $drivers{$id} && $strict and error("$f:$line: multiple entry for $id (skipping $module $text)");
	    $drivers{$id} ||= [ $rm_quote->($module), defined($text) ? $rm_quote->($text) : undef, $line ];
	} else {
	    die "$f:$line: bad line\n";
	}
    }
    \%drivers;
}

sub read_kernel_pcimap {
    my ($f) = @_;
    my (%drivers, %driver_with_classes);
    foreach (cat_($f)) {
	chomp;
	next if /^#/ || /^\s*$/;
	my ($module, $id1, $id2, $subid1, $subid2) = split;
	next if $module eq 'pci';
	($subid1, $subid2) = ("ffff", "ffff") if hex($subid1) == 0 && hex($subid2) == 0;
     if ($id2 =~ /ffff$/ && $id1 !~ /ffff$/) {
         # $driver_with_classes{$id1} = [ $module, '' ];
         $driver_with_classes{join '', map { /(....)$/ } $id1, $id2, $subid1, $subid2} = [ $module, '' ];
     } else {
         $drivers{join '', map { /(....)$/ } $id1, $id2, $subid1, $subid2} = [ $module, '' ];
     }
    }
    \%drivers, \%driver_with_classes;
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
    my ($id1, $id2, $class, $line, %class);
    foreach (cat_($f)) {
	chomp; $line++;
	next if /^#/ || /^;/ || /^\s*$/;
	if (/^C\s/) {
	    last;
	} elsif (my ($subid1, $subid2, $text) = /^\t\t(\S+)\s+(\S+)\s+(.+)/) {
	    $text =~ s/\t/ /g;
	    $id1 && $id2 or die "$f:$line: unexpected device\n";
	    $drivers{sprintf qq(%04x%04x%04x%04x), hex($id1), hex($id2), hex($subid1), hex($subid2)} = [ "unknown", "$class|$text" ];
	} elsif (/^\t(\S+)\s+(.+)/) {
	    ($id2, $text) = ($1, $2);
	    $text =~ s/\t/ /g;
	    $id1 && $id2 or die "$f:$line: unexpected device\n";
	    $drivers{sprintf qq(%04x%04xffffffff), hex($id1), hex($id2)} = [ "unknown", "$class|$text" ];
	} elsif (/^(\S+)\s+(.+)/) {
	    $id1 = $1;
	    $class = $class{$2} || $2;
	    $class =~ s/(Advanced Micro Devices) \[AMD\]/$1/;
	} else {
	    warn "bad line: $_\n";
	}
    }
    \%drivers;
}

sub read_pcilst {
    my ($f) = @_;
    my %drivers;
    my ($class, $line, %class);
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
    my %drivers;

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
	my ($id1, $id2, $_class, $module, $_undef, $descr) = /(....):(....)\s+(\S+)\s+(\S+)(\s+(.*))/ or next;
	$drivers{"$id1${id2}ffffffff"} = [ $module, $descr ];
    }
    \%drivers;
}

sub read_hwinfo_x11 {
    my ($f) = @_;

    my (%drivers, %e, %vendors, $line);
    foreach (cat_($f)) {
	$line++;
	s/\s*$//;
	if (my ($add, $name, $val) = /^([ &])(\w+)\.id\s+(.*)/) {
	    if (!$add) {
		warn "read_hwinfo_x11:$line: unused %e\n" if %e;
		%e = ();
	    }
	    if ($val =~ /^pci\s+0x([0-9a-f]{4})/i) {
		$val = hex $1;
	    } else {
		warn "read_hwinfo_x11:$line: weird value $val\n";
	    }
	    $e{$name} = $val;
	} elsif (/^\+vendor\.name\s+(.*)/) {
            $vendors{$e{vendor}} = $1;
	} elsif (/^\+(?:sub)?device\.name\s+(.*)/) {
	    $e{name} = $1;
	} elsif (my ($driver) = /^\+driver\.xfree\s+(.*)/) {
	    if (exists $e{vendor} && exists $e{device}) {
		my $vendor = $vendors{$e{vendor}};
		my $module = $driver =~ /^4\|(\w+)/ ? "Driver:$1" : "Card:$driver";
		$drivers{sprintf qq(%04x%04x%04x%04x), $e{vendor}, $e{device}, 
			 $e{subvendor} || 0xffff, $e{subdevice} || 0xffff} = [ $module, "$vendor|$e{name}" ];
	    } else {
		warn "read_hwinfo_x11:$line: $driver but no vendor or no device\n";
	    }
	} elsif (/^$/) {
	    %e = ();
	} elsif (/^\+driver\.xfree\.config/) {
	    # drop
	} else {
	    warn "read_hwinfo_x11:$line: unknown line $_\n";
	}
    }
    \%drivers;
}

sub read_begent_pcids_htm {
    my ($f) = @_;
    my %drivers;
    my $F;
    open $F, $f or die "can't open $f\n";

    # drop until TBODY
    local $_;
    while (<$F>) { last if m|<TBODY>| }

    my $get_one = sub { map { scalar <$F> } 1 .. 6 };
    my $from_h = sub { 
	local $_ = lc $_[0]; 
	/([0-9a-g]{4})h/ or die "$.: bad number $_\n";
	$1;
    };

    # drop first line
    $get_one->();

    my ($cur_vendor, $cur_vendor_descr, $cur_id);

    while (1) {
	my ($tr, $vendor, $device, $sub, $text, $tr2) = map { m|<td>(.*)</td>| ? $1 : $_ } $get_one->();
	last if $tr =~ m|</TBODY>|;
	$tr  =~ m|<tr>|  or die "$f:$.: bad <tr> line $tr\n";
	$tr2 =~ m|</tr>| or die "$f:$.: bad </tr> line $tr2\n";

	if ($vendor) {
	    $device eq '-' && $sub eq '-' or die "$f:$.: bad vendor line\n";
	    $cur_vendor = $vendor;
	    ($cur_vendor_descr) = $text =~ m|<b>(.*)</b>| or die "$f:$.: vendor descr not bold\n";
	} else {
	    $cur_id = $device || $cur_id;
	    my $sub_t =
	      $sub ? do {
		  $sub =~ /^rev / and next; # ignoring "rev " thingy
		  if ($sub =~ /^(.....)$/) {
		      'ffff' . $from_h->($sub);
		  } else {
		      my ($s1, $s2) = $sub =~ /^(....)(.....)$/ or die "$f:$.: bad subid $sub\n";
		      $from_h->($s2) . $from_h->($s1 . 'h');
		  }
	      } : 'ffffffff';

	    $drivers{$from_h->($cur_vendor) . $from_h->($cur_id) . $sub_t} = [ 'unknown', "$cur_vendor_descr|$text" ];
	}
    }
    \%drivers;
}

sub read_nvidia_readme {
    my ($f) = @_;
    my %drivers;
    my $section;
    foreach (cat_($f)) {
	chomp;
	last if ($section > 3);
	if (!($section % 2)) {
	    next unless (/^\s+NVIDIA GPU product\s+Device PCI ID/);
	    $section++;
	    next;
        }
	if (/^\s*$/) {
	    $section++;
	    next;
        }
	next if (/^\s+-+\s+-+$/);
	my ($description, $id) = /^\s+(.+?)\s+0x(....)/;
	$drivers{"10de".lc($id)."ffffffff"} = [ 'Card:NVIDIA_UNKNOWN', $description ];
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


sub merge_entries_with_wildcards {
    my ($drivers, $classes) = @_;
    foreach (keys %$classes) {
        my ($vendor, $id, $subvendor, $subid);
        next unless ($vendor, $id, $subvendor, $subid) = /^([0-9a-f]{4,4})([0-9a-f]{4,4})/;

        # handle PCI_ANY_ID as PCI device ID:
        if ($vendor !~ /ffff$/ && $id =~ /ffff$/) {
            foreach my $old (keys %$drivers) {
                next if $old !~ /^$vendor/ || $drivers->{$old}[0] ne 'unknown';
                # blacklist AGP for now;
                next if $classes->{$_}[0] =~ /agp/;
                # the following test would be better but still generates some wrong entries (the only real check is to check
                # PCI_CAP_ID_AGP at probing time):
                # next if $classes->{$_}[0] =~ /-agp/ && $drivers->{$old}[1] !~ /Bridge|Controller|Host/i;
                $drivers->{$old}[0] = $classes->{$_}[0]; # if $drivers->{$old}[0] eq "unknown";
            }
        }
     }
}

sub merge {
    my ($drivers, $new, $classes) = @_;
    merge_entries_with_wildcards($drivers, $classes) if $wildcards;

    foreach (keys %$new) {
	next if $new->{$_}[0] =~ /parport_pc|i810_ng/;
	if ($drivers->{$_}) {
	    if ($new->{$_}[0] ne "unknown") {
		if ($drivers->{$_}[0] eq "unknown" || $force || member($new->{$_}[0], @force_modules)) {
		    $drivers->{$_}[0] = $new->{$_}[0];
		} elsif ($drivers->{$_}[0] ne $new->{$_}[0]) {
		    my $different = 1;
		    $different = 0 if $new->{$_}[0] =~ /fb/;
		    $different = 0 if $drivers->{$_}[0] =~ /^(Card|Server):/;
		    $different = 0 if $drivers->{$_}[0] =~ /^ISDN:([^,]+)/ && $new->{$_}[0] eq $1;
		    print STDERR "different($drivers->{$_}[0] $new->{$_}[0]): ", to_string($_, $drivers->{$_}), "\n" if $different;
		}
	    }
	    next if !$new->{$_}[1];
	    $drivers->{$_}[1] = $new->{$_}[1] if !$drivers->{$_}[1] || $drivers->{$_}[1] =~ /\|$/;
	} else {
	    if (!/ffffffff$/ && $new->{$_}[0] eq "unknown") {
		# keep sub-entry with major-entry module
		# will be dropped if every subids have the same module
		# ie. if no subids already present have a different module than the main one
		if (/(........)/) {
              $new->{$_}[0] = $drivers->{$1 . 'ffffffff'}[0] || "unknown" 
                if exists $drivers->{$1 . 'ffffffff'};
          }
	    }

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
	    $text = $e->[1] if length($e->[1]) > length($text) || $subid eq 'ffffffff'; # favour previous text
	}
	if (keys(%modules) == 1) {
	    my ($module, undef) = each %modules;
	    			
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

sub error {
    our $error = 1;
    print STDERR "$_[0]\n";
}
