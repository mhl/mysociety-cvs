#!/usr/bin/perl -w -I../../perllib
#
# THIS IS NOT THE ORIGINAL MOIN CGI SCRIPT!
#
# It is a wrapper script to implement anti-spam measures.
#
# Please contact me (Chris Lightfoot, chris@ex-parrot.com) if you want to make
# changes to this.
#

use strict;
use CGI;
use LWP::Simple;
use Storable;
use mySociety::Config;

mySociety::Config::set_file('../conf/general');
our $captcha_url = mySociety::Config::get('MS_CAPTCHA_URL');
our $moin_script = mySociety::Config::get('MS_MOIN_SCRIPT');

sub is_cookie_valid ($;$) {
    my ($c, $inval) = @_;
    $inval ||= 0;
    return 0 if ($c =~ /[^0-9a-f]/i);
    my $x = LWP::Simple::get("$captcha_url?check=$c" . ($inval ? ';invalidate=1' : ''));
    return 1 if ($x eq "YES\n");
    return 0;
}

my $q = new CGI;

# turn parameter into cookie
my $c;
if (defined($c = $q->param('captcha_cookie'))) {
    $q->delete('captcha_cookie');
    print $q->redirect(
                -url => $q->self_url(),
                -cookie => $q->cookie(
                    -name => 'captcha_cookie',
                    -value => $c,
                    -path => '/'
                )
            );
    exit(0);
}

my $action = $q->param('action');
$c = $q->cookie('captcha_cookie');

if ($action and ($action eq 'savepage' or $action eq 'edit')) {
    my %ipexceptions = map { $_ => 1 } qw(
                82.69.12.16 80.177.16.113 84.9.135.177
            );
    if (!exists($ipexceptions{$q->remote_host()}) and (!$c or !is_cookie_valid($c))) {
        if (lc($q->request_method()) eq 'post') {
            # If this is a POST request, we need to save our state and redirect
            # back.
            my $name = 'moin_captcha_temp_';
            $name .= sprintf("%08x", int(rand(0xffffffff))) foreach (qw(1 2 3 4));

            # Note that we can store/retrieve the CGI object here, because when
            # we retrieve it, the calling environment will be basically the same
            # as when we saved it. This wouldn't work if we were loading it back
            # in a different script.
            Storable::nstore($q, "/tmp/$name");

            $q->param('repost', $name);
        }
        my $u = $q->self_url();
        $u =~ s/([^A-Z0-9])/sprintf('%%%02x', ord($1))/gei;
        print $q->redirect("$captcha_url?origurl=$u;brand=mysociety");
        exit(0);
    }

}

my $r;
if (($r = $q->param('repost')) and ($r =~ m#^moin_captcha_temp_[A-Fa-f0-9]+$#)) {
    print $q->header(),
        $q->start_html('Continue...'),
        $q->start_form(-name => 'continue_form'),
        $q->submit(-name => 'catpcha_continue_submit',
                    -value => 'Click here to continue...');
    my $q2;
    $q2 = Storable::retrieve("/tmp/" . $q->param('repost')) or die "/tmp/" . $q->param('repost') . ": $!\n";
    unlink("/tmp/" . $q->param('repost'));
    foreach my $p ($q2->param()) {
        my @v = $q2->param($p);
        foreach (@v) {
            print $q->hidden(-name => $p, -default => $_, -override => 1);
        }
    }
    print $q->end_form(),
            <<'EOF',
<script language="javascript">document.continue_form.submit();</script>
EOF
        $q->end_html();
    exit(0);
}

my $script = "python $moin_script";
is_cookie_valid($c, 1) if ($q->param('button_save'));
if (lc($q->request_method()) eq 'post') {
    # yuk.
    my $content = '';
    foreach my $p ($q->param()) {
        foreach ($q->param($p)) {
            $content .= '&' if (length($content));
            $content .= $p;
            my $x = $_;
            $x =~ s/([^A-Z0-9])/sprintf('%%%02x', ord($1))/gei;
            $content .= "=$x";
        }
    }
    $ENV{CONTENT_LENGTH} = $ENV{HTTP_CONTENT_LENGTH} = length($content);
    open(POST, "|$script");
    print POST $content;
    close(POST);
    wait();
    exit($? & 0xff);
} else {
    exec("/bin/sh", "-c", $script);
}
