<?php
if(preg_match('#' . basename(__FILE__) . '#', $_SERVER['PHP_SELF'])) { die('TDOMF: You are not allowed to call this page directly.'); }

/** 
* Super class for widget classes. Supports validation, preview, hacking, admin
* email, admin error and multiple instances. Common features can be added to
* all widgets via this class.
* 
* @author Mark Cunningham <tdomf@thedeadone.net> 
* @version 2.0 
* @since 0.13.0
* @access public 
* @copyright Mark Cunningham
* 
*/ 
class TDOMF_Widget {
    
    /** 
     * Determines if widget can be hacked on the form   
     * 
     * @var boolean 
     * @access public 
     * @see enableHack() 
     */ 
    var $hack = false;
    
    /** 
     * Enables or disables widget hacking on the form
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enableHack($hack = true) {
        if($this->started && $this->hack != $hack) {
           if($hack && !$this->multipleInstances) {
               tdomf_register_form_widget_hack($this->internalName,$this->displayName, array($this, '_form_hack'), $this->modes);
           } # remove not supported
        }
        $this->hack = $hack;
        return true;
    }
    
    /** 
     * Determines if widget has a preview   
     * 
     * @var boolean 
     * @access public 
     * @see enablePreview() 
     */
    var $preview = false;

    /** 
     * Enables or disables widget preview
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enablePreview($preview = true) {
        if($this->started && $this->preview != $preview) {
           if($preview && !$this->multipleInstances) {
               tdomf_register_form_widget_preview($this->internalName,$this->displayName, array($this, '_preview'), $this->modes);
           } # remove not supported
        }        
        $this->preview = $preview;
        return true;
    }

    /** 
     * Determines if widget preview can be hacked
     * 
     * @var boolean 
     * @access public 
     * @see enablePreviewHack() 
     */
    var $previewHack = false;

    /** 
     * Enables or disables widget preview hack
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enablePreviewHack($previewHack = true) {
        if($this->started && $this->previewHack != $previewHack) {
           if($previewHack && !$this->multipleInstances) {
               tdomf_register_form_widget_preview_hack($this->internalName,$this->displayName, array($this, '_previewHack'), $this->modes);
           } # remove not supported
        }
        $this->previewHack = $previewHack;
        return true;
    }
    
    /** 
     * Determines if widget input will be validated
     * 
     * @var boolean 
     * @access public 
     * @see enableValidate() 
     */
    var $validate = false;

    /** 
     * Enables or disables widget validation
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enableValidate($validate = true) {
        if($this->started && $this->validate != $validate) {
           if($validate && !$this->multipleInstances) {
               tdomf_register_form_widget_validate($this->internalName,$this->displayName, array($this, '_validate'), $this->modes);
           } # remove not supported
        }
        $this->validate = $validate;
        return true;
    }

    /** 
     * Determines if widget input should be validated on preview
     * 
     * @var boolean 
     * @access public 
     * @see enableValidatePreview() 
     */
    var $validatePreview = true;

    /** 
     * Enables or disables widget validation
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enableValidatePreview($validatePreview = true) {
        $this->validatePreview = $validatePreview;
        return true;
    }    
    
    /** 
     * Determines if widget modifies actual post
     * 
     * @var boolean 
     * @access public 
     * @see enablePost() 
     */
    var $post = false;

    /** 
     * Enables or disables widget post modification
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enablePost($post = true) {
        if($this->started && $this->post != $post) {
           if($post && !$this->multipleInstances) {
               tdomf_register_form_widget_preview_hack($this->internalName,$this->displayName, array($this, '_post'), $this->modes);
           } # remove not supported
        }
        $this->post = $post;
        return true;
    }
    
    /** 
     * Determines if widget sends admin email
     * 
     * @var boolean 
     * @access public 
     * @see enableAdminEmail() 
     */
    var $adminEmail = false;

    /** 
     * Enables or disables widget sending admin email
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enableAdminEmail($adminEmail = true) {
        if($this->started && $this->adminEmail != $adminEmail) {
           if($adminEmail && !$this->multipleInstances) {
               tdomf_register_form_widget_adminemail($this->internalName,$this->displayName, array($this, '_adminEmail'), $this->modes);
           } # remove not supported
        }        
        $this->adminEmail = $adminEmail;
        return true;
    }

    /** 
     * Enables support for displaying an error message
     * 
     * @var boolean 
     * @access public 
     * @see enableAdminError() 
     */
    var $adminError = false;

