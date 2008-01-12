<script type="text/javascript" src="swfobject.js"></script>

<?php 

function interactive_map($config_file, $id, $width, $height) { ?>

<div style="text-align: center">

<div id="<?=$id?>">If you can see this for more than a moment, please enable Javascript for this page and make sure you have installed <a href="http://www.adobe.com/products/flashplayer/">Flash Player 9</a> from Adobe.</div>

<script type="text/javascript">
    function queryToHash(q) {
        var newh = new Array();
        var vars = q.replace(/#/, "").split("&");
        for (var i=0;i<vars.length;i++) {
            var pair = vars[i].split("=");
            newh[pair[0]] = pair[1];
        }
        return newh
     }
     function hashToQuery(h) {
        q = "";
        for (var i in h) {
            if (i != "") {
                q = q + i + "=" + h[i] + "&";
            }
        }
        return "#" + q
     }

    function setHash(h) {
        curh = queryToHash(location.hash);
        newh = queryToHash(h);
        for (var i in newh) {
            curh[i] = newh[i];
        }
        location.hash = hashToQuery(curh);
    }

    function getHash() {
        return location.hash;
    }

   var so = new SWFObject("MysocietyThresholds.swf", "MysocietyThresholds", "<?=$width?>", "<?=$height?>", "9", "#000000");
   so.useExpressInstall('expressinstall.swf');
   so.addVariable("configURL", "<?= $config_file ?>");
   so.write("<?=$id?>");
</script>

</div>

<?php } 


?>
