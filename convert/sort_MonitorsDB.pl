#!/usr/bin/perl

use POSIX;
use locale;
$ENV{LC_COLLATE} || $ENV{LANG} or setlocale(LC_COLLATE, "fr_FR");

my @l = <>;

@l = map { $_->[1] } sort { $a->[0] cmp $b->[0] } map {
    my $val = $_;
    chomp;
    s!^\s*(#.*|$)!!;
    s!(;.*?);.*!$1!;
    s/(\d+)/sprintf("%06d", $1)/e;
    [ $_, $val ];
} @l;

print foreach @l;
