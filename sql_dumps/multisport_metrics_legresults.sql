CREATE DATABASE  IF NOT EXISTS `multisport_metrics` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `multisport_metrics`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: multisport_metrics
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `legresults`
--

DROP TABLE IF EXISTS `legresults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `legresults` (
  `AthleteID` char(10) NOT NULL,
  `RaceName` varchar(30) NOT NULL,
  `RaceDate` date NOT NULL,
  `LegName` enum('swim','bike','run') NOT NULL,
  `Time` float unsigned DEFAULT '0',
  PRIMARY KEY (`AthleteID`,`RaceName`,`RaceDate`,`LegName`),
  KEY `fk_racename_lr_idx` (`RaceName`),
  KEY `fk_legname_lr_idx` (`LegName`),
  KEY `fk_leginfo_idx` (`RaceName`,`RaceDate`,`LegName`),
  CONSTRAINT `fk_leginfo` FOREIGN KEY (`RaceName`, `RaceDate`, `LegName`) REFERENCES `leg` (`RaceName`, `RaceDate`, `LegName`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `legresults`
--

LOCK TABLES `legresults` WRITE;
/*!40000 ALTER TABLE `legresults` DISABLE KEYS */;
INSERT INTO `legresults` VALUES ('2469716968','Patriots Half','2023-06-17','swim',2331),('2469716968','Patriots Half','2023-06-17','bike',11926),('2469716968','Patriots Half','2023-06-17','run',5996),('3261298872','Patriots Sprint','2023-06-18','swim',1279),('3261298872','Patriots Sprint','2023-06-18','bike',2161),('3261298872','Patriots Sprint','2023-06-18','run',1194),('3761084756','Patriots Sprint','2023-06-18','swim',1267),('3761084756','Patriots Sprint','2023-06-18','bike',2754),('3761084756','Patriots Sprint','2023-06-18','run',1804),('3937274148','Patriots Sprint','2023-06-18','swim',1525),('3937274148','Patriots Sprint','2023-06-18','bike',2403),('3937274148','Patriots Sprint','2023-06-18','run',1378),('5485772096','Patriots Sprint','2023-06-18','swim',804),('5485772096','Patriots Sprint','2023-06-18','bike',2429),('5485772096','Patriots Sprint','2023-06-18','run',1359),('5713059843','CLASH Daytona Sprint','2023-12-01','swim',674),('5713059843','CLASH Daytona Sprint','2023-12-01','bike',2129),('5713059843','CLASH Daytona Sprint','2023-12-01','run',1379),('5713059843','Patriots Sprint','2023-06-18','swim',744),('5713059843','Patriots Sprint','2023-06-18','bike',2213),('5713059843','Patriots Sprint','2023-06-18','run',1179),('7239494167','CLASH Daytona Sprint','2023-12-01','swim',701),('7239494167','CLASH Daytona Sprint','2023-12-01','bike',1825),('7239494167','CLASH Daytona Sprint','2023-12-01','run',1191),('7239494167','Patriots Olympic','2023-06-18','swim',1441),('7239494167','Patriots Olympic','2023-06-18','bike',4016),('7239494167','Patriots Olympic','2023-06-18','run',2615),('8980209414','Patriots Olympic','2023-06-18','swim',1448),('8980209414','Patriots Olympic','2023-06-18','bike',4079),('8980209414','Patriots Olympic','2023-06-18','run',3013),('9146096775','Patriots Olympic','2023-06-18','swim',1883),('9146096775','Patriots Olympic','2023-06-18','bike',4331),('9146096775','Patriots Olympic','2023-06-18','run',3555),('9170718028','Patriots Sprint','2023-06-18','swim',906),('9170718028','Patriots Sprint','2023-06-18','bike',2101),('9170718028','Patriots Sprint','2023-06-18','run',1132),('9523120725','CLASH Daytona Half','2023-12-02','swim',2020),('9523120725','CLASH Daytona Half','2023-12-02','bike',10622),('9523120725','CLASH Daytona Half','2023-12-02','run',7204),('9523120725','Patriots Half','2023-06-17','swim',2429),('9523120725','Patriots Half','2023-06-17','bike',11826),('9523120725','Patriots Half','2023-06-17','run',8145),('9740530843','Patriots Sprint','2023-06-18','swim',871),('9740530843','Patriots Sprint','2023-06-18','bike',2392),('9740530843','Patriots Sprint','2023-06-18','run',1262);
/*!40000 ALTER TABLE `legresults` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-02 16:58:35
