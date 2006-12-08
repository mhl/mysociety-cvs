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

    $survey_url = "http://www.wavex.co.uk/projects/survey.asp";
    if (!$project && $page == 7) {
        header("Location: $survey_url");
        exit;
    }
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <title>mySociety Survey - Guidance Notes</title>
    
    <link rel="stylesheet" href="survey.css" type="text/css" media="projection,screen" />
    </head>
<body>

<? if ($project == "wtt") { ?>
    <? if ($page == 1) { ?>
<h1>WriteToThem - Introduction</h1>

<p> <img src="award.jpeg" align="right" style="margin: 1em"> WriteToThem.com is a highly popular, award-winning
service which allows members of the public to easily discover and then get in
touch with any of their elected representatives.


<p>We currently cover most UK councillors, MPs, MEPs, MSPs, Welsh and
London assembly members.

<p>WriteToThem.com is the successor to the multi-award winning
FaxYourMP.com.

    <? } elseif ($page == 2) { ?>
<h1>WriteToThem - How it works</h1>

<p>WriteToThem.com has been designed so that any local government
organisation can have a version appear consistently branded on its own
site. For example, your site homepage can feature an 'Enter Your
Postcode' box on any page which leads people to a page listing all
of their elected representatives, with descriptions of their different
responsibilities. The page appears to be entirely within and consistent in
visual appearance and brand identity with your local authority website.

<p>The user then chooses a representative and writes them a message. It is
then sent through our ultra-usable, abuse-proofed email or fax systems.

<p>To see an example of this in action, go to Cheltenham Borough Council's
implementation by
<a href="http://www.cheltenham.gov.uk/libraries/templates/thecouncil.asp?FolderID=8" target="_blank">clicking here</a> (look for "Contact your Councillors, MP and MEPs right here" half way down the right
hand side of the page).

    <? } elseif ($page == 3) { ?>
<h1>WriteToThem - Priority Outcomes</h1>

<p>2005 ODPM Priority Outcomes supported by WriteToThem:

<ul>
<li>No. 2 - Community Information
<li>No. 3 - Democratic Renewal
<li>No. 12 - Accessibility of Services
<li>No. 13 - High takeup of web based transactional services
</ul>

    <? } elseif ($page == 4) { ?>
<h1>WriteToThem - Specific Benefits</h1>

<ol>
<li>A simpler, more usable interface will put more people in contact
with their elected representatives than previously possible.
<li>Citizens who have gone to the wrong local authority website, or to
an entirely wrong part of government will still be given the correct
contact information, and won't require time or resource consuming
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
<li>WriteToThem has a proven track record of being used by less
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

<p>Pledgebank is a widely reported and highly popular site designed to
get people doing things in their local communities that they wouldn't
otherwise get round to.

<p>PledgeBank lets users make pledges in the form "I'll do something, but
only if 10 other people will do it too." Launched in June 2005,
PledgeBank has already had over 21,000 signatures on over 700 pledges,
varying from cleaning up a river bank in Cardiff, donating blood, using
energy efficient light bulbs and replacing the broken windows of an
East London mosque as a show of local solidarity after racist
violence.
    <? } elseif ($page == 2) { ?>
<h1>PledgeBank - An example of a successful pledge</h1>
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

<li>The ability to sign up to receive emails in a local area, and to be
notified when people create local pledges at any point in the future.
</ul>

    <? } elseif ($page == 5) { ?>

<h1>PledgeBank - Priority Outcomes</h1>

<p>2005 ODPM Priority Outcomes supported by PledgeBank

<ul>
<li>No. 3 - Democratic Renewal
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

<p>View a <a href="http://very.unfortu.net/~tom/pbpublicsector.ppt"
target="_blank">more detailed presentation</a> about PledgeBank (will open as a
Powerpoint file) or <a href="http://www.pledgebank.com" target="_blank">visit PledgeBank itself</a>.

    <? } elseif ($page == 7) { ?>
<? $end_project = 1 ?>
    <? } ?>
<? } elseif ($project == "ycml") { ?>
    <? if ($page == 1) { ?>
<h1>YourConstituencyMailingList</h1>

<p>YourConstituencyMailingList (a placeholder name) is mySociety's next major
citizen focussed web project.

<p>It is designed to let MPs and other elected representatives email their
constituents about matters which they consider to be important,
and to discuss those in a public forum.

    <? } elseif ($page == 2) { ?>
    <h1>YourConstituencyMailingList - How does it work?</h1>

    <p>A constituent enters their postcode, name and email address, and they
    are  added  to a queue of other people in their constituency. When
    enough people have signed up, the MP representing that area will
    automatically be sent an email. The email will say  '20 of your
    constituents would like to hear what you're up to - hit reply to talk
    to them'. If they don't reply nothing will happen, and the
    constituents will have to wait. But at some point in the future the MP
    will get another email which says 100 people; 200 people; or 500 people are
    waiting to hear from them - the day-to-day operation of the site will create
    incentives for the MP to respond, even if they choose not to for the first
    few times.
    
    <p>When the MP replies users are given a controlled opportunity to discuss
    the MP's message. Each email sent will have a link at the bottom, which
    takes users straight to a custom designed discussion forum. The first post
    in the forum is the MP's emailed message, and users can respond then and
    there, if they wish.  There's no tiresome login procedure - users can
    just start talking with a single click. And the MP can choose directly
    to engage with the group or respond to individual constituents privately.

    <? } elseif ($page == 3) { ?>
<h1>YourConstituencyMailingList - Screenshot of pre-launch site</h1>
<img src="ycmlscreen.gif" alt="YCML screenshot">

    <? } elseif ($page == 4) { ?>
<h1>YourConstituencyMailingList - Questions</h1>

<h2>How do councillors fit in?</h2>

<p>Whilst the service is being launched as a service for MPs, it is
technically easy to adapt the site to create 'Your Ward Mailing Lists'
for councillors. We would very much like to work with partner local
authorities to test councillor-run lists, and we can easily integrate
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
<? } elseif ($project == "gia") { ?>
    <? if ($page == 1) { ?>
    <h1>Give It Away - Introduction</h1>
    <p>Give It Away is our final citizen facing project being built with round 1
    E-Innovations funding.

    <p>It is a service to make it very easy for people to give away unwanted goods
    to local charities and community groups. Its goal is to increase the
    amount of valuable goods which are sold or re-used by organisations in
    local communities.
    <? } elseif ($page == 2) { ?>
    <h1>Give It Away - How it will work</h1>
    <p>A user starts by being in possession of some item or items they want
    to get rid of. They visit GiveItAway, enter a postcode and their email
    address, and enter the type of item they want to give away.

    <p>Moments later they receive an email which is copied into both the user
    as well as a nearby charity or community group which has previously
    indicated interest in this type of item. They can then discuss with
    the charity the details of whether the item is wanted, and if so, how
    it can be donated or collected.

    <p>The key to GiveItAway is minimalism and simplicity - as a website it
    features a single page, and relies on email to contact charities.
    This design demands a lower level of technical knowledge than any other
    internet-based interaction.

    <? } elseif ($page == 3) { ?>
    <h1>Give It Away - How it can be used by local authorities</h1>

    <p>As with most citizen-facing mySociety projects, GiveItAway can be
    rebranded and integrated within existing local authority websites.

    <p>An ideal location will be on the waste disposal information pages of a
    local council website. Next to information on garbage collection a
    council could place a prominent option which said "Are you about to
    throw something away that might be of value to someone else? Why not
    GiveItAway?"
    <? } elseif ($page == 4) { ?>
    <h1>Give It Away - Priority Outcomes</h1>
    <p>2005 ODPM Priority Outcomes supported by Give It Away:

    <ul>
    <li>No. 2 - Community information
    <li>No. 4 - Local Environment
    </ul>

    <h1>Benefits to citizens</h1>

    <ul>
    <li>Getting more resources to local community groups and charities
    <li>Increasing recycling/decreasing landfill
    </ul>

    <? } elseif ($page == 5) { ?>
<? $end_project = 1 ?>
    <? } ?>

<? } elseif ($project == "notapathetic") { ?>
    <? if ($page == 1) { ?>
    <h1>Not Apathetic</h1>
    <p>NotApathetic was a short-term project during the 2005 general election
    to find out why people weren't voting.

    <p>It gathered 3000 responses, and was reported in the media across the
    world. You can see the responses at <a href="http://www.notapathetic.com">www.NotApathetic.com</a>

    <p>We are including this in the survey as it is based on a very simple,
    easy to use technology that can be repurposed whenever you are trying
    to ask a large group of people one question, to solicit opinions. It
    is not a replacement for consultation software, but it has proven
    success at gathering large numbers of qualitative responses, as you
    can also see at <a href="http://www.ivotedforyoubecause.com">www.IVotedForYouBecause.com</a>

    <? } elseif ($page == 2) { ?>
<? $end_project = 1 ?>
    <? } ?>
<? } elseif ($project == "dadem") { ?>
    <? if ($page == 1) { ?>
    <h1>DaDem</h1>
    <p>DaDem is a web service, and therefore of interest to people with
    responsibilities for backend IT systems in local government
    organisations of all kinds.

    <p>The service provides licensed users with
    details on all the elected representatives in the UK: who they are,
    the areas they represent, their contact details, and in some cases
    an image and a history of changed contact details. We use it to manage
    the 20,000+ pieces of contact information required to run
    WriteToThem.com.

    <? } elseif ($page == 2) { ?>
    <h1>DaDem</h1>
<p>DaDem could be used in many useful and innovative ways by interested
local authorities - here are just a couple:

<p>1 - DaDem could be queried by the council-tax bill printing systems,
and every time a council tax bill was sent out, details of each
citizen's specific councillors could be printed it.

<p>2 - If a citizen phoned a council call-centre to report a broken
paving slab, the call-centre assistant could have an instant readout
of who the local councillors were for that citizen, to pass on or
escalate complaints as required.

    <? } elseif ($page == 3) { ?>
<? $end_project = 1 ?>
    <? } ?>

<? } elseif ($project == "mapit") { ?>
    <? if ($page == 1) { ?>
    <h1>MaPit</h1>
    <p>MapIt is a web service, and therefore of interest people with
    responsibilities for backend IT systems in local government
    organisations of all kinds.

    <p>The service converts users' postcodes to the electoral and administrative
    regions in which those postcodes lie (ward, electoral division,
    district, county, constituency, devolved assembly electoral region
    etc.) as well as their geographical (grid) coordinates. It is
    presented as a web service which may be used by any licensed website
    or other application.

    <? } elseif ($page == 2) { ?>
    <h1>MaPit</h1>
    <p>The underlying Mapit service can be customised for easy integration
    with existing or planned applications through an industry-standard or
    any sui generis interface. Further, coverage can be limited to
    specific areas (e.g., "within the area of Newtown Borough Council") or
    types of geographies (e.g., "only wards and constituencies") where
    only a subset of the available data is relevant.

    <p>So, for example:

    <p>1 - It can be used on websites or in call-centres to confirm that users
    are actually contacting the correct local authority.

    <p>2 - It can be combined with any number of services to find the
    closest/most appropriate public service to the user's location.

    <? } elseif ($page == 3) { ?>
<? $end_project = 1 ?>
    <? } ?>

<? } elseif ($project == "sams") { ?>
    <? if ($page == 1) { ?>
    <h1>SAMS</h1>
    <p>mySociety is currently developing SAMS, the Syndicatable, Annotatable
    Mapping Service.

    <p>This is a generic mapping service built on top of Google Maps which
    allows users to annotate maps with data, and for that data to be made
    available to other services via an API.

    <p>Our first demo implementation is YourHistoryHere - a local cultural
    knowledge site build in conjunction with the Young Foundation. This is
    specifically of use to educational, tourism and cultural establishments,
    but there are many other uses of the same technology,
    for example citizens using SAMS to locate and report broken civic
    infrastructure.
    <? } elseif ($page == 2) { ?>
<? $end_project = 1 ?>
    <? } ?>

<? } else { ?>

    <? if ($page == 1) { ?>
    <h1>mySociety Survey - Guidance Notes</h1>

    <p>Welcome to the the mySociety/ODPM E-Innovation Fund survey.

    <p>You are one of a small group of people identified by mySociety and the
    ODPM as a key representative of an organisation or sector with an
    interest in e-democracy, electronic public service provision or
    e-engagement generally. mySociety operates in these fields, and during
    this survey we will tell you about our work and its relevance to your
    organisations.

    <p>We know that many of you will not be familiar with mySociety's projects,
    so we've included some concise information on each of the projects,
    explaining what they do and highlighting specific benefits.

    <p>Thank you for taking the time to complete this survey - your responses
    are of great importance to the future of our project, and we believe
    that you will find our work interesting and useful.

    <? } elseif ($page == 2) { ?>
    <h1>What is this survey about?</h1>

    <p>mySociety is a charitable organisation, funded largely by ODPM's
    E-Innovations Fund, with the following aims:

    <p>
    <ul>
    <li><i>To build websites which give people simple, tangible benefits
    in the civic and community aspects of their lives.</i>
    <li><i>To teach the public and voluntary sectors, through demonstration, how
    to most efficiently use the internet to improve lives.</i>
    </ul>

    <p>Following these aims mySociety has built a set of popular products,
    using ODPM funding. The purpose of the survey is to collect your thoughts
    and opinions on the current and future value of mySociety products and
    services to you, your organisation and, where appropriate, the sector in
    which you operate.

    <p>As such, we will ask questions about your current spending on
    e-services and future plans. All answers provided will be treated in
    strict confidence. As we are asking your opinion on future products
    and services, we recognise that you are not committing your
    organisation to any future procurement from mySociety. We are simply
    attempting to assess the likely value of mySociety products to you and
    your organisation both now and in the future.

    <? } elseif ($page == 3) { ?>

    <h1>What is mySociety?</h1>

    <p>mySociety builds websites which give people simple, tangible benefits
    in the civic and community aspects of their lives.

    <p>It was founded in September 2003, having emerged from the voluntary
    programming community which built FaxYourMP.com in 2000. In March 2004
    we were awarded &pound;250,000 in a joint bid with West Sussex County
    Council. The money came from the Office of the Deputy Prime Minister's
    E-Innovations Fund, and we commenced building web projects in October
    of that year.

    <p>The organisation is directed by Tom Steinberg, who was formerly a
    government policy analyst working in the Prime Minister's
    Strategy Unit and Defra. The organisation consists of a small team of
    core, paid developers and a looser volunteer group of programmers,
    designers and non-technical helpers.

    <p>mySociety has created its services in partnership with West
    Sussex county council, but we are keen to work with further partners.

    <p>For more details on the organisation, its aims and ambitions, please
    <a href="http://www.mysociety.org/faq" target="_blank">click here</a>.

    <? } elseif ($page == 4) { ?>
    <h1>E-Innovations Fund</h1>

    <p>The E-Innovations Fund is an ODPM-backed government programme. The focus
    of E-Innovations is to encourage practical examples of new and
    innovative approaches to joined-up working, effective service delivery
    and community engagement which are sustainable in the long term.

    <p>The first round of support for E-Innovations is now well under way
    with 34 councils receiving matched funding of &pound;6.2m to deliver their
    innovative ideas by September 2005.

    <p>mySociety, in conjunction with West Sussex County Council, was a
    successful applicant in Round 1 of the Fund. The products of this
    funding are now in the public arena, and you will be given the chance
    to read about them shortly.

    <p>For more about the E-Innovation Fund, please 
    <a href="http://www.localegov.gov.uk/en/1/einnovation.html" target="_blank">click here</a>.

    <? } elseif ($page == 5) { ?>

    <h1>mySociety Projects</h1>

    <p>Choose the project you'd like to find out about:

    <h2 align="center">Live citizen facing projects</h2>

    <div class="project" id="pb"><strong>PledgeBank</strong> - We all know what it
    is like to feel powerless, that our own actions can't really change the things
    that we want to change.  PledgeBank is about beating that feeling. Read about
    our newest and most popular site yet.
    <a href="?page=1&project=pb">Click here to find out about PledgeBank &gt;&gt;</a>
    </div>

    <div class="project" id="wtt">
    <strong>WriteToThem</strong> - Our first site, which was winning awards after just twelve weeks online,
    makes it easy for any British citizen to contact their Councillors, MP, MEPs,
    MSPs, or Welsh and London Assembly Members for free.
    <a href="?page=1&project=wtt">Click here to find out about WriteToThem &gt;&gt;</a>
    </div>

    <h2 align="center">Next citizen facing projects</h2>

    <div class="project" id="ycml">
    <strong>YourConstituencyMailingList</strong> - Our next site allows MPs and councillors
    to contact their constituents. More than 3500 people have subscribed pre-launch.
    <a href="?page=1&project=ycml">Click here to find out about YourConstituencyMailingList &gt;&gt;</a>
    </div>

    <div class="project" id="gia">
    <strong>Give It Away</strong> - Lowering the barriers to giving things away.
    <a href="?page=1&project=gia">Click here to find out about Give It Away &gt;&gt;</a>
    </div>

    <h2 align="center">Back-office services</h2>

    <div class="project" id="dadem">
    DaDem - Web service database of elected representatives.
    <a href="?page=1&project=dadem">Click here to find out about DaDem &gt;&gt;</a>
    </div>
    <div class="project" id="sams">
    SAMS - Web service for annotatable maps.
    <a href="?page=1&project=sams">Click here to find out about SAMS &gt;&gt;</a>
    </div>
    <div class="project" id="mapit">
    Mapit - Web service database of electoral boundaries and postcodes.
    <a href="?page=1&project=mapit">Click here to find out about MaPit &gt;&gt;</a>
    </div>
    <h2 align="center">The survey</h2>
    <? $project_choice_page = 1 ?>

    <? } elseif ($page == 6) { ?>
    <h1>Timing and survey requirements</h1>

    <p>All surveys need to be completed by close of business on 20th
    September 2005.

    If you have any queries please contact 
    <a href="mailto:tom@mysociety.org">tom@mysociety.org</a>.

    <p><a href="?page=<?=$nextpage?>&project=<?=urlencode($project)?>">Next &gt;&gt;&gt;</a>

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

    <h1>Data Usage and Protection Information</h1>

    <p>The data you provide for the survey will be stored, analysed and
    protected in line with the 8 principles of the Data Protection Act of
    1998

    <p>The data will remain confidential and will be provided only to the ODPM's
    e-government unit. The data will not be used to resell any third party products
    or services to you.
    <p>By providing information about your organisation you make no commitment to
    purchase or agree to purchase in future and product or
    service from mySociety or its partners.
    <p>The data is obtained solely for the ODPM's e-innovations program. It
    will not be provided to any third parties or other organisations.
    <p>The data is adequate, relevant and not excessive to the ODPM's
    e-innovations program.
    <p>The data will be kept until the final research has been received and
    signed-off by the ODPM.
    <p>The data will be kept secure against unlawful or unauthorised
    processing, or accidental loss or erasure
    <p>The data will not be tranferred to a country outside the European Economic Area
    
    <? } ?>
<? } ?>
<? if ($end_project) { ?>
<p>Now you can either go back and read about the other projects, or
proceed to take the survey.
<p><a href="?page=5">Read about the other projects &gt;&gt;&gt;</a>
<br><a href="?page=6">Take the survey &gt;&gt;&gt;</a>
<? } elseif ($project_choice_page) { ?>
<p style="clear:all"><a href="?page=6">Click here</a> to take the survey straight away 
(although we recommend you take a quick tour through at least 
<a href="?page=1&project=pb">PledgeBank</a> and <a
href="?page=1&project=wtt">WriteToThem</a> first).
<!--<p style="clear:all"><a href="?page=6">Take the survey &gt;&gt;&gt;</a>-->
<? } else { ?>
<p>
<? if ($prevpage) { ?>
<!--<a href="?page=<?=$prevpage?>&project=<?=urlencode($project)?>">&lt;&lt;&lt; Prev</a>-->
<? } ?>
<a href="?page=<?=$nextpage?>&project=<?=urlencode($project)?>">Next &gt;&gt;&gt;</a>
<? } ?>
<p><img align="center" src="/mslogo.gif"> 
&nbsp;<img align="center" src="/wscc_logo.jpg"> 
&nbsp;<img align="center" src="/odpm_logo.gif">


</body>
</html>

