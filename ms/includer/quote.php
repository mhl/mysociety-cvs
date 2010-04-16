<?php

require_once dirname(__FILE__) . "/../../phplib/evel.php";

$sent = false;

if (isset($_POST['_is_postback']) && $_POST['_is_postback'] && strtolower($_POST['theWord']) == 'tangent') {

    $to = OPTION_QUOTE_EMAIL;
    $from_email = $_POST['txtEmail'];
    $from_name = $_POST['txtName'];
    $area = $_POST['area'];
    $org = $_POST['txtOrganisation'];

    $subject = "[mySociety Quote Request] $area";
    if ($org) {
        $subject .= " - $org";
    }

    $body = $_POST['information'] . "\n-- \nForm submission from the mySociety website\n";

    evel_send(array(
        '_body_' => $body,
        'To' => $to,
        'From' => array($from_email, $from_name),
        'Subject' => $subject,
    ), $to);

    $sent = true;

}

?>

<h1>Request a quote</h1>

<?php if ($sent == false) { ?>
    <form method="POST">
        <input type="hidden" name="_is_postback" value="1" />
        <ul class="nobullets form">
            <li>
                <label for="txtName">Name *</label>
                <input type="text" class="textbox large" id="txtName" name="txtName" />
            </li>
            <li>
                <label for="txtEmail">Email *</label>
                <input type="text" class="textbox large" id="txtEmail" name="txtEmail" />
            </li>
            <li>
                <label for="txtOrganisation">Organisation</label>
                <input type="text" class="textbox large" id="txtOrganisation" name="txtOrganisation" />
            </li>
            <li>
                <label for="quote_area">Area of interest</label>
                <select name="area" id="quote_area">
                    <option>Petitions
                    <option>FixMyStreet
                    <option>Maps
                    <option>Consultancy
                    <option>Other
                    </select>
                </li>
                <li>
                    <label for="quote_information">More information</label>
                    <textarea id="quote_information" name="information" cols=10 rows=50></textarea>
                    <small>e.g. What you are specifically interested in, what you&rsquo;re after</small>
                </li>
                <li>
                  <p>Please enter the word "tangent" into the box below so we know that it's not just spam</p>
                    <label for="theWord">Enter "tangent"</label>
                    <input type="text" class="textbox large" id="theWord" name="theWord" />
                </li>
            </ul>
            <div class="buttons">
                <input type="submit" value="Request quote" />
            </div>
        </form>

<?php } else { ?>

    <p>Thanks, your request has been sent and someone will get back to you soon.
    <br /><a href="/">Return to the mySociety homepage</a></p>

<?php } ?>
