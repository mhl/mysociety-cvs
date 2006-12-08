<?php 
/*
 * User is redirected to this page by paypal auto_return after
 * successful donation
 */

include "wordpress/wp-blog-header.php";
include "wordpress/wp-content/themes/mysociety/header.php";
?>

<div class="item_head">
  Thank you for your donation!
</div>

<div class="item">
<p>Your transaction has been completed, and a receipt for your purchase
has been emailed to you. If you have a paypal account, you may log
into your account at <a href="http://www.paypal.com/">www.paypal.com</a>
to view details of this transaction.</p>
</div>
<div class="item_foot">
</div>

<?php include "wordpress/wp-content/themes/mysociety/footer.php"; ?>

