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
-- Table structure for table `transitionresults`
--

DROP TABLE IF EXISTS `transitionresults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transitionresults` (
  `AthleteID` char(10) NOT NULL,
  `RaceName` varchar(30) NOT NULL,
  `RaceDate` date NOT NULL,
  `TName` enum('T1','T2') NOT NULL,
  `Time` float unsigned DEFAULT '0',
  PRIMARY KEY (`AthleteID`,`RaceName`,`RaceDate`,`TName`),
  KEY `rk_raceinfo_tr_idx` (`RaceName`,`RaceDate`),
  CONSTRAINT `rk_athleteid_tr` FOREIGN KEY (`AthleteID`) REFERENCES `athlete` (`AthleteID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `rk_raceinfo_tr` FOREIGN KEY (`RaceName`, `RaceDate`) REFERENCES `race` (`RaceName`, `RaceDate`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transitionresults`
--

LOCK TABLES `transitionresults` WRITE;
/*!40000 ALTER TABLE `transitionresults` DISABLE KEYS */;
INSERT INTO `transitionresults` VALUES ('2469716968','Patriots Half','2023-06-17','T1',288),('2469716968','Patriots Half','2023-06-17','T2',72),('3261298872','Patriots Sprint','2023-06-18','T1',172),('3261298872','Patriots Sprint','2023-06-18','T2',122),('3761084756','Patriots Sprint','2023-06-18','T1',253),('3761084756','Patriots Sprint','2023-06-18','T2',52),('3937274148','Patriots Sprint','2023-06-18','T1',224),('3937274148','Patriots Sprint','2023-06-18','T2',102),('5485772096','Patriots Sprint','2023-06-18','T1',185),('5485772096','Patriots Sprint','2023-06-18','T2',80),('5713059843','CLASH Daytona Sprint','2023-12-01','T1',86),('5713059843','CLASH Daytona Sprint','2023-12-01','T2',83),('5713059843','Patriots Sprint','2023-06-18','T1',125),('5713059843','Patriots Sprint','2023-06-18','T2',47),('7239494167','CLASH Daytona Sprint','2023-12-01','T1',105),('7239494167','CLASH Daytona Sprint','2023-12-01','T2',82),('7239494167','Patriots Olympic','2023-06-18','T1',144),('7239494167','Patriots Olympic','2023-06-18','T2',51),('8980209414','Patriots Olympic','2023-06-18','T1',152),('8980209414','Patriots Olympic','2023-06-18','T2',76),('9146096775','Patriots Olympic','2023-06-18','T1',177),('9146096775','Patriots Olympic','2023-06-18','T2',88),('9170718028','Patriots Sprint','2023-06-18','T1',121),('9170718028','Patriots Sprint','2023-06-18','T2',49),('9523120725','CLASH Daytona Half','2023-12-02','T1',203),('9523120725','CLASH Daytona Half','2023-12-02','T2',237),('9523120725','Patriots Half','2023-06-17','T1',232),('9523120725','Patriots Half','2023-06-17','T2',132),('9740530843','Patriots Sprint','2023-06-18','T1',163),('9740530843','Patriots Sprint','2023-06-18','T2',91);
/*!40000 ALTER TABLE `transitionresults` ENABLE KEYS */;
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
