-- Database schema for groupsnearyou.com.
-- Needs to be run against a mysql database

CREATE TABLE `category` (
  `category_id` int(11) NOT NULL auto_increment
  `name` varchar(100) NOT NULL default ''
  `hint` varchar(255) default NULL
  `url_id` varchar(20) NOT NULL default ''
  PRIMARY KEY  (`category_id`)
);

CREATE TABLE `confirmation` (
  `confirmation_id` int(11) NOT NULL auto_increment,
  `parent_table` varchar(40) NOT NULL default '',
  `parent_id` int(11) NOT NULL default '0',
  `link_key` varchar(40) NOT NULL default '',
  `argument` varchar(50) default NULL
  PRIMARY KEY  (`confirmation_id`),
);

CREATE TABLE `contact_email` (
  `contact_email_id` int(11) NOT NULL auto_increment,
  `to_email` varchar(150) NOT NULL default '',
  `message` text NOT NULL,
  `subject` varchar(255) NOT NULL default '',
  `from_email` varchar(150) NOT NULL default '',
  `from_name` varchar(150) default NULL,
  PRIMARY KEY  (`contact_email_id`)
);

CREATE TABLE `country` (
  `iso` char(2) NOT NULL default '',
  `name` varchar(80) NOT NULL default '',
  `printable_name` varchar(80) NOT NULL default '',
  `iso3` char(3) default NULL,
  `numcode` smallint(6) default NULL,
  `disabled` tinyint(1) default '0',
  PRIMARY KEY  (`iso`)
);

CREATE TABLE `groups` (
  `group_id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '',
  `byline` text NOT NULL,
  `description` text,
  `category_id` int(11) default NULL
  `tags` text,
  `involved_type` varchar(50) NOT NULL default '',
  `involved_link` varchar(150) default NULL,
  `created_name` varchar(100) default NULL,
  `created_date` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `created_email` varchar(100) NOT NULL default '',
  `confirmed` tinyint(1) NOT NULL default '0',
  `long_bottom_left` float NOT NULL default '0',
  `lat_bottom_left` float NOT NULL default '0',
  `long_top_right` float NOT NULL default '0',
  `lat_top_right` float NOT NULL default '0',
  `zoom_level` int(11) NOT NULL default '0',
  `long_centroid` float NOT NULL default '0',
  `lat_centroid` float NOT NULL default '0',
  `location_desc` text,
  `url_id` varchar(150) NOT NULL default '',
  `involved_email` varchar(150) default NULL,
  PRIMARY KEY  (`group_id`),
  KEY `url` (`url_id`),
);

CREATE TABLE `stat` (
  `stat_key` varchar(100) NOT NULL default ''
  `stat_value` varchar(100) NOT NULL default ''
  `stat_id` int(11) NOT NULL auto_increment
  PRIMARY KEY  (`stat_id`)
);


CREATE TABLE `game_user` (
  `game_user_id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '',
  `email` varchar(150) NOT NULL default '',
  PRIMARY KEY  (`game_user_id`)
);

CREATE TABLE `game_group` (
  `game_group_id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '',
  `link` varchar(255) NOT NULL default '',
  `category` varchar(255) default NULL,
  `description` text,
  `notlocal` tinyint(1) default '0',
  `game_user_id` int(11) default NULL,
  `matched` tinyint(1) default '0',
  `guid` varchar(100) default NULL,
  `by_line` varchar(255) default NULL,
  PRIMARY KEY  (`game_group_id`)
);
