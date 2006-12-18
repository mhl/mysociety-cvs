<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Donate - mySociety</title>
<link rel="stylesheet" href="global.css" type="text/css" media="screen">
</head>

<body>
<div class="top">
<div class="masthead"><a href="http://www.mysociety.org/"><img border="0" src="/mslogo.gif" alt="mySociety.org"></a></div>
</div>

<div class="page-body">
<div class="menu">
&nbsp;<a href="http://www.mysociety.org/">News</a>&nbsp;|
&nbsp;<a href="http://www.mysociety.org/faq">FAQ</a> &nbsp;|
&nbsp;<a href="http://www.mysociety.org/projects">Projects</a>&nbsp;|
&nbsp;<a href="http://www.mysociety.org/category/developers">Developers' Blog</a>&nbsp;|
&nbsp;<a href="http://www.mysociety.org/moin.cgi">Wiki</a> |
&nbsp;<a href="http://www.mysociety.org/volunteertasks">Volunteer</a> |
&nbsp;<a href="https://secure.mysociety.org/admin/lists/mailman/listinfo/">Email Lists</a> |
&nbsp;<a href="http://www.mysociety.org/contact">Contact</a>
</div>
<?php

/* Should be in config file */
if ($_SERVER['HTTP_HOST'] != 'secure.mysociety.org') {
    /* STAGING settings */
    $paypal_url = "https://www.sandbox.paypal.com/cgi-bin/webscr";
    $business = "bob@evilmysociety.org";
    $return_url = "http://staging.mysociety.org/donatethanks";
    $cancel_url = "http://staging.mysociety.org/donatecancel";
} else {
    /* LIVE settings */
    $paypal_url = "https://www.paypal.com/cgi-bin/webscr";
    $business = 'james' . "@" . 'mysociety.org';
    $return_url = "https://secure.mysociety.org/donate/thanks";
    $cancel_url = "https://secure.mysociety.org/donate/cancel";
}

?>

<div id="betteritemdiv">

<div id="donatebox">

<img src="ccs_sm.gif" align="right" width="75" height="49" alt="">
<h3 class="f">Make a one off donation via PayPal</h3>

<form action="<?php echo $paypal_url; ?>" method="post">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="<?php echo $business; ?>">
<input type="hidden" name="item_name" value="Donation to mySociety">
<input type="hidden" name="no_shipping" value="2">
<input type="hidden" name="tax" value="0">
<input type="hidden" name="lc" value="GB">
<input type="hidden" name="bn" value="PP-DonationsBF">
<input type="hidden" name="rm" value="1">
<input type="hidden" name="return" value="<?php echo $return_url; ?>">
<input type="hidden" name="cancel_return" value="<?php echo $cancel_url; ?>">
<input type="hidden" name="cn" value="Please tell us why you're donating">

<p><label for="amount_donate">I would like to donate</label><br>
<select id="currency" name="currency_code">
<option value="GBP">UK &pound;</option>
<option value="USD">US Dollar $</option>
<option value="EUR">Euro &euro;</option>
<option value="AUD">Australian Dollar</option>
<option value="CAD">Canadian Dollar</option>
<option value="CZK">Czech Koruna</option>
<option value="DKK">Danish Krone</option>
<option value="HKD">Hong Kong Dollar</option>
<option value="HUF">Hungarian Forint</option>
<option value="JPY">Japanese Yen</option>
<option value="NOK">Norwegian Krone</option>
<option value="NZD">New Zealand Dollar</option>
<option value="PLN">Polish Zloty</option>
<option value="SEK">Swedish Krona</option>
<option value="CHF">Swiss Franc</option>
<option value="SGD">Singapore Dollar</option>
<option value="THB">Thai Baht</option>
</select>
<input id="amount_donate" name="amount" size="10">
</p>

<input type="hidden" name="on0" value="Donation with Gift Aid">
<p>I want all donations I make to UK Citizens Online Democracy from this date until further notice to be Gift Aid donations:
<input type="radio" id="giftaid_yes" name="os0" value="Yes">
<label for="giftaid_yes">Yes</label>
<input type="radio" id="giftaid_no" name="os0" value="No" checked>
<label for="giftaid_no">No</label>
(<a href="#giftaid">?</a>)</p>

<p align="right">
<input type="submit" value="Donate"></p>
</form>

<p>Sorry, but due to money laundering regulations, we can't simply make
our BACS information available, even though that would be really
convenient.</p>

<h3 class="d">Set up a regular monthly payment via PayPal</h3>

<form action="<?php echo $paypal_url; ?>" method="post">
<input type="hidden" name="cmd" value="_xclick-subscriptions">
<input type="hidden" name="business" value="<?php echo $business; ?>">
<input type="hidden" name="item_name" value="Monthly Donation to mySociety">
<input type="hidden" name="no_shipping" value="1">
<input type="hidden" name="lc" value="GB">
<input type="hidden" name="bn" value="PP-SubscriptionsBF">
<input type="hidden" name="p3" value="1">
<input type="hidden" name="t3" value="M">
<input type="hidden" name="src" value="1">
<input type="hidden" name="sra" value="1">
<input type="hidden" name="rm" value="1">
<input type="hidden" name="return" value="<?php echo $return_url; ?>">
<input type="hidden" name="cancel_return" value="<?php echo $cancel_url; ?>">
<input type="hidden" name="cn" value="Please tell us why you're donating">

