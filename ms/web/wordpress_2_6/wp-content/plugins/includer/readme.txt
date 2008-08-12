=== includer ===
Contributors: angie@mysociety.org
Tags: include php text post
Requires at least: 2.6
Tested up to: 2.6
Stable tag: 2.6

Include php and other files in your posts and pages.

== Description ==

Allows you you embedd php and text from files on your server into your posts.

To use you need to have a folder called includer at the root of your web serving directory.
You place files you will be wanting to include in pages or posts here.
eg a file called testy.php 

to embed the contents of that file in your post you call it with the includer tag:

<!-- includer:filename -->

eg 

<!-- includer:testy.php -->

the text <!-- includer:testy.php --> would then be replaced with the contents of the file.

You can of course use php and access your server variables and the like here so be careful as always.

== Installation ==
= New install =
1. Upload the folder includer to wp-content/plugin directory
2. Activate it
3. Use <!-- includer:testy.php --> tag to embed your includes in your posts


== Frequently Asked Questions ==

==Change log==
=1.0 (12/08/2008)= 

Initial release
