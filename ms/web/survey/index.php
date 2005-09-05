<?  
    $page = $_GET['page']; 
    if (!$page)
        $page = 1;
    $nextpage = $page + 1;

    if ($page == 10) {
        header("Location: http://www.wavex.co.uk/projects/survey.asp");
        exit;
    }
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <title>mySociety Survey</title>
    
    <link rel="stylesheet" href="survey.css" type="text/css" media="screen" />
    </head>
<body>

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
<h1>Who are mySociety?</h1>

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

<p><a href="?page=<?=$nextpage?>">Next &gt;&gt;&gt;</a>

<p><img align="center" src="/mslogo.gif">

</body>
</html>

