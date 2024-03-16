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
-- Table structure for table `race`
--

DROP TABLE IF EXISTS `race`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `race` (
  `RaceName` varchar(30) NOT NULL,
  `City` varchar(20) DEFAULT NULL,
  `State` varchar(20) DEFAULT NULL,
  `Type` enum('sprint','olympic','half ironman','ironman','other') DEFAULT NULL,
  `RaceDate` date NOT NULL,
  PRIMARY KEY (`RaceName`,`RaceDate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `race`
--

LOCK TABLES `race` WRITE;
/*!40000 ALTER TABLE `race` DISABLE KEYS */;
INSERT INTO `race` VALUES ('Azalea Sprint','Wilmington','North Carolina','sprint','2019-03-01'),('Belews Lake Olympic','Stokesdale','North Carolina','olympic','2020-04-01'),('Belews Lake Olympic','Stokesdale','North Carolina','olympic','2021-04-01'),('Belews Lake Sprint','Stokesdale','North Carolina','sprint','2020-04-01'),('Belews Lake Sprint','Stokesdale','North Carolina','sprint','2021-04-01'),('Belews Lake Sprint','Stokesdale','North Carolina','sprint','2023-05-27'),('Blue Ridge Draft Legal','Huddleston','Virginia','sprint','2023-10-14'),('CLASH Daytona Half','Daytona','Florida','half ironman','2023-12-02'),('CLASH Daytona Sprint','Daytona','Florida','sprint','2023-12-01'),('Conferences - Draft Legal','Smith Mountain Lake','Virginia','sprint','2022-10-15'),('Giant Acord Olympic','unknown','Virginia','olympic','2018-03-01'),('Giant Acorn Olympic','Lake Anna','Virginia','olympic','2019-09-21'),('Giant Acorn Olympic','Lake Anna','Virginia','olympic','2021-09-25'),('Giant Acorn Olympic','Lake Anna','Virginia','olympic','2022-09-24'),('Giant Acorn Olympic','Lake Anna','Virginia','olympic','2023-09-23'),('Giant Acorn Sprint','Lake Anna','Virginia','sprint','2023-09-23'),('Kinetic Cup Olympic','Smith Mountain Lake','Virginia','olympic','2019-10-19'),('Kinetic Cup Olympic','Smith Mountain Lake','Virginia','olympic','2021-10-16'),('Kinetic Cup Olympic','Smith Mountain Lake','Virginia','olympic','2022-10-15'),('Liberty Olympic','Lynchburg','Virginia','olympic','2019-03-01'),('Luray Olympic','Luray','Virginia','olympic','2018-03-01'),('Luray Sprint','Luray','Virginia','sprint','2018-03-01'),('Nationals - Buford','Buford','Virginia','olympic','2021-11-01'),('Nationals - Buford GA','Buford','Georgia','olympic','2023-06-01'),('Nationals - Tempe Olympic','Tempe','Arizona','olympic','2019-03-01'),('Nationals Sprint - Buford GA','Buford','Georgia','sprint','2023-06-01'),('Patriots Half','unknown','Virginia','half ironman','2018-03-01'),('Patriots Half','Williamsburg','Virginia','half ironman','2021-09-11'),('Patriots Half','Williamsburg','Virginia','half ironman','2022-09-10'),('Patriots Half','Williamsburg','Virginia','half ironman','2023-06-17'),('Patriots Olympic','unknown','Virginia','olympic','2018-03-01'),('Patriots Olympic','Williamsburg','Virginia','olympic','2021-09-11'),('Patriots Olympic','Williamsburg','Virginia','half ironman','2022-09-10'),('Patriots Olympic','Williamsburg','Virginia','olympic','2023-06-18'),('Patriots Sprint','unknown','Virginia','sprint','2018-03-01'),('Patriots Sprint','Williamsburg','Virginia','sprint','2019-09-07'),('Patriots Sprint','Williamsburg','Virginia','sprint','2021-09-11'),('Patriots Sprint','Williamsburg','Virginia','half ironman','2022-09-10'),('Patriots Sprint','Williamsburg','Virginia','sprint','2023-06-18'),('Pleasants Landing','Bumpass','Virginia','olympic','2023-10-07'),('Richmond Sprint','Richmond','Virginia','sprint','2019-03-01'),('Smithfield Sprint','Smithfield','Virginia','sprint','2023-05-03'),('Tempe DL Sprint','Tempe','Arizona','sprint','2019-03-01'),('Tri-at-the-Trump Sprint','Mooresville','North Carolina','sprint','2019-10-01');
/*!40000 ALTER TABLE `race` ENABLE KEYS */;
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
