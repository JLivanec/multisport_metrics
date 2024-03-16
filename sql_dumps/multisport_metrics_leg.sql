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
INSERT INTO `leg` VALUES ('Azalea Sprint','2019-03-01','swim',300,0),('Azalea Sprint','2019-03-01','bike',12.4,0),('Azalea Sprint','2019-03-01','run',3.1,0),('Belews Lake Olympic','2020-04-01','swim',1500,1),('Belews Lake Olympic','2020-04-01','bike',24.83,0),('Belews Lake Olympic','2020-04-01','run',6.2,0),('Belews Lake Olympic','2021-04-01','swim',1500,1),('Belews Lake Olympic','2021-04-01','bike',24.8,0),('Belews Lake Olympic','2021-04-01','run',6.2,0),('Belews Lake Sprint','2020-04-01','swim',750,1),('Belews Lake Sprint','2020-04-01','bike',12.4,0),('Belews Lake Sprint','2020-04-01','run',3.1,0),('Belews Lake Sprint','2021-04-01','swim',750,1),('Belews Lake Sprint','2021-04-01','bike',12.4,0),('Belews Lake Sprint','2021-04-01','run',3.1,0),('Belews Lake Sprint','2023-05-27','swim',750,1),('Belews Lake Sprint','2023-05-27','bike',12.4,0),('Belews Lake Sprint','2023-05-27','run',3.1,0),('Blue Ridge Draft Legal','2023-10-14','swim',750,1),('Blue Ridge Draft Legal','2023-10-14','bike',12.4,0),('Blue Ridge Draft Legal','2023-10-14','run',3.1,0),('CLASH Daytona Half','2023-12-02','swim',2000,1),('CLASH Daytona Half','2023-12-02','bike',56.2,150),('CLASH Daytona Half','2023-12-02','run',13.1,50),('CLASH Daytona Sprint','2023-12-01','swim',750,1),('CLASH Daytona Sprint','2023-12-01','bike',12.4,50),('CLASH Daytona Sprint','2023-12-01','run',3.1,5),('Conferences - Draft Legal','2022-10-15','swim',750,1),('Conferences - Draft Legal','2022-10-15','bike',12.4,0),('Conferences - Draft Legal','2022-10-15','run',3.1,0),('Giant Acord Olympic','2018-03-01','swim',1500,1),('Giant Acord Olympic','2018-03-01','bike',24.8,0),('Giant Acord Olympic','2018-03-01','run',6.2,0),('Giant Acorn Olympic','2019-09-21','swim',1500,1),('Giant Acorn Olympic','2019-09-21','bike',24.8,0),('Giant Acorn Olympic','2019-09-21','run',6.2,0),('Giant Acorn Olympic','2021-09-25','swim',1500,1),('Giant Acorn Olympic','2021-09-25','bike',24.8,0),('Giant Acorn Olympic','2021-09-25','run',6.2,0),('Giant Acorn Olympic','2022-09-24','swim',1500,1),('Giant Acorn Olympic','2022-09-24','bike',24.8,0),('Giant Acorn Olympic','2022-09-24','run',6.2,0),('Giant Acorn Olympic','2023-09-23','swim',1500,1),('Giant Acorn Olympic','2023-09-23','bike',24.8,0),('Giant Acorn Olympic','2023-09-23','run',6.2,0),('Giant Acorn Sprint','2023-09-23','swim',750,1),('Giant Acorn Sprint','2023-09-23','bike',12.4,0),('Giant Acorn Sprint','2023-09-23','run',3.1,0),('Kinetic Cup Olympic','2019-10-19','swim',1500,1),('Kinetic Cup Olympic','2019-10-19','bike',24.8,0),('Kinetic Cup Olympic','2019-10-19','run',6.2,0),('Kinetic Cup Olympic','2021-10-16','swim',1500,1),('Kinetic Cup Olympic','2021-10-16','bike',24.8,0),('Kinetic Cup Olympic','2021-10-16','run',6.2,0),('Kinetic Cup Olympic','2022-10-15','swim',1500,1),('Kinetic Cup Olympic','2022-10-15','bike',24.8,0),('Kinetic Cup Olympic','2022-10-15','run',6.2,0),('Liberty Olympic','2019-03-01','swim',1500,1),('Liberty Olympic','2019-03-01','bike',24.8,0),('Liberty Olympic','2019-03-01','run',6.2,0),('Luray Olympic','2018-03-01','swim',1500,1),('Luray Olympic','2018-03-01','bike',24.8,0),('Luray Olympic','2018-03-01','run',6.2,0),('Luray Sprint','2018-03-01','swim',750,1),('Luray Sprint','2018-03-01','bike',12.4,0),('Luray Sprint','2018-03-01','run',3.1,0),('Nationals - Buford','2021-11-01','swim',750,1),('Nationals - Buford','2021-11-01','bike',24.8,0),('Nationals - Buford','2021-11-01','run',6.2,0),('Nationals - Buford GA','2023-06-01','swim',1500,1),('Nationals - Buford GA','2023-06-01','bike',24.8,0),('Nationals - Buford GA','2023-06-01','run',6.2,0),('Nationals - Tempe Olympic','2019-03-01','swim',150,1),('Nationals - Tempe Olympic','2019-03-01','bike',24.8,0),('Nationals - Tempe Olympic','2019-03-01','run',6.2,0),('Nationals Sprint - Buford GA','2023-06-01','swim',750,1),('Nationals Sprint - Buford GA','2023-06-01','bike',12.4,0),('Nationals Sprint - Buford GA','2023-06-01','run',3.1,0),('Patriots Half','2018-03-01','swim',1900,1),('Patriots Half','2018-03-01','bike',56,0),('Patriots Half','2018-03-01','run',13.1,0),('Patriots Half','2021-09-11','swim',1900,1),('Patriots Half','2021-09-11','bike',56,0),('Patriots Half','2021-09-11','run',13.1,0),('Patriots Half','2022-09-10','swim',1900,1),('Patriots Half','2022-09-10','bike',56,0),('Patriots Half','2022-09-10','run',13.1,0),('Patriots Half','2023-06-17','swim',1931,1),('Patriots Half','2023-06-17','bike',56.2,0),('Patriots Half','2023-06-17','run',13.1,0),('Patriots Olympic','2018-03-01','swim',1500,1),('Patriots Olympic','2018-03-01','bike',24.8,0),('Patriots Olympic','2018-03-01','run',6.2,0),('Patriots Olympic','2021-09-11','swim',1500,1),('Patriots Olympic','2021-09-11','bike',24.8,0),('Patriots Olympic','2021-09-11','run',6.2,0),('Patriots Olympic','2022-09-10','swim',1500,1),('Patriots Olympic','2022-09-10','bike',24.8,0),('Patriots Olympic','2022-09-10','run',6.2,0),('Patriots Olympic','2023-06-18','swim',1500,1),('Patriots Olympic','2023-06-18','bike',24.8,0),('Patriots Olympic','2023-06-18','run',6.2,0),('Patriots Sprint','2018-03-01','swim',750,1),('Patriots Sprint','2018-03-01','bike',12.4,0),('Patriots Sprint','2018-03-01','run',3.1,0),('Patriots Sprint','2019-09-07','swim',750,1),('Patriots Sprint','2019-09-07','bike',12.4,0),('Patriots Sprint','2019-09-07','run',3.1,0),('Patriots Sprint','2021-09-11','swim',750,1),('Patriots Sprint','2021-09-11','bike',12.4,0),('Patriots Sprint','2021-09-11','run',3.1,0),('Patriots Sprint','2022-09-10','swim',750,1),('Patriots Sprint','2022-09-10','bike',12.4,0),('Patriots Sprint','2022-09-10','run',3.1,0),('Patriots Sprint','2023-06-18','swim',750,1),('Patriots Sprint','2023-06-18','bike',12.4,0),('Patriots Sprint','2023-06-18','run',3.1,0),('Pleasants Landing','2023-10-07','swim',1500,1),('Pleasants Landing','2023-10-07','bike',24.8,0),('Pleasants Landing','2023-10-07','run',6.2,0),('Richmond Sprint','2019-03-01','swim',750,1),('Richmond Sprint','2019-03-01','bike',12.4,0),('Richmond Sprint','2019-03-01','run',3.1,0),('Smithfield Sprint','2023-05-03','swim',300,0),('Smithfield Sprint','2023-05-03','bike',12.4,0),('Smithfield Sprint','2023-05-03','run',3.1,0),('Tempe DL Sprint','2019-03-01','swim',750,1),('Tempe DL Sprint','2019-03-01','bike',12.4,0),('Tempe DL Sprint','2019-03-01','run',3.1,0),('Tri-at-the-Trump Sprint','2019-10-01','swim',750,1),('Tri-at-the-Trump Sprint','2019-10-01','bike',12.4,0),('Tri-at-the-Trump Sprint','2019-10-01','run',3.1,0);
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

-- Dump completed on 2024-03-15 22:52:40
