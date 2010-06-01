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

my $vhostsFilename = "/data/servers/vhosts.pl";

$vhostsFilename = "vhosts.pl" unless -e $vhostsFilename; # uses a local copy if can't find the real one (useful for offline testing!)

my $isInList = 0;
my @report;
my @problems;

print "Content-type: text/$contentType\n\n";

unless ($return = do $vhostsFilename) {
    push @problems, "Couldn't parse $vhostsFilename: $@\n" if $@;
    push @problems, "Couldn't do $vhostsFilename: $!\n" unless defined $return;
    push @problems, "Couldn't run $vhostsFilename\n" unless $return;
    if (@problems){
        say "---++ Problem (sorry, $0 failed)\n";
        say "   * $_" foreach @problems;
    }
}

if (not @problems){
  my %vh = %$vhosts if $vhosts; # $vhosts is declared in vhosts.pl
  my %vhostsByServer; # to contain: e.g., 'balti' => ['dave.fixmystreet.com', 'gut.dave.thingummy']
  my ($totalVhosts, %vhostsByName);
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
          $vhostsByName{$vhost}++;
      }
  }

  my $totalServers = 0;

  foreach my $server (sort keys %vhostsByServer){ 
      $totalServers++;
      my $aRef = $vhostsByServer{$server};
      my @vhostsOnThisServer = @$aRef if $aRef;
      my $cVhosts = @vhostsOnThisServer;
      say("---++ $server");
      if ($cVhosts){
          say(($cVhosts-1?"$cVhosts vhosts are":"Only one vhost is") . " configured on $server:");
          foreach (sort @vhostsOnThisServer){
            my $b = /^(www|secure|news|intranet|lists)\./? '*':'';
            say("   * $b$_$b");
            $totalVhosts++;
          } 
      } else {
          say("No vhosts running on this server.")
      }
  }
  my (@homeless, $totalUniqueVhosts);
  foreach (sort keys %vhostsByName){
      if ($vhostsByName{$_}){
          $totalUniqueVhosts++
      } else {
          push @homeless, $_
      }
   }
  my $selfLink = qq{ | <a href="$0" target="_top">click for full page</a>};
  say("=$vhostsFilename parsed at " . gmtime() . "=" . $selfLink); 
  presay("Vhosts declared but not on any server: " . join(", ", @homeless)) if @homeless;
  presay("Total: $totalVhosts vhosts ($totalUniqueVhosts unique) configured across $totalServers servers. $selfLink");
  presay("---+ vhosts.pl summary");
}

my $report = join "\n", @report;
my $html = do {local $/;<DATA>};
$html=~s/%CONTENT%/$report\n$1/;
print $html;

sub presay{unshift @report, twiki2html(shift)}
sub say{push @report, twiki2html(shift)}

sub twiki2html{
    my $line = shift;
    return $line if $contentType ne "html";
    $line =~ s/=((\/|\w)[^=]*)=(?=\s)/<code>$1<\/code>/g;
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
</style>
</head>
<body class="patternViewPage" style="margin-top:10px;">
<div id="patternPage">
<div id="patternMainContents">
<div id="patternContent"><div id="patternTopic">
%CONTENT%
</div></div></div></div>
</body>
</html>
