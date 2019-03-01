-- MySQL dump 10.16  Distrib 10.1.38-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ircon
-- ------------------------------------------------------
-- Server version	10.1.38-MariaDB-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `controller`
--

DROP TABLE IF EXISTS `controller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controller` (
  `controller_id` varchar(36) NOT NULL,
  `controller_name` varchar(255) NOT NULL,
  `controller_type_id` varchar(36) NOT NULL,
  PRIMARY KEY (`controller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controller`
--

LOCK TABLES `controller` WRITE;
/*!40000 ALTER TABLE `controller` DISABLE KEYS */;
/*!40000 ALTER TABLE `controller` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `controller_type`
--

DROP TABLE IF EXISTS `controller_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controller_type` (
  `controller_type_id` varchar(36) NOT NULL,
  `controller_type_name` varchar(255) NOT NULL,
  PRIMARY KEY (`controller_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controller_type`
--

LOCK TABLES `controller_type` WRITE;
/*!40000 ALTER TABLE `controller_type` DISABLE KEYS */;
INSERT INTO `controller_type` VALUES ('b1fe29e5-e5c2-11e8-9e76-30e37a141928','Bench'),('c82f849c-e5c2-11e8-9e76-30e37a141928','Boom'),('d3abd001-e5c2-11e8-9e76-30e37a141928','Echo');
/*!40000 ALTER TABLE `controller_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eq_curtain`
--

DROP TABLE IF EXISTS `eq_curtain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eq_curtain` (
  `curtain_id` varchar(36) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `short_name` varchar(64) DEFAULT NULL,
  `close_io_uri` varchar(255) DEFAULT NULL,
  `open_io_uri` varchar(255) DEFAULT NULL,
  `stroke_seconds` int(11) DEFAULT NULL,
  PRIMARY KEY (`curtain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eq_curtain`
--

LOCK TABLES `eq_curtain` WRITE;
/*!40000 ALTER TABLE `eq_curtain` DISABLE KEYS */;
INSERT INTO `eq_curtain` VALUES ('40aa5bc2-3bca-11e9-ae2a-0d3d0b7f5e59','Retail Shade Curtain','RETSHADE','gpio://5','gpio://6',280);
/*!40000 ALTER TABLE `eq_curtain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eq_heater`
--

DROP TABLE IF EXISTS `eq_heater`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eq_heater` (
  `heater_id` varchar(36) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `short_name` varchar(64) DEFAULT NULL,
  `on_io_uri` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`heater_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eq_heater`
--

LOCK TABLES `eq_heater` WRITE;
/*!40000 ALTER TABLE `eq_heater` DISABLE KEYS */;
INSERT INTO `eq_heater` VALUES ('bf6a1810-ea11-11e8-9e76-30e37a141928','Heat #1 (93% eff)','HEAT01','gpio://7'),('cbdc3e72-ea11-11e8-9e76-30e37a141928','Heat #2 (85% eff)','HEAT02','gpio://8');
/*!40000 ALTER TABLE `eq_heater` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eq_rh_sensor`
--

DROP TABLE IF EXISTS `eq_rh_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eq_rh_sensor` (
  `rh_sensor_id` varchar(36) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `short_name` varchar(64) DEFAULT NULL,
  `rh_sensor_io_uri` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`rh_sensor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eq_rh_sensor`
--

LOCK TABLES `eq_rh_sensor` WRITE;
/*!40000 ALTER TABLE `eq_rh_sensor` DISABLE KEYS */;
INSERT INTO `eq_rh_sensor` VALUES ('b19cbbff-ea15-11e8-9e76-30e37a141928','RH Zone 01','RH01','http://localhost:9900/humidity'),('b6e9b939-ea15-11e8-9e76-30e37a141928','RH Zone 02','RH02','http://localhost:9900/humidity');
/*!40000 ALTER TABLE `eq_rh_sensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eq_sun_sensor`
--

DROP TABLE IF EXISTS `eq_sun_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eq_sun_sensor` (
  `sun_id` varchar(36) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `short_name` varchar(64) DEFAULT NULL,
  `sun_io_uri` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`sun_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eq_sun_sensor`
--

LOCK TABLES `eq_sun_sensor` WRITE;
/*!40000 ALTER TABLE `eq_sun_sensor` DISABLE KEYS */;
INSERT INTO `eq_sun_sensor` VALUES ('840afb77-3bc8-11e9-ae2a-0d3d0b7f5e59','Outdoor Light Sensor','SUN','http://localhost:9900/sun');
/*!40000 ALTER TABLE `eq_sun_sensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eq_temp`
--

DROP TABLE IF EXISTS `eq_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eq_temp` (
  `temp_id` varchar(36) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `short_name` varchar(64) DEFAULT NULL,
  `temp_io_uri` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`temp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eq_temp`
--

LOCK TABLES `eq_temp` WRITE;
/*!40000 ALTER TABLE `eq_temp` DISABLE KEYS */;
INSERT INTO `eq_temp` VALUES ('97bc9d74-ea15-11e8-9e76-30e37a141928','Temp Zone 01','TEMP01','http://localhost:9900/temp'),('a01f1219-ea15-11e8-9e76-30e37a141928','Temp Zone 02','TEMP02','http://localhost:9900/temp');
/*!40000 ALTER TABLE `eq_temp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eq_vent`
--

DROP TABLE IF EXISTS `eq_vent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eq_vent` (
  `vent_id` varchar(36) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `short_name` varchar(64) DEFAULT NULL,
  `close_io_uri` varchar(255) DEFAULT NULL,
  `open_io_uri` varchar(255) DEFAULT NULL,
  `stroke_seconds` int(11) DEFAULT NULL,
  PRIMARY KEY (`vent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eq_vent`
--

LOCK TABLES `eq_vent` WRITE;
/*!40000 ALTER TABLE `eq_vent` DISABLE KEYS */;
INSERT INTO `eq_vent` VALUES ('1a45bedf-e969-11e8-9e76-30e37a141928','Production Roof 1-3','PRODROOF1','gpio://4','gpio://5',60),('e488fa06-e968-11e8-9e76-30e37a141928','Retail Roof','RETROOF','gpio://2','gpio://3',60);
/*!40000 ALTER TABLE `eq_vent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grower`
--

DROP TABLE IF EXISTS `grower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grower` (
  `grower_id` varchar(36) NOT NULL,
  `grower_name` varchar(255) NOT NULL,
  PRIMARY KEY (`grower_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grower`
--

LOCK TABLES `grower` WRITE;
/*!40000 ALTER TABLE `grower` DISABLE KEYS */;
/*!40000 ALTER TABLE `grower` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solenoid`
--

DROP TABLE IF EXISTS `solenoid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solenoid` (
  `solenoid_id` varchar(36) NOT NULL,
  `controller_id` varchar(36) NOT NULL,
  `solenoid_type_id` varchar(36) NOT NULL,
  `solenoid_name` varchar(255) DEFAULT NULL,
  `solenoid_addr` varchar(255) DEFAULT NULL,
  `gpm` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`solenoid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solenoid`
--

LOCK TABLES `solenoid` WRITE;
/*!40000 ALTER TABLE `solenoid` DISABLE KEYS */;
/*!40000 ALTER TABLE `solenoid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solenoid_type`
--

DROP TABLE IF EXISTS `solenoid_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solenoid_type` (
  `solenoid_type_id` varchar(36) NOT NULL,
  `solenoid_type_name` varchar(255) NOT NULL,
  PRIMARY KEY (`solenoid_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solenoid_type`
--

LOCK TABLES `solenoid_type` WRITE;
/*!40000 ALTER TABLE `solenoid_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `solenoid_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-28 21:47:34
