<?php 
$menu_proposals2006 = true;
require_once "../../phplib/utility.php";
$page = get_http_var('page');

if ($page == 'submit') {
    include "wordpress/wp-blog-header.php";
    include "wordpress/wp-content/themes/mysociety/header.php";     

    $errors = array();
    if ($_POST['proposal_submit'] && !get_http_var("submitreedit")) {
        if (strlen(trim(get_http_var('name'))) == 0)
            $errors['name'] = 'Please fill in your name.';
        if (strlen(trim(get_http_var('email'))) == 0)
            $errors['email'] = 'Please fill in your email address.';
        elseif (!validate_email($_POST['email'])) 
            $errors['email'] = 'The email address doesn\'t look right.';
        if (strlen(trim(get_http_var('title'))) == 0)
            $errors['title'] = 'Please fill in the title of your proposal.';
        if (strlen(trim(get_http_var('body_need'))) == 0)
            $errors['body_need'] = 'Please fill in the NEED section.';
        if (strlen(trim(get_http_var('body_approach'))) == 0)
            $errors['body_approach'] = 'Please fill in the APPROACH section.';
        if (strlen(trim(get_http_var('body_benefit'))) == 0)
            $errors['body_benefit'] = 'Please fill in the BENEFIT section.';
        if (strlen(trim(get_http_var('body_competition'))) == 0)
            $errors['body_competition'] = 'Please fill in the COMPETITION section.';
        if (strlen(trim(get_http_var('body_logistics'))) == 0)
            $errors['body_logistics'] = 'Please fill in the BUDGET &amp; LOGISTICS section.';

        if (!$errors) {
            $joined_post = 
                "<strong>What NEED does this meet?</strong>\n\n" . get_http_var('body_need') . "\n\n" .
                "<strong>What is the APPROACH?</strong>\n\n" . get_http_var('body_approach') . "\n\n" .
                "<strong>What are the BENEFITS to people?</strong>\n\n" . get_http_var('body_benefit') . "\n\n" .
                "<strong>What is the COMPETITION?</strong>\n\n" . get_http_var('body_competition') . "\n\n" .
                "<strong>What BUDGETS &amp; LOGISTICS are required?</strong>\n\n" . get_http_var('body_logistics') . "\n\n";
            $preview_post = apply_filters("the_content", $joined_post);
            $title = apply_filters("the_title", get_http_var('title'));

            if (get_http_var("submitfinal")) {
                $dummy_user_name = bin2hex(random_bytes(8));
                $wpdb->query("INSERT INTO `wp_users` (`user_login`, `user_pass`, `user_firstname`, `user_lastname`, `user_nickname`, `user_icq`, `user_email`, `user_url`, `user_ip`, `user_domain`, `user_browser`, `dateYMDhour`, `user_level`, `user_aim`, `user_msn`, `user_yim`, `user_idmode`, `user_description`, `user_activation_key`, `user_status`, `user_nicename`, `user_registered`) 
                    VALUES ('$dummy_user_name','NOPASSWORD','".$wpdb->escape(get_http_var('name'))."','','$dummy_user_name',0,'".$wpdb->escape(get_http_var('email'))."','','','','',now(),0,'','','','namefl','','',0,'$dummy_user_name',now())");
                $proposal_user_id = $wpdb->insert_id;
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
                    <INPUT TYPE="hidden" NAME="name" VALUE="<?=htmlspecialchars(get_http_var('name'))?>">
                    <INPUT TYPE="hidden" NAME="email" VALUE="<?=htmlspecialchars(get_http_var('email'))?>">
                    <INPUT TYPE="hidden" NAME="title" VALUE="<?=htmlspecialchars(get_http_var('title'))?>">
                    <INPUT TYPE="hidden" NAME="body_need" VALUE="<?=htmlspecialchars(get_http_var('body_need'))?>">
                    <INPUT TYPE="hidden" NAME="body_approach" VALUE="<?=htmlspecialchars(get_http_var('body_approach'))?>">
                    <INPUT TYPE="hidden" NAME="body_benefit" VALUE="<?=htmlspecialchars(get_http_var('body_benefit'))?>">
                    <INPUT TYPE="hidden" NAME="body_competition" VALUE="<?=htmlspecialchars(get_http_var('body_competition'))?>">
                    <INPUT TYPE="hidden" NAME="body_logistics" VALUE="<?=htmlspecialchars(get_http_var('body_logistics'))?>">
                    <INPUT TYPE="hidden" NAME="proposal_submit" VALUE="1">
                    <INPUT TYPE="submit" NAME="submitreedit" VALUE="&lt;&lt; Make some corrections">
                    <P><INPUT TYPE="submit" NAME="submitfinal" VALUE="Final step - Submit your proposal &gt;&gt;">
                </FORM>
            </div>
            <div class="item_foot">
            </div>


<?
exit;
        }
    }

?>
    <div class="item_head">
        Submit your proposal for a new mySociety project
    </div>
    <div class="item">
<?
    if ($errors) {
        print '<div id="errors"><ul><li>';
        print join ('</li><li>', array_values($errors));
        print '</li></ul></div>';
    }
?>
        <TABLE CELLSPACING="0" CELLPADDING="2" BORDER="0" BGCOLOR="#f0f0ff">
            <TR>
            <TD VALIGN="top">
                        <TABLE CELLSPACING="0" CELLPADDING="8" BORDER="0" BGCOLOR="#f0f0ff">
                <TR><TD COLSPAN="2" CLASS="smallb">
        <p><strong>PLEASE!</strong> Make sure you've <a href="/proposals2006/guidelines">read the guidelines</a> first.
        </TD></TR>
                <TR><FORM METHOD="POST" NAME="">
                <TD VALIGN="top">
            </TD>
                <TD VALIGN="top" ALIGN="right">
                    <TABLE CELLPADDING="2" CELLSPACING="0" BORDER="0">
                    <TR>
                    <TD CLASS="smallb">your name (will be public):</TD>
                    <TD><INPUT <? if (array_key_exists('name', $errors)) print ' class="error"' ?> NAME="name" VALUE="<?=htmlspecialchars(get_http_var('name'))?>" TYPE="text" SIZE="30"></TD>
                    </TR>

                    <TR>
                    <TD CLASS="smallb">your email (just for our records):</TD>
                    <TD><INPUT <? if (array_key_exists('email', $errors)) print ' class="error"' ?> NAME="email" VALUE="<?=htmlspecialchars(get_http_var('email'))?>" TYPE="text" SIZE="30">
                    </TD>
                    </TR>
                    </TABLE><BR></TD>
                </TR>
                <TR>
                <TD COLSPAN="2" CLASS="smallb">
                    Now describe your proposal:</SPAN>
                </TD>
                </TR>
                            <TR>
                    <TD CLASS="smallb">Title:</TD>
                    <TD><INPUT <? if (array_key_exists('title', $errors)) print ' class="error"' ?> NAME="title" VALUE="<?=htmlspecialchars(get_http_var('title'))?>" TYPE="text" SIZE="60">
                    </TD>
                    </TR>
                
                <TR>
                <TD COLSPAN="2">
                NEED: What need are you serving? What itch does your idea scratch? If it's not obvious, can you define the group of
        people this will help?"<BR>
                <TEXTAREA <? if (array_key_exists('body_need', $errors)) print ' class="error"' ?>ROWS="8" COLS="80" MAXLENGTH="2000" NAME="body_need" TEXTWRAP="physical" VALUE=""><?=htmlspecialchars(get_http_var('body_need'))?></TEXTAREA></TD>
                </TR>
                        <TR>
                <TD COLSPAN="2">
                APPROACH:    What's the plan, Stan? How is your approach distinctive?<BR>
                <TEXTAREA <? if (array_key_exists('body_approach', $errors)) print ' class="error"' ?>ROWS="8" COLS="80" MAXLENGTH="2000" NAME="body_approach" TEXTWRAP="physical" VALUE=""><?=htmlspecialchars(get_http_var('body_approach'))?></TEXTAREA></TD>
                </TR>
                        <TR>
                <TD COLSPAN="2">
                BENEFIT: What is  it about your idea that will make people's lives easier?<BR>
                <TEXTAREA <? if (array_key_exists('body_benefit', $errors)) print ' class="error"' ?>ROWS="8" COLS="80" MAXLENGTH="2000" NAME="body_benefit" TEXTWRAP="physical" VALUE=""><?=htmlspecialchars(get_http_var('body_benefit'))?></TEXTAREA></TD>
                </TR>
                        <TR>
                <TD COLSPAN="2">
                COMPETITION:  Any other similar services out there? Why must your idea win out?<BR>
                <TEXTAREA <? if (array_key_exists('body_competition', $errors)) print ' class="error"' ?>ROWS="8" COLS="80" MAXLENGTH="2000" NAME="body_competition" TEXTWRAP="physical" VALUE=""><?=htmlspecialchars(get_http_var('body_competition'))?></TEXTAREA></TD>
                </TR>
                                
                <TR>
                <TD COLSPAN="2">
                BUDGET &amp; LOGISTICS:  How expensive and difficult will it be to build your idea?<BR>
                <TEXTAREA <? if (array_key_exists('body_logistics', $errors)) print ' class="error"' ?>ROWS="8" COLS="80" MAXLENGTH="2000" NAME="body_logistics" TEXTWRAP="physical" VALUE="body_logistics"><?=htmlspecialchars(get_http_var('body_logistics'))?></TEXTAREA></TD>
                </TR>
                
                <TR>
                <TD ALIGN="left">&nbsp;</TD>
                <TD ALIGN="right">
        <INPUT TYPE="hidden" NAME="proposal_submit" VALUE="1">
        <INPUT TYPE="submit" NAME="SUBMIT" VALUE="Next step - Preview your proposal &gt;&gt;"><BR></TD>
                </TR></FORM>
                </TABLE>
            </TD>
            </TR>
            </TABLE>
        <P> 
        <P>
        <P>&nbsp;
        
        </TD>
        </TR>
        </TABLE>
    </div>
    <div class="item_foot">
    </div>
<?
    include "wordpress/wp-content/themes/mysociety/footer.php";
} elseif ($page == 'guidelines') {
    include "wordpress/wp-blog-header.php";
    include "wordpress/wp-content/themes/mysociety/header.php"; 
?>
    <div class="item_head">
        mySociety.org supports projects that have three broad attributes:
    </div>
    <div class="item">
        <ol>
            <li><B>Founded on electronic networks.</B> This includes the internet, mobile and
            telephone networks, wireless, fax and anything related.</LI>
            <li><B>Real world impact.</B>  The projects must have an impact which is above and
            beyond helping users to use their computers or mobiles more efficiently. We
            understand that there is a degree of philosophical ambiguity here (isn't
            faster browsing a real life impact?), so we've developed the following list
            of desirable outcomes from projects. 
            <UL>
                <LI><a href="http://www.bowlingalone.com/socialcapital.php3">Increased social
                capital</a>, preferably bridging between groups.</LI>
                <LI> <a
                href="http://www.google.com/search?q=define:Social+Exclusion">Reduced social exclusion</a></LI>
                <LI> Improved human capital and employment prospects</LI>
                <LI> Decreased occurrence of common social problems</LI>
            </UL>
            NB Projects are not limited to these
            outcomes - if you've got something good which doesn't fit in here,
            please <a href="mailto:tom@mysociety.org">let us know anyway</a>.</li>
            <li><B>Low or zero cost scalability.</B> This is key. We are looking for
            projects that cost the same (or virtually the same) to run for ten or a
            million users. This doesn't exclude the possibility of SMS based services,
            but it does rule out one-on-one tuition or building a site just for your
            community.</li>
        </ol>
    </div>
    <div class="item_foot">
    </div>
    <div class="item_head">
        Other Lower Priority Attributes That Would Be Nice
    </div>
    <div class="item">
        <ul>
            <LI> Development Community. The possibility that projects will attract self
            sustaining development communities.</LI>
            <LI> Low maintenance. Projects that are as reliable as a trusty screwdriver are
            desirable. Simple tools than can go online and never be thought about again
            will have an advantage.</LI>
            <LI>Things People Already Do, Done Better.</LI>
        </ul>
    </div>
    <div class="item_foot">
    </div>
<?
    include "wordpress/wp-content/themes/mysociety/footer.php";
} elseif ($page == 'about') {
    include "wordpress/wp-blog-header.php";
    include "wordpress/wp-content/themes/mysociety/header.php"; 
?>

    <div class="item_head">
        mySociety's Call for Proposals 2006
    </div>
    <div class="item">
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
        <p>Here's what to do:</p>
        <ul>
        <li>First <a href="/proposals2006/guidelines">read the guidelines</a>. Then either</li>
        <li><a href="/proposals2006/submit">Submit your own proposal</a> OR </li>
        <li><a href="/proposals2006/view">Read and comment</a> on other people's proposals.</li>
    </div>
    <div class="item_foot">
    </div>


<?
    include "wordpress/wp-content/themes/mysociety/footer.php";
} else {
    if (empty($_GET['cat'])) {
        $cat = 3;
    }
    /* Short and sweet */
    define('WP_USE_THEMES', true);
    require('wordpress/wp-blog-header.php');
}
?>
