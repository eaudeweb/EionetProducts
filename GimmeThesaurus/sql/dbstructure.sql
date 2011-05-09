-- MySQL dump 10.13  Distrib 5.1.36, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: gemet2008
-- ------------------------------------------------------
-- Server version	5.1.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `concept`
--

DROP TABLE IF EXISTS `concept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `concept` (
  `ns` int(11) NOT NULL DEFAULT '0',
  `id_concept` int(11) NOT NULL DEFAULT '0',
  `id_status` char(1) NOT NULL DEFAULT '',
  `datent` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `datchg` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ns`,`id_concept`),
  KEY `id_status` (`id_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `definition_sources`
--

DROP TABLE IF EXISTS `definition_sources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `definition_sources` (
  `abbr` varchar(10) NOT NULL DEFAULT '',
  `author` varchar(255) DEFAULT '',
  `title` varchar(255) DEFAULT '',
  `url` varchar(255) DEFAULT '',
  `publication` varchar(255) DEFAULT '',
  `place` varchar(255) DEFAULT '',
  `year` varchar(10) DEFAULT '',
  PRIMARY KEY (`abbr`),
  KEY `author` (`author`),
  KEY `title` (`title`),
  KEY `url` (`url`),
  KEY `publication` (`publication`),
  KEY `place` (`place`),
  KEY `year` (`year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Contains definition sources';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `foreign_relation`
--

DROP TABLE IF EXISTS `foreign_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `foreign_relation` (
  `id_concept` int(11) NOT NULL DEFAULT '0',
  `source_ns` int(11) NOT NULL DEFAULT '0',
  `relation_uri` varchar(255) NOT NULL,
  `id_type` varchar(40) NOT NULL,
  `show_in_html` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_concept`,`source_ns`,`relation_uri`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Outgoing links';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `language`
--

DROP TABLE IF EXISTS `language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `language` (
  `langcode` varchar(10) NOT NULL DEFAULT '',
  `language` varchar(255) DEFAULT NULL,
  `charset` varchar(100) DEFAULT NULL,
  `alt_langcode` varchar(3) DEFAULT NULL,
  `direction` varchar(3) DEFAULT 'ltr',
  PRIMARY KEY (`langcode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Dictionary table for languages';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `namespace`
--

DROP TABLE IF EXISTS `namespace`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `namespace` (
  `id_ns` int(11) NOT NULL DEFAULT '0',
  `ns_url` varchar(255) NOT NULL DEFAULT '',
  `heading` varchar(255) NOT NULL,
  `version` varchar(255) NOT NULL,
  PRIMARY KEY (`id_ns`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `property`
--

DROP TABLE IF EXISTS `property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `property` (
  `ns` int(11) NOT NULL DEFAULT '0',
  `id_concept` int(11) NOT NULL DEFAULT '0',
  `langcode` varchar(10) NOT NULL DEFAULT '',
  `name` varchar(50) NOT NULL DEFAULT '',
  `value` text,
  `is_resource` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ns`,`id_concept`,`langcode`,`name`),
  KEY `code` (`langcode`),
  KEY `id_concept` (`id_concept`),
  KEY `name_langcode_value` (`name`,`langcode`,`value`(1)) USING BTREE,
  KEY `name_langcode_ns` (`name`,`langcode`,`ns`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Holds properties for concepts';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `property_history`
--

DROP TABLE IF EXISTS `property_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `property_history` (
  `id_property_history` int(11) NOT NULL AUTO_INCREMENT,
  `ns` int(11) NOT NULL DEFAULT '0',
  `id_concept` int(11) NOT NULL DEFAULT '0',
  `langcode` varchar(10) DEFAULT NULL,
  `name` varchar(50) NOT NULL DEFAULT '',
  `value` text,
  `author` text,
  `id_status` char(1) NOT NULL DEFAULT '',
  `datchg` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id_property_history`),
  UNIQUE KEY `id` (`id_property_history`),
  KEY `langcode` (`langcode`),
  KEY `id_status` (`id_status`),
  KEY `ns` (`ns`,`id_concept`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Holds history of concept properties';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `property_type`
--

DROP TABLE IF EXISTS `property_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `property_type` (
  `id_type` varchar(40) NOT NULL,
  `label` varchar(100) DEFAULT NULL,
  `uri` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_type`),
  UNIQUE KEY `uri` (`uri`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `relation`
--

DROP TABLE IF EXISTS `relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relation` (
  `source_ns` int(11) NOT NULL DEFAULT '0',
  `id_concept` int(11) NOT NULL DEFAULT '0',
  `target_ns` int(11) NOT NULL DEFAULT '0',
  `id_relation` int(11) NOT NULL DEFAULT '0',
  `id_type` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`source_ns`,`id_concept`,`target_ns`,`id_relation`),
  KEY `id_type` (`id_type`),
  KEY `source_ns` (`source_ns`,`id_concept`),
  KEY `target_ns` (`target_ns`,`id_relation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Defines relations among the concepts: narrower, broader and ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `source`
--

DROP TABLE IF EXISTS `source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `source` (
  `id_source` int(11) NOT NULL AUTO_INCREMENT,
  `ns` int(11) NOT NULL DEFAULT '0',
  `id_concept` int(11) NOT NULL DEFAULT '0',
  `description` text,
  PRIMARY KEY (`id_source`),
  KEY `ns` (`ns`,`id_concept`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `id_status` char(1) NOT NULL DEFAULT '',
  `description` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Dictionary table for concepts statuses: new, changed, delete';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2009-07-23 20:17:52
