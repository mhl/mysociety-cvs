<?  
    $page = $_GET['page']; 
    if (!$page)
        $page = 1;
    $nextpage = $page + 1;
    if ($page > 1) {
        $prevpage = $page - 1;
    } else 
        $prevpage = null;
    $project = $_GET['project'];

    if (!$project && $page == 7) {
        header("Location: http://www.wavex.co.uk/projects/survey.asp");
        exit;
    }
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <title>mySociety Survey</title>
    
    <link rel="stylesheet" href="survey.css" type="text/css" media="projection,screen" />
    </head>
<body>

<? if ($project == "wtt") { ?>
    <? if ($page == 1) { ?>
<h1>WriteToThem - Introduction</h1>

<p>WriteToThem.com is a highly popular, award-winning service which
allows members of the public to easily discover and then get in touch
with any of their elected representatives.

<p>We currently cover all UK councillors, MPs, MEPs, MSPs, Welsh and
London assembly members.

<p>WriteToThem.com is the successor to the multi-award winning
FaxYourMP.com, and has been funded by the ODPM's e-innovations fund,
in partnership with West Sussex County Council.

    <? } elseif ($page == 2) { ?>
<h1>WriteToThem - How it works</h1>

<p>WriteToThem.com has been designed so that any local government
organisation can have a version appear consistently branded on its own
site. For example, your site homepage can feature an 'Enter Your
Postcode' box on any page which leads people to a page containing all
of their elected representatives, with descriptions of their different
responsibilities.

<p>The page appears to be entirely within and consistent in visual
appearance and brand identity with your local authority website. The
user then chooses a representative, writes them a message, and it
would be sent through our ultra-usable, abuse-proofed email or fax
systems.

<p>To see an example of this in action, go to Cheltenham Borough Councils'
implementation by
<a href="http://www.cheltenham.gov.uk/libraries/templates/thecouncil.asp?FolderID=8">clicking here</a> (look for "Contact your Councillors, MP and MEPs right here" half way down the right
hand side of the page).

    <? } elseif ($page == 3) { ?>
<h1>WriteToThem - Priority Outcomes</h1>

<p>2005 ODPM Priority Outcomes helped by WriteToThem:

<ul>
<li>No. 2 - Community Information
<li>No. 3 - Democractic Renewal
<li>No. 12 - Accessibility of Services
<li>No. 13 - High takeup of web based transactional services
</ul>

    <? } elseif ($page == 4) { ?>
<h1>WriteToThem - Specific Benefits</h1>

<ol>
<li>A simpler, more usable interface will put more people in contact
with their elected representatives than previously possible.
<li>Citizens who have gone to the wrong local authority website, or to
the wrong entire part of government will still be given the correct
contact information, and won't require time and resource consuming
mail redirection by council staff.
<li>WriteToThem.com protects elected representatives from spam or
abusive mail more effectively than the postal service, email services,
or fax.
<li>IT maintenance expense concerning councillor data will fall. After
an extremely rapid and simple installation process, the service
becomes effectively maintenance free from an IT department
perspective.
<li>A redirection service which will enable misdirected messages to be
sent to the correct representatives (i.e. mail that should have gone
to an MSP, or an MP) with a minimum of time, difficulty or expense.
<li>WriteToThem has a proven trackrecord of being used by less
tech-literate audiences - 60% of users reported they were writing to
their MP for the first time.
</ol>
    <? } elseif ($page == 5) { ?>
<h1>WriteToThem - Branding</h1>
<p>Question - Why can't we just link to WriteToThem?

<p>Answer - You can, but there are two reasons why it is better to have
your own branded version:

<p>1) You get no quality of service agreement (QoS), meaning that you
have no assurances that the site you link to will be live and
delivering the service you expect.

<p>2) As soon as your user clicks through  they lose your local authority
branding, and they are transferred to our site with our branding. This
also means that you cannot put in special instructions,  wording or
images specific to your councillors or local authority.

    <? } elseif ($page == 6) { ?>

<? $end_project = 1 ?>

    <? } ?>
