<?php
/*
 * HTML forms stuff.
 * 
 * Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
 * Email: francis@mysociety.org; WWW: http://www.mysociety.org
 *
 * $Id: forms.php,v 1.6 2005-01-11 17:19:04 chris Exp $
 * 
 */

require_once "HTML/QuickForm.php";
require_once "HTML/QuickForm/Rule.php";
require_once "HTML/QuickForm/Renderer/Default.php";

// Returns an array with all POST and GET variables, and any hidden form
// variables which were saved with function add_all_variables_hidden
// below.
function get_all_variables() {
    debug("SERIALIZE", "_GET", $_GET);
    debug("SERIALIZE", "_POST", $_POST);

    // All post and get variables, get have priority
    $variables = array_merge($_POST, $_GET);

    // Look for hidden serialised ones
    if (array_key_exists('mysociety_serialized_variables', $variables)) {
        $set_vars = unserialize(base64_decode($variables['mysociety_serialized_variables']));
        debug("SERIALIZE", "mysociety_serialized_variables", $set_vars);
        $variables = array_merge($set_vars, $variables);
    }
    
    unset($variables['mysociety_serialized_variables']);
    return $variables;
}

// Saves all variables in one simple form variable.
function add_all_variables_hidden(&$form, $variables) {
    debug("SERIALIZE", "Writing hidden vars:", $variables);
    $ser_vars = base64_encode(serialize($variables));
    $html_hidden = "<input name=\"mysociety_serialized_variables\" type=\"hidden\" value=\"$ser_vars\" \/>";
    // I tried using a 'hidden' element here, but it refuses to change
    // the value of the contents, just uses the one in _POST rather
    // than the new one.
    $form->addElement('html', $html_hidden);
}

class HTML_QuickForm_Renderer_mySociety extends HTML_QuickForm_Renderer_Default {

    function HTML_QuickForm_Renderer_mySociety() {
        // TODO: Properly CSS this
        $this->HTML_QuickForm_Renderer_Default();
        $this->setFormTemplate('
            <form{attributes}>
            <table border="0">
            {content}
            </table>
            </form>');
        $this->setElementTemplate('
                <TR>  
                <TD CLASS="small<!-- BEGIN required -->b<!-- END required -->">{label}</TD>
                <TD>
                    {element} 
                    <!-- BEGIN error --><span style="color: #ff0000"><br>{error}</span><!-- END error --> 
                </TD>
                </TR>
        ');
        $this->setRequiredNoteTemplate("");
        // Not sure what this is for - just set to default for now:
        $this->setHeaderTemplate('
            <tr>
                <td style="white-space: nowrap; background-color: #CCCCCC;" align="left" valign="top" colspan="2"><b>{header}</b></td>
            </tr>');
    }
}

?>
