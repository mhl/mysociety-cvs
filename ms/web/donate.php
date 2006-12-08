<?php
include "wordpress/wp-blog-header.php";
include "wordpress/wp-content/themes/mysociety/header.php";

if ($_SERVER['HTTP_HOST'] != 'secure.mysociety.org') {
    /* STAGING settings */
    $paypal_url = "https://www.sandbox.paypal.com/cgi-bin/webscr";
    $business = "bob@evilmysociety.org";
    $return_url = "http://staging.mysociety.org/donatethanks";
    $cancel_url = "http://staging.mysociety.org/donatecancel";
} else {
    /* LIVE settings */
    
    // TODO!!!!
    $business = "";
    // TODO!!!!
    
    $paypal_url = "https://www.paypal.com/cgi-bin/webscr";
    $return_url = "https://secure.mysociety.org/donate/thanks";
    $cancel_url = "https://secure.mysociety.org/donate/cancel";
}

/*

Paypal currency codes:

AUD Australian Dollar
CAD Canadian Dollar
CHF Swiss Franc
CZK Czech Koruna
DKK Danish Krone
EUR Euro
GBP Pound Sterling
HKD Hong Kong Dollar
HUF Hungarian Forint
JPY Japanese Yen
NOK Norwegian Krone
NZD New Zealand Dollar
PLN Polish Zloty
SEK Swedish Krona
SGD Singapore Dollar
THB Thai Baht
USD U.S. Dollar
*/

?>

<div id="betteritemdiv">

<div id="donatebox">

<h3 class="f">Make a one off donation</h3>

<form action="<?php echo $paypal_url; ?>" method="post">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="<?php echo $business; ?>">
<input type="hidden" name="item_name" value="Donation to mySociety">
<input type="hidden" name="no_shipping" value="2">
<input type="hidden" name="no_note" value="1">
<input type="hidden" name="tax" value="0">
<input type="hidden" name="lc" value="GB">
<input type="hidden" name="bn" value="PP-DonationsBF">
<input type="hidden" name="rm" value="2">
<input type="hidden" name="return" value="<?php echo $return_url; ?>">
<input type="hidden" name="cancel_return" value="<?php echo $cancel_url; ?>">


<p><label for="amount_donate">I would like to donate</label><br />
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
<input id="amount_donate" name="amount" size="10" />
</p>

<input type="hidden" name="on0" value="Donation with Gift Aid" />
<p>I want all donations I make to UK Citizens Online Democracy from this date until further notice to be Gift Aid donations:
<input type="radio" id="giftaid_yes" name="os0" value="Yes" />
<label for="giftaid_yes">Yes</label>
<input type="radio" id="giftaid_no" name="os0" value="No" checked="checked" />
<label for="giftaid_no">No</label>
(<a href="#giftaid">?</a>)</p>

<p align="right">
<img src="logo_ccVisa.gif" alt="" width="37" height="21" align="middle">
<img src="logo_ccMC.gif" alt="" width="37" height="21" align="middle">
<input type="submit" value="Donate" /></p>
</form>

<?
/*
<p>Or simply transfer money to our bank account! Our sort code is
40-03-28, our account number 31546341.</p>
*/
?>

<h3 class="d">Set up a regular monthly payment</h3>

<form action="<?php echo $paypal_url; ?>" method="post">
<input type="hidden" name="cmd" value="_xclick-subscriptions">
<input type="hidden" name="business" value="<?php echo $business; ?>">
<input type="hidden" name="item_name" value="Monthly Donation to mySociety">
<input type="hidden" name="no_shipping" value="1">
<input type="hidden" name="no_note" value="1">
<input type="hidden" name="lc" value="GB">
<input type="hidden" name="bn" value="PP-SubscriptionsBF">
<input type="hidden" name="p3" value="1">
<input type="hidden" name="t3" value="M">
<input type="hidden" name="src" value="1">
<input type="hidden" name="sra" value="1">
<input type="hidden" name="rm" value="2">
<input type="hidden" name="return" value="<?php echo $return_url; ?>">
<input type="hidden" name="cancel_return" value="<?php echo $cancel_url; ?>">

<p><label for="amount_regular">I would like to donate</label><br />
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

<input id="amount_regular" name="a3" size="10" />
once a month, starting tomorrow, until I cancel the payments.</p>

<input type="hidden" name="on0" value="Donation with Gift Aid" />
<p>I want all donations I make to UK Citizens Online
Democracy from this date until further notice to be
Gift Aid donations:
<input type="radio" id="giftaid_yes_s" name="os0" value="Yes" />
<label for="giftaid_yes_s">Yes</label>
<input type="radio" id="giftaid_no_s" name="os0" value="No" checked="checked" />
<label for="giftaid_no_s">No</label>
(<a href="#giftaid">?</a>)</p>

<p align="right">
<img src="logo_ccVisa.gif" alt="" width="37" height="21" align="middle">
<img src="logo_ccMC.gif" alt="" width="37" height="21" align="middle">
<input type="submit" value="Donate" /></p>
</form>

<p>Or download a <a href="standing_order.pdf">Standing Order form</a> and fill
it in if you'd prefer that.</p>

<h3 class="d"><a name="giftaid" id="giftaid"></a>Are you from the UK? Gift Aid it!</h3>
<p>
To increase the value your donations at no extra cost to yourself,
if you are a UK tax payer, please select the appropriate option.
You must pay an amount of Income
Tax and/or Capital Gains Tax at least equal to the tax that we'll
reclaim on your donations (currently 28p for each &pound;1 you give).
</p>

</div>

<h2>Support mySociety</h2>

<p>To support the work of mySociety, you can make a donation to UK Citizens Online Democracy, mySociety's parent charity.</p>

<p>Despite being part of a registered charity mySociety has never asked for donations from the public before. But some people might say that when your own users start asking if they can give you cash, it might be churlish to refuse. </p>
<p>If you love mySociety and its sites with such unbridled passion that you don't need any actual persuading to donate, then please just &lt;go ahead and let rip&gt;. But if you want some reasons, here they are... </p>

<ul>
<li>44% of people who used <a href="/moin.cgi/WriteToThem">WriteToThem</a> last year had never written to a politician ever before. mySociety shows that the net can connect normal people with the political process, not just extend the power of those already in the know. </li>

<li>Over 10,000 people a day visit <a href="/moin.cgi/TheyWorkForYou">TheyWorkForYou</a> to get unbiased, uneditorialised information on what their MPs have been doing, saying and voting on. Also, every day Parliament is in session over 10,000 people get sent personalised emails from <a href="/moin.cgi/TheyWorkForYou">TheyWorkForYou</a> telling them what their MP said the day before, or showing them where an issue they care about was discussed. </li>

<li>mySociety is starting to influence the way in which government and politicians use the net for the better. We've been told of politician's offices who have got better at responding to mail because of our league tables, and we successfully persuaded No10 to run a petition system that is truly transparent and willing to host even harsh criticisms of government policy. Nearly 90 MPs have used
<a href="http://www.hearfromyourmp.com/">HearFromYourMP</a> to talk with their constituents, even though they're trading off absolute control in exchange for dialogue. </li>

<li>We can use money donated to do all sorts of good things, including:
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
<p>Do you work in the House of Commons and use our site every day? Yes? Well GIVE US SOME MONEY TO DO THE COMMITTEES THEN. Thanks <img src="/wiki/mstheme/img/smile.png" alt=":)" height="15" width="15"> </p>

</div>

<?php include "wordpress/wp-content/themes/mysociety/footer.php"; ?>
