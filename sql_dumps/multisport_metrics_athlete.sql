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
-- Table structure for table `athlete`
--

DROP TABLE IF EXISTS `athlete`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `athlete` (
  `AthleteID` char(10) NOT NULL,
  `FirstName` varchar(20) DEFAULT NULL,
  `LastName` varchar(20) DEFAULT NULL,
  `GradYear` char(4) DEFAULT NULL,
  `Hometown` varchar(20) DEFAULT NULL,
  `Sex` enum('M','F','O') DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  PRIMARY KEY (`AthleteID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `athlete`
--

LOCK TABLES `athlete` WRITE;
/*!40000 ALTER TABLE `athlete` DISABLE KEYS */;
INSERT INTO `athlete` VALUES ('0294994685','Jack','Quinn','2027','Cape Elizabeth, ME','M',NULL),('2469716968','William','Salisbury','2026','Falls Church, VA','M',NULL),('2552176071','Julianne','Wood','2025','Westerly, RI','F',NULL),('2696104754','Tommy','Doubleday','2024','Park Ridge, IL','M',NULL),('3064803113','Trevor','Sorenson','2027','Burke, VA','M',NULL),('3261298872','Zachary','Kuhn','2027','Richmond, VA','M',NULL),('3453171754','Emma','Nylund','2027',NULL,'F',NULL),('3734421932','Brice','Biediger','2026',NULL,'M',NULL),('3761084756','Antoni','Reynolds','2025',NULL,'M',NULL),('3937274148','Chase','Stabolepszy','2025','Great Falls, VA','M',NULL),('4764654361','Spencer','McGehee','2025','Blacksburg, VA','M',NULL),('4968292801','Leo','Lombardi','2024','Richmond, VA','M',NULL),('5113544648','Yash','Sharma','2024','Woodbridge, NJ','M',NULL),('5485772096','Kennon','Downes','2025','Mechanicsville, VA','M',NULL),('5713059843','Matt','Stelmokas','2025','Belchertown, MA','M','2003-01-01'),('5774333930','Ann-Sidney','Ragsdale','2027','Richmond, VA','F',NULL),('5788073021','Hugh','Grennan','2026','Morristown, NJ','M',NULL),('6420791129','Spencer','Kearns','2026','Moneta, VA','M',NULL),('6443831339','Khadija','ElBouchti','2024','Lovettsville, VA','F',NULL),('6993059391','Drew','Conboy','2025','Williamsburg, VA','M',NULL),('7025345402','Evan','Donohoe','2026','McLean, VA','M',NULL),('7239494167','Jonathan \"Joota\"','Ravid','2025','Roswell, GA','M','2003-01-01'),('7663564361','Cameron','Menzies','2027','Roswell, GA','M',NULL),('8104140960','Sam','Northrup','2027','North Kingstown, RI','M',NULL),('8337824653','Andrew','Bickford','2025','McLean, VA','M',NULL),('8559642249','Jackson','Livanec','2024','Williamsburg, VA','M','1999-04-19'),('8980209414','Anna','Sullivan','2024','Vienna, VA','F',NULL),('9095138819','Cooper','Dereszynski','2027','Fayetteville, NY','M',NULL),('9146096775','Adaline','Bisese','2025','Buchanan, VA','F',NULL),('9170718028','Tamir','Zharmagambetov','2026','Almaty, Kazakhstan','M',NULL),('9307267646','Henry','Berger','2027',NULL,'M','2004-01-01'),('9523120725','Cason','TeVault','2024','Winston Salem, NC','M','2002-01-01'),('9740530843','Kelly','Smith','2026','Clemmons, NC','F',NULL),('9750397432','Kyle','Reeder','2027',NULL,'M',NULL);
/*!40000 ALTER TABLE `athlete` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-26 15:23:43
