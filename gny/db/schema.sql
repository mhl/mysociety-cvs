/* 

	database schema for groupsnearyou.com. Needs to be run against a mysql database

*/


DROP TABLE IF EXISTS `confirmation`;
CREATE TABLE  `confirmation` (
  `confirmation_id` int(11) NOT NULL auto_increment,
  `parent_table` varchar(40) NOT NULL,
  `parent_id` int(11) NOT NULL,
  `link_key` varchar(40) NOT NULL,
  PRIMARY KEY  (`confirmation_id`),
  UNIQUE KEY (`link_key`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `contact_email`;
CREATE TABLE  `contact_email` (
  `contact_email_id` int(11) NOT NULL auto_increment,
  `to_email` varchar(150) NOT NULL,
  `message` text NOT NULL,
  `subject` varchar(255) NOT NULL,
  `from_email` varchar(150) NOT NULL,
  `from_name` varchar(150) default NULL,
  PRIMARY KEY  (`contact_email_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `country`;
CREATE TABLE  `country` (
  `iso` char(2) NOT NULL,
  `name` varchar(80) NOT NULL,
  `printable_name` varchar(80) NOT NULL,
  `iso3` char(3) default NULL,
  `numcode` smallint(6) default NULL,
  `disabled` tinyint(1) default '0',
  PRIMARY KEY  (`iso`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `group_id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL,
  `byline` text NOT NULL,
  `description` text NOT NULL,
  `tags` text,
  `involved_type` varchar(50) NOT NULL,
  `involved_link` varchar(150) default NULL,
  `created_name` varchar(100) NOT NULL,
  `created_date` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `created_email` varchar(100) NOT NULL,
  `confirmed` tinyint(1) NOT NULL default '0',
  `long_bottom_left` float NOT NULL,
  `lat_bottom_left` float NOT NULL,
  `long_top_right` float NOT NULL,
  `lat_top_right` float NOT NULL,
  `zoom_level` int(11) NOT NULL,
  `long_centroid` float NOT NULL,
  `lat_centroid` float NOT NULL,
  `location_desc` text default '' NOT NULL,
  `url_id` varchar(150) NOT NULL,
  `involved_email` varchar(150) default NULL,
  PRIMARY KEY  (`group_id`),
  UNIQUE KEY `url` (`url_id`),
  KEY (`confirmed`,`long_bottom_left`, `lat_bottom_left`, `long_top_right`, `lat_top_right`)
) ENGINE=MyISAM AUTO_INCREMENT=123 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `stat`;
CREATE TABLE  `stat` (
  `stat_key` varchar(100) NOT NULL,
  `stat_value` varchar(100) NOT NULL,
  `stat_id` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`stat_id`),
  UNIQUE KEY (`stat_key`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
