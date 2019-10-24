-- Authors: Jennifer Kim, Alexander Drath
-- CS340 Database Project Group 20
-- Gather Database Dump 

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `g_event_tag`;
DROP TABLE IF EXISTS `g_event_participant`;
DROP TABLE IF EXISTS `g_event_host`;
DROP TABLE IF EXISTS `g_group_member`;
DROP TABLE IF EXISTS `gather_tag`;
DROP TABLE IF EXISTS `gather_event`;
DROP TABLE IF EXISTS `gather_group`;
DROP TABLE IF EXISTS `gather_user`;


-- Table structure for table `gather_user`
CREATE TABLE `gather_user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Dumping data for table `gather_user`
--
LOCK TABLES `gather_user` WRITE;
INSERT INTO `gather_user` VALUES (1,'Jen', 'Kim'),(2,'Alex', 'Drath'),(3,'Demo', 'Demo');
UNLOCK TABLES;


-- Table structure for table `gather_group`
CREATE TABLE `gather_group` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(255) NOT NULL,
  PRIMARY KEY (`group_id`),
  UNIQUE KEY `group_name` (`group_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Dumping data for table `gather_group`
--
LOCK TABLES `gather_group` WRITE;
INSERT INTO `gather_group` VALUES (1,'SF Bay Area'),(2,'Soccer'),(3,'Algorithms');
UNLOCK TABLES;


-- Table structure for table `gather_tag`
CREATE TABLE `gather_tag` (
  `tag_name` varchar(50) NOT NULL,
  PRIMARY KEY (`tag_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Dumping data for table `gather_tag`
--
LOCK TABLES `gather_tag` WRITE;
INSERT INTO `gather_tag` VALUES ('sf'),('soccer'),('cs'), ('bay area'),('sports'),('coding');
UNLOCK TABLES;


-- Table structure for table `gather_event`
-- if group_id gets updated/deleted, the event also gets updated/deleted
CREATE TABLE `gather_event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `group_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_date` date DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `location` varchar(255) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  CONSTRAINT `gather_event_fk_gid` FOREIGN KEY (`group_id`) REFERENCES `gather_group` (`group_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Dumping data for table `gather_event`
--
LOCK TABLES `gather_event` WRITE;
INSERT INTO `gather_event` VALUES 
	(1, 'May Beginning Lindy Hop Lessons', 1, 
	'2019-05-09', '08:30:00', 
	'2019-05-09', '10:00:00', 
	'Union Square', 
	'Join us in May for our Lindy lessons!'),
	(2, 'Sunday Soccer at Willard Park', 2, 
	'2019-05-26', '16:00:00', 
	'2019-05-26', '18:00:00', 
	'Willard Park', 
	'Running three 7v7 or 8v8 soccer pickup matches at Willard Park. \n New persons attending pre-pay to Venmo upon signing up. Returners can pay cash at the event and/or pay Venmo.\n Please keep your status up to date to the last possible moment. This includes all waitlist players as well. No-Show policy is 24hrs prior to and will be associated with a $5 fee.'), 
	(3, 'Coffee and Algorithms', 3, 
	'2019-05-30', '13:00:00', 
	'2019-05-30', '15:00:00', 
	'Philz Coffee - Berkeley, CA', 
	'Join us for coffee and some algorithms!'),
	(4, 'Ramen Class', 1, 
	'2019-06-15', '19:00:00', 
	NULL, NULL, 
	'Sound & Savor', 
	'Come join us for our popular ramen making class.\n In this hands on class you will learn to make your own noodles, broth and toppings.\n We will make ramen noodles, a creamy shoyu broth and pickled sprouts, stir fried greens, braised enoki and more.'),
  (5, 'SF Glow Run', 1,
	'2019-05-01', '17:00:00',
	NULL, NULL,
	'Embarcadero',
	'Join us for 3rd annual SF Glow Run!');
UNLOCK TABLES;


-- Relationship Tables Set-up

-- Table structure for table `g_group_member`
CREATE TABLE `g_group_member` (
  `group_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  PRIMARY KEY (`group_id`, `member_id`),
  CONSTRAINT `g_group_member_fk_gid` FOREIGN KEY (`group_id`) 
  REFERENCES `gather_group` (`group_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `g_group_member_fk_mid` FOREIGN KEY (`member_id`) 
  REFERENCES `gather_user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Dumping data for table `g_group_member`
--
LOCK TABLES `g_group_member` WRITE;
INSERT INTO `g_group_member` VALUES (1,1),(1,3),(2,2),(3,3),(3,1),(3,2),(2,3);
UNLOCK TABLES;


-- Table structure for table `g_event_host`
CREATE TABLE `g_event_host` (
  `event_id` int(11) NOT NULL,
  `host_id` int(11) NOT NULL,
  PRIMARY KEY (`event_id`),
  CONSTRAINT `g_event_host_fk_eid` FOREIGN KEY (`event_id`) 
  REFERENCES `gather_event` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `g_event_host_fk_hid` FOREIGN KEY (`host_id`) 
  REFERENCES `gather_user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Dumping data for table `g_event_host`
--
LOCK TABLES `g_event_host` WRITE;
INSERT INTO `g_event_host` VALUES (1,1),(2,2),(3,3),(4,3),(5,1);
UNLOCK TABLES;


-- Table structure for table `g_event_participant`
CREATE TABLE `g_event_participant` (
  `event_id` int(11) NOT NULL,
  `participant_id` int(11) NOT NULL,
  PRIMARY KEY (`event_id`, `participant_id`),
  CONSTRAINT `g_event_participant_fk_eid` FOREIGN KEY (`event_id`) 
  REFERENCES `gather_event` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `g_event_participant_fk_pid` FOREIGN KEY (`participant_id`) 
  REFERENCES `gather_user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Dumping data for table `g_event_participant`
--
LOCK TABLES `g_event_participant` WRITE;
INSERT INTO `g_event_participant` VALUES (1,3),(4,1),(2,3),(3,1),(3,2),(4,3);
UNLOCK TABLES;


-- Table structure for table `g_event_tag`
CREATE TABLE `g_event_tag` (
  `event_id` int(11) NOT NULL,
  `tag_name` varchar(50) NOT NULL,
  PRIMARY KEY (`event_id`, `tag_name`),
  CONSTRAINT `g_event_tag_fk_eid` FOREIGN KEY (`event_id`) 
  REFERENCES `gather_event` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `g_event_tag_fk_tag` FOREIGN KEY (`tag_name`) 
  REFERENCES `gather_tag` (`tag_name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Dumping data for table `g_event_tag`
--
LOCK TABLES `g_event_tag` WRITE;
INSERT INTO `g_event_tag` VALUES (1,'sf'),(5,'sf'),(2,'soccer'),(3,'cs'), (1,'bay area'),(2,'sports'),(3,'coding'), (4,'bay area');
UNLOCK TABLES;

SET FOREIGN_KEY_CHECKS = 1;