<?php 
$menu_proposals2006 = true;
require_once "../../phplib/utility.php";

# Get all variables before we include WordPress
$q_page = get_http_var('page');
$q_name = get_http_var('name');
$q_email = get_http_var('email');
$q_title = get_http_var('title');
$q_body_need = get_http_var('body_need');
$q_body_approach = get_http_var('body_approach');
$q_body_benefit = get_http_var('body_benefit');
$q_body_competition = get_http_var('body_competition');
$q_body_logistics = get_http_var('body_logistics');

# Make sure we are in proposals category
if (empty($_GET['cat'])) {
    $cat = 3;
}

if ($q_page == 'submit') {
    include "wordpress/wp-blog-header.php";
    include "wordpress/wp-content/themes/mysociety/header.php";     

    $errors = array();
    if ($_POST['proposal_submit'] && !get_http_var("submitreedit")) {
        if (strlen(trim($q_name)) == 0)
            $errors['name'] = 'Please fill in your name.';
        if (strlen(trim($q_email)) == 0)
            $errors['email'] = 'Please fill in your email address.';
        elseif (!validate_email($q_email)) 
            $errors['email'] = 'The email address doesn\'t look right.';
        if (strlen(trim($q_title)) == 0)
            $errors['title'] = 'Please fill in the title of your proposal.';
        if (strlen(trim($q_body_need)) == 0)
            $errors['body_need'] = 'Please fill in the Need section.';
        if (strlen(trim($q_body_approach)) == 0)
            $errors['body_approach'] = 'Please fill in the Approach section.';
        if (strlen(trim($q_body_benefit)) == 0)
            $errors['body_benefit'] = 'Please fill in the Benefit section.';
        if (strlen(trim($q_body_competition)) == 0)
            $errors['body_competition'] = 'Please fill in the Competition section.';
        if (strlen(trim($q_body_logistics)) == 0)
            $errors['body_logistics'] = 'Please fill in the Budget &amp; Logistics section.';

        $errors['any'] = 'New submissions are now closed, sorry!';

        if (!$errors) {
            $joined_post = 
                "<strong>What NEED does this meet?</strong>\n\n" . $q_body_need . "\n\n" .
                "<strong>What is the APPROACH?</strong>\n\n" . $q_body_approach . "\n\n" .
                "<strong>What are the BENEFITS to people?</strong>\n\n" . $q_body_benefit . "\n\n" .
                "<strong>What is the COMPETITION?</strong>\n\n" . $q_body_competition . "\n\n" .
                "<strong>What BUDGETS &amp; LOGISTICS are required?</strong>\n\n" . $q_body_logistics . "\n\n";
            $preview_post = apply_filters("the_content", $joined_post);
            $title = apply_filters("the_title", $q_title);


            if (get_http_var("submitfinal")) {
                $dummy_user_name = bin2hex(random_bytes(8));
                $wpdb->query("INSERT INTO `wp_users` (`user_login`, `user_pass`, `user_email`, `user_url`, `dateYMDhour`,
                `user_activation_key`, `user_status`, `display_name`, `user_registered`, `user_nicename`)
                 VALUES ('$dummy_user_name','NOPASSWORD','".$wpdb->escape($q_email)."','',now(),
                 '',0,'".$wpdb->escape($q_name)."',now(),'$dummy_user_name')");
                $proposal_user_id = $wpdb->insert_id;
                $wpdb->query("INSERT INTO `wp_usermeta` (`user_id`, `meta_key`, `meta_value`) VALUES ('$proposal_user_id', 'wp_user_level', 0)");
                $wpdb->query("INSERT INTO `wp_usermeta` (`user_id`, `meta_key`, `meta_value`) VALUES ('$proposal_user_id', 'wp_capabilities', 'a:1:{s:10:\"subscriber\";b:1;}')");
                $wpdb->query("INSERT INTO `wp_usermeta` (`user_id`, `meta_key`, `meta_value`) VALUES ('$proposal_user_id', 'first_name', '".$wpdb->escape($q_name)."')");
                $post_data = array('post_content' => $joined_post,
                    'post_title' => $title,
                    'post_author' => $proposal_user_id, 
                    'post_category' => array(3) /* category for proposals 2006 */, 
                    'post_status' => 'publish');
                $post_ID = wp_insert_post($post_data);
                $post_link = "http://www.mysociety.org/?p=$post_ID";
?>
            <div class="item_head">
                Thanks for submitting your proposal!
            </div>
            <div class="item">
                <ul>
                <li>You can see your proposal at <a href="<?=$post_link?>"><?=$post_link?></a> &mdash;
                please <strong>send that link to friends or contacts</strong>
                who might have useful thoughts to add to your proposal.</li>
                <li>We're always <strong>looking for new volunteers</strong> to help with our
                existing or future projects. Whatever skills you've got, go to
                our <a href="http://www.mysociety.org/volunteertasks">volunteers page</a>
                for more information.</li>
                </ul>
            </div>
            <div class="item_foot">
            </div>
<?
                exit;
            }
?>
            <div class="item_head">
                Preview your proposal
            </div>
            <div class="item">
                <p>Please check your proposal below.</p>
            </div>
            <div class="item_foot">
            </div>

            <div class="item_head">
                <?=$title ?>
            </div>
            <div class="item">
                <?=$preview_post ?>
            </div>
            <div class="item_foot">
            </div>

            <div class="item_head">
            </div>
            <div class="item">
                <FORM METHOD="POST" NAME="">
                    <INPUT TYPE="hidden" NAME="name" VALUE="<?=htmlspecialchars($q_name)?>">
                    <INPUT TYPE="hidden" NAME="email" VALUE="<?=htmlspecialchars($q_email)?>">
                    <INPUT TYPE="hidden" NAME="title" VALUE="<?=htmlspecialchars($q_title)?>">
                    <INPUT TYPE="hidden" NAME="body_need" VALUE="<?=htmlspecialchars($q_body_need)?>">
                    <INPUT TYPE="hidden" NAME="body_approach" VALUE="<?=htmlspecialchars($q_body_approach)?>">
                    <INPUT TYPE="hidden" NAME="body_benefit" VALUE="<?=htmlspecialchars($q_body_benefit)?>">
                    <INPUT TYPE="hidden" NAME="body_competition" VALUE="<?=htmlspecialchars($q_body_competition)?>">
                    <INPUT TYPE="hidden" NAME="body_logistics" VALUE="<?=htmlspecialchars($q_body_logistics)?>">
                    <INPUT TYPE="hidden" NAME="proposal_submit" VALUE="1">
                    <INPUT TYPE="submit" NAME="submitreedit" VALUE="Make some corrections">
                    <P><INPUT TYPE="submit" NAME="submitfinal" VALUE="Final step - Submit your proposal">
                </FORM>
            </div>
            <div class="item_foot">
            </div>


<?
exit;
        }
    }

?>
<?
    if ($errors) {
        print '<p><div id="errors"><ul><li>';
        print join ('</li><li>', array_values($errors));
        print '</li></ul></div>';
    }
?>
    <div class="item_head">
        Guidelines for proposals
    </div>
    <div class="item">
        <p>mySociety projects have three broad attributes:
        <ol class="proposals">
            <li><B>Founded on electronic networks.</B> This includes the internet, mobile and
            telephone networks, wireless, fax and anything related.</LI>
            <li><B>Real world impact on democratic and community aspects of
            people's lives.</B>  The internet is full of excellent commerce
            and entertainment sites: we are not about building more of those.
            It is also full of great information sites: we aren't about building
            these either. We want sites that users visit and leave
            having gained something tangible: a nascent relationship wth
            their MP, or the knowledge that they can achieve something with
            other people near them.
            </li>
            <li><B>Low or zero cost scalability.</B> This is key. We are looking for
            projects that cost the same (or virtually the same) to run for ten or a
            million users. This doesn't exclude the possibility of SMS based services,
            but it does rule out one-on-one tuition or building a site just for your
            community.  Projects that are as reliable as a trusty screwdriver
            are desirable. Simple tools that can go online and never be thought
            about again will have an advantage.</li>
    </div>
    <div class="item_foot">
    </div>


    <div class="item_head">
        New submissions for 2006 are now closed
    </div>
    <div class="item">
        <p>Now we've just got to decide which one wins.</p>
        <p>You can help out by <a href="/proposals2006/view">adding
        your thoughts</a> to the proposals which were submitted.
        </p>
    </div>
    <div class="item_foot">
    </div>
<!--
    <div class="item_head">
        Submit your proposal for a new mySociety project
    </div>
    <div class="item">
                <FORM METHOD="POST" NAME="">
                    <p><strong>Please!</strong> Make sure you've read the guidelines (above) first.
                    <P>Your name:
                    <INPUT <? if (array_key_exists('name', $errors)) print ' class="error"' ?> NAME="name" VALUE="<?=htmlspecialchars($q_name)?>" TYPE="text" SIZE="30"> (will be public)
                    <P>Your email:
                    <INPUT <? if (array_key_exists('email', $errors)) print ' class="error"' ?> NAME="email" VALUE="<?=htmlspecialchars($q_email)?>" TYPE="text" SIZE="30"> (just for our records)
                    <p>Now describe your proposal:
                    <p><strong>Title:</strong>
                    <INPUT <? if (array_key_exists('title', $errors)) print ' class="error"' ?> NAME="title" VALUE="<?=htmlspecialchars($q_title)?>" TYPE="text" SIZE="60">
                
                <P><strong>1. Need:</strong> What need are you serving? What itch does your idea scratch? If it's not obvious, can you define the group of
        people this will help?"</P>
                <TEXTAREA <? if (array_key_exists('body_need', $errors)) print ' class="error"' ?>ROWS="8" COLS="80" MAXLENGTH="2000" NAME="body_need" TEXTWRAP="physical" VALUE=""><?=htmlspecialchars($q_body_need)?></TEXTAREA>
                <P><strong>2. Approach:</strong>    What's the plan, Stan? How is your approach distinctive?</P>
                <TEXTAREA <? if (array_key_exists('body_approach', $errors)) print ' class="error"' ?>ROWS="8" COLS="80" MAXLENGTH="2000" NAME="body_approach" TEXTWRAP="physical" VALUE=""><?=htmlspecialchars($q_body_approach)?></TEXTAREA>
                <P><strong>3. Benefit:</strong> What is  it about your idea that will make people's lives easier?</P>
                <TEXTAREA <? if (array_key_exists('body_benefit', $errors)) print ' class="error"' ?>ROWS="8" COLS="80" MAXLENGTH="2000" NAME="body_benefit" TEXTWRAP="physical" VALUE=""><?=htmlspecialchars($q_body_benefit)?></TEXTAREA>
                <P><strong>4. Competition:</strong>  Any other similar services out there? Why must your idea win out?</P>
                <TEXTAREA <? if (array_key_exists('body_competition', $errors)) print ' class="error"' ?>ROWS="8" COLS="80" MAXLENGTH="2000" NAME="body_competition" TEXTWRAP="physical" VALUE=""><?=htmlspecialchars($q_body_competition)?></TEXTAREA>

                <P><strong>5. Budget &amp; Logistics:</strong>  How expensive and difficult will it be to build your idea?</P>
                <TEXTAREA <? if (array_key_exists('body_logistics', $errors)) print ' class="error"' ?>ROWS="8" COLS="80" MAXLENGTH="2000" NAME="body_logistics" TEXTWRAP="physical" VALUE="body_logistics"><?=htmlspecialchars($q_body_logistics)?></TEXTAREA>
                
        <INPUT TYPE="hidden" NAME="proposal_submit" VALUE="1">
        <P><INPUT TYPE="submit" NAME="SUBMIT" VALUE="Next step - Preview your proposal &gt;&gt;"><BR>
        <P> 
        <P>
        <P>&nbsp;
    </div>
    <div class="item_foot">
    </div>
-->
<?
    include "wordpress/wp-content/themes/mysociety/footer.php";
} elseif ($q_page == 'about') {
    include "wordpress/wp-blog-header.php";
    include "wordpress/wp-content/themes/mysociety/header.php"; 
?>

    <div class="item_head">
        New submissions for 2006 are now closed
    </div>
    <div class="item">
        <p><a href="/proposals2006/view">Head on over here</a> to
        read all the proposals. Thanks everyone for submitting lots
        of great ideas!
        </p>
        
        <p>We'll announce the winner when we've properly read and considered
        them all.  Help out by leaving your comments as to what is good or bad
        about them.</p>
    </div>
    <div class="item_foot">
    </div>

    <div class="item_head">
        mySociety will build the best site submitted
    </div>
    <div class="item">
        <img style="float:right" src="/proposals-radio.png" alt="">
        <p>It's two and a half years since our 
        <a href="http://news.bbc.co.uk/2/hi/technology/3228339.stm">last call for proposals</a>, 
        which led to us building <a href="/projects.php">four projects</a>
        including <a href="http://www.pledgebank.com">PledgeBank.com</a> and 
        <a href="http://www.writetothem.com">WriteToThem.com</a>. At the time
        we had almost no funding and could only promise to try and raise money
        to build the projects. That worked, and now we've got a little bit of a
        surplus (charity language for a profit) left over from our government
        support.</p>

        <p>The time has come to open the call for proposals up again, this time
        with one difference: we pledge to build the winning project, using a
        combination of some of the leftover cash and the help of any willing
        volunteers.</p>

        <p>So, whether you have an idea you'd like to propose, or whether you'd
        just like to read and comment on other people's proposals, you've come
        to the right place.</p>

        </p>
        <p>Here's what to do. Either:</p>
        <ul>
        <li><a href="/proposals2006/submit">Submit your own proposal</a> OR </li>
        <li><a href="/proposals2006/view">Read and comment</a> on other people's proposals.</li>
    </div>
    <div class="item_foot">
    </div>


<?
    include "wordpress/wp-content/themes/mysociety/footer.php";
} else {
    /* Short and sweet */
    define('WP_USE_THEMES', true);
    require('wordpress/wp-blog-header.php');
}
?>
