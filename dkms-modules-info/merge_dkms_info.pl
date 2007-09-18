#!/usr/bin/perl

use MDK::Common;

my $prefix = "dkms-modules";

my %fields;
my %filters = (
    alias => sub {
        my ($module, $values) = @_;
        map { "alias $_ $module\n" } sort(uniq(@$values));
    },
    description => sub {
        my ($module, $values) = @_;
        my $desc = find { $_} @$values;
        if_($desc, "$module\t$desc\n");
    },
);

foreach my $kver (grep { $_ ne ".svn" && -d $_ } all(".")) {
    foreach my $file (all($kver)) {
        my ($module, $type) = $file =~ /^(.+)\.(.+?)$/ or next;
        push @{$fields{$type}{$module}}, chomp_(cat_($kver . '/' . $file));
    }
}

foreach my $type (keys %filters) {
    output("$prefix.$type", map { $filters{$type}->($_, $fields{$type}{$_}) } sort(keys(%{$fields{$type}})));
}