<? } elseif ($project == "pb") { ?>
    <? if ($page == 1) { ?>
<h1>PledgeBank - Introduction</h1>

<p>A widely reported and highly popular site, which engages local people
to achieve things together that they otherwise wouldn't do, building
on a sense of community spirit.

<p>PledgeBank lets users make pledges in the form "I'll do something, but
only if 10 other people will do it too." Launched in June 2005,
PledgeBank has already had over 21,000 signatures on over 600 pledges,
varying from cleaning up riverbank in Cardiff, donating blood, using
energy efficient light bulbs and replacing the broken windows of an
East London mosque as a show of local solidarity after racist
violence.
    <? } elseif ($page == 2) { ?>
<h1>PledgeBank - Screenshot</h1>
<img src="rivertaff.jpg" alt="[screenshot of PledgeBank]">
    <? } elseif ($page == 3) { ?>
<h1>PledgeBank - Benefits to Local Authorities</h1>

<ul>
<li>Proven track record of getting people to collaborate on a range of
activities that they otherwise wouldn't have done.

<li>Customisable so that it just shows and highlights pledges created in one area.

<li>Acts as a lever to improve the effectiveness of a wider range of
pre-existing local agendas for healthier local democracy, better
schooling, and cleaner local environment and beyond.
</ul>
    <? } elseif ($page == 4) { ?>
<h1>PledgeBank - Benefits to local citizens</h1>

<ul>
<li>Improving and building community cohesion.

<li>Reassurance that if a citizen chooses to take action of benefit to
their local community, they won't be left isolated, trying to achieve
change on their own.

<li>The ability to signup to receive emails in a local area, and to be
notified when people create local pledges at any point in the future.
</ul>

    <? } elseif ($page == 5) { ?>

<h1>PledgeBank - Priority Outcomes</h1>

<p>2005 ODPM Priority Outcomes helped by PledgeBank

<ul>
<li>No. 3 - Democractic Renewal
<li>No. 4 - Local Environment
<li>No. 5 - Library Sport and Leisure
<li>No. 8 - Supporting new ways of working
</ul>
    <? } elseif ($page == 6) { ?>
<h1>PledgeBank - Local adaptation</h1>

<p>We can create versions of PledgeBank that are branded for specific
local organisations (say a London borough, or an agency like Sport
London). These will only show local pledges within the remit of those
bodies.

<p>PledgeBank can also be adapted for use within organisations, for
example organising volunteering or social activities within a local
authority intranet (i.e I will volunteer 3 hours a week on project X,
but only if 5 other people in this building will too)

    <? } elseif ($page == 7) { ?>
<? $end_project = 1 ?>
    <? } ?>
<? } elseif ($project == "ycml") { ?>
    <? if ($page == 1) { ?>
<h1>YourConstituencyMailingList</h1>

<p>YourConstituencyMailingList (a placeholder name) is mySociety's next major
citizen focussed  web project.

<p>It is designed to let MPs and other elected representatives email their
constituents about matters which they consider to be important,
and to discuss those in a public forum.

    <? } elseif ($page == 2) { ?>
    <h1>YourConstituencyMailingList - How does it work?</h1>

    <p>A constituent enters their postcode, name and email address, and they
    are  added  to a queue of other people in their constituency. When
    enough people have signed up, the MP representing that area will be
    automatically sent an email. The email will say  '20 of your
    constituents would like to hear what you're up to - hit reply to talk
    to them'. If they don't reply nothing will happen, and the
    constituents will have to wait. But at some point in the future the MP
    will get another email which says 100 people; 200 people; 500 people -
    the day-to-day operation of the site will create incentives for the MP
    to respond, even if they choose not to for the first few times.

    <p>When the MP replies, the result isn't one-way spam or an uncontrolled
    email free-for-all. Instead, each email will have a link at the
    bottom, which will take you straight to a forum where the first post
    will contain the MP's email. There'll be no tiresome login procedure,
    users can just start talking with a single click. And the MP can
    engage directly or watch from a distance, depending on their
    preference.

    <? } elseif ($page == 3) { ?>
<h1>YourConstituencyMailingList - Screenshot</h1>
<img src="ycmlscreen.gif" alt="YCML screenshot">

    <? } elseif ($page == 4) { ?>
<h1>YourConstituencyMailingList - Questions</h1>

<h2>How do councillors fit in?</h2>

<p>Whilst the service is being launched as a service for MPs, it is
technically easy to adapt the site to create 'Your Ward Mailing Lists'
for councillors. We would very much like to work with partner local
authorities to test councillor run lists, and we can easily integrate
the whole site into local authority websites.

<h2>When does it launch?</h2>

<p>We plan to start testing YourConstituencyMailingList with real MPs and
constituents in mid-September. We already have over 3500 people signed
up, showing the great latent demand for an easy way to hear from local
politicians.
    <? } elseif ($page == 5) { ?>
<h1>YourConstituencyMailingList - Priority Outcomes</h1>
<p>2005 ODPM Priority Outcomes supported by YourConstituencyMailingList:

<ul>
<li>No. 2 - Community information
<li>No. 3 - Democratic renewal
<li>No. 11 -  Supporting new ways of working
</ul>
    <? } elseif ($page == 6) { ?>
<? $end_project = 1 ?>
    <? } ?>
<? } else { ?>

    <? if ($page == 1) { ?>
    <h1>Introduction</h1>

    <p>Welcome to the the mySociety/ODPM e-innovation fund survey

    <p>You are one of a small group of people identified by mySociety and the
    ODPM as a key representative of an organisation or sector with an
    interest in e-democracy, electronic public service provision or
    e-engagement generally. mySociety operates in these fields, and during
    this survey we will tell you about our work and it's relevence to your
    organisations.

    <p>The information on this site is designed to help you complete the
    survey as quickly and painlessly as possible.

    <p>Thank you for taking the time to complete this survey - your responses
    are of great importance to the future of our project, and we believe
    that you will find our work interesting and useful.

    <? } elseif ($page == 2) { ?>
    <h1>What is this survey about?</h1>

    <p>mySociety is a charitable organisation, funded largely by ODPM's
    e-innovations fund, with the following aims:

    <p><blockquote>To build websites which give people simple, tangible benefits
    in the civic and community aspects of their lives.

    To teach the public and voluntary sectors, through demonstration, how
    to most efficiently use the internet to improve lives. </blockquote>

    <p>The purpose of the survey is to collect your thoughts and opinions on
    the current and future value of mySociety products and services to
    you, your organisation and, where appropriate, the sector in which you
    operate.

    <p>As such, we will ask questions about your current spending on
    e-services and future plans. All answers provided will be treated in
    strict confidentiality. As we asking your opinion on future products
    and services, we recognise that you are not committing your
    organisation to any future procurement from mySociety. We are simply
    attempting to assess the likely value of mySociety products to you and
    your organisation both now and in the future.

    <? } elseif ($page == 3) { ?>
    <h1>e-Innovations Fund</h1>

    <p>The e-innovations fund is an ODPM backed government program. The focus
    of e-innovations is to encourage practical examples of new and
    innovative approaches to joined-up working, effective service delivery
    and community engagement which are sustainable in the long term.

    <p>The first round of support for e-Innovations is now well under way
    with 34 councils receiving matched funding of &pound;6.2m to deliver their
    innovative ideas by September 2005

    <p>mySociety, in conjunction with West Sussex County Council, was a
    successful applicant to Round 1 of the Fund. The products of this
    funding are now in the public arena, and you will be given the chance
    to read about them shortly.

    <p>For more about the e-innovation fund, please 
    <a href="http://www.localegov.gov.uk/en/1/einnovation.html">click here</a>.

    <? } elseif ($page == 4) { ?>

    <h1>What is mySociety?</h1>

    <p>mySociety builds websites which give people simple, tangible benefits
    in the civic and community aspects of their lives.

    <p>It was founded in September 2003, having emerged from the voluntary
    programming community which built FaxYourMP.com in 2000. In March 2004
    we were awarded &pound;250,000 in a joint bid with West Sussex County
    Council. The money came from the Office of the Deputy Prime Ministers
    e-innovations fund, and we commenced building web projects in October
    of that year.

    <p>The organization is directed by Tom Steinberg, who was formerly
    government policy analyst serving time with the Prime Minister's
    Strategy Unit and Defra. The organization consists of a small team of
    core, paid developers and a looser volunteer group of programmers,
    designers and non-technical helpers.

    <p>mySociety has created its services working in partnership with West
    Sussex county council but we are keen to work with further partners.

    <p>For more details on the organization, its aims and ambitions, please
    <a href="http://www.mysociety.org/faq.php">click here</a>.

    <? } elseif ($page == 5) { ?>

    <h1>Choose the project you'd like to find out about:</h1>

    <h2>Citizen facing projects</h2>

    <div class="project" id="pb"><strong>PledgeBank</strong> - We all know what it
    is like to feel powerless, that our own actions can't really change the things
    that we want to change.  PledgeBank is about beating that feeling. Read about
    our newest and most popular site yet.
    <a href="?page=1&project=pb">Click here to find out about PledgeBank &gt;&gt;</a>
    </div>

    <div class="project" id="wtt">
    <strong>WriteToThem</strong> - Our first site, award winning in only 12 weeks,
    makes it easy for any British citizen to contact their Councillors, MP, MEPs,
    MSPs, or Welsh and London Assembly Members for free.
    <a href="?page=1&project=wtt">Click here to find out about WriteToThem &gt;&gt;</a>
    </div>

    <h2>Future citizen facing projects</h2>

    <div class="project" id="ycml">
    <strong>YourConstituencyMailingList</strong> - Our next site allows MPs and councillors
    to contact their constituents. 3500+ subscribers so far and the site not
    launched yet.
    <a href="?page=1&project=ycml">Click here to find out about YourConstituencyMailingList &gt;&gt;</a>
    </div>

    <div class="project" id="gia">
    <strong>Give It Away</strong> - Lowering the barriers to giving things away
    </div>

    <h2>Backoffice services</h2>

    <ul>
    <li>DaDem - Web service database of elected representatives
    <li>Mapit - Web service database of electoral boundaries and postcodes
    </ul>
    <? $project_choice_page = 1 ?>

    <? } elseif ($page == 6) { ?>
    <h1>Timing and survey requirements</h1>

    <p>All surveys need to be completed by close of business on Monday 12th
    September 2005.

    If you have any queries please contact 
    <a href="mailto:tom@mysociety.org">tom@mysociety.org</a>.

    <h1>Interviews</h1>

    <p>If you feel you any opinions or thoughts regarding mySociety's future
    development, we are looking to undertake a small number of 30 minute
    interviews in addition to completion of the survey. In these
    interviews we would look to examine particular sectors and
    organisations and how mySociety could best engage with them.

    <p>These include:

    <ul>
    <li>E-democracy units within Local Authorities
    <li>Regional bodies (London Connects, etc) interested in syndication
    and/or use of products
    <li>Local authorities interested in annual subscriptions to mySociety
    products tailored for their use.
    <li>Academic communities and Universities
    <li>For-profit companies
    <li>Media and publishing organisations
    <li>Charities
    <li>Social Entrepreneurs
    </ul>

    <p>If you feel you are able to assist by offering some time for a
    face-to-face or telephone interview, or can recommend someone who
    would be interested, please email 
    <a href="mailto:tom@mysociety.org">tom@mysociety.org</a>.
    <? } ?>
<? } ?>
<? if ($end_project) { ?>
<p>Now you can either go back and read about the other projects, or
proceed to take the survey.
<p><a href="?page=5">Read about the other projects &gt;&gt;&gt;</a>
<br><a href="?page=6">Take the survey &gt;&gt;&gt;</a>
<? } elseif ($project_choice_page) { ?>
<a href="?page=6">Take the survey &gt;&gt;&gt;</a>
<? } else { ?>
<p>
<? if ($prevpage) { ?>
<!--<a href="?page=<?=$prevpage?>&project=<?=urlencode($project)?>">&lt;&lt;&lt; Prev</a>-->
<? } ?>
<a href="?page=<?=$nextpage?>&project=<?=urlencode($project)?>">Next &gt;&gt;&gt;</a>
<? } ?>
<p><img align="center" src="/mslogo.gif">

</body>
</html>