    /** 
     * Enables or disables support for error message
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enableAdminError($adminError = true) {
        if($this->started && $this->adminError != $adminError) {
           if($adminError) {
               tdomf_register_form_widget_admin_error($this->internalName,$this->displayName, array($this, '_adminError'), $this->modes);
           } # remove not supported
        }              
        $this->adminError = $adminError;
        return true;
    }
    
    /** 
     * Determines if widget can be configured
     * 
     * @var boolean 
     * @access public 
     * @see enableControl() 
     */    
    var $control = true;
    
    /** 
     * Width of Control Panel
     * 
     * @var integer 
     * @access public 
     * @see enableControl() 
     */        
    var $controlWidth = 100;
    
    /** 
     * Height of Control Panel
     * 
     * @var integer 
     * @access public 
     * @see enableControl() 
     */    
    var $controlHeight = 100;

    /** 
     * Enables or disables widget control panel
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enableControl($control = true, $width = 100, $height = 100) {
        if($width <= 0 || $height <= 0) {
            return false;
        }
        
        if($this->started && $this->control != $control) {
           if($control && !$this->multipleInstances) {
               tdomf_register_form_widget_adminemail($this->internalName,$this->displayName, array($this, '_adminEmail'), $width, $height, $this->modes);
           } # remove not supported
        }              
        $this->control = $control;
        $this->controlWidth = $width;
        $this->controlHeight = $height;
        return true;
    }
    
    /** 
     * Multiple Instances Support
     * 
     * @var integer 
     * @access public 
     * @see enableMultipleInstances(() 
     */    
    var $multipleInstances = false;
    
    /** 
     * Key of Multiple Instances count option
     * 
     * @var integer 
     * @access public 
     * @see enableMultipleInstances(() 
     */    
    var $multipleInstancesOptionKey = false;
    
    /** 
     * Display name of multiple instances (must include a %d)
     * 
     * @var integer 
     * @access public 
     * @see enableMultipleInstances(() 
     */    
    var $multipleInstancesDisplayName = false;

    /** 
     * For backwards compatibility, does the first instance have an index?
     * 
     * @var integer 
     * @access public 
     * @see enableMultipleInstances(() 
     */   
    var $multipleInstancesNoIndexOnFirst = false;
    
    /** 
     * Sets modes widget supports. Must be done before widget is started.
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enableMultipleInstances($multipleInstances = true, $displayName = false, $optionKey = false, $noIndexOnFirst = false) {    
        $this->multipleInstances = $multipleInstances;
        if($displayName) {
            $this->multipleInstancesDisplayName = $displayName;
        } else {
            $this->multipleInstancesDisplayName = $this->displayName;
        }        
        if($optionKey) {
            $this->multipleInstancesOptionKey = $optionKey;
        } else {
            $this->multipleInstancesOptionKey = 'tdomf_'.$this->internalName.'_widget';
        }
        $this->multipleInstancesNoIndexOnFirst = $noIndexOnFirst;
        return true;
    }   
    
    /** 
     * Displays the Multiple Instances Form on the Widget Page
     * 
     * @access private 
     */     
    function _multipleInstancesForm($form_id,$mode) {
        $count = tdomf_get_option_widget($this->multipleInstancesOptionKey,$form_id);
        if($count <= 0){ $count = 1; }
        $max = tdomf_get_option_form(TDOMF_OPTION_WIDGET_INSTANCES,$form_id);
        if($max == false){ $max = 9; }
        if($count > ($max+1)){ $count = ($max+1); }
  
        if($max > 1) {
  ?>
  <div class="wrap">
    <form method="post">
      <h2><?php echo $this->displayName ?></h2>
      <p style="line-height: 30px;"><?php printf(__("How many %s widgets would you like?","tdomf"),$this->displayName); ?>
      <select id="tdomf-widget-<?php echo $this->internalName; ?>-number" name="tdomf-widget-<?php echo $this->internalName; ?>-number" value="<?php echo $count; ?>">
      <?php for($i = 1; $i < ($max+1); $i++) { ?>
        <option value="<?php echo $i; ?>" <?php if($i == $count) { ?> selected="selected" <?php } ?>><?php echo $i; ?></option>
      <?php } ?>
      </select>
      <span class="submit">
        <input type="submit" value="<?php _e("Save","tdomf"); ?>" id="tdomf-widget-<?php echo $this->internalName; ?>-number-submit" name="tdomf-widget-<?php echo $this->internalName; ?>-number-submit" />
      </span>
      </p>
    </form>
  </div><?php 
        }
    }
    
