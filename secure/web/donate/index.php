<?php

$file = file_get_contents('http://www.mysociety.org/donate/');
$file = preg_replace('#href="/#', 'href="http://www.mysociety.org/', $file);
$file = preg_replace('#(rel="stylesheet" href=")http://www.mysociety.org/#', '$1/nonsecure/', $file);
$file = preg_replace('#src="/#', 'src="/nonsecure/', $file);
$file = preg_replace('#<!-- Piwik.*?/Piwik -->#s', '', $file);
print $file;

