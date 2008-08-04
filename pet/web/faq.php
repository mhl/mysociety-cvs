<?
// faq.php:
// FAQs
//
// Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
// Email: matthew@mysociety.org. WWW: http://www.mysociety.org
//
// $Id: faq.php,v 1.20 2008-08-04 10:48:07 matthew Exp $

// Load configuration file
require_once "../phplib/pet.php";

header('Cache-Control: max-age=300');
page_header('Questions and Answers');
?>

<h2 class="page_title_border">Questions and Answers</h2>

<h3>General questions</h3>

<dl>
<dt>What is an e-petition?</dt>
<dd>
<p>An e-petition is a form of petition posted on a website. Individuals or groups can create a petition on the site and visitors can add their details to the petition to "sign" it. The format makes it easy to collect signatures, and it also makes it easier for us to respond directly using email.</p>
</dd>

<dt>What's the difference between an e-petition and a paper petition?</dt>
<dd>
<p>There is no theoretical difference, only the way in which the signatures are collected and delivered. A petition can gather names and addresses in either or both forms, though once someone has signed a petition in one format, they cannot sign it in another.
</p>
</dd>

<dt>How do I get in touch with the team behind the website?</dt>
<dd>
<p>If you have any comments on the functioning of the petitions system, please contact
<a href="mailto:number10&#64;petitions.pm.gov.uk">number10&#64;petitions.pm.gov.uk</a>.
</p>
</dd>
</dl>

<h3>Petition signing questions</h3>

<dl>
<dt>How do I sign a petition?</dt>

<dd>
<p>
To sign a petition, you will need to give your name, address and email on the form provided. Once you have signed the petition, you will receive an email asking you to confirm that you wish to add your name to the petition by clicking a link. Once you have done this, your name will be added to the petition.
</p>
</dd>

<dt>What will you do with my name and address details if I sign a petition?</dt>

<dd>
<p>
Nothing, unless you expressly ask to sign up for other services available on
the Downing Street website (e.g. email updates). We will use your email address
to confirm your signature and, unless you ask us not to, we will also send you
a maximum of two responses to the issues raised in the petition. In the future
we may introduce a facility to enable the creator of the petition to send you a
maximum of two emails as well.  See our <a href="/privacy">privacy policy</a>
for more information. The data themselves are held by mySociety and not by the
Prime Minister's Office or any other government bodies or agencies.
</p>
</dd>

<dt>More than one person shares my email address &mdash; can we sign the petition?</dt>
<dd>
<p>
I'm afraid that there is a trade-off to be made between allowing anyone
to sign the petitions regardless of having an email address, and
protecting the petitions from too much abuse. 

We have come down on the side of using one email address per person to act
as an anti-abuse mechanism because it is now possible for anyone to get an
email address for free in a few moments. On the converse, if we let people
use one address to sign multiple times we will likely see considerable fake
signatures almost straight away.
</p>
</dd>

<dt>Why not "sign against" petitions?</dt>

<dd>
<p>Many people have suggested changes to the e-petitions service during this
test phase, and a number of improvements have been made as a result.</p>

<p>One of the most popular proposals has been the creation of a 'sign against'
mechanism, which would allow users to disagree with petitions. After much
discussion, we have decided not to add this function.</p>

<p>The rationale is this: "e-petitions" is designed essentially as a modern
equivalent of the traditional petitions presented at the door of No.10. It
enables people to put their views to the Prime Minister. It is not intended to
be a form of quasi-referendum or unrepresentative opinion poll (professional
polls use special techniques to ensure balanced samples). With a "vote against"
function, that is what it would effectively become.</p>

<p>It is of course possible to create a counter-petition to an existing
campaign (as many people already have). This remains the best option if you
disagree with a particular petition.</p>
</dd>

</dl>

<h3>Petition creation questions</h3>

<dl>

<dt>How do I start an e-petition?
<dd>
<p>
You can start a petition using our <a href="/new">e-petition form</a>. You will be asked to provide some basic information about yourself and your petition. We aim to make your petition live on the website within five working days, although during busy periods it may take longer.
</p>
</dd>

<dt>Do you accept all petitions?</dt>

<dd>
<p>We aim to accept as many petitions as possible. However this site has to
meet standards that are set out in our
<a href="/terms">terms and conditions</a> and in the Civil Service Code.</p>

<p>Petitioners may freely disagree with the Government or call for changes of policy. There will be no attempt to exclude critical views and decisions to accept or reject will not be made on a party political basis.</p>
</dd>

<dt>What happens if my petition is rejected?</dt>

<dd>
<p>If your petition does not meet these criteria, we will send it back to you along with an explanation of the reason(s) for rejection. We will give you the option of altering and resubmitting the petition.</p>

<p>If you decide not to resubmit your petition, or if your second iteration is also rejected, we will list your petition and the reason(s) for not accepting it on this website.</p>
</dd>

<dt>Can I still send in a paper petition?</dt>

<dd>
<p>
Yes. Paper petitions can still be posted/delivered to Downing Street. If you would prefer to collect signatures on paper, you should send them to:
</p>
<p>
10 Downing Street
London SW1A 2AA
</p>
</dd>

<dt>How long will my petition run for?</dt>

<dd>
<p>
You can decide how long your petition can run for and we will carry it for up to 12 months.
</p>
</dd>

<dt>What will happen to my petition once it is finished?</dt>

<dd>
<p>Once your petition has closed, usually provided there are 200 signatures or more, it
will be passed to officials who work for the Prime Minister in Downing
Street, or sent to the relevant Government department for a response.</p>

<p>Every person who signs such a petition will receive an email detailing the
Government's response to the issues raised.</p>
</dd>

<h3>Organisational questions</h3>

<dt>Who are mySociety and what is their involvement in the e-petition service?</dt>

<dd>
<p>
mySociety is a charitable project that builds websites which give people simple, tangible
benefits in the civic and community aspects of their lives. It is strictly neutral on party
political issues, and is run by registered charity UKCOD (no. 1076346). mySociety's role
was in designing and building the petitioning software to be as easy to use, as transparent
and as trustworthy as possible.
</p>
</dd>

<dt>Why have you set up this service?</dt>

<dd>
<p>
We are offering this service to enable as many people as possible to make their views known to the Government. The service will enable smaller groups who may not have the funds to set up a website to still collect signatures online. It also will enable us to respond directly to those who have signed the petition online via email.
</p>
</dd>

<dt>Can I make my own petitions site?</dt>

<dd>Yes, the software behind this petitions site is open source, and
available to you under the GNU Affero GPL software license. You can
<a
href="https://secure.mysociety.org/cvstrac/dir?d=mysociety">download the source code</a>
(look under 'pet') and help us develop it. You're welcome to use
it in your own projects, although you must also make available
the source code to any such projects.
</dd>

</dl>

<?  page_footer('FAQ');