    /** 
     * Handles the multiple instances input from the form on the Widget Page
     * 
     * @access private 
     */      
    function _multipleInstancesHandler($form_id,$mode) {
        if ( isset($_POST['tdomf-widget-'.$this->internalName.'-number-submit']) ) {
        $count = $_POST['tdomf-widget-'.$this->internalName.'-number'];
        if($count > 0){ tdomf_set_option_widget($this->multipleInstancesOptionKey,$count,$form_id); }
      }
    }
    
    /** 
     * Does the initilisation of multiple instance widgets
     * 
     * @access private 
     */  
    function _multipleInstancesInit($form_id,$mode) {
        $count = tdomf_get_option_widget($this->multipleInstancesOptionKey,$form_id);
        if($count <= 0){ $count = 1; } 
     
        $max = tdomf_get_option_form(TDOMF_OPTION_WIDGET_INSTANCES,$form_id);
        if($max <= 1){ $count = 1; }
        else if($count > ($max+1)){ $count = $max + 1; }
     
        $start = 1;
        if($this->multipleInstancesNoIndexOnFirst) {

           // some of the original widgets were adapted later to multiple
           // instances but had to preserve the original options. I did this
           // by not including an index on the first element... now have to 
           // support it here for backwards compatibility
            
           $start = 2;
            
           tdomf_register_form_widget($this->internalName,sprintf($this->multipleInstancesDisplayName,1), array($this, '_form'), $this->modes);
              
           if($this->hack)
               tdomf_register_form_widget_hack($this->internalName,sprintf($this->multipleInstancesDisplayName,1), array($this, '_formHack'), $this->modes);
           
           if($this->control)
               tdomf_register_form_widget_control($this->internalName,sprintf($this->multipleInstancesDisplayName,1), array($this, '_control'), $this->controlWidth, $this->controlHeight, $this->modes);
           
           if($this->preview) {
               tdomf_register_form_widget_preview($this->internalName,sprintf($this->multipleInstancesDisplayName,1), array($this, '_preview'), $this->modes);
           }
           
           if($this->previewHack) {
               tdomf_register_form_widget_preview_hack($this->internalName,sprintf($this->multipleInstancesDisplayName,1), array($this, '_previewHack'), $this->modes);
           }
           
           if($this->validate)
               tdomf_register_form_widget_validate($this->internalName,sprintf($this->multipleInstancesDisplayName,1), array($this, '_validate'), $this->modes);
           
           if($this->post)
               tdomf_register_form_widget_post($this->internalName,sprintf($this->multipleInstancesDisplayName,1), array($this, '_post'), $this->modes);
           
           if($this->adminEmail)
               tdomf_register_form_widget_adminemail($this->internalName,sprintf($this->multipleInstancesDisplayName,1), array($this, '_adminEmail'), $this->modes);
           
           if($this->adminError)
               tdomf_register_form_widget_admin_error($this->internalName,sprintf($this->multipleInstancesDisplayName,1), array($this, '_adminError'), $this->modes);
            
        }
        
        for($i = $start; $i <= $count; $i++) {          
           tdomf_register_form_widget($this->internalName.$this->internalNameSeperator.$i,sprintf($this->multipleInstancesDisplayName,$i), array($this, '_form'), $this->modes, $i);
               
           if($this->hack)
               tdomf_register_form_widget_hack($this->internalName.$this->internalNameSeperator.$i,sprintf($this->multipleInstancesDisplayName,$i), array($this, '_formHack'), $this->modes, $i);
           
           if($this->control)
               tdomf_register_form_widget_control($this->internalName.$this->internalNameSeperator.$i,sprintf($this->multipleInstancesDisplayName,$i), array($this, '_control'), $this->controlWidth, $this->controlHeight, $this->modes, $i);
           
           if($this->preview) {
               tdomf_register_form_widget_preview($this->internalName.$this->internalNameSeperator.$i,sprintf($this->multipleInstancesDisplayName,$i), array($this, '_preview'), $this->modes, $i);
           }
           
           if($this->previewHack) {
               tdomf_register_form_widget_preview_hack($this->internalName.$this->internalNameSeperator.$i,sprintf($this->multipleInstancesDisplayName,$i), array($this, '_previewHack'), $this->modes, $i);
           }
           
           if($this->validate)
               tdomf_register_form_widget_validate($this->internalName.$this->internalNameSeperator.$i,sprintf($this->multipleInstancesDisplayName,$i), array($this, '_validate'), $this->modes, $i);
           
           if($this->post)
               tdomf_register_form_widget_post($this->internalName.$this->internalNameSeperator.$i,sprintf($this->multipleInstancesDisplayName,$i), array($this, '_post'), $this->modes, $i);
           
           if($this->adminEmail)
               tdomf_register_form_widget_adminemail($this->internalName.$this->internalNameSeperator.$i,sprintf($this->multipleInstancesDisplayName,$i), array($this, '_adminEmail'), $this->modes, $i);
           
           if($this->adminError)
               tdomf_register_form_widget_admin_error($this->internalName.$this->internalNameSeperator.$i,sprintf($this->multipleInstancesDisplayName,$i), array($this, '_adminError'), $this->modes, $i);
        }
    }
    
