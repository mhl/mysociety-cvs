<?php
/*
Plugin Name: Excerpt Editor
Plugin URI: http://www.laptoptips.ca/projects/wordpress-excerpt-editor/
Description: Add or edit excerpts for Posts and Pages.
Version: 1.1
Author: Andrew Ozz
Author URI: http://www.laptoptips.ca/

Released under the GPL version 2, http://www.gnu.org/copyleft/gpl.html

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
*/

$pgee_load_txtdomain = true;
function pgee_txtdomain() {
    global $pgee_load_txtdomain;
    
    if( $pgee_load_txtdomain ) {
        load_plugin_textdomain('excerpt-editor', 'wp-content/plugins/excerpt-editor/languages');
        $pgee_load_txtdomain = false;
    }
}

function pgee_append_css() {
    global $wp_query;
    
    if( empty($wp_query->is_single) && empty($wp_query->is_page) ) return;
    
    $appendopt = get_option('pgee_append_options');
    if( $appendopt['append_to_posts'] == '1' || $appendopt['append_to_pages'] == '1' || $appendopt['append_subpages'] == '1') {
        
// ***************************************************************
// Edit below to change the appearance of the appended excerpts 
?>
<style type="text/css">
.pgee-exc-before {
font: normal 1.3em 'Lucida Grande', 'Lucida Sans Unicode', Verdana, Helvetica, sans-serif;
margin: 20px 0 10px;
}
.pgee-exc-title {
font: bold 1.1em Arial, Helvetica, sans-serif;
margin: 15px 0 5px;
}
.pgee-exc-text {
font-size: 0.9em;
}
.pgee-read-more {
font-size: 0.9em;
}
</style>
<?php 
// End editing
// ****************************************************************
    }
}
add_action( 'wp_head', 'pgee_append_css' );

function pgee_make($pst) {
    $autoopt = get_option('pgee_auto_options');
    
    if( ! empty($autoopt['pgee_tags']) ) $html_tags = $autoopt['pgee_tags'];
    else $html_tags = false;

    $cut = true;
    if ( strpos($pst, '<!--more') && $autoopt['pgee_more'] == '1' ) {
        $pst = substr( $pst, 0, strpos($pst, '<!--more') );
        $cut = false;
    }

    $pst = preg_replace('@<script[^>]*?>.*?</script>@si', '', $pst); //remove js <? 
    $pst = preg_replace('@<![\s\S]*?--[ \t\n\r]*>@', '', $pst); // remove CDATA, html comments 
    
    if ( $html_tags ) $pst = strip_tags($pst, $html_tags);
	else $pst = strip_tags($pst);

    if( $cut ) {
        
        $words = explode(' ', $pst, $autoopt['pgee_length'] + 1); // from WP
        if (count($words) > $autoopt['pgee_length']) array_pop($words);
        $pst = implode(' ', $words);
        
        if ( $html_tags ) {
            if ( strpos($pst, '<') !== false && ( ! strpos($pst, '>') || strrpos($pst, '<') > strrpos($pst, '>') ) ) $pst = substr( $pst, 0, strrpos($pst, '<') );
        }
        
        $pst = rtrim($pst);
        $pst = rtrim($pst, '.,:;');
    }
    
    if ( $html_tags ) $pst = balanceTags($pst, true);
	
    return $pst;
}

function pgee_auto_generate($the_post = '') {
    global $wp_query;
    
    if( ! is_object($the_post) ) return '';
    
    if( '' == trim($the_post->post_excerpt) && '' == trim($the_post->post_content) ) return '';
    pgee_txtdomain();
    
    if ( ! empty($the_post->post_password) ) { // if there's a password (from WP)
        if ( $_COOKIE['wp-postpass_'.COOKIEHASH] != $the_post->post_password ) {  // and it doesn't match the cookie
            $excerpt = __('Protected post.', 'excerpt-editor');
            return $excerpt;
        }
    }
    
    $autoopt = get_option('pgee_auto_options');
    $replaceopt = get_option('pgee_replace_options');
    
    $exc = trim($the_post->post_excerpt);
    if ( empty($exc) ) {
        $generated = true;
        $exc = pgee_make($the_post->post_content);
    }
    
    $excerpt = convert_chars($exc);
    if( $wp_query->is_feed ) $excerpt = ent2ncr($excerpt);
    else {
        $excerpt = wptexturize($excerpt);
        $excerpt = convert_smilies($excerpt);
        $excerpt = wpautop($excerpt);
    }
    
    $p = false;
    $excerpt = trim($excerpt);
    if ( substr( $excerpt, -4 ) == '</p>' ) {
        $excerpt = substr( $excerpt, 0, -4 ); 
        $p = true;
    }

    if ( $generated && substr( $excerpt, -1 ) != '>' ) $excerpt .= '&#8230; ';

    if ( $autoopt['more_link'] == '1' ) {
        if ( substr( $excerpt, -1 ) != '>' ) $tg = 'span';
        else $tg = 'div';
        
        $more_text = sprintf( stripslashes($autoopt['more_text']), $the_post->post_title );
        
        $excerpt .= ' <' . $tg . ' class="pgee-read-more"><a href="' . get_permalink($the_post->ID) . '">' . $more_text . '</a>';
        if( $autoopt['more_link_cc'] == '1' && $replaceopt['no_cmnt_count'] != '1' ) {
            if( $the_post->comment_count > 1 )
                $excerpt .= ' | <a href="' . get_permalink($the_post->ID) . '#comments">' . $the_post->comment_count . ' ' . __('Comments', 'excerpt-editor') . '</a>';
            if( $the_post->comment_count == 1 )
                $excerpt .= ' | <a href="' . get_permalink($the_post->ID) . '#comments"> 1 ' . __('Comment', 'excerpt-editor') . '</a>';
        }
        $excerpt .= '</' . $tg . '>';
    }
    if ( $p ) $excerpt .= '</p>';
    return $excerpt;
}