<p><label for="amount_regular">I would like to donate</label><br>
<select name="currency_code">
<option value="GBP">UK &pound;</option>
<option value="USD">US Dollar $</option>
<option value="EUR">Euro &euro;</option>
<option value="AUD">Australian Dollar</option>
<option value="CAD">Canadian Dollar</option>
<option value="CZK">Czech Koruna</option>
<option value="DKK">Danish Krone</option>
<option value="HKD">Hong Kong Dollar</option>
<option value="HUF">Hungarian Forint</option>
<option value="JPY">Japanese Yen</option>
<option value="NOK">Norwegian Krone</option>
<option value="NZD">New Zealand Dollar</option>
<option value="PLN">Polish Zloty</option>
<option value="SEK">Swedish Krona</option>
<option value="SGD">Singapore Dollar</option>
<option value="CHF">Swiss Franc</option>
<option value="THB">Thai Baht</option>
</select>

<input id="amount_regular" name="a3" size="10">
once a month, starting tomorrow, until I cancel the payments.</p>

<input type="hidden" name="on0" value="Donation with Gift Aid">
<p>I want all donations I make to UK Citizens Online
Democracy from this date until further notice to be
Gift Aid donations:
<input type="radio" id="giftaid_yes_s" name="os0" value="Yes">
<label for="giftaid_yes_s">Yes</label>
<input type="radio" id="giftaid_no_s" name="os0" value="No" checked>
<label for="giftaid_no_s">No</label>
(<a href="#giftaid">?</a>)</p>

<p align="right">
<input type="submit" value="Donate"></p>
</form>

<h3 class="d">Set up a regular donation via Standing Order</h3>

<p>This needs to be done a slightly more old-fashioned way &mdash; please
download and fill in our <a href="standing_order.pdf">standing order form</a>.
</p>

<h3 class="d"><a name="giftaid" id="giftaid"></a>Are you from the UK? Gift Aid it!</h3>
<p>
To increase the value your donations at no extra cost to yourself,
if you are a UK tax payer, please select the appropriate option.
You must pay an amount of Income
Tax and/or Capital Gains Tax at least equal to the tax that we'll
reclaim on your donations (currently 28p for each &pound;1 you give).
</p>

</div>

<h2>Donate to mySociety</h2>

<p>To support the work of mySociety, you can make a donation to UK Citizens Online Democracy, mySociety's parent charity.</p>

<p>Despite being part of a registered charity mySociety has never asked for donations from the public before. But when your own users start asking if they can give you cash, it would be churlish to refuse. </p>
<p>If you love mySociety and its sites with such unbridled passion that you don't need any actual persuading to donate, then please just go ahead and let rip (fill in the form to the right). But if you want some reasons, here they are... </p>

<ul>
<li>44% of people who used <a href="http://www.writetothem.com/">WriteToThem</a> last year had never written to a politician ever before. mySociety shows that the net can connect normal people with the political process, not just extend the power of those already in the know. </li>

<li>Over 10,000 people a day visit <a href="http://www.theyworkforyou/com/">TheyWorkForYou</a>
to get unbiased, uneditorialised information on what their MPs have been doing,
saying and voting on. Also, every day Parliament is in session over 10,000
people get sent personalised emails from <a href="http://www.theyworkforyou.com/">TheyWorkForYou</a>
telling them what their MP said the day before, or showing them where an issue they care about was discussed. </li>

<li>mySociety is starting to influence the way in which government
and politicians use the net for the better. We've been told of
politicians' offices who have got better at responding to mail
because of our league tables, and we successfully persuaded No10
to run a petition system that is truly transparent and willing to
host even harsh criticisms of government policy. Just 90 MPs have used
<a href="http://www.hearfromyourmp.com/">HearFromYourMP</a> to talk with their constituents, even though they're trading off absolute control in exchange for dialogue. </li>

<li>We will use money donated to do all sorts of good things, including but not limited to:
<ul>
<li>Building new sites</li>
<li>Keeping the old ones working</li>
<li>Handling support email</li>
<li>Adding new features</li>
<li>Advertising our sites (which we've never yet done offline)</li>
<li>Holding events to attract/ensnare volunteers</li>
</ul>
</li>

<li>The money we've had so far has done much more than help build the sites themselves: it has generated a sizeable community of friends and volunteers. In particular, it has attracted more people who simply don't have the time or income to give up months of their lives to build a whole project, but who now have various sites and tools which they can hack on, make additions to, or simply use for their own nefarious purposes. </li>

<li>None of your money will go into buying goats, unlike all the rest of your christmas presents. </li>
</ul>

<p>UPDATE 1 </p>
<p>Our volunteer Alan has pointed out that we haven't been balanced in our self-eulogising. So here are some of his reasons NOT to give to mySociety. </p>
<ol>
<li>You believe that public data works better when locked away and bound up in red tape. </li>
<li>Your coffers have been drained because you are a serial victim of chuggers. </li>
<li>You hate your fellow man. </li>
<li>The warm toasty glow of helping democracy in fact makies you feel cold and clammy. </li>
<li>You are personally scared what our next league table might show. </li>
</ol>
<p>Thanks Alan! </p>
<p>UPDATE 2 </p>
<p>Do you work in the House of Commons and use our site every day? Yes? Well
GIVE US SOME MONEY TO DO THE COMMITTEES THEN. Thanks :)</p>

</div>

</div>
</body>
</html>
