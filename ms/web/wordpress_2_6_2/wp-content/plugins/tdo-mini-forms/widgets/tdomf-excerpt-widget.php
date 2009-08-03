<?php
/*
Name: "Excerpt"
URI: http://thedeadone.net/software/tdo-mini-forms-wordpress-plugin/
Description: This widget provides a box to edit the excerpt of a submission
Version: 1
Author: Mark Cunningham
Author URI: http://thedeadone.net
*/

if(preg_match('#' . basename(__FILE__) . '#', $_SERVER['PHP_SELF'])) { die('TDOMF: You are not allowed to call this page directly.'); }


/////////////////////////////////////////
// Default options for the excerpt widget 
//
function tdomf_widget_excerpt_get_options($form_id) {
   $options = tdomf_get_option_widget('tdomf_excerpt_widget',$form_id);
    if($options == false) {
       $options = array();
       $options['title'] = "";
       $options['text-required'] = true;
       $options['text-cols'] = 40;
       $options['text-rows'] = 10; 
       $options['quicktags'] = false;
       $options['restrict-tags'] = true;
       $options['allowable-tags'] = "<p><b><em><u><strong><a><img><table><tr><td><blockquote><ul><ol><li><br><sup>";
    }
    if(!isset($options['char-limit'])) {
       $options['char-limit'] = 0;
    }
    if(!isset($options['word-limit'])) {
       $options['word-limit'] = 0;
    }
  return $options;
}

//////////////////////////////
// Display the excerpt widget! 
//
function tdomf_widget_excerpt($args) {
  extract($args);
  $options = tdomf_widget_excerpt_get_options($tdomf_form_id);

  $output = $before_widget;
  if($options['title'] != "") {
    $output .= $before_title.$options['title'].$after_title;
  }

    if($options['text-required']) {
      $output .= '<label for="excerpt_excerpt" class="required">'.__("Excerpt (Required): ","tdomf")."<br/>\n";      
    } else {
      $output .= '<label for="excerpt_excerpt">'.__("Excerpt: ","tdomf")."<br/>\n";
    }
    $output .= "</label>\n";    
    if($options['allowable-tags'] != "" && $options['restrict-tags']) {
      $output .= sprintf(__("<small>Allowable Tags: %s</small>","tdomf"),htmlentities($options['allowable-tags']))."<br/>";
    }
    if($options['word-limit'] > 0) {
      $output .= sprintf(__("<small>Max Word Limit: %d</small>","tdomf"),$options['word-limit'])."<br/>";
    }
    if($options['char-limit'] > 0) {
      $output .= sprintf(__("<small>Max Character Limit: %d</small>","tdomf"),$options['char-limit'])."<br/>";
    }
    if($options['quicktags'] == true) {
      $qt_path = TDOMF_URLPATH."tdomf-quicktags.js.php?postfix=excerpt_widget";
      if($options['allowable-tags'] != "" && $options['restrict-tags']) {
        $qt_path = TDOMF_URLPATH."tdomf-quicktags.js.php?postfix=excerpt_widget&allowed_tags=".urlencode($options['allowable-tags']);
      }
      $output .= "\n<script src='$qt_path' type='text/javascript'></script>\n";
      $output .= "\n<script type='text/javascript'>edToolbarexcerpt_widget();</script>\n";
    }
    $output .= '<textarea title="true" rows="'.$options['text-rows'].'" cols="'.$options['text-cols'].'" name="excerpt_excerpt" id="excerpt_excerpt" >'.$excerpt_excerpt.'</textarea>';
    if($options['quicktags'] == true) {
      $output .= "\n<script type='text/javascript'>var edCanvasexcerpt_widget = document.getElementById('excerpt_excerpt');</script>\n";
    }

  $output .= $after_widget;
  return $output;
}
tdomf_register_form_widget('excerpt',__('Excerpt','tdomf'), 'tdomf_widget_excerpt', $modes = array('new'));

