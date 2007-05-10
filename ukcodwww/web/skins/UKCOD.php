<?php
/**
 * UKCOD theme
 *
 * @todo document
 * @package MediaWiki
 * @subpackage Skins
 */

if( !defined( 'MEDIAWIKI' ) )
	die( -1 );

/** */
require_once('includes/SkinTemplate.php');

/**
 * Inherit main code from SkinTemplate, set the CSS and template filter.
 * @todo document
 * @package MediaWiki
 * @subpackage Skins
 */
class SkinUKCOD extends SkinTemplate {
	/** Using ukcod. */
	function initPage( &$out ) {
		SkinTemplate::initPage( $out );
		$this->skinname  = 'ukcod';
		$this->stylename = 'ukcod';
		$this->template  = 'UKCODTemplate';
	}
}

/**
 * @todo document
 * @package MediaWiki
 * @subpackage Skins
 */
class UKCODTemplate extends QuickTemplate {
	/**
	 * Template filter callback for UKCOD skin.
	 * Takes an associative array of data set from a SkinTemplate-based
	 * class, and a wrapper for MediaWiki's localization database, and
	 * outputs a formatted page.
	 *
	 * @access private
	 */
	function execute() {
		// Suppress warnings to prevent notices about missing indexes in $this->data
		wfSuppressWarnings();

        include($_SERVER['DOCUMENT_ROOT']."/header.html");
        global $title;

?>	
	<a href="#menu" class="hiddentext">Menu</a>
	<a href="#content" class="hiddentext">Content</a>
	<a herf="/" id="site-title-link"><h1 class="hiddentext">UK Citizens Online Democracy</h1></a>

	<ul id="menu">
		<li <?= ($title == 'Main_Page' || $title == 'UK_Citizens_Online_Democracy') ? 'class="selected"' : '' ?> ><a href="/UK_Citizens_Online_Democracy">Structure</a></li>
		<li <?= ($title == 'Trustees') ? 'class="selected"' : '' ?> ><a href="/Trustees">Trustees</a></li>
		<li <?= ($title == 'mySociety_Ltd_Board_Members') ? 'class="selected"' : '' ?> ><a href="/mySociety_Ltd_Board_Members">Board Members</a></li>
		<li <?= ($title == 'Finance') ? 'class="selected"' : '' ?> ><a href="/Finances">Finance</a></li>
		<li <?= ($title == 'Paid_Staff') ? 'class="selected"' : '' ?> ><a href="/Paid_Staff">Paid Staff</a></li>
		<li <?= ($title == 'Contact') ? 'class="selected"' : '' ?> ><a href="/Contact">Contact</a></li>
	</ul>


	<div id="content">
		<a name="top" id="top"></a>
		<?php if($this->data['sitenotice']) { ?><div id="siteNotice"><?php $this->html('sitenotice') ?></div><?php } ?>
		<h1 class="firstHeading"><?php $this->data['displaytitle']!=""?$this->html('title'):$this->text('title') ?></h1>

		<div id="bodyContent">
			<div id="contentSub"><?php $this->html('subtitle') ?></div>
			<?php if($this->data['undelete']) { ?><div id="contentSub2"><?php     $this->html('undelete') ?></div><?php } ?>
			<?php if($this->data['newtalk'] ) { ?><div class="usermessage"><?php $this->html('newtalk')  ?></div><?php } ?>
			<?php /*if($this->data['showjumplinks']) { ?><div id="jump-to-nav"><?php $this->msg('jumpto') ?> <a href="#column-one"><?php $this->msg('jumptonavigation') ?></a>, <a href="#searchInput"><?php $this->msg('jumptosearch') ?></a></div><?php } */?>
			<!-- start content -->
			<?php $this->html('bodytext') ?>
			<?php if($this->data['catlinks']) { ?><div id="catlinks"><?php       $this->html('catlinks') ?></div><?php } ?>
			<!-- end content -->
			<div class="visualClear"></div>
		</div>
	</div>

	<!--	<li><a href="#">foo</a></li>
		<li class="selected"><a href="#">foo</a></li>	-->
	<ul id="footer">
    <!-- article/edit/history -->
	<?php			foreach($this->data['content_actions'] as $key => $tab) { ?>
					 <li id="ca-<?php echo Sanitizer::escapeId($key) ?>"<?php
					 	if($tab['class']) { ?> class="<?php echo htmlspecialchars($tab['class']) ?>"<?php }
					 ?>><a href="<?php echo htmlspecialchars($tab['href']) ?>"><?php
					 echo htmlspecialchars($tab['text']) ?></a></li>
	<?php			 } ?>

    <!-- login etc. -->
<?php 			foreach($this->data['personal_urls'] as $key => $item) { 
                    if ($key == 'anontalk' || $key == 'anonuserpage') continue;
                ?>
				<li id="pt-<?php echo Sanitizer::escapeId($key) ?>"<?php
					if ($item['active']) { ?> class="active"<?php } ?>><a href="<?php
				echo htmlspecialchars($item['href']) ?>"<?php
				if(!empty($item['class'])) { ?> class="<?php
				echo htmlspecialchars($item['class']) ?>"<?php } ?>><?php
				echo htmlspecialchars($item['text']) ?></a></li>
<?php			} ?>

	</ul>		

<? /* ?>

	<script type="<?php $this->text('jsmimetype') ?>"> if (window.isMSIE55) fixalpha(); </script>
	<div id="p-search" class="portlet">
		<h5><label for="searchInput"><?php $this->msg('search') ?></label></h5>
		<div id="searchBody" class="pBody">
			<form action="<?php $this->text('searchaction') ?>" id="searchform"><div>
				<input id="searchInput" name="search" type="text" <?php
					if($this->haveMsg('accesskey-search')) {
						?>accesskey="<?php $this->msg('accesskey-search') ?>"<?php }
					if( isset( $this->data['search'] ) ) {
						?> value="<?php $this->text('search') ?>"<?php } ?> />
				<input type='submit' name="go" class="searchButton" id="searchGoButton"	value="<?php $this->msg('searcharticle') ?>" />&nbsp;
				<input type='submit' name="fulltext" class="searchButton" id="mw-searchButton" value="<?php $this->msg('searchbutton') ?>" />
			</div></form>
		</div>
	</div>

		</div><!-- end of the left (by default at least) column -->
			<div class="visualClear"></div>
			<div id="footer">
			<ul id="f-list">
<?php
		$footerlinks = array(
		#	'lastmod', 'viewcount', 'numberofwatchingusers', 'credits', 'copyright',
		#	'privacy', 'about', 'disclaimer', 'tagline',
        'lastmod'
		);
		foreach( $footerlinks as $aLink ) {
			if( isset( $this->data[$aLink] ) && $this->data[$aLink] ) {
?>				<li id="<?php echo$aLink?>"><?php $this->html($aLink) ?></li>
<?php 		}
		}
?>
			</ul>
<? */ ?>

	<?php $this->html('bottomscripts'); /* JS call to runBodyOnloadHook */ ?>
<?php $this->html('reporttime') ?>
<?php if ( $this->data['debug'] ): ?>
<!-- Debug output:
<?php $this->text( 'debug' ); ?>

-->
<?php endif;
    include($_SERVER['DOCUMENT_ROOT']."/header.html");
	wfRestoreWarnings();
	} // end of execute() method
} // end of class
?>