    /** 
     * Modes the widget supports
     * 
     * @var Array 
     * @access public 
     * @see setModes() 
     */    
    var $modes = array();
    
    /** 
     * Sets modes widget supports. Must be done before widget is started
     * 
     * @return Boolean 
     * @access public 
     */ 
    function setModes($modes = array()) {
        $retVal = false;
        if(!$this->started && is_array($modes)) {
            $retVal = true;
            $this->modes = $modes;
        }
        return $retVal;
    }   
    
    /** 
     * Widget supports title
     * 
     * @var boolean 
     * @access public 
     * @see enableWidgetTitle() 
     */
    var $widgetTitle = false;

    /** 
     * For backwards compatibility, you can set the previous title key
     * 
     * @var boolean 
     * @access public 
     * @see enableWidgetTitle() 
     */
    var $widgetTitleKey = 'tdomf-title';
        
    /** 
     * Enables support for title in widget display
     * 
     * @return Boolean 
     * @access public 
     */ 
    function enableWidgetTitle($widgetTitle = true,$widgetTitleKey = 'tdomf-title') {
        $this->widgetTitle = $widgetTitle;
        $this->widgetTitleKey = $widgetTitleKey;
        return true;
    }

    /** 
     * Internal name of widget
     * 
     * @var boolean 
     * @access public 
     * @see setInternalName() 
     */    
    var $internalName = false;

    /** 
     * Seperator for internal name for use in multiple instances mode
     * 
     * @var boolean 
     * @access public 
     * @see setInternalName() 
     */
    var $internalNameSeperator = '';
    
    /** 
     * Set internal name of widget. Must be done before widget is started
     * 
     * @return Boolean 
     * @access public 
     */ 
    function setInternalName($name,$seperator = '') {
        $retVal = false;
        if(!$this->started) {
            $retVal = true;
            $this->internalName = $name;
            $this->internalNameSeperator = $seperator;
            if(!$this->optionKey) {
                $this->optionKey = 'tdomf_'.$this->internalName.'_widget';
            }
        }
        return $retVal;
    }    
    
    /** 
     * Name of widget displayed to user. 
     * 
     * @var boolean 
     * @access public 
     * @see setDisplayName() 
     */        
    var $displayName = false;
    
    /** 
     * Set display name of widget. Must be done before widget is started.
     * 
     * @return Boolean 
     * @access public 
     */ 
    function setDisplayName($name) {
        $retVal = false;
        if(!$this->started) {
            $retVal = true;
            $this->displayName = $name;
            if($this->multipleInstances && !$this->multipleInstancesDisplayName) {
                $this->multipleInstancesDisplayName = $name;
            }
        }
        return $retVal;
    }   
    
    /** 
     * Name of options stored in database. Normally genreated from internal
     * name but can be overwritten
     * 
     * @var boolean 
     * @access public 
     * @see setOptionKey() 
     */    
    var $optionKey = false;

    /** 
     * Seperator for option key for use in multiple instances mode
     * 
     * @var boolean 
     * @access public 
     * @see setInternalName() 
     */
    var $optionKeySeperator = '';    
    
    /** 
     * Set option key string.. Must be done before widget is started.
     * 
     * @return Boolean 
     * @access public 
     */ 
    function setOptionKey($key,$seperator = '') {
        $retVal = false;
        if(!$this->started) {
            $retVal = true;
            $this->optionKey = $key;
            $this->optionKeySeperator = $seperator;
        }
        return $retVal;
    }   
    
    /** 
     * List of fields that are modified by this widget 
     * 
     * @var mixed
     * @access public 
     * @see setFields() 
     */    
    var $fields = false;
    
    /** 
     * Set list of fields that are modified by this widget
     * 
     * @return Boolean 
     * @access public 
     */     
    function setFields($fields = false) {
        $retVal = false;
        if(is_array($fields) || $fields == false) {
            $this->fields = $fields;
            $retVal = true;
        }
        return $retVal;
    }
    