// Hacked version
//
function tdomf_widget_excerpt_hack($args) {
  extract($args);
  $options = tdomf_widget_excerpt_get_options($tdomf_form_id);
  
  $output = $before_widget;
  
  if($options['title'] != "") {
    $output .= $before_title.$options['title'].$after_title;
  }
  
    if($options['text-required']) {
      $output .= "\t\t".'<label for="excerpt_excerpt" class="required">'.__("Post Text (Required): ","tdomf")."\n\t\t\t<br/>\n";      
    } else {
      $output .= "\t\t".'<label for="excerpt_excerpt">'.__("Post Text: ","tdomf")."\n\t\t\t<br/>\n";
    }
    $output .= "\t\t</label>\n";    
    if($options['allowable-tags'] != "" && $options['restrict-tags']) {
      $output .= "\t\t".sprintf(__("<small>Allowable Tags: %s</small>","tdomf"),htmlentities($options['allowable-tags']))."\n\t\t<br/>\n";
    }
    if($options['word-limit'] > 0) {
      $output .= "\t\t".sprintf(__("<small>Max Word Limit: %d</small>","tdomf"),$options['word-limit'])."\n\t\t<br/>\n";
    }
    if($options['char-limit'] > 0) {
      $output .= "\t\t".sprintf(__("<small>Max Character Limit: %d</small>","tdomf"),$options['char-limit'])."\n\t\t<br/>\n";
    }
    if($options['quicktags'] == true) {
      $qt_path = TDOMF_URLPATH."tdomf-quicktags.js.php?postfix=excerpt_widget";
      if($options['allowable-tags'] != "" && $options['restrict-tags']) {
        $qt_path = TDOMF_URLPATH."tdomf-quicktags.js.php?postfix=excerpt_widget&allowed_tags=".urlencode($options['allowable-tags']);
      }
      $output .= "\t\t<script src='$qt_path' type='text/javascript'></script>\n";
      $output .= "\t\t<script type='text/javascript'>edToolbarexcerpt_widget();</script>\n";
    }
    $output .= "\t\t".'<textarea title="true" rows="'.$options['text-rows'].'" cols="'.$options['text-cols'].'" name="excerpt_excerpt" id="excerpt_excerpt" >';
    $output .= '<?php echo $excerpt_excerpt; ?></textarea>'."\n"; 
    if($options['quicktags'] == true) {
      $output .= "\t\t<script type='text/javascript'>var edCanvasexcerpt_widget = document.getElementById('excerpt_excerpt');</script>";
    }

  $output .= $after_widget;
  return $output;
}
tdomf_register_form_widget_hack('excerpt',__('Excerpt','tdomf'), 'tdomf_widget_excerpt_hack', $modes = array('new'));

///////////////////////////////////////
// Preview the post's excerpt
//
function tdomf_widget_excerpt_preview($args) {
  extract($args);
  $options = tdomf_widget_excerpt_get_options($tdomf_form_id);

  $output = $before_widget;
  if($options['title'] != "") {
    $output .= $before_title.$options['title'].$after_title;
  }
  if($options['title-enable']) {
    $output .= "<b>".__("Title: ","tdomf")."</b>";
    $output .= $excerpt_title;
    $output .= "<br/>";
  }

    $output .= "<b>".__("Excerpt: ","tdomf")."</b><br/>";

    if($options['allowable-tags'] != "" && $options['restrict-tags']) {
      $output .= apply_filters('the_excerpt', strip_tags($excerpt_excerpt,$options['allowable-tags']));
    } else {
      $output .= apply_filters('the_excerpt', $excerpt_excerpt);
    }

  $output .= $after_widget;
  return $output;
}
tdomf_register_form_widget_preview('excerpt',__('Excerpt','tdomf'), 'tdomf_widget_excerpt_preview', $modes = array('new'));

