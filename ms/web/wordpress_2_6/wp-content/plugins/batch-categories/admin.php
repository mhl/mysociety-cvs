<?php

function bc_menus() {
	add_management_page('Batch Categories', 'Batch Categories', 9, 'batch_categories', 'bc_admin_screen');
}
add_action('admin_menu', 'bc_menus');

function bc_admin_head() {
	if ( @$_GET['page'] == 'batch_categories' ) {
		echo '
		<script type="text/javascript" src="' . get_option('siteurl') . '/wp-content/plugins/batch-categories/admin.js"></script>
		<link rel="stylesheet" type="text/css" href="' . get_option('siteurl') . '/wp-content/plugins/batch-categories/admin.css" />
		';
	}
}
add_action('admin_head', 'bc_admin_head');

function bc_admin_screen() {
	global $wpdb, $bc_urls;
	
	// Maybe make this an option some time
	$per_page = 15;
	$paged = empty($_GET['paged']) ? 1 : intval($_GET['paged']);
	
	$orderbys = array(
		'Author'        => 'post_author',
		'Date Posted'   => 'post_date',
		'Date Modified' => 'post_modified',
		'Title'         => 'post_title',
		'Status'        => 'post_status'
	);
	$orderbys_flip = array_flip($orderbys);
	
	// Sorting
	$orderby = ( in_array($_GET['orderby'], $orderbys) ) ? $_GET['orderby'] : 'post_date';
	$order   = ( strtolower($_GET['order']) == 'asc' )   ? 'asc'             : 'desc';
	
	$_POST = stripslashes_deep($_POST);
	$_GET = stripslashes_deep($_GET);
	
	$posts = array();
	
	$num = intval($_GET['num']);
	$what = htmlentities($_GET['what']);
	$message = '';
	// Deal with any update messages we might have:
	switch ( $_GET['done'] ) {
		case 'add':
			$message = "Added $num posts to the category &ldquo;$what&rdquo;.";
			break;
		case 'remove':
			$message = "Removed $num posts from the category &ldquo;$what&rdquo;.";
			break;
		case 'tag':
			$message = "Tagged $num posts with &ldquo;$what&rdquo;.";
			break;
		case 'untag':
			$message = "Untagged $num posts with &ldquo;$what&rdquo;.";
			break;
	}
	
	if ( !empty($message) ) {
		echo "<div id='message' class='updated fade'><p><strong>$message</strong></p></div>";
	}
	
	// Create the hidden input which passes our current filter to the action script.
	if ( !empty($_GET['cat']) )
		$filter = '<input type="hidden" name="cat" value="' . urlencode($_GET['cat']) . '" />';
	if ( !empty($_GET['s']) )
		$filter = '<input type="hidden" name="s" value="' . urlencode($_GET['s']) . '" />';
	if ( !empty($_GET['t']) )
		$filter = '<input type="hidden" name="t" value="' . urlencode($_GET['t']) . '" />';
	
	echo '
		<div class="wrap">
			<h2>Batch Categories</h2>
	';
	
	// Filtering
	echo '
	<div id="filters" class="tablenav">
		<form method="get" action="edit.php">
		<input type="hidden" name="page" value="batch_categories" />
	';
	
	// Sorting
	echo '
		<div class="filter">
			<label for="orderby">Sort by:</label>
			<select name="orderby" id="orderby">
	';
	foreach ( $orderbys as $title => $value ) {
		$selected = ( $orderby == $value ) ? ' selected="selected"' : '';
		echo "<option value='$value'$selected>$title</option>\n";
	}
	echo '
			</select>
			<select name="order" id="order">
			<option value="asc"' . ( $order == 'asc' ? ' selected="selected"' : '' ) . '>Asc.</option>
			<option value="desc"' . ( $order == 'desc' ? ' selected="selected"' : '' ) . '>Desc.</option>
			</select>
		</div>
	';
	
	// Category drop-down
	echo '
		<div class="filter">
			<label for="cat">Category:</label>
			' . wp_dropdown_categories('hide_empty=0&hierarchical=1&echo=0&selected=' . ( isset($_GET['cat']) ? intval($_GET['cat']) : -1 )) . '
		</div>
	';
	
	// ...then the keyword search.
	echo '
		<div class="filter">
			<label for="s">Keyword:</label>
			<input type="text" name="s" id="s" value="' . htmlentities($_GET['s']) . '" title="Use % for wildcards." />
		</div>
	';
	
	// ...then the tag filter.
	echo '
		<div class="filter">
			<label for="s">Tag:</label>
			<input type="text" name="t" id="t" value="' . htmlentities($_GET['t']) . '" title="\'foo, bar\': posts tagged with \'foo\' or \'bar\'. \'foo+bar\': posts tagged with both \'foo\' and \'bar\'." />
		</div>
	';
	
	echo '
		<div class="filter">
			<input type="submit" value="Filter &raquo;" name="submit" />
		</div>
	</form>';
	
	// Fetch our posts.
	
	if ( !empty($_GET['cat']) || !empty($_GET['s']) || !empty($_GET['t']) ) {
		// A cat has been given; fetch posts that are in that category.
		$q = "paged=$paged&posts_per_page=$per_page&orderby=$orderby&order=$order&post_type=post";
		if ( !empty($_GET['cat']) ) {
			$cat = get_cat_name(intval($_GET['cat']));
			$q .= "&category_name=$cat";
		}
		
		// A keyword has been given; get posts whose content contains that keyword.
		if ( !empty($_GET['s']) ) {
			$q .= "&s=" . urlencode($_GET['s']);
		}
		
		// A tag has been given; get posts tagged with that tag.
		if ( !empty($_GET['t']) ) {
			$t = preg_replace('#[^a-z0-9\-\,\+]*#i', '', $_GET['t']);
			$q .= "&tag=$t";
		}
		
		$query = new WP_Query;
		$posts = $query->query($q);
		
		// Pagination
		$pagination = '';
		if ( $query->max_num_pages > 1 ) {
			$current = preg_replace('/&?paged=[0-9]+/i', '', strip_tags($_SERVER['REQUEST_URI'])); // I'll happily take suggestions on a better way to do this, but it's 3am so
			
			$pagination .= "<div class='tablenav-pages'>";
			
			if ( $paged > 1 ) {
				$prev = $paged - 1;
				$pagination .= "<a class='prev page-numbers' href='$current&amp;paged=$prev'>&laquo; Previous</a>";
			}
			
			for ( $i = 1; $i <= $query->max_num_pages; $i++ ) {
				if ( $i == $paged ) {
					$pagination .= "<span class='page-numbers current'>$i</span>";
				} else {
					$pagination .= "<a class='page-numbers' href='$current&amp;paged=$i'>$i</a>";
				}
			}
			
			if ( $paged < $query->max_num_pages ) {
				$next = $paged + 1;
				$pagination .= "<a class='next page-numbers' href='$current&amp;paged=$next'>Next &raquo;</a>";
			}
			
			$pagination .= "</div>";
		}
		
		echo $pagination;
	}
	
	echo "</div>"; // tablenav
	
	// No posts have been fetched, let's tell the user:
	if ( empty($_GET['cat']) && empty($_GET['s']) && empty($_GET['t']) ) {
		echo '
			<p>To get started, select some criteria above.</p>
		';
	} else {
		// Criteria were given, but no posts were matched.
		if ( empty($posts) ) {
			echo '
				<p>No posts matched that criteria, sorry! Try again with something different.</p>
			';
		} 
		// Criteria were given, posts were matched... let's go!
		else {
			echo '
				<form method="get" action="' . get_option('siteurl') . '/wp-content/plugins/batch-categories/action.php">
				<div id="posts">
				
				<table class="widefat">
					<caption>' . 
						sprintf(
							'Looked for posts in <strong>%s</strong>, tagged with <strong>%s</strong>, %s ordered by <strong>%s</strong> %s. Found <strong>%s</strong> posts; displaying <strong>%s</strong> per page.',
							!empty($_GET['cat']) ? get_cat_name($cat) : 'any category',
							!empty($_GET['t']) ? htmlentities($_GET['t']) : 'any tag',
							!empty($_GET['s']) ? 'containing the string <strong>' . htmlentities($_GET['s']) . '</strong>, ' : '', 
							strtolower($orderbys_flip[$orderby]),
							$order == 'asc' ? 'ascending' : 'descending',
							$query->found_posts,
							$per_page
						)
					. '</caption>
					<thead>
						<tr>
							<th scope="col"><input type="checkbox" id="toggle" title="Select all posts" /></th>
							<th scope="col">ID</th>
							<th scope="col">Date</th>
							<th scope="col">Title</th>
							<th scope="col">Current Categories</th>
							<th scope="col">Current Tags</th>
							<th scope="col"></th>
							<th scope="col"></th>
						</tr>
					</thead>
					<tbody id="the-list">
			';
			foreach ( (array) $posts as $post ) {
				
				$categories = wp_get_post_categories($post->ID);
				$cats = '';
				foreach ( (array) $categories as $cat ) {
					$cats .= '<a href="' . sprintf($bc_urls['category'], $cat) . '">' . get_cat_name($cat). '</a> ';
				}
				
				$_tags = wp_get_post_tags($post->ID);
				$tags = '';
				foreach ( $_tags as $tag ) {
					$tags .= "<a href='?page=batch_categories&t=$tag->slug'>$tag->name</a>, ";
				}
				$tags = substr($tags, 0, strlen($tags) - 2);
				if ( empty ($tags) ) {
					$tags = 'No Tags';
				}
				
				echo '
						<tr' . ( $i++ % 2 == 0  ? ' class="alternate"' : '' ) .'>
							<td><input type="checkbox" name="ids[]" value="' . $post->ID . '" /></td>
							<td>' . $post->ID . '</td>
							<td>
				';
				
				if ( '0000-00-00 00:00:00' == $post->post_date ) {
					_e('Unpublished');
				} else {
					if ( ( time() - get_post_time() ) < 86400 ) {
						echo sprintf( __('%s ago'), human_time_diff( get_post_time() ) );
					} else {
						echo date(__('Y/m/d'), strtotime($post->post_date));
					}
				}
				
				echo '</td>
							<td>' . $post->post_title . '</td>
							<td>' . $cats . '</td>
							<td>' . $tags . '</td>
							<td><a href="' . get_permalink($post->ID) . '">View</a></td>
							<td><a href="post.php?action=edit&post=' . $post->ID . '">Edit</a></td>
						</tr>
				';
			}
			echo '
					</tbody>
				</table>
			';
			
			// Now, our actions.
			echo '
			<div id="actions" class="tablenav">
				' . $filter . '
				<div class="action">
					<label for="cat">Category:</label>
					' . wp_dropdown_categories('hide_empty=0&hierarchical=1&echo=0') . '
					<input type="submit" name="add" value="Add to" title="Add the selected posts to this category." />
					<input type="submit" name="remove" value="Remove from" title="Remove the selected posts from this category." />
				</div>
				
				<div class="action">
					<label for="cat">Tags:</label>
					<input type="text" name="tags" title="Separate multiple tags with commas." />
					<input type="submit" name="replace_tags" value="Replace" title="Replace the selected posts\' current tags with these ones." />
					<input type="submit" name="tag" value="Add" title="Add these tags to the selected posts without altering the posts\' existing tags." />
					<input type="submit" name="untag" value="Remove" title="Remove these tags from the selected posts." />
				</div>
				
				' . $pagination . '
			</div>
			';
			
			wp_nonce_field('batch_categories-edit');
			echo '
				</form>
				</div>
			';
		}
	}
}

?>
