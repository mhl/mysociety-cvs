<?php
include "wordpress/wp-blog-header.php";
include "wordpress/wp-content/themes/mysociety/header.php";
?>


<div class="item_head">Support mySociety</div>

<div class="item">
<p>To support the work of mySociety, you can make a donation to UK Citizens Online Democracy, mySociety's parent charity.</p>
</div>

<!--

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
-->


<div class="item_inner_head">Are you from the UK? Gift Aid it!</div>
<div class="item">
<p>
To increase the value your donations at no extra cost to yourself, if you are a UK tax payer, please tick the 'I want my donation to be a Gift Aid donation' box below. You must pay an amount of Income Tax and/or Capital Gains Tax at least equal to the tax that we'll reclaim on your donations (currently 28p for each &pound;1 you give).
</p>
</div>
<div class="item_inner_head">Make a one off donation</div>


<div class="item">

<form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="bob@evilmysociety.org">
<input type="hidden" name="item_name" value="Donation to mySociety">
<input type="hidden" name="no_shipping" value="2">
<input type="hidden" name="no_note" value="1">
<!-- <input type="hidden" name="currency_code" value="GBP"> -->
<input type="hidden" name="tax" value="0">
<input type="hidden" name="lc" value="GB">
<input type="hidden" name="bn" value="PP-DonationsBF">

<label for="currency">I would like to donate</label>
<select id="currency" name="currency_code">
<option value="GBP">UK Sterling &pound;</option>
<option value="USD">US Dollars $</option>
</select>
<input name="amount" />
<br />

<input type="hidden" name="on0" value="Donation with Gift Aid" />
<label for="giftaid">I want all donations I make to UK Citizens Online Democracy from this date until further notice to be Gift Aid donations</label>
Yes: <input type="radio" id="giftaid" name="os0" value="Yes" />
No: <input type="radio" id="giftaid" name="os0" value="No" checked="checked" />
<br />

<input type="image" src="https://www.paypal.com/en_US/i/btn/x-click-butcc-donate.gif" border="0" name="submit" alt="Make payments with PayPal - it's fast, free and secure!">
<img alt="" border="0" src="https://www.paypal.com/en_GB/i/scr/pixel.gif" width="1" height="1">
</form>

</div>

<div class="item_inner_head">Set up a regular monthly payment</div>



<div  class="item">

<form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_xclick-subscriptions">
<input type="hidden" name="business" value="bob@evilmysociety.org">
<input type="hidden" name="item_name" value="Monthly Donation to mySociety">
<input type="hidden" name="no_shipping" value="1">
<input type="hidden" name="no_note" value="1">
<input type="hidden" name="lc" value="GB">
<input type="hidden" name="bn" value="PP-SubscriptionsBF">
<input type="hidden" name="p3" value="1">
<input type="hidden" name="t3" value="M">
<input type="hidden" name="src" value="1">
<input type="hidden" name="sra" value="1">


<p>I would like to donate
<select name="currency_code">
<option value="GBP">UK Sterling &pound;</option>
<option value="USD">US Dollars $</option>
</select>

<input name="a3" /> once a month, starting tomorrow, until I cancel the payments.</p>
<br />

<input type="hidden" name="on0" value="Donation with Gift Aid" />
<label for="giftaid">I want all donations I make to UK Citizens Online Democracy from this date until further notice to be Gift Aid donations</label>
Yes: <input type="radio" id="giftaid" name="os0" value="Yes" />
No: <input type="radio" id="giftaid" name="os0" value="No" checked="checked" />
<br />

<input type="image" src="https://www.paypal.com/en_US/i/btn/x-click-butcc-subscribe.gif" border="0" name="submit" alt="Make payments with PayPal - it's fast, free and secure!">
<img alt="" border="0" src="https://www.paypal.com/en_GB/i/scr/pixel.gif" width="1" height="1">
</form>

</div>
<div class="item_foot">
</div>

<?php include "wordpress/wp-content/themes/mysociety/footer.php"; ?>