    /** 
     * List of custom fields that are modified by this widget 
     * 
     * @var mixed
     * @access public 
     * @see setFields() 
     */    
    var $customFields = false;
    
    /** 
     * Set list of custom fields that are modified by this widget
     * 
     * @return Boolean 
     * @access public 
     */     
    function setCustomFields($customFields = false) {
        $retVal = false;
        if(is_array($customFields) || $customFields == false) {
            $this->customFields = $customFields;
            $retVal = true;
        }
        return $retVal;
    }
    
    /** 
     * Flags if the widget has been started yet
     * 
     * @return Boolean 
     * @access private 
     */     
    var $started = false;
    
    function TDOMF_Widget() {
        /* do nothing */
    }
    
    /**
     * Start widget
     *
     * @access public
     */
    function start() {
       $retVal = false;
       if(!$this->started || !$this->internalName || !$this->displayName)
       {
           $retVal = true;
           
           if($this->multipleInstances) {
               add_action('tdomf_generate_form_start',array($this,'_multipleInstancesInit'),10,2);
               add_action('tdomf_create_post_start',array($this,'_multipleInstancesInit'),10,2);
               add_action('tdomf_control_form_start',array($this,'_multipleInstancesInit'),10,2);
               add_action('tdomf_control_form_start',array($this,'_multipleInstancesHandler'),10,2);
               add_action('tdomf_widget_page_bottom',array($this,'_multipleInstancesForm'),10,2);
               
               // for multiple instances, init is handled in _multipleInstancesInit function
               
           } else { 
               tdomf_register_form_widget($this->internalName, $this->displayName, array($this, '_form'), $this->modes);
               
               if($this->hack)
                   tdomf_register_form_widget_hack($this->internalName,$this->displayName, array($this, '_formHack'), $this->modes);
               
               if($this->control)
                   tdomf_register_form_widget_control($this->internalName, $this->displayName, array($this, '_control'), $this->controlWidth, $this->controlHeight, $this->modes);
               
               if($this->preview) {
                   tdomf_register_form_widget_preview($this->internalName, $this->displayName, array($this, '_preview'), $this->modes);
               }
               
               if($this->previewHack) {
                   tdomf_register_form_widget_preview_hack($this->internalName, $this->displayName, array($this, '_previewHack'), $this->modes);
               }
               
               if($this->validate)
                   tdomf_register_form_widget_validate($this->internalName, $this->displayName, array($this, '_validate'), $this->modes);
               
               if($this->post)
                   tdomf_register_form_widget_post($this->internalName, $this->displayName, array($this, '_post'), $this->modes);
               
               if($this->adminEmail)
                   tdomf_register_form_widget_adminemail($this->internalName, $this->displayName, array($this, '_adminEmail'), $this->modes);
               
               if($this->adminError)
                   tdomf_register_form_widget_admin_error($this->internalName, $this->displayName, array($this, '_adminError'), $this->modes);
           }
       }
        return $retVal;
    }
    
    /** 
     * Wraps form output of the widget
     * 
     * @return String 
     * @access private 
     */ 
    function _form($args,$params=array()) {
        extract($args);
        $postfix = $this->getPostfixFromParams($params);
        $options = $this->getOptions($tdomf_form_id,$postfix);

        $output = $before_widget;
        if($this->widgetTitle && $options[$this->widgetTitleKey] != "") {
            $output .= $before_title.$options[$this->widgetTitleKey].$after_title;
        }
        $output .= $this->form($args,$options,$postfix);
        $output .= $after_widget;
        return $output;
    }
    
    /** 
     * Individual widgets should override this function
     * 
     * @return String 
     * @access public
     */    
    function form($args,$options,$postfix='') {
        # do nothing
        return "";
    }

    /** 
     * Wraps post of the widget
     * 
     * @return Mixed 
     * @access private 
     */     
    function _post($args,$params=array()) {
        extract($args);
        $postfix = $this->getPostfixFromParams($params);
        $options = $this->getOptions($tdomf_form_id,$postfix);
        $this->updateFields($args);
        return $this->post($args,$options,$postfix);
    }
    
    /** 
     * Individual widgets that implement post should override this function
     * 
     * @return Mixed 
     * @access public
     */        
    function post($args,$options,$postfix='') {
        # do nothing
        return NULL;
    }   
    
