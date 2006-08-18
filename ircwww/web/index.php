<?php 
include "../wordpress/wp-blog-header.php";
include "../wordpress/wp-content/themes/mysociety/header.php"; 
?>

<p>Please choose a "nickname", then press the Login button.</p>

<form method="post" action="irc.cgi" name="loginform">
<input type="hidden" name="interface" value="nonjs">
<input type="hidden" name="server" value="irc.mysociety.org">
<input type="hidden" name="channel" value="#mschat">
<table border="0" cellpadding="5" cellspacing="0">
<tr><td colspan="2" align="center" bgcolor="#c0c0dd"><b>mySociety Chat Login</b></td></tr>
<tr><td align="right" bgcolor="#f1f1f1">Nickname</td><td align="left"
bgcolor="#f1f1f1"><input type="text" name="Nickname" value="Passerby"></td></tr>
<tr><td align="left" bgcolor="#d9d9d9">
</td><td align="right" bgcolor="#d9d9d9">
<input type="submit" value="Login" style="background-color: #d9d9d9">
</td></tr></table></form>

<?php include "../wordpress/wp-content/themes/mysociety/footer.php"; ?>
