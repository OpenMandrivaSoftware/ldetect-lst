#!/usr/bin/perl

use lib qw(/usr/lib/libDrakX);
use detect_devices;

require './merge2pcitable.pl';
my $usbtable = read_pcitable($ARGV[0]);

foreach (values %$usbtable) {
    my $s = detect_devices::usb_description2removable($_->[1]) or next;
    if ($_->[0] =~ /Removable:(.*)/) {
	print STDERR "Conflicting $1 and $s for $_->[1]\n" if $1 ne $s;
    } else {
	print STDERR "Suggesting $s for $_->[1]\n";
	$_->[0] = "Removable:$s" if $_->[0] eq 'usb-storage';
    }
}
write_pcitable($usbtable);