    /** 
     * Wraps preview output of the widget
     * 
     * @return String
     * @access private 
     */         
    function _preview($args,$params=array()) {
        extract($args);
        $postfix = $this->getPostfixFromParams($params);
        $options =  $this->getOptions($tdomf_form_id,$postfix);
    
        $output = "";    
        $widget_output = $this->preview($args,$options,$postfix);
        if($widget_output && !empty($widget_output)) {
          $output  = $before_widget;
          if($this->widgetTitle && $options[$this->widgetTitleKey] != '') {
              $output .= $before_title.$options[$this->widgetTitleKey].$after_title;
          }
          $output .= $widget_output;  
          $output .= $after_widget;
        }
        return $output;
    }
    
    /** 
     * Individual widgets that implement preview should override this function
     * 
     * @return Mixed 
     * @access public
     */        
    function preview($args,$options,$postfix='') {
        # do nothing
        return false;
    }
    
    /** 
     * Wraps validation of the widget input
     * 
     * @return Mixed
     * @access private 
     */      
    function _validate($args,$preview,$params=array()) {
        extract($args);
        $postfix = $this->getPostfixFromParams($params);
        $options = $this->getOptions($tdomf_form_id,$postfix);
        
        if(!$preview || $this->validatePreview) {
            $output = $this->validate($args,$options,$preview,$postfix);
            if($output != NULL && !empty($output)) {
                return $before_widget.$output.$after_widget;
            }
        }
        
        return NULL;
    }
    
    /** 
     * Individual widgets that implement validation should override this function
     * 
     * @return Mixed 
     * @access public
     */            
    function validate($args,$options,$preview,$postfix='') {
        # do nothing
        return NULL;
    }
    
    /** 
     * Wraps admin email of the widget input
     * 
     * @return String
     * @access private 
     */        
    function _adminEmail($args,$params=array()){
        extract($args);
        $postfix = $this->getPostfixFromParams($params);
        $options = $this->getOptions($tdomf_form_id,$postfix);
        $output = "";    
        $widget_output = $this->adminEmail($args,$options,$post_ID,$postfix);
        if($widget_output && !empty($widget_output)) {
          $output  = $before_widget;
          if($this->widgetTitle && $options[$this->widgetTitleKey] != '') {
              $output .= $before_title.$options[$this->widgetTitleKey].$after_title;
          }
          $output .= $widget_output;  
          $output .= $after_widget;
        }
        return $output;
    }
    
    /** 
     * Individual widgets that implement admin should override this function
     * 
     * @return String
     * @access public
     */      
    function adminEmail($args,$options,$post_ID,$postfix='') {
        # do nothing
        return '';
    }
    
    /** 
     * Wraps configuration panel of widget
     * 
     * @access private 
     */       
    function _control($form_id,$params=array()) {
        
        $postfixOptionKey = $this->getPostfixFromParams($params);
        
        $postfixInternalName = '';
        if($this->multipleInstances) {
            $postfixInternalName = 0;
            if(is_array($params) && count($params) >= 1){
                $postfixInternalName = $params[0];
            }
            if($this->multipleInstancesNoIndexOnFirst && $postfixInternalName <= 1) {
                // ignore postfix for first element
                $postfixInternalName = '';
            } else {
                $postfixInternalName = $this->internalNameSeperator.$postfixInternalName;
            }
        }
        
        $options = $this->getOptions($form_id,$postfixOptionKey);
                
        if ( $_POST[$this->internalName.$postfixOptionKey.'-submit'] ) {
            if($this->widgetTitle) {
                $newoptions[$this->widgetTitleKey] = $_POST[$this->internalName.$postfixOptionKey.'-tdomf-title'];
            }
            if($this->hack) {
                $newoptions['tdomf-hack'] = isset($_POST[$this->internalName.$postfixOptionKey.'-tdomf-hack']);
            }
            if($this->previewHack) {
                $newoptions['tdomf-preview-hack'] = isset($_POST[$this->internalName.$postfixOptionKey.'-tdomf-preview-hack']);
            }
            if ( $options != $newoptions ) {
                $this->updateOptions($options,$form_id,$postfixOptionKey);
                $options = $newoptions;
            }
        }
        $this->control($options,$form_id,$postfixOptionKey,$postfixInternalName);
    }
    
    /** 
     * Individual widgets that implement a control panel should override this function
     * 
     * @access public
     */     
    function control($options,$form_id,$postfixOptionKey='',$postfixInternalName='') {
        # do nothing
    }

