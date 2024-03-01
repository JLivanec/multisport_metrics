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
-- Table structure for table `raceresults`
--

DROP TABLE IF EXISTS `raceresults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `raceresults` (
  `AthleteID` char(10) NOT NULL,
  `RaceName` varchar(30) NOT NULL,
  `RaceDate` date NOT NULL,
  `TimeTotal` varchar(10) DEFAULT NULL,
  `PlaceOA` varchar(2) DEFAULT NULL,
  `PlaceAG` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`AthleteID`,`RaceName`,`RaceDate`),
  KEY `fk_race_date_idx` (`RaceDate`),
  KEY `fk_raceinfo_rr_idx` (`RaceName`,`RaceDate`),
  CONSTRAINT `fk_athleteid_rr` FOREIGN KEY (`AthleteID`) REFERENCES `athlete` (`AthleteID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_raceinfo_rr` FOREIGN KEY (`RaceName`, `RaceDate`) REFERENCES `race` (`RaceName`, `RaceDate`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raceresults`
--

LOCK TABLES `raceresults` WRITE;
/*!40000 ALTER TABLE `raceresults` DISABLE KEYS */;
INSERT INTO `raceresults` VALUES ('2469716968','Patriots Half','2023-06-17','20615',NULL,'1'),('3261298872','Patriots Sprint','2023-06-18','4930',NULL,NULL),('3761084756','Patriots Sprint','2023-06-18','6133',NULL,NULL),('3937274148','Patriots Sprint','2023-06-18','5633',NULL,NULL),('5485772096','Patriots Sprint','2023-06-18','4859',NULL,NULL),('5713059843','CLASH Daytona Sprint','2023-12-01','4350',NULL,'5'),('5713059843','Patriots Sprint','2023-06-18','4311',NULL,NULL),('7239494167','CLASH Daytona Sprint','2023-12-01','3902',NULL,'1'),('7239494167','Patriots Olympic','2023-06-18','8270','3',NULL),('8559642249','CLASH Daytona Half','2023-12-02','21148',NULL,NULL),('8980209414','Patriots Olympic','2023-06-18','8770','2',NULL),('9146096775','Patriots Olympic','2023-06-18','10036',NULL,'1'),('9170718028','Patriots Sprint','2023-06-18','4312',NULL,NULL),('9523120725','CLASH Daytona Half','2023-12-02','20285',NULL,NULL),('9523120725','Patriots Half','2023-06-17','22767',NULL,'2'),('9740530843','Patriots Sprint','2023-06-18','4780',NULL,NULL);
/*!40000 ALTER TABLE `raceresults` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-29 20:29:00
