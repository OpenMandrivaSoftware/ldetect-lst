#!/usr/bin/perl

use MDK::Common;

foreach my $file (glob("dmidecode.*")) {
    my %wanted = cat_($file) =~ /\(=> (\S+): (\S+)\)/g;

    my %got = map {
	s/\s*: .*//;
	/(\S+):(.*)/ ? ($1 => $2) : ();
    } `lspcidrake -p /dev/null -u /dev/null --dmidecode $file`;

    my @missing = difference2([ keys %wanted ], [ keys %got ]);
    if (@missing) {
	warn "for $file, missing: ", join(' ', @missing), "\n";
    }

    my @surprise = difference2([ keys %got ], [ keys %wanted ]);
    if (@surprise) {
	warn "for $file, surprise: ", join(' ', map { "$_ => $got{$_}" } @surprise), "\n";
    }

    my @bad = grep { $wanted{$_} ne $got{$_} } intersection([ keys %wanted ], [ keys %got ]);
    if (@bad) {
	warn "for $file, bad $_: $wanted{$_} != $got{$_}\n" foreach @bad;
    }
}
