<?php 
/* XXX can't override the title easily, which will make us look like total
 * morons. For this page it should be, "Travel-time maps". */
include "../../wordpress/wp-blog-header.php";
include "../../wordpress/wp-content/themes/mysociety/header.php"; 
include "interactive_map.php";
?>

<h1>Travel time and house price maps</h1>

<p>This page contains two larger, more detailed travel time and house price maps of
London. Read the <a href="index.php">main page</a> to learn more about these maps.

<h2>BBC Television Center</h2>

<p>This map is quite zoomed in, showing 20km round the BBC Television Center at
W12 7RJ. Adjust the sliders to see areas within varying travel times to work
and with varying house prices.

<?php interactive_map("w127rj-800-20km/config.xml", "maphouse2", 800, 909) ?>

<h2>Olympic Stadium Site</h2>

<p>This map shows more of London, 40 km round the Olympic Stadium Site in
Stratford at E15 2NQ. Adjust the sliders to see areas within varying travel
times to work and with varying house prices.

<?php interactive_map("e152nq-800-40km/config.xml", "maphouse3", 800, 909) ?>

<p><a href="index.php">Main page explaining these maps</a>

<?php include "../../wordpress/wp-content/themes/mysociety/footer.php"; ?>
