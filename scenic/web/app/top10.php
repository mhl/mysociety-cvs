<?php

include ROOT . "/app/helper/h_place.php";
include ROOT . "/app/helper/h_top10.php";

function get_places($places)
{
   global $mySQL;
   
   foreach($places as $place_id => $ranking)
   {
      if($place_id)
      {
         $mySQL->query("select * from place where id=$place_id");
         $place = $mySQL->fetchArray();
         
         $places[$place_id] = $place;
         $places[$place_id]['score'] = $ranking;            
         $places[$place_id]['image_link'] = local_image($places[$place_id]['image_uri']);

         $mySQL->query("select * from vote where place=$place_id");
         $places[$place_id]['votes'] = $mySQL->numRows();
      }
   }

   return $places;
}



$rankings = $places = $votes = array();
$stats['total_rated'] = $stats['partially_rated'] = 0;

$mySQL->query("select place, count(place) as vote_count, avg(rating) as score from vote group by place");
while($place = $mySQL->fetchObject())
{
   if($place->vote_count > 3)
   {
      $rankings[$place->place] = array(round($place->score, 1), $place->vote_count);
   }
   
   if($place->vote_count >= 3)
   {
      $stats['total_rated']++;
   }
   else
   {
      $stats['partially_rated']++;
   }
}

$num = 10;

arsort($rankings);
$top = get_places(array_slice($rankings, 0, $num, true));

function cmp($a, $b) {
    if ($a[0] < $b[0]) return -1;
    if ($a[0] > $b[0]) return 1;
    if ($a[1] < $b[1]) return 1;
    if ($a[1] > $b[1]) return -1;
    return 0;
}
uasort($rankings, 'cmp');
$bottom = get_places(array_slice($rankings, 0, $num, true));



//
// Work out some stats
//

$stats['total_places'] = $config['site']['place_count'];
$stats['total_votes'] = $mySQL->singleValueQuery("select count(*) from vote");

// The percentage of images with 3 or more votes
$stats['percentage_rated'] = round($stats['total_rated'] / $stats['total_places'] * 100, 2);

// The percentage of images with votes 0 < v < 3
$stats['percentage_partial'] = round($stats['partially_rated'] / $stats['total_places'] * 100, 2);

// Total land mass of 229,334km obtained here: http://en.wikipedia.org/wiki/List_of_countries_and_outlying_territories_by_area
$stats['percentage_coverage'] = round($stats['total_places'] / 229334 * 100, 2);

// The percentage of images with 3 or more votes
$stats['percentage_rated'] = round($stats['total_rated'] / $stats['total_places'] * 100, 2);


//
// Go to view
//

include VIEW_DIR . "/_top10.php";

?>
