#!/usr/bin/perl
# returns pretty list of servers gleaned from vhosts.pl
# intended to be suitable for embedding using %INCLUDE% in a TWiki page...
# ...but there are issues with that on a secure site since credentials aren't
# passed on and even if %INCLUDE% was enabled it doesn't allow https.
# So instead this generates TWiki style output then, at the end, HTMLifies it.
#
# script by dave@mysociety.org
#------------------------------------------------------------------------------

my $contentType = "html"; # set "html" for standalone page, or "plain" for inclusion in TWiki

my @vhostsFilenames = ("/data/vhosts.pl", "./vhosts.pl"); # try in this order: useful for testing

my $isInList = 0;

our $vhosts;
our $databases;

my %uniqueServers;
my $totalServers = 0;

print "Content-type: text/$contentType\n\n";

my $vhostsFilename = shift @vhostsFilenames;
while ($vhostsFilename){
    if ($return = do $vhostsFilename) {
        last;
    } else {
        my @problems;
        push @problems, "Couldn't parse =$vhostsFilename= &mdash; $@\n" if $@;
        push @problems, "Couldn't do =$vhostsFilename= &mdash; $!\n" unless defined $return;
        push @problems, "Couldn't run =$vhostsFilename=\n" unless $return;
        if (@problems){
            say("---++ Problem (sorry, $0 failed)\n");
            say("   * $_") foreach @problems;
        }
        if ($vhostsFilename = shift @vhostsFilenames){
            say("   * <span style='background:#ff0000;color:#ffffff;padding:4px;'>now trying $vhostsFilename instead...</span>");
        }
    }
}

my %vh = %$vhosts if $vhosts; # $vhosts is declared in vhosts.pl
my %vhostsByServer; # to contain: e.g., 'balti' => ['dave.fixmystreet.com', 'gut.dave.thingummy']
my ($totalVhosts, %vhostsByName, %productionVhosts);

foreach my $vhost (sort keys %vh) {
    my $hRef = $vh{$vhost};
    my %vhostData = %$hRef;
    my $aRef = $vhostData{"servers"};
    my @servers = @$aRef if ref $aRef eq 'ARRAY';
    $vhostsByName{$vhost} ||= 0;
    foreach my $server (@servers){ # because a vhost may be deployed on more than one server
        $aRef = $vhostsByServer{$server};
        my @vhostsOnThisServer = $aRef? @$aRef : ();
        push @vhostsOnThisServer, $vhost;        
        $vhostsByServer{$server}=\@vhostsOnThisServer;
	$productionVhosts{$vhost}++ unless $vhostData{"staging"};
        $vhostsByName{$vhost}++;
        $uniqueServers{$server}++;
    }
}

my %db = %$databases if $databases; # $databases is declared in vhosts.pl
my %databasesByServer; # to contain: e.g., 'balti' => ['dbfoo', 'dbbar']
my (%databasesByName, %databaseTypeByName);

foreach my $db (sort keys %db) {
    my $hRef = $db{$db};
    my %databaseData = %$hRef;
    my $host = $databaseData{"host"};
    $databaseTypeByName{$db}=$databaseData{"type"};
    $databasesByName{$db} ||= 0;
    $aRef = $databasesByServer{$host};
    my @databasesOnThisServer = $aRef? @$aRef : ();
    push @databasesOnThisServer, $db;        
    $databasesByServer{$host}=\@databasesOnThisServer;
    $databasesByName{$db}++;
    $uniqueServers{$host}++;
}

my @report;

foreach my $server (sort keys %uniqueServers){ 
    $totalServers++;
    say("---++ $server");

    say("<div class='vhosts-col'>");
    my $aRef = $vhostsByServer{$server};
    my @vhostsOnThisServer = @$aRef if $aRef;
    my $cVhosts = @vhostsOnThisServer;
    if ($cVhosts){
        say(($cVhosts-1?"$cVhosts vhosts are":"Only one vhost is") . " configured on $server:");
        foreach (sort @vhostsOnThisServer){
          my $b = '*' if $productionVhosts{$_};
          say("   * $b$_$b");
          $totalVhosts++;
        } 
    } else {
        say("No vhosts running on this server.")
    }
    say("</div>");    

    say("<div class='vhosts-col'>");
    $aRef = $databasesByServer{$server};
    my @databasesOnThisServer = @$aRef if $aRef;
    my $cDatabases = @databasesOnThisServer;
    if ($cDatabases){
        say(($cDatabases-1?"$cDatabases databases are":"Only one database is") . " configured on $server:");
        foreach (sort @databasesOnThisServer){
          say("   * $_ <span class='db-type'>[$databaseTypeByName{$_}]</span>");
        } 
    } else {
        say("No databases running on this server.")
    }
    say("</div>");
    say("<div style='clear:both;height:1px'></div>");    
}

my $totalUniqueDatabases = keys %databasesByName;
my @homelessVhosts;
my $totalUniqueVhosts = 0;

foreach (sort keys %vhostsByName){
    if ($vhostsByName{$_}){
        $totalUniqueVhosts++
    } else {
        push @homelessVhosts, $_
    }
}
my $cProductionSites = scalar keys %productionVhosts;
my $selfLink = qq{ | <a href="$0" target="_top">click for full page</a>};
say("=$vhostsFilename parsed at " . gmtime() . "=" . $selfLink) if $vhostsFilename; 
presay("Vhosts declared but not on any server: " . join(", ", @homelessVhosts)) if @homelessVhosts;
presay("Total: $totalVhosts vhosts ($totalUniqueVhosts unique, $cProductionSites production) and $totalUniqueDatabases databases configured across $totalServers servers. $selfLink");
presay("---+ vhosts.pl summary");

my $report = join "\n", @report;
my $html = do {local $/;<DATA>};
$html=~s/%CONTENT%/$report\n$1/;
print $html;

sub presay{unshift @report, twiki2html(shift)}
sub say{push @report, twiki2html(shift)}

sub twiki2html{
    my $line = shift;
    return $line if $contentType ne "html";
    $line =~ s/=((\/|\.|\w)[^=]*)=(?=\s)/<code>$1<\/code>/g;
    $line =~ s/\*(\S.*?)\*/<b>$1<\/b>/g;
    if ($line=~/^   \*(.*)/){
        $line = "<li> $1 </li>";
        $line = "<ul style='margin-top:8px;'>\n$line" unless $isInList;
        $isInList++
    } else {
        if ($line=~/^---(\++)(.*)/){
            my $h = length $1;
            $line = "<h$h> $2 </h$h>"
        } else {
            $line = "<p> $line </p>"
        }
        $line = "</ul>\n$line" if $isInList;
        $isInList = 0;
    }
    return $line
}

__DATA__
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-us" lang="en-us">
<head>
<title>summary of vhosts.pl</title>
<style type="text/css" media="all">
	@import url('https://secure.mysociety.org/intranet/pub/TWiki/PatternSkin/layout.css');
	@import url('https://secure.mysociety.org/intranet/pub/TWiki/PatternSkin/style.css');
	@import url('https://secure.mysociety.org/intranet/pub/TWiki/PatternSkin/colors.css');
	@import url("https://secure.mysociety.org/intranet/pub/TWiki/PatternSkin/print.css");
	.db-type{color:#cccccc;padding-left:1em;}
	.db-type:hover{color:#666666;}
	.vhosts-col{float:left; width:45%;}
	body{margin-top:10px;}
</style>
</head>
<body class="patternViewPage">
<div id="patternPage">
<div id="patternMainContents">
<div id="patternContent">
<div id="patternTopic">
%CONTENT%
</div>
</div>
</div>
</div>
</body>
</html>
