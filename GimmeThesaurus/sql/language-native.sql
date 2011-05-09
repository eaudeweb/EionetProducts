-- MySQL dump 10.13  Distrib 5.1.42, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: gemet2008
-- ------------------------------------------------------
-- Server version	5.1.42

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
-- Dumping data for table `language`
--

LOCK TABLES `language` WRITE;
/*!40000 ALTER TABLE `language` DISABLE KEYS */;
INSERT INTO `language` VALUES ('ar','عربي','utf8_general_ci','ARA','rtl');
INSERT INTO `language` VALUES ('bg','Български','utf8_general_ci','BUL','ltr');
INSERT INTO `language` VALUES ('cs','Čeština','utf8_czech_ci','CZE','ltr');
INSERT INTO `language` VALUES ('da','Dansk','utf8_danish_ci','DAN','ltr');
INSERT INTO `language` VALUES ('de','Deutsch','utf8_general_ci','GER','ltr');
INSERT INTO `language` VALUES ('el','Ελληνικά','utf8_general_ci','GRE','ltr');
INSERT INTO `language` VALUES ('en','English','utf8_general_ci','ENG','ltr');
INSERT INTO `language` VALUES ('en-US','English (US)','utf8_general_ci','USA','ltr');
INSERT INTO `language` VALUES ('es','Español','utf8_spanish_ci','SPA','ltr');
INSERT INTO `language` VALUES ('et','Eesti keel','utf8_estonian_ci','EST','ltr');
INSERT INTO `language` VALUES ('eu','Euskara','utf8_general_ci','BAQ','ltr');
INSERT INTO `language` VALUES ('fi','Suomi','utf8_general_ci','FIN','ltr');
INSERT INTO `language` VALUES ('fr','Français','utf8_general_ci','FRE','ltr');
INSERT INTO `language` VALUES ('ga','Ghaeilge','utf8_general_ci','GLE','ltr');
INSERT INTO `language` VALUES ('hu','Magyar','utf8_general_ci','HUN','ltr');
INSERT INTO `language` VALUES ('it','Italiano','utf8_general_ci','ITA','ltr');
INSERT INTO `language` VALUES ('lt','Lietuvių kalba','utf8_general_ci','LIT','ltr');
INSERT INTO `language` VALUES ('lv','Latviešu','utf8_general_ci','LAV','ltr');
INSERT INTO `language` VALUES ('mt','Malti','utf8_general_ci','MLT','ltr');
INSERT INTO `language` VALUES ('nl','Nederlands','utf8_general_ci','DUT','ltr');
INSERT INTO `language` VALUES ('no','Norsk','utf8_general_ci','NOR','ltr');
INSERT INTO `language` VALUES ('pl','Polski','utf8_polish_ci','POL','ltr');
INSERT INTO `language` VALUES ('pt','Português','utf8_general_ci','POR','ltr');
INSERT INTO `language` VALUES ('ro','Română','utf8_general_ci','RUM','ltr');
INSERT INTO `language` VALUES ('ru','Русский','utf8_general_ci','RUS','ltr');
INSERT INTO `language` VALUES ('sk','Slovenčina','utf8_general_ci','SLO','ltr');
INSERT INTO `language` VALUES ('sl','Slovenščina','utf8_slovenian_ci','SLV','ltr');
INSERT INTO `language` VALUES ('sv','Svenska','utf8_swedish_ci','SVE','ltr');
INSERT INTO `language` VALUES ('tr','Türkçe','utf8_general_ci','TUR','ltr');
/*!40000 ALTER TABLE `language` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-02-08 10:40:08