    /** 
     * Displays common configuration options
     * 
     * @access public
     */    
    function controlCommon($options,$postfix='') {

        if($this->widgetTitle) { ?>
<label for="<?php echo $this->internalName.$postfix; ?>-tdomf-title" style="line-height:35px;"><?php _e("Widget Title: ","tdomf"); ?></label>
<input type="textfield" id="<?php echo $this->internalName.$postfix; ?>-title" name="<?php echo $this->internalName.$postfix; ?>-tdomf-title" value="<?php echo htmlentities($options[$this->widgetTitleKey],ENT_QUOTES,get_bloginfo('charset')); ?>" /></label>
<br/>
        <?php  }
        if($this->hack) { ?>
<input type="checkbox" name="<?php echo $this->internalName.$postfix; ?>-tdomf-hack" id="<?php echo $this->internalName.$postfix; ?>-tdomf-hack" <?php if($options['tdomf-hack']) echo "checked"; ?> >
<label for="<?php echo $this->internalName.$postfix; ?>-tdomf-hack" style="line-height:35px;"><?php _e("This widget can be modified in the form hacker","tdomf"); ?></label>
<br/>
        <?php }
       if($this->previewHack && $this->preview) { ?>
<input type="checkbox" name="<?php echo $this->internalName.$postfix; ?>-preview-hack" id="<?php echo $this->internalName.$postfix; ?>-tdomf-preview-hack" <?php if($options['tdomf-preview-hack']) echo "checked"; ?> >
<label for="<?php echo $this->internalName.$postfix; ?>-preview-hack" style="line-height:35px;"><?php _e("This widget's preview can be modified in the form hacker","tdomf"); ?></label>
<br/>
        <?php }
    }
    
    /** 
     * Wraps hacked form output of the widget
     * 
     * @return String 
     * @access private 
     */ 
    function _formHack($args,$params=array()) {
        extract($args);
        $postfix = $this->getPostfixFromParams($params);
        $options = $this->getOptions($tdomf_form_id,$postfix);
        if($options['tdomf-hack']) {
            $output = $before_widget;
            if($this->widgetTitle && $options[$this->widgetTitleKey] != "") {
                $output .= $before_title.$options[$this->widgetTitleKey].$after_title;
            }
            $output .= $this->formHack($args,$options,$postfix);
            $output .= $after_widget;
            return $output;
        }
        return TDOMF_MACRO_WIDGET_START.$this->internalName.TDOMF_MACRO_END;
    }
    
    /** 
     * Individual widgets that implement hacked form should override this function
     * 
     * @access public
     * @return String 
     */      
     function formHack($args,$options,$postfix='') {
         return TDOMF_MACRO_WIDGET_START.$this->internalName.TDOMF_MACRO_END."\n";
     }
    
    /** 
     * Wraps hacked form preview output of the widget
     * 
     * @return String 
     * @access private 
     */ 
    function _previewHack($args,$params=array()) {
        extract($args);
        $postfix = $this->getPostfixFromParams($params);
        $options = $this->getOptions($tdomf_form_id,$postfix);
        if($options['tdomf-hack']) {
            $output = $before_widget;
            if($this->widgetTitle && $options[$this->widgetTitleKey] != "") {
                $output .= $before_title.$options[$this->widgetTitleKey].$after_title;
            }
            $output .= $this->previewHack($args,$options,$postfix);
            $output .= $after_widget;
            return $output;
        }
        return TDOMF_MACRO_WIDGET_START.$this->internalName.TDOMF_MACRO_END;        
    }
    
    /** 
     * Individual widgets that implement hacked preview should override this function
     * 
     * @access public
     * @return String 
     */      
     function previewHack($args,$options,$postfix) {
         return TDOMF_MACRO_WIDGET_START.$this->internalName.TDOMF_MACRO_END;
     }  
     
    /** 
     * Wraps error handler of the widget
     * 
     * @return String 
     * @access private 
     */ 
     function _adminError($form_id,$params=array()) {
        $postfix = $this->getPostfixFromParams($params);
        $options = $this->getOptions($form_id,$postfix);
        return $this->adminError($options,$form_id,$postfix);
     }
     
    /** 
     * Individual widgets that implement an error handler should override this function
     * 
     * @access public
     * @return Mixed 
     */       
     function adminError($options,$form_id,$postfix='') {
         return "";
     }

    /** 
     * Returns the options for this widget
     * 
     * @return Array
     * @access public
     */       
    function getOptions($form_id,$postfix='') {
        $defaults = array( $this->widgetTitleKey => $this->displayName,
                          'tdomf-hack'           => $this->hack,
                          'tdomf-preview-hack'   => $this->previewHack );
        $options = tdomf_get_option_widget($this->optionKey.$postfix,$form_id);
        # A bug in a previous version used the unmodified 'internalName' as the option key
        if($options == false) { $options = tdomf_get_option_widget('tdomf_widget_'.$this->internalName,$form_id); }
        if($options == false) { $options = array(); }
        $options = wp_parse_args($options, $defaults);
        return $options;
    }
    