function pgee_page_excerpt() {
    global $post;
?>
    <input type="hidden" name="excerpt" id="excerpt" value="<?php echo $post->post_excerpt; ?>" />
<?php
}
add_action( 'edit_page_form', 'pgee_page_excerpt' );

function pgee_append_excerpts($content) {
    global $post, $wp_query, $wpdb;
    
    if( ( empty($wp_query->is_single) && empty($wp_query->is_page) ) || $wp_query->is_feed ) 
        return $content;
    
    $appendopt = get_option('pgee_append_options');
    if( $appendopt['append_to_posts'] != '1' && $appendopt['append_to_pages'] != '1' && $appendopt['append_subpages'] != '1' )
        return $content;

    if( in_array($post->ID, (array) $appendopt['dont_append']) ) return $content;
    (array) $appendopt['append_exclude'][] = $post->ID;
    $output = '';
    
    if( ! empty($appendopt['append_include']) && $post->ID != $appendopt['append_include'] ) {
        $included = get_post($appendopt['append_include']);
        $appendopt['append_exclude'][] = $appendopt['append_include'];
    }
    
    sort($appendopt['append_exclude']);
    $excluded = implode( ',', $appendopt['append_exclude'] );
    
    if( ( ($appendopt['append_to_posts'] == '1' && $wp_query->is_single) 
    || ($appendopt['append_to_pages'] == '1' && $wp_query->is_page) )
    && $appendopt['append_number_posts'] > '0' ) {
        $getposts_args = array( 'numberposts' => $appendopt['append_number_posts'], 'exclude' => $excluded );
        $getposts = get_posts( $getposts_args );
    } else {
        $getposts = '';
    }

    if( ! empty($appendopt['before_appended']) ) $before_appended = stripslashes($appendopt['before_appended']);
    else $before_appended = '';
    
    if( $post->post_type == 'post' && $appendopt['append_to_posts'] == '1' ) {

        if( $appendopt['append_newest_post'] == '1' && empty($getposts) ) {
            $newest = get_posts( array('numberposts' => '1') );
            $newest_post = $newest['0'];
            if( $newest_post->ID != $post->ID ) {
                $exc = pgee_auto_generate($newest_post);
                $output .= '<div class="pgee-exc-title"><a href="' . get_permalink($newest_post->ID) . '">' . $newest_post->post_title . '</a></div>' . "\n";
                $output .= '<div class="pgee-exc-text">' . $exc . '</div>' . "\n\n";
            }
        }
        
        if( ! empty($included) ) {
            $exc = pgee_auto_generate($included);
            $output .= '<div class="pgee-exc-title"><a href="' . get_permalink($included->ID) . '">' . $included->post_title . '</a></div>' . "\n";
            $output .= '<div class="pgee-exc-text">' . $exc . '</div>' . "\n\n";
        }
        
        if( ! empty($getposts) ) {
            foreach( $getposts as $the_post ) {
                $exc = pgee_auto_generate($the_post);
                $output .= '<div class="pgee-exc-title"><a href="' . get_permalink($the_post->ID) . '">' . $the_post->post_title . '</a></div>' . "\n";
                $output .= '<div class="pgee-exc-text">' . $exc . '</div>' . "\n\n";
            }
        }
        
        if( $output && ! empty($before_appended) ) $output = '<div class="pgee-exc-before">' . $before_appended . '</div>' . "\n" . $output;
        
        return $content . $output;
    }
    
    if( $post->post_type == 'page' && ( $appendopt['append_to_pages'] == '1' || $appendopt['append_subpages'] == '1' ) ) {
        
        if( $appendopt['append_newest_post'] == '1' ) {
            if( ! empty($getposts) ) {
                $newest_post = $getposts['0'];
                unset($getposts['0']);
            } else {
                $newest = get_posts( array('numberposts' => '1') );
                $newest_post = $newest['0'];
            }
            
            $exc = pgee_auto_generate($newest_post);
            $output .= '<div class="pgee-exc-title"><a href="' . get_permalink($newest_post->ID) . '">' . $newest_post->post_title . '</a></div>' . "\n";
            $output .= '<div class="pgee-exc-text">' . $exc . '</div>' . "\n\n";
        }

        if( ! empty($included) ) {
            $exc = pgee_auto_generate($included);
            $output .= '<div class="pgee-exc-title"><a href="' . get_permalink($included->ID) . '">' . $included->post_title . '</a></div>' . "\n";
            $output .= '<div class="pgee-exc-text">' . $exc . '</div>' . "\n\n";
        }
        
        if( $appendopt['append_subpages'] == '1' && $appendopt['append_number_pages'] > 0 ) {
            
            $order_by = 'post_date'; // order of page children
            $limit = (int) $appendopt['append_number_pages'];
            $sql = "SELECT * FROM $wpdb->posts WHERE post_parent = $post->ID AND post_type = 'page' AND post_status = 'publish' AND ID NOT IN ($excluded) ORDER BY $order_by DESC LIMIT $limit ";
            $getpages = $wpdb->get_results($sql);

            if( $getpages ) {
                foreach( $getpages as $the_page ) {
                    $exc = pgee_auto_generate($the_page);
                    $output .= '<div class="pgee-exc-title"><a href="' . get_permalink($the_page->ID) . '">' . $the_page->post_title . '</a></div>' . "\n";
                    $output .= '<div class="pgee-exc-text">' . $exc . '</div>' . "\n\n";
                }
            }
        }
        
        if( $appendopt['append_to_pages'] == '1' && ! empty($getposts) ) {
            foreach( $getposts as $the_post ) {
                $exc = pgee_auto_generate($the_post);
                $output .= '<div class="pgee-exc-title"><a href="' . get_permalink($the_post->ID) . '">' . $the_post->post_title . '</a></div>' . "\n";
                $output .= '<div class="pgee-exc-text">' . $exc . '</div>' . "\n\n";
            }
        }

        if( $output && ! empty($before_appended) ) $output = '<div class="pgee-exc-before">' . $before_appended . '</div>' . "\n" . $output;
        
        return $content . $output;
    } 
    return $content;
}
add_filter( 'the_content', 'pgee_append_excerpts', 65 );