///////////////////////////////////////
// Hack the preview the post's excerpt and title
//
function tdomf_widget_excerpt_preview_hack($args) {
  extract($args);
  $options = tdomf_widget_excerpt_get_options($tdomf_form_id);

  $output = $before_widget;
  if($options['title'] != "") {
    $output .= $before_title.$options['title'].$after_title;
  }
  
    // prep output
    $output .= "\t<?php ";
    if($options['allowable-tags'] != "" && $options['restrict-tags']) {
      $output .= "\t".'$excerpt_excerpt = apply_filters(\'the_excerpt\', strip_tags($excerpt_excerpt,\''.$options['allowable-tags'].'\'));';
    } else {
      $output .= "\t".'$excerpt_excerpt = apply_filters(\'the_excerpt\', $excerpt_excerpt);';
    }
    $output .= " ?>\n";
    $output .= "\t<b>".__("Excerpt: ","tdomf")."</b>\n\t<br/>\n";
    $output .= "\t<?php echo \$excerpt_excerpt; ?>";

  $output .= $after_widget;
  return $output;
}
tdomf_register_form_widget_preview_hack('excerpt',__('Excerpt','tdomf'), 'tdomf_widget_excerpt_preview_hack', $modes = array('new'));

///////////////////////////////////////
// Add the excerpt to the post 
//
function tdomf_widget_excerpt_post($args) {
  extract($args);
  $options = tdomf_widget_excerpt_get_options($tdomf_form_id);
  
  // Grab existing data
  $post = wp_get_single_post($post_ID, ARRAY_A);
  if(!empty($post['post_excerpt'])) {
    $post = add_magic_quotes($post);
  }
  $post_excerpt = $post['post_excerpt'];
  
  if($options['allowable-tags'] != "" && $options['restrict-tags']) {
    tdomf_log_message("Excerpt Widget: Stripping tags from excerpt!");
    $post_excerpt .= strip_tags($excerpt_excerpt,$options['allowable-tags']);
  } else {
    $post_excerpt .= $excerpt_excerpt;
  }
  
  $post = array (
      "ID"                      => $post_ID,
      "post_excerpt"            => $post_excerpt,
  );

  $post_ID = wp_update_post($post);
  return NULL;
}
tdomf_register_form_widget_post('excerpt',__('Excerpt','tdomf'), 'tdomf_widget_excerpt_post', $modes = array('new'));

///////////////////////////////////////////////////
// Display and handle excerpt widget control panel 
//
function tdomf_widget_excerpt_control($form_id) {
  $options = tdomf_widget_excerpt_get_options($form_id);
  // Store settings for this widget
    if ( $_POST['excerpt-submit'] ) {
     $newoptions['title'] = strip_tags(stripslashes($_POST['excerpt-title']));
     $newoptions['text-required'] = isset($_POST['excerpt-text-required']);
     $newoptions['text-cols'] = intval($_POST['excerpt-text-cols']);
     $newoptions['text-rows'] = intval($_POST['excerpt-text-rows']); 
     $newoptions['restrict-tags'] = isset($_POST['excerpt-restrict-tags']);
     $newoptions['allowable-tags'] = $_POST['excerpt-allowable-tags'];
     $newoptions['quicktags'] = $_POST['excerpt-quicktags'];
     $newoptions['char-limit'] = intval($_POST['excerpt-char-limit']);
     $newoptions['word-limit'] = intval($_POST['excerpt-word-limit']);
     if ( $options != $newoptions ) {
        $options = $newoptions;
        tdomf_set_option_widget('tdomf_excerpt_widget', $options,$form_id);
        
     }
  }

   // Display control panel for this widget
  
  extract($options);

        ?>
<div>
<label for="excerpt-title" style="line-height:35px;display:block;"><?php _e("Title: ","tdomf"); ?><input type="textfield" id="excerpt-title" name="excerpt-title" value="<?php echo htmlentities($options['title'],ENT_QUOTES,get_bloginfo('charset')); ?>" /></label>

<h4><?php _e("Excerpt of Post","tdomf"); ?></h4>
<label for="excerpt-text-required" style="line-height:35px;"><?php _e("Required","tdomf"); ?> <input type="checkbox" name="excerpt-text-required" id="excerpt-text-required" <?php if($options['text-required']) echo "checked"; ?> ></label>
<br/>
<label for="excerpt-quicktags" style="line-height:35px;"><?php _e("Use Quicktags","tdomf"); ?> <input type="checkbox" name="excerpt-quicktags" id="excerpt-quicktags" <?php if($options['quicktags']) echo "checked"; ?> ></label>
<br/>
<label for="excerpt-char-limit" style="line-height:35px;"><?php _e("Character Limit <i>(0 indicates no limit)</i>","tdomf"); ?> <input type="textfield" name="excerpt-char-limit" id="excerpt-char-limit" value="<?php echo htmlentities($options['char-limit'],ENT_QUOTES,get_bloginfo('charset')); ?>" size="3" /></label>
<br/>
<label for="excerpt-word-limit" style="line-height:35px;"><?php _e("Word Limit <i>(0 indicates no limit)</i>","tdomf"); ?> <input type="textfield" name="excerpt-word-limit" id="excerpt-word-limit" value="<?php echo htmlentities($options['word-limit'],ENT_QUOTES,get_bloginfo('charset')); ?>" size="3" /></label>
<br/>
<label for="excerpt-text-cols" style="line-height:35px;"><?php _e("Cols","tdomf"); ?> <input type="textfield" name="excerpt-text-cols" id="excerpt-text-cols" value="<?php echo htmlentities($options['text-cols'],ENT_QUOTES,get_bloginfo('charset')); ?>" size="3" /></label>
<label for="excerpt-text-rows" style="line-height:35px;"><?php _e("Rows","tdomf"); ?> <input type="textfield" name="excerpt-text-rows" id="excerpt-text-rows" value="<?php echo htmlentities($options['text-rows'],ENT_QUOTES,get_bloginfo('charset')); ?>" size="3" /></label>
<br/>
<label for="excerpt-restrict-tags" style="line-height:35px;"><?php _e("Restrict Tags","tdomf"); ?> <input type="checkbox" name="excerpt-restrict-tags" id="excerpt-restrict-tags" <?php if($options['restrict-tags']) echo "checked"; ?> ></label>
<br/>
<label for="excerpt-allowable-tags" style="line-height:35px;"><?php _e("Allowable Tags","tdomf"); ?> <textarea title="true" cols="30" name="excerpt-allowable-tags" id="excerpt-allowable-tags" ><?php echo $options['allowable-tags']; ?></textarea></label>
</div>
        <?php 
}
tdomf_register_form_widget_control('excerpt',__('Excerpt','tdomf'), 'tdomf_widget_excerpt_control', 340, 520, $modes = array('new'));

