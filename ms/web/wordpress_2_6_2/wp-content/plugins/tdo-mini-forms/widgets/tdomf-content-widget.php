<?php
/*
Name: "Content"
URI: http://thedeadone.net/software/tdo-mini-forms-wordpress-plugin/
Description: One of the default widgets, allows submitting and editing of post content and title
Version: 1
Author: Mark Cunningham
Author URI: http://thedeadone.net
*/

if(preg_match('#' . basename(__FILE__) . '#', $_SERVER['PHP_SELF'])) { die('TDOMF: You are not allowed to call this page directly.'); }
  
  /** 
   * Content Widget. This widget allows users to modify the content and title
   * 
   * @author Mark Cunningham <tdomf@thedeadone.net> 
   * @version 1.0 
   * @since 0.13.0
   * @access public 
   * @copyright Mark Cunningham
   * 
   */ 
  class TDOMF_WidgetContent extends TDOMF_Widget
  {
      /** 
       * Initilise and start widget
       * 
       * @access public
       */ 
      function TDOMF_WidgetContent() {
          $this->enableHack();
          $this->enablePreview();
          $this->enablePreviewHack();
          $this->enableValidate();
          $this->enableValidatePreview();
          $this->enablePost();
          $this->enableAdminEmail();
          $this->enableWidgetTitle();
          $this->enableControl(true,450,600);
          $this->setInternalName('content');
          $this->setDisplayName(__('Content','tdomf'));
          $this->setOptionKey('tdomf_content_widget');
          $this->setModes(array('new','edit'));
          $this->setFields(array('post_content' => __('Post Content','tdomf'),
                                 'post_title' => __('Post Title','tdomf')));
          $this->start();
      }
      
      /**
       * What to display in form
       * 
       * @access public
       * @return String
       */
      function form($args,$options) {
         if(!$options['title-enable'] && !$options['text-enable']) { return ""; }
         extract($args);
         $output = "";
         
         if(TDOMF_Widget::isEditForm($mode,$tdomf_form_id)) {
             $post = get_post($tdomf_post_id);
             if($post) {
                 if(!isset($args['content_title'])) {
                     $content_title = $post->post_title;
                 }
                 if(!isset($args['content_content'])) {
                     $content_content = $post->post_content;
                 }
             }
         }
         
         if($options['title-enable']) {
              if($options['title-required']) {
                  $output .= '<label for="content_title" class="required">'.__("Post Title (Required): ","tdomf")."<br/></label>\n";
              } else {
                  $output .= '<label for="content_title">'.__("Post Title: ","tdomf")."<br/></label>\n";
              }
              $output .= '<input type="text" name="content_title" id="content_title" size="'.$options['title-size'].'" value="'.htmlentities($content_title,ENT_QUOTES,get_bloginfo('charset')).'" />';
              if($options['text-enable']) {
                  $output .= "<br/><br/>";
              }
          }
          if($options['text-enable']) {
            if($options['text-required']) {
                $output .= '<label for="content_content" class="required">'.__("Post Text (Required): ","tdomf")."<br/>\n";      
            } else {
                $output .= '<label for="content_content">'.__("Post Text: ","tdomf")."<br/>\n";
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
                $qt_path = TDOMF_URLPATH."tdomf-quicktags.js.php?postfix=content_widget";
                if($options['allowable-tags'] != "" && $options['restrict-tags']) {
                    $qt_path = TDOMF_URLPATH."tdomf-quicktags.js.php?postfix=content_widget&allowed_tags=".urlencode($options['allowable-tags']);
                }
                $output .= "\n<script src='$qt_path' type='text/javascript'></script>\n";
                $output .= "\n<script type='text/javascript'>edToolbarcontent_widget();</script>\n";
            }
            $output .= '<textarea title="'.htmlentities(__('Post Content','tdomf'),ENT_QUOTES,get_bloginfo('charset')).'" rows="'.$options['text-rows'].'" cols="'.$options['text-cols'].'" name="content_content" id="content_content" >'.$content_content.'</textarea>';
            if($options['quicktags'] == true) {
                $output .= "\n<script type='text/javascript'>var edCanvascontent_widget = document.getElementById('content_content');</script>\n";
            }
          }
          return $output;
      }
      
      /**
       * Code for hacking form output
       * 
       * @access public
       * @return String
       */
      function formHack($args,$options) {
          if(!$options['title-enable'] && !$options['text-enable']) { return ""; }
          extract($args);          
         
          $output = "";
          
          if(TDOMF_Widget::isEditForm($mode,$tdomf_form_id)) {
              $output .= "\t\t".'<?php $post = get_post($post_id); if($post) {'."\n";
              if($options['title-enable']) {
                  $output .= "\t\t\t".'if(!isset($content_title)) { $content_title = $post->post_title; }'."\n";
              }
              if($options['text-enable']) {
                  $output .= "\t\t\t".'if(!isset($content_content)) { $content_content = $post->post_content; }'."\n";
              }
              $output .= "\t\t".'} ?>'."\n";
          }
          
          if($options['title-enable']) {
            if($options['title-required']) {
              $output .= "\t\t".'<label for="content_title" class="required">'.__("Post Title (Required): ","tdomf")."\n\t\t\t<br/>\n";
            } else {
              $output .= "\t\t".'<label for="content_title">'.__("Post Title: ","tdomf")."\n\t\t\t<br/>\n";
            }
            $output .= "\t\t</label>\n";            
            $output .= "\t\t\t".'<input type="text" name="content_title" id="content_title" size="'.$options['title-size'].'" value="';
            $output .= '<?php echo htmlentities($content_title,ENT_QUOTES,get_bloginfo(\'charset\')); ?>" />'."\n";
            if($options['text-enable']) {
              $output .= "\t\t<br/>\n\t\t<br/>\n";
            }
          }
          
          if($options['text-enable']) {
            if($options['text-required']) {
              $output .= "\t\t".'<label for="content_content" class="required">'.__("Post Text (Required): ","tdomf")."\n\t\t\t<br/>\n";      
            } else {
              $output .= "\t\t".'<label for="content_content">'.__("Post Text: ","tdomf")."\n\t\t\t<br/>\n";
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
              $qt_path = TDOMF_URLPATH."tdomf-quicktags.js.php?postfix=content_widget";
              if($options['allowable-tags'] != "" && $options['restrict-tags']) {
                $qt_path = TDOMF_URLPATH."tdomf-quicktags.js.php?postfix=content_widget&allowed_tags=".urlencode($options['allowable-tags']);
              }
              $output .= "\t\t<script src='$qt_path' type='text/javascript'></script>\n";
              $output .= "\t\t<script type='text/javascript'>edToolbarcontent_widget();</script>\n";
            }
            $output .= "\t\t".'<textarea title="'.htmlentities(__('Post Content','tdomf'),ENT_QUOTES,get_bloginfo('charset')).'" rows="'.$options['text-rows'].'" cols="'.$options['text-cols'].'" name="content_content" id="content_content" >';
            $output .= '<?php echo $content_content; ?></textarea>'."\n"; 
            if($options['quicktags'] == true) {
              $output .= "\t\t<script type='text/javascript'>var edCanvascontent_widget = document.getElementById('content_content');</script>";
            }
            
          }
          return $output;
      }
      
      /**
       * Overrides "getOptions" with defaults for this widget
       * 
       * @access public
       * @return String
       */
      function getOptions($form_id) {
          $defaults = array(   'title-enable' => true,
                               'title-required' => false,
                               'title-size' => 30,
                               'text-enable' => true,
                               'text-required' => true,
                               'text-cols' => 40,
                               'text-rows' => 10, 
                               'quicktags' => false,
                               'restrict-tags' => true,
                               'allowable-tags' => "<p><b><em><u><strong><a><img><table><tr><td><blockquote><ul><ol><li><br><sup>",
                               'char-limit' => 0,
                               'word-limit' => 0 );
          $options = TDOMF_Widget::getOptions($form_id); 
          $options = wp_parse_args($options, $defaults);
          return $options;
      }   
      
      /**
       * Generate preview of widget
       * 
       * @access public
       * @return String
       */      
      function preview($args,$options) {
          if(!$options['title-enable'] && !$options['text-enable']) { return ""; }
          extract($args);
          $output = "";
          if($options['title-enable']) {
            $output .= "<b>".__("Title: ","tdomf")."</b>";
            $output .= $content_title;
            $output .= "<br/>";
          }
          if($options['text-enable']) {
            $content_content = preg_replace('|\<!--tdomf_form.*-->|', '', $content_content);
            $content_content = preg_replace('|\[tdomf_form.*\]|', '', $content_content);
            $output .= "<b>".__("Text: ","tdomf")."</b><br/>";
            if(!tdomf_get_option_form(TDOMF_OPTION_MODERATION,$tdomf_form_id)){
             // if moderation is enabled, we don't do kses filtering, might as well
             // give full picture to user!
             $content_content = wp_filter_post_kses($content_content);
            }
            if($options['allowable-tags'] != "" && $options['restrict-tags']) {
              $output .= apply_filters('the_content', strip_tags($content_content,$options['allowable-tags']));
            } else {
              $output .= apply_filters('the_content', $content_content);
            }
          }
          return $output;
      }

      /**
       * Generate preview hack code of widget
       * 
       * @access public
       * @return String
       */      
      function previewHack($args,$options) {
          if(!$options['title-enable'] && !$options['text-enable']) { return ""; }
          extract($args);          
          $output = "";
          if($options['title-enable']) {
            $output .= "\t<b>".__("Title: ","tdomf")."</b>";
            $output .= "<?php echo \$content_title; ?>\n";
            $output .= "\t<br/>\n";
          }
          if($options['text-enable']) {
            // prep output
            $output .= "\t<?php ";
            $output .= '$content_content = preg_replace(\'|\<!--tdomf_form.*-->|\', \'\', $content_content);'."\n";
            $output .= "\t".'$content_content = preg_replace(\'|\\[tdomf_form.*\\]|\', \'\', $content_content);'."\n";
            if(!tdomf_get_option_form(TDOMF_OPTION_MODERATION,$tdomf_form_id)){
              $output .= "\t".'$content_content = wp_filter_post_kses($content_content);'."\n";
            }
             if($options['allowable-tags'] != "" && $options['restrict-tags']) {
              $output .= "\t".'$content_content = apply_filters(\'the_content\', strip_tags($content_content,\''.$options['allowable-tags'].'\'));';
            } else {
              $output .= "\t".'$content_content = apply_filters(\'the_content\', $content_content);';
            }
            $output .= " ?>\n";
            $output .= "\t<b>".__("Text: ","tdomf")."</b>\n\t<br/>\n";
            $output .= "\t<?php echo \$content_content; ?>";
          }
          return $output;
      }
      
      /**
       * Process form input for widget
       * 
       * @access public
       * @return Mixed
       */
      function post($args,$options) {
          extract($args);
  
          // if sumbitting a new post (as opposed to editing)
          // make sure to *append* to post_content. For editing, overwrite.
          //
          if(TDOMF_Widget::isSubmitForm($mode)) {
              
              // Grab existing data
              $post = wp_get_single_post($post_ID, ARRAY_A);
              if(!empty($post['post_content'])) {
                $post = add_magic_quotes($post);
              }

              // Append
              $post_content = $post['post_content'];
              if($options['allowable-tags'] != "" && $options['restrict-tags']) {
                tdomf_log_message("Content Widget: Stripping tags from post!");
                $post_content .= strip_tags($content_content,$options['allowable-tags']);
              } else {
                $post_content .= $content_content;
              }
          } else { // $mode startswith "edit-"
              // Overwrite 
              if($options['allowable-tags'] != "" && $options['restrict-tags']) {
                tdomf_log_message("Content Widget: Stripping tags from post!");
                $post_content = strip_tags($content_content,$options['allowable-tags']);
              } else {
                $post_content = $content_content;
              }
          }

          // Title

          if($options['title-enable'] && !isset($content_title)) {
            $content_title = tdomf_protect_input($post['post_title']);
          }
          
          // Update actual post

          $post = array (
              "ID"                      => $post_ID,
              "post_content"            => $post_content,
          );
          if($options['title-enable']) {
              $post["post_title"] = $content_title;
              $post["post_name"] = sanitize_title($content_title);
          }
        
          $post_ID = wp_update_post($post);
          return NULL;
      }
      
      /**
       * Configuration panel for widget
       * 
       * @access public
       */      
      function control($options,$form_id) {
          
          // Store settings for this widget
          //
          if ( $_POST[$this->internalName.'-submit'] ) {
                 $newoptions['title'] = strip_tags(stripslashes($_POST['content-title']));
                 $newoptions['title-enable'] = isset($_POST['content-title-enable']);
                 $newoptions['title-required'] = isset($_POST['content-title-required']);
                 $newoptions['title-size'] = intval($_POST['content-title-size']); 
                 $newoptions['text-enable'] = isset($_POST['content-text-enable']);
                 $newoptions['text-required'] = isset($_POST['content-text-required']);
                 $newoptions['text-cols'] = intval($_POST['content-text-cols']);
                 $newoptions['text-rows'] = intval($_POST['content-text-rows']); 
                 $newoptions['restrict-tags'] = isset($_POST['content-restrict-tags']);
                 $newoptions['allowable-tags'] = $_POST['content-allowable-tags'];
                 $newoptions['quicktags'] = $_POST['content-quicktags'];
                 $newoptions['char-limit'] = intval($_POST['content-char-limit']);
                 $newoptions['word-limit'] = intval($_POST['content-word-limit']);
                 $options = wp_parse_args($newoptions, $options);
                 $this->updateOptions($options,$form_id);
          }

          // Display control panel for this widget
          //
          extract($options);
          ?>
<div>          
          <?php $this->controlCommon($options); ?>
     
<h4><?php _e("Title of Post","tdomf"); ?></h4>
<label for="content-title-enable" style="line-height:35px;"><?php _e("Show","tdomf"); ?> <input type="checkbox" name="content-title-enable" id="content-title-enable" <?php if($options['title-enable']) echo "checked"; ?> ></label>
<label for="content-title-required" style="line-height:35px;"><?php _e("Required","tdomf"); ?> <input type="checkbox" name="content-title-required" id="content-title-required" <?php if($options['title-required']) echo "checked"; ?> ></label>
<label for="content-title-size" style="line-height:35px;"><?php _e("Size","tdomf"); ?> <input type="textfield" name="content-title-size" id="content-title-size" value="<?php echo htmlentities($options['title-size'],ENT_QUOTES,get_bloginfo('charset')); ?>" size="3" /></label>

<h4><?php _e("Content of Post","tdomf"); ?></h4>
<label for="content-text-enable" style="line-height:35px;"><?php _e("Show","tdomf"); ?> <input type="checkbox" name="content-text-enable" id="content-text-enable" <?php if($options['text-enable']) echo "checked"; ?> ></label>
<label for="content-text-required" style="line-height:35px;"><?php _e("Required","tdomf"); ?> <input type="checkbox" name="content-text-required" id="content-text-required" <?php if($options['text-required']) echo "checked"; ?> ></label>
<br/>
<label for="content-quicktags" style="line-height:35px;"><?php _e("Use Quicktags","tdomf"); ?> <input type="checkbox" name="content-quicktags" id="content-quicktags" <?php if($options['quicktags']) echo "checked"; ?> ></label>
<br/>
<label for="content-char-limit" style="line-height:35px;"><?php _e("Character Limit <i>(0 indicates no limit)</i>","tdomf"); ?> <input type="textfield" name="content-char-limit" id="content-char-limit" value="<?php echo htmlentities($options['char-limit'],ENT_QUOTES,get_bloginfo('charset')); ?>" size="3" /></label>
<br/>
<label for="content-word-limit" style="line-height:35px;"><?php _e("Word Limit <i>(0 indicates no limit)</i>","tdomf"); ?> <input type="textfield" name="content-word-limit" id="content-word-limit" value="<?php echo htmlentities($options['word-limit'],ENT_QUOTES,get_bloginfo('charset')); ?>" size="3" /></label>
<br/>
<label for="content-text-cols" style="line-height:35px;"><?php _e("Cols","tdomf"); ?> <input type="textfield" name="content-text-cols" id="content-text-cols" value="<?php echo htmlentities($options['text-cols'],ENT_QUOTES,get_bloginfo('charset')); ?>" size="3" /></label>
<label for="content-text-rows" style="line-height:35px;"><?php _e("Rows","tdomf"); ?> <input type="textfield" name="content-text-rows" id="content-text-rows" value="<?php echo htmlentities($options['text-rows'],ENT_QUOTES,get_bloginfo('charset')); ?>" size="3" /></label>
<br/>
<label for="content-restrict-tags" style="line-height:35px;"><?php _e("Restrict Tags","tdomf"); ?> <input type="checkbox" name="content-restrict-tags" id="content-restrict-tags" <?php if($options['restrict-tags']) echo "checked"; ?> ></label>
<br/>
<label for="content-allowable-tags" style="line-height:35px;"><?php _e("Allowable Tags","tdomf"); ?> <textarea title="true" cols="30" name="content-allowable-tags" id="content-allowable-tags" ><?php echo $options['allowable-tags']; ?></textarea></label>
</div>
        <?php
      }
      
      /**
       * Validate widget input
       * 
       * @access public
       * @return Mixed
       */
      function validate($args,$options,$preview) {
          if(!$options['title-enable'] && !$options['text-enable']) { return ""; }  
          extract($args);
          $output = "";

          if($options['title-enable'] && $options['title-required']
               && (empty($content_title) || trim($content_title) == "")) {
              if($output != "") { $output .= "<br/>"; }
              $output .= __("You must specify a post title.","tdomf");
          }

          if($options['text-enable'] && $options['text-required']
               && (empty($content_content) || trim($content_content) == "")) {
              if($output != "") { $output .= "<br/>"; }
              $output .= __("You must specify some post text.","tdomf");
          }
          
          if(TDOMF_Widget::isEditForm($mode,$tdomf_form_id)) {

               // when it goes to validation, the tdomf_post_id will be the 
               // real post id

              $post = &get_post( $tdomf_post_id );
              
              // for post content, this is probably not the most exact way to do it
              //
              if($options['text-enable'] && $options['text-required']) {
                  if(trim($post->post_content) == trim($content_content)) {
                      if($output != "") { $output .= "<br/>"; }
                      $output .= __("You must modify the post text.","tdomf");
                  }
              }
              
              if($options['title-enable'] && $options['title-required']) {
                  if(trim($post->post_title) == trim($content_title)) {
                      if($output != "") { $output .= "<br/>"; }
                      $output .= __("You must modify the post title.","tdomf");
                  }
              }
          }
                    
          if($options['word-limit'] > 0 || $options['char-limit'] > 0) {
              
              // prefitler the content so it's as close to the end result as possible
              //
              $content_prefiltered = preg_replace('|\[tdomf_form.*\]|', '', $content_content);
              $content_prefiltered = preg_replace('|<!--tdomf_form.*-->|', '', $content_prefiltered);
              if(!tdomf_get_option_form(TDOMF_OPTION_MODERATION,$tdomf_form_id)){
                 // if moderation is enabled, we don't do kses filtering, might as well
                 // give full picture to user!
                 $content_prefiltered = wp_filter_post_kses($content_prefiltered);
              }
              if($options['allowable-tags'] != "" && $options['restrict-tags']) {
                 $content_prefiltered = strip_tags($content_prefiltered,$options['allowable-tags']);
              } 
        
              // don't apply content filters!
              //$content_prefiltered = apply_filters('the_content', $content_prefiltered);
              
              if($options['char-limit'] > 0 && strlen($content_prefiltered) > $options['char-limit']) {
                $output .= sprintf(__("You have exceeded the max character length by %d characters","tdomf"),(strlen($content_prefiltered) - $options['char-limit'])); 
              } else if($options['word-limit'] > 0) {
                // Remove all HTML tags as they do not count as "words"!
                $content_prefiltered = trim(strip_tags($content_prefiltered));
                // Remove excess whitespace
                $content_prefiltered = preg_replace('/\s\s+/', ' ', $content_prefiltered);
                // count the words!
                $word_count = count(explode(" ", $content_prefiltered));
                if($word_count > $options['word-limit']) {
                  $output .= sprintf(__("You have exceeded the max word count by %d words","tdomf"),($word_count - $options['word-limit']));
                }
              }
          }
          // return output if any
          if($output != "") {
              return $output;
          } else {
              return NULL;
          }
      }
  }
  
    
  // Create and start the widget
  //
  global $tdomf_widget_content;
  $tdomf_widget_content = new TDOMF_WidgetContent();

?>
