<?php

require_once dirname(__FILE__) . "/../../phplib/evel.php";

$sent = false;

if (isset($_POST['_is_postback']) && $_POST['_is_postback'] && strtolower($_POST['theWord']) == 'tangent') {

    $to = OPTION_QUOTE_EMAIL;
    $from_email = $_POST['txtEmail'];
    $from_name = $_POST['txtName'];
    $area = $_POST['area'];
    $org = $_POST['txtOrganisation'];
    $info = $_POST['information'];

    if ($from_name && $from_email && $area && $info) {

        $subject = "[mySociety Quote Request] $area";
        if ($org) {
            $subject .= " - $org";
        }

        $body = "$info\n-- \nForm submission from the mySociety website\n";

        evel_send(array(
            '_body_' => $body,
            'To' => $to,
            'From' => array($from_email, $from_name),
            'Subject' => $subject,
        ), $to);
        $sent = true;

        print '<p>Thanks, your request has been sent and someone will get back to you soon.
        <br /><a href="/">Return to the mySociety homepage</a></p>';
    } else {
        print '<p>Please check and fill in the required fields below.</p>';
    }
}

if (!$sent) {

?>
    <form method="POST">
        <input type="hidden" name="_is_postback" value="1" />
        <ul class="nobullets form">
            <li>
                <label for="txtName">Name *</label>
                <input type="text" class="textbox large" id="txtName" name="txtName" value="<?=htmlspecialchars($_POST['txtName'])?>" />
            </li>
            <li>
                <label for="txtEmail">Email *</label>
                <input type="text" class="textbox large" id="txtEmail" name="txtEmail" value="<?=htmlspecialchars($_POST['txtEmail'])?>" />
            </li>
            <li>
                <label for="txtOrganisation">Organisation</label>
                <input type="text" class="textbox large" id="txtOrganisation" name="txtOrganisation" value="<?=htmlspecialchars($_POST['txtOrganisation'])?>" />
            </li>
            <li>
                <label for="quote_area">Area of interest *</label>
                <select name="area" id="quote_area">
                    <option>Petitions
                    <option>FixMyStreet
                    <option>Maps
                    <option>Consultancy
                    <option>Other
                    </select>
                </li>
                <li>
                    <label for="quote_information">Details of your enquiry *</label>
                    <textarea id="quote_information" name="information" cols=40 rows=10><?=htmlspecialchars($_POST['information'])?></textarea>
                    <br /><small>e.g. what you are specifically interested in, what is your budget, timescale, etc.</small>
                </li>
                <li>
                  <p>Please enter the word &ldquo;tangent&rdquo; into the box below so we know that you&rsquo;re a real person, thanks.</p>
                    <label for="theWord">Enter &ldquo;tangent&rdquo;</label>
                    <input type="text" class="textbox large" id="theWord" name="theWord" value="<?=htmlspecialchars($_POST['theWord'])?>" />
                </li>
            </ul>
            <div class="buttons">
                <input type="submit" value="Request quote" />
            </div>
        </form>

<?php

}