///////////////////////////////////////
// Validate title and excerpt from form 
//
function tdomf_widget_excerpt_validate($args,$preview) {
  extract($args);
  $options = tdomf_widget_excerpt_get_options($tdomf_form_id);
  $output = "";
  if($options['text-required']
       && (empty($excerpt_excerpt) || trim($excerpt_excerpt) == "")) {
      if($output != "") { $output .= "<br/>"; }
      $output .= __("You must specify some post text.","tdomf");
  }
  if($options['word-limit'] > 0 || $options['char-limit'] > 0) {

      if($options['allowable-tags'] != "" && $options['restrict-tags']) {
         $excerpt_excerpt = strip_tags($excerpt_excerpt,$options['allowable-tags']);
      } 

      $excerpt_excerpt = apply_filters('the_excerpt', $excerpt_excerpt);
      
      if($options['char-limit'] > 0 && strlen($excerpt_prefiltered) > $options['char-limit']) {
        $output .= sprintf(__("You have exceeded the max character length by %d characters","tdomf"),(strlen($excerpt_excerpt) - $options['char-limit'])); 
      } else if($options['word-limit'] > 0) {
        // Remove all HTML tags as they do not count as "words"!
        $excerpt_excerpt = trim(strip_tags($excerpt_prefiltered));
        // Remove excess whitespace
        $excerpt_excerpt = preg_replace('/\s\s+/', ' ', $excerpt_prefiltered);
        // count the words!
        $word_count = count(explode(" ", $excerpt_excerpt));
        if($word_count > $options['word-limit']) {
          $output .= sprintf(__("You have exceeded the max word count by %d words","tdomf"),($word_count - $options['word-limit']));
        }
      }
  }
  // return output if any
  if($output != "") {
    return $before_widget.$output.$after_widget;
  } else {
    return NULL;
  }
}
tdomf_register_form_widget_validate('excerpt',__('Excerpt','tdomf'), 'tdomf_widget_excerpt_validate', $modes = array('new'));

?>
