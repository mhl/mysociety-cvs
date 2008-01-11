<script type="text/javascript" src="swfobject.js"></script>

<?php 

function interactive_map($config_file, $id, $width, $height) { ?>

<div style="text-align: center">

<div id="<?=$id?>">If you can see this for more than a moment, please enable Javascript for this page and make sure you have installed <a href="http://www.adobe.com/products/flashplayer/">Flash Player 9</a> from Adobe.</div>

<script type="text/javascript">
   var so = new SWFObject("MysocietyThresholds.swf", "MysocietyThresholds", "<?=$width?>", "<?=$height?>", "9", "#000000");
   so.useExpressInstall('expressinstall.swf');
   so.addVariable("configURL", "<?= $config_file ?>");
   so.write("<?=$id?>");
</script>

</div>

<?php } 


?>