function pgee_deactiv() {
    delete_option('pgee_options');
    delete_option('pgee_auto_options');
    delete_option('pgee_append_options');
    delete_option('pgee_replace_options');
}
add_action( 'deactivate_excerpt-editor/excerpt-editor.php', 'pgee_deactiv' );

function pgee_insert_excerpt($excerpt) {
    global $post, $wp_query;
    $autoopt = get_option('pgee_auto_options');
    
    if ( $wp_query->is_feed && $autoopt['in_rss'] == '1' ) return pgee_auto_generate($post);
    if ( ! $wp_query->is_feed && $autoopt['on_site'] == '1' )   return pgee_auto_generate($post);
    return $excerpt;
}
add_filter( 'the_excerpt', 'pgee_insert_excerpt' );
add_filter( 'the_excerpt_rss', 'pgee_insert_excerpt' );

function pgee_replace_posts($content) {
    global $post, $wp_query;

    if( ( empty($wp_query->is_home) && empty($wp_query->is_archive) && empty($wp_query->is_tag) ) || $wp_query->is_feed ) 
        return $content;

    $replaceopt = get_option('pgee_replace_options');
    
    if( $replaceopt['keep_latest'] == '1' ) {
        $latest = get_posts( array('numberposts' => '1') );
        if( $latest[0]->ID == $post->ID ) return $content;
    }

    if( ($wp_query->is_home && $replaceopt['replace_home'] == '1') ||
    ($wp_query->is_archive && $replaceopt['replace_archives'] == '1') ||
    ($wp_query->is_tag && $replaceopt['replace_tags'] == '1') ) 
        $content = pgee_auto_generate($post);

    return $content;
}
add_filter( 'the_content', 'pgee_replace_posts', 60 );

function pgee_adminpage() {
	include_once( dirname(__FILE__).'/pgee_admin.php' );
}

function pgee_adminpage_head() {
?>
<link rel="stylesheet" href="<?php bloginfo('wpurl'); ?>/wp-content/plugins/excerpt-editor/excerpt-editor.css" type="text/css" />
<?php
}

function pgee_menu() { 
    if( function_exists('add_management_page') ) {
	   pgee_txtdomain();
       $page = add_management_page( __('Excerpt Editor', 'excerpt-editor'), __('Excerpt Editor', 'excerpt-editor'), 8,  __FILE__, 'pgee_adminpage' );
	   add_action("admin_print_scripts-$page", 'pgee_adminpage_head');
    }
}
add_action( 'admin_menu', 'pgee_menu' );
?>