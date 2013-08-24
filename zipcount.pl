#!/usr/bin/perl -w

open FILE, $ARGV[0] or die $!;
print "Zip code count\n";

my $currentZip = "00000";
my $storedZip  = "99999";
my $count = 1;

while($currentZip = <FILE>) {
  chomp $currentZip;
  if($currentZip eq $storedZip) {
    $count++;
  } else {
    print $storedZip . ", " . $count . "\n";
    $storedZip = $currentZip;
    $count = 1;
  }
}

print $storedZip . ", " . $count . "\n";


close FILE or die $!;
