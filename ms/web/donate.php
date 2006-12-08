<?php
include "wordpress/wp-blog-header.php";
include "wordpress/wp-content/themes/mysociety/header.php";

/* TODO: I'm sure there's some clever mySociety Staging/Testing var somewhere I could pick up here... */

$stagingsite = "yes";

if( $stagingsite="yes" )
{
	/* STAGING settings */
	$paypal_url = "https://www.sandbox.paypal.com/cgi-bin/webscr";
	$business = "bob@evilmysociety.org";
	$return_url = "http://staging.mysociety.org/donatethanks";
	$cancel_url = "http://staging.mysociety.org/donatecancel";
}
else
{
	/* LIVE settings */
	
	// TODO!!!!
	$business = "";
	// TODO!!!!
	
	$paypal_url = "https://www.paypal.com/cgi-bin/webscr";
	$return_url = "http://mysociety.org/donatethanks";
	$cancel_url = "http://mysociety.org/donatecancel";
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


<div class="item_head">Support mySociety</div>

<div class="item">
<p>To support the work of mySociety, you can make a donation to UK Citizens Online Democracy, mySociety's parent charity.</p>
</div>


<div class="item_inner_head">Are you from the UK? Gift Aid it!</div>
<div class="item">
<p>
To increase the value your donations at no extra cost to yourself,
if you are a UK tax payer, please select the appropriate option below.
You must pay an amount of Income
Tax and/or Capital Gains Tax at least equal to the tax that we'll
reclaim on your donations (currently 28p for each &pound;1 you give).
</p>
</div>
<div class="item_inner_head">Make a one off donation</div>

<div class="item">

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


<p><label for="currency">I would like to donate</label>
<select id="currency" name="currency_code">
<option value="GBP">UK Sterling &pound;</option>
<option value="USD">US Dollars $</option>
<option value="EUR">Euro &euro;</option>
<option value="AUD">Australian Dollar</option>
<option value="CAD">Canadian Dollar</option>
<option value="CHF">Swiss Franc</option>
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
</select>
<input name="amount" size="5" />
</p>

<input type="hidden" name="on0" value="Donation with Gift Aid" />
<p>I want all donations I make to UK Citizens Online Democracy from this date until further notice to be Gift Aid donations:
<label for="giftaid_yes">Yes:</label> <input type="radio" id="giftaid_yes" name="os0" value="Yes" />
<label for="giftaid_no">No:</label> <input type="radio" id="giftaid_no" name="os0" value="No" checked="checked" />
</p>

<p><input type="image" src="https://www.paypal.com/en_US/i/btn/x-click-butcc-donate.gif" border="0" name="submit" alt="Make payments with PayPal - it's fast, free and secure!"></p>
</form>

</div>

<div class="item_inner_head">Set up a regular monthly payment</div>

<div  class="item">

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

<p>I would like to donate
<select name="currency_code">
<option value="GBP">UK Sterling &pound;</option>
<option value="USD">US Dollars $</option>
<option value="EUR">Euro &euro;</option>
<option value="AUD">Australian Dollar</option>
<option value="CAD">Canadian Dollar</option>
<option value="CHF">Swiss Franc</option>
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
</select>

<input name="a3" size="5" /> once a month, starting tomorrow, until I cancel the payments.</p>

<input type="hidden" name="on0" value="Donation with Gift Aid" />
<p>I want all donations I make to UK Citizens Online Democracy from this date until further notice to be Gift Aid donations
<label for="giftaid_yes_s">Yes:</label>
<input type="radio" id="giftaid_yes_s" name="os0" value="Yes" />
<label for="giftaid_no_s">No:</label>
<input type="radio" id="giftaid_no_s" name="os0" value="No" checked="checked" />
</p>

<p><input type="image" src="https://www.paypal.com/en_US/i/btn/x-click-butcc-subscribe.gif" border="0" name="submit" alt="Make payments with PayPal - it's fast, free and secure!"></p>
</form>

</div>
<div class="item_foot">
</div>

<?php include "wordpress/wp-content/themes/mysociety/footer.php"; ?>