    /** 
     * Updates options for this widget
     * 
     * @access public
     */
    function updateOptions($options,$form_id,$postfix='') {
        $options = tdomf_set_option_widget($this->optionKey.$postfix,$options,$form_id);
    }
    
    /** 
     * Returns if the input form or mode is a edit form or not
     * 
     * @return Boolean
     * @access public
     */    
    /*public static*/ function isEditForm($mode,$form_id=false) {
        if($form_id != false) {
            $mode = tdomf_generate_default_form_mode($form_id);
        }
        if(strpos($mode, "edit-") === 0) {
            return true;
        }
        return false;
    }

    /** 
     * Returns if the input form or mode is a submit/new form or not
     * 
     * @return Boolean
     * @access public
     */    
    /*public static*/ function isSubmitForm($mode,$form_id=false) {
        if($form_id != false) {
            $mode = tdomf_generate_default_form_mode($form_id); 
        }
        if(strpos($mode, "new-") === 0) {
            return true;
        }
        return false;
    }
    
    /** 
     * Returns the postfix from an input param
     * 
     * @return Mixed
     */ 
    function getPostfixFromParams($params = array()) {
        $postfix = '';
        if($this->multipleInstances) {
            $postfix = 0;
            if(is_array($params) && count($params) >= 1){
                $postfix = $params[0];
            }
            if($this->multipleInstancesNoIndexOnFirst && $postfix <= 1) {
                // ignore postfix for first element
                $postfix = '';
            } else {
                $postfix = $this->optionKeySeperator.$postfix;
            }
        }
        return $postfix;
    }
    
    /** 
     * Updates fields and custom fields used by this widget
     * 
     * @return Boolean
     * @access private 
     */  
    function updateFields($args) {
        extract($args);
        if(is_array($this->fields) || is_array($this->customFields)) {
            
            if(TDOMF_Widget::isEditForm($mode)) {
                $edit = tdomf_get_edit($edit_id);
                
                if(is_array($this->fields)) {
                    if(!isset($edit->data[TDOMF_KEY_FIELDS]) || !is_array($edit->data[TDOMF_KEY_FIELDS])) {
                        $edit->data[TDOMF_KEY_FIELDS] = $this->fields;
                    } else {
                        $currentFields = array_merge($edit->data[TDOMF_KEY_FIELDS],$this->fields);
                        $edit->data[TDOMF_KEY_FIELDS] = $currentFields;
                    }
                }
                if(is_array($this->customFields)) {
                    if(!isset($edit->data[TDOMF_KEY_CUSTOM_FIELDS]) || !is_array($edit->data[TDOMF_KEY_CUSTOM_FIELDS])) {
                        $edit->data[TDOMF_KEY_CUSTOM_FIELDS] = $this->customFields;
                    } else {
                        $currentFields = array_merge($edit->data[TDOMF_KEY_CUSTOM_FIELDS],$this->customFields);
                        $edit->data[TDOMF_KEY_CUSTOM_FIELDS] = $currentFields;
                    }
                }
                // do update once
                tdomf_set_data_edit($edit->data,$edit_id);
                        
                // update the post id and not revision's list
                $id = $edit->post_id;
            } else {
                // submit form, so just update the post
                $id = $post_ID;
            }
             
            if(is_array($this->fields)) {
                    $currentFields = get_post_meta($id, TDOMF_KEY_FIELDS, true);
                    if(!is_array($currentFields)) {
                        add_post_meta($id, TDOMF_KEY_FIELDS, $this->fields, true);
                    } else {
                        $currentFields = array_merge($currentFields,$this->fields);
                        update_post_meta($id, TDOMF_KEY_FIELDS, $currentFields );
                    }
            }
            if(is_array($this->customFields)) {
                $currentFields = get_post_meta($id, TDOMF_KEY_CUSTOM_FIELDS, true);
                if(!is_array($currentFields)) {
                    add_post_meta($id, TDOMF_KEY_CUSTOM_FIELDS, $this->customFields, true);
                } else {
                    $currentFields = array_merge($currentFields,$this->customFields);
                    update_post_meta($id, TDOMF_KEY_CUSTOM_FIELDS, $currentFields );
                }
            }
        }
        return true;
    }
}

?>