#!/usr/bin/perl

use lib qw(/usr/lib/libDrakX);
use Xconfig::card;
require './merge2pcitable.pl';

$cards = Xconfig::card::readCardsDB("../lst/Cards+");

@cards = map {
    my $drivers = read_pcitable("../lst/$_");
    map { /^Card:(.*)/ } grep { /^Card/ } map { $_->[0] } values %$drivers;
} qw(pcitable usbtable);

foreach (@cards) {
    $nb++;
    if (!$cards->{$_}) {
	print STDERR "unknown card: $_\n";
	$bad++;
    }
}

exit $bad;
