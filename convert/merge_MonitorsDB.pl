#!/usr/bin/perl

# ./merge_MonitorsDB.pl ../../monitor-edid/test/new_MonitorsDB ../lst/MonitorsDB > MonitorsDB.new
# diff -u ../lst/MonitorsDB MonitorsDB.new

@ARGV == 2 or die "usage: $0 [--verif | <entries to add>] <mdk MonitorsDB>\n";

my ($to_add, $MonitorsDB) = @ARGV;
my $verif = $to_add eq '--verif';


use MDK::Common;

my $monitors_db = readMonitorsDB($MonitorsDB);

if ($verif) {
    verif($monitors_db);
} else {
    my $to_add = readMonitorsDB($to_add);

    rationalize_EISA_ID($_) foreach @$to_add, @$monitors_db;

    my %EISA_ID_to_VendorName = EISA_ID_to_VendorName($monitors_db);
    foreach (@$to_add) {
	my $VendorName = $_->{EISA_ID} =~ /(...)/ && $EISA_ID_to_VendorName{$1} or next;

	$_->{ModelName} =~ s/^(\Q$_->{VendorName}\E|\Q$VendorName\E)\s//i;
	$_->{VendorName} = $VendorName;
	$_->{ModelName} = "$VendorName $_->{ModelName}";
	$_->{text} = join_line($_);
    }

    #- first see if the EISA_ID is already there
    my %to_add = map { $_->{EISA_ID} => $_ } @$to_add;
    foreach (@$monitors_db) {
	$to_add{$_->{EISA_ID}} or next;

	$_->{text} =~ s!.*\n$!$to_add{$_->{EISA_ID}}{text}!;
	delete $to_add{$_->{EISA_ID}};
    }

    my @to_add = sort { lc($a->{text}) cmp lc($b->{text}) } values %to_add;
    foreach (@$monitors_db) {
	while (@to_add && lc("$to_add[0]{VendorName}; $to_add[0]{ModelName}") lt lc("$_->{VendorName}; $_->{ModelName}")) {
	    $_->{text} = (shift @to_add)->{text} . $_->{text};
	}
    }

    print $_->{text} foreach (@$monitors_db, @to_add);
}

sub verif {
    my ($monitors_db) = @_;
    
    my %l; 
    foreach my $e (@$monitors_db) {	
	rationalize_EISA_ID($e, sub {
	    my ($previous) = @{$l{$e->{EISA_ID}} || []} or return;
	    my @vs = map { 
		$e->{$_} eq $previous->{$_} ? () : "$e->{$_} vs $previous->{$_}";
	    } 'ModelName', 'HorizSync', 'VertRefresh';
	    warn "$e->{lineno}: duplicate $e->{EISA_ID}: " . (@vs ? join(", ", @vs) : $e->{ModelName}) . "\n";
	});

	push @{$l{$e->{EISA_ID}}}, $e;
    }
}

sub rationalize_EISA_ID {
    my ($e, $o_verif) = @_;

    if ($e->{EISA_ID} =~ /^([A-Z]{3})([0-9a-f]{4})$/i) {
	# perfect!
	$e->{EISA_ID} = uc($1) . lc($2);
	$o_verif and $o_verif->();
    } elsif ($e->{EISA_ID} eq '0') {
	# ok
    } elsif ($e->{EISA_ID} =~ /^([a-z]{3})([0-9a-f]{0,3})$/i) {
	# we can correct this (?)
	warn sprintf("$e->{lineno}: $e->{EISA_ID} should be %s%04x\n", $1, hex($2)) if $verif;
    } else {
	warn "$e->{lineno}: bad EISA_ID $e->{EISA_ID}\n" if $o_verif;
    }
}

sub EISA_ID_to_VendorName {
    my ($monitors_db) = @_;

    my %l;
    foreach (@$monitors_db) {
	$_->{EISA_ID} =~ /(...)/ and $l{$1}{$_->{VendorName}}++;
    }
    map {
	my $v = $l{$_};
	my @l = sort { $v->{$b} <=> $v->{$a} } keys %$v;
	$_ => $l[0];
    } keys %l;
}

BEGIN {
    our @fields = qw(VendorName ModelName EISA_ID HorizSync VertRefresh dpms);
}

sub join_line {
    my ($e) = @_;
    join('; ', @$e{@fields}) . "\n";
}
sub split_line {
    my ($s) = @_;
    my %l; @l{@fields} = split(/\s*;\s*/, $s);
    \%l;
}

sub readMonitorsDB {
    my ($f) = @_;
    my $s = '';
    my @monitors_db;
    my $lineno = 0;
    foreach (cat_($f)) {
	$lineno++;
	$s .= $_;
	s/\s+$//;
	/^#/ and next;
	/^$/ and next;

	my $e = split_line($_);
	($e->{text}, $s) = ($s, '');
	$e->{lineno} = $lineno;
	push @monitors_db, $e;
    }
    \@monitors_db;
}
