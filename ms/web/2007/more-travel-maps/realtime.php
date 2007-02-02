<?php 
/* XXX can't override the title easily, which will make us look like total
 * morons. For this page it should be, "Travel-time maps". */
include "../../wordpress/wp-blog-header.php";
include "../../wordpress/wp-content/themes/mysociety/header.php"; 
?>

<h1>Real time travel maps</h1>

<p>This work was funded and supported by the <a href="http://www.dft.gov.uk/">Department&nbsp;for&nbsp;Transport</a>.</p>

<ul>
<li><a href="#introduction">Introduction</a></li>
<li><a href="#railplanner">Using RailPlanner</a></li>
<li><a href="#"></a></li>
<li><a href="#"></a></li>
</ul>

<h2><a name="introduction"></a>Introduction</h2>

After seeing our travel time maps (<a href="/2006/travel-time-maps">here</a>
and <a href="index.php">here</a>), the next thing that everyone asks is "can I
have one for my journey to work?". We investigated in detail two ways
of providing real time versions of these maps, and suggest a third way
which requires new data.

<h2><a name="screenscraping"></a>Better screen scraping</h2>

<p>Suppose we want to create a time contour map of journey time to work by 9am
for any selected postcode in the UK.  How long this takes depends on where in
the country the map is centred. In particular, it depends on the density of bus
stops and railway stations. First, some background explanation.

<h1>Basic screen scraping</h1>

<p>"Basic screen scraping" is the technique which we used to generate the
example travel time maps which you've seen. This was done by "screen scraping"
the <a href="http://www.transportdirect.info">Transport Direct</a> website.
That is, writing a computer program which operated the normal web interface of
the site to calculate journey times between lots of points and the destination
postcode.

<p>The obvious thing to do would be to fetch the journey between every single
point on the final diagram and the destination postcode.  However, this would
involve far too many queries. Instead we only queried for the journey between
every public transport stop and the destination postcode. We then used our own
replication of part of the Transport Direct algorithm to calculate the journey
time from a specific point to the destination postcode. This is done by adding
the walking time to the appropriately nearest/fastest public transport stop.

<p>So, we have the journey time from every point to the destination postcode.
This takes a long time to generate, as the query to the website for each
journey takes 8 seconds. For example, there are about 1900 public transport
stops in a 20km square around Cardiff central railway station. That makes
in total about 4 hours and 15 minutes for Cardiff. From that point on, the
contour maps are quick to produce.

<p>This table shows the calculation time 

<table border=1>
<tr><th>City</th><th>Public transport stops<br>in 20km square (approx)</th><th>Basic screen scraping<br>Generation time (estimate)</th>
<tr><td>Cardiff</td><td>1900</td><td>4 hours 15 mins</td></tr>
<tr><td>Edinburgh</td><td>2700</td><td>6 hours</td></tr>
<tr><td>Birmingham</td><td>6600</td><td>14 hours 45 mins</td></tr>
<tr><td>London</td><td>10100</td><td>22 hours 30 mins</td></tr>
</table>

<h1>Parallel screen scraping</h1>

<p>The slow generation time was not a problem for making a few maps.  However,
we would very much like to be able to offer everyone who wants it there own
map. 

# 64 processes - 110-120 seconds / separate query = query every 1.79 seconds
# 32 processes -  40- 50 seconds / separate query = query every 1.40 seconds
# 16 processes -  25     seconds / separate query = query every 1.56 seconds
#  8 processes -  17     seconds / separate query = query every 2.13 seconds
#  4 processes -  14     seconds / separate query = query every 3.50 seconds
#  2 processes -  11     seconds / separate query = query every 5.50 seconds
#  1 process   -   8     seconds / separate query = query every 8.00 seconds


<h1>Smarter algorithm</h1>

<h2><a name="railplanner"></a>Using RailPlanner</h2>
What Chris did with rails as local (need screenshots)

<p><a href="ttm-screenshot.png"><img src="ttm-screenshot_small.png" alt="Realtime isochrone maps"></a>
<br><em>Click image for bigger version.</em><br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>

<h2><a name="background"></a>Future</h2>
What could do if had data / local timetabler ourselves

<?php include "../../wordpress/wp-content/themes/mysociety/footer.php"; ?>
