#!/usr/bin/perl

$vendors = join '|', map { chomp; quotemeta } <DATA>;

%substs = (
"3Dlabs" => "3DLabs",
"COMPAQ" => "Compaq",
"Creative Blaster Exxtreme" => "Creative Labs Blaster Exxtreme",
"ELSA" => "Elsa",
"ATrend" => "Atrend",
"Ocean (octek)" => "Octek",
"HOT" => "Spacewalker Hot",
);

print "# This file is auto-generated from Cards+, DO NOT MODIFY\n";
print "#\n";

foreach (<>) {
    my ($n) = /^NAME (.*)/ or next;
    $_ = $n;
    while (my ($k, $v) = each %substs) { s/^\Q$k/$v/; }

    if (my ($v, $more) = /^($vendors)\s*-?(.*)/) {
	$_ = "$v|$more";
    } else {
	$_ = "Other|$_";
    }
    print qq{$_=>$n\n};
}

__DATA__
3DLabs
Compaq
Dell
Elsa
Rendition Verite
Intel
Oak
Ark Logic
Cardex
Digital
RIVA
Spider
Canopus
Leadtek
NVIDIA
Octek
ASUS
Actix
Avance Logic
ET
Genoa
SMI
SPEA
VideoLogic
Creative Labs
Toshiba
Orchid
Chaintech
Cirrus Logic
AOpen
SiS
Chips & Technologies
Number Nine
Miro
STB
Matrox
Hercules
Trident
Sun
Diamond
S3
ATI
