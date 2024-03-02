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
-- Table structure for table `leg`
--

DROP TABLE IF EXISTS `leg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leg` (
  `RaceName` varchar(30) NOT NULL,
  `RaceDate` date NOT NULL,
  `LegName` enum('swim','bike','run') NOT NULL,
  `Distance` float unsigned DEFAULT '0',
  `Elevation` float unsigned DEFAULT '0',
  PRIMARY KEY (`RaceName`,`RaceDate`,`LegName`),
  KEY `fk_racedate_leg_idx` (`RaceDate`),
  CONSTRAINT `fk_raceinfo` FOREIGN KEY (`RaceName`, `RaceDate`) REFERENCES `race` (`RaceName`, `RaceDate`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leg`
--

LOCK TABLES `leg` WRITE;
/*!40000 ALTER TABLE `leg` DISABLE KEYS */;
INSERT INTO `leg` VALUES ('Blue Ridge Draft Legal','2023-10-14','swim',750,1),('Blue Ridge Draft Legal','2023-10-14','bike',12.4,0),('Blue Ridge Draft Legal','2023-10-14','run',3.1,0),('CLASH Daytona Half','2023-12-02','swim',2000,1),('CLASH Daytona Half','2023-12-02','bike',56.2,150),('CLASH Daytona Half','2023-12-02','run',13.1,50),('CLASH Daytona Sprint','2023-12-01','swim',750,1),('CLASH Daytona Sprint','2023-12-01','bike',12.4,50),('CLASH Daytona Sprint','2023-12-01','run',3.1,5),('Giant Acorn Olympic','2023-09-23','swim',1500,1),('Giant Acorn Olympic','2023-09-23','bike',24.8,0),('Giant Acorn Olympic','2023-09-23','run',6.2,0),('Patriots Half','2023-06-17','swim',1931,1),('Patriots Half','2023-06-17','bike',56.2,0),('Patriots Half','2023-06-17','run',13.1,0),('Patriots Olympic','2023-06-18','swim',1500,1),('Patriots Olympic','2023-06-18','bike',24.8,0),('Patriots Olympic','2023-06-18','run',6.2,0),('Patriots Sprint','2023-06-18','swim',750,1),('Patriots Sprint','2023-06-18','bike',12.4,0),('Patriots Sprint','2023-06-18','run',3.1,0),('Pleasants Landing','2023-10-07','swim',1500,1),('Pleasants Landing','2023-10-07','bike',24.8,0),('Pleasants Landing','2023-10-07','run',6.2,0);
/*!40000 ALTER TABLE `leg` ENABLE KEYS */;
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
