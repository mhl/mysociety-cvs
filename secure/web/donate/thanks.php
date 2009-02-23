<?
header('Content-Type: text/html; charset=utf-8');
print file_get_contents('header.html');
?>

<h1>Thank you for your donation!</h1>

<p>Your transaction has been completed, and a receipt for your purchase
has been emailed to you. If you have a paypal account, you may log
into your account at <a href="http://www.paypal.com/">www.paypal.com</a>
to view details of this transaction.</p>

<p>
Numerous independent studies have shown conclusively that donations
to mySociety are effective in:

<ul>
<li>helping to combat climate change</li>
<li>increasing the happiness of whales, baby seals and kittens</li>
<li>preventing baldness</li>
</ul>
So please... take a little time to pat yourself on the back. Maybe you
could have a nice cup of tea and a sit down.
</p>

<p>
You've earned it.
</p>
<?
print file_get_contents('footer.html');

