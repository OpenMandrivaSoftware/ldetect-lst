#!/usr/bin/perl

use lib qw(/usr/lib/libDrakX);
use Xconfig::card;
require './merge2pcitable.pl';

$cards = Xconfig::card::readCardsDB("../lst/Cards+");

foreach my $file (qw(pcitable usbtable)) {
    my $drivers = read_pcitable("../lst/$file");
    foreach (values %$drivers) {
	my ($driver, $name, $line) = @$_;
	my ($card) = $driver =~ /^Card:(.*)/ or next;
	if (!$cards->{$card}) {
	    warn "$file:$line: unknown card $name\n";
	    $bad++;
	} elsif (!$cards->{$card}{Driver}) {
	    warn "$file:$line: no Driver for card $name\n";
	    $bad++;
	}
    }
}

exit $bad;
