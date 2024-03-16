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
  `GradYear` int DEFAULT NULL,
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
INSERT INTO `athlete` VALUES ('0201768553','Kenny','Culbertson',NULL,NULL,'M',NULL),('0249763617','Calvin','Graves',NULL,NULL,'M',NULL),('0294994685','Jack','Quinn',2027,'Cape Elizabeth, ME','M',NULL),('0388662324','Samuel','Umidi',NULL,NULL,'M',NULL),('0599744246','Payton','Harrigal',NULL,NULL,'F',NULL),('0667937186','Ryan','Schurr',NULL,NULL,'M',NULL),('0972572374','Pat','Hanlon',NULL,NULL,'M',NULL),('1448635233','Eddie','Williams',NULL,NULL,'M',NULL),('1545455861','Brogan','Dineen',NULL,NULL,'M',NULL),('1611430793','Mike','Ackerman',NULL,NULL,'M',NULL),('2006769864','Tim','Pote',NULL,NULL,'M',NULL),('2066802910','Andrew','Douglas',NULL,NULL,'M',NULL),('2114625963','Paul','Atwood',NULL,NULL,'M',NULL),('2116602935','Johnathan','Sullivan',NULL,NULL,'M',NULL),('2469716968','William','Salisbury',2026,'Falls Church, VA','M',NULL),('2552176071','Julianne','Wood',2025,'Westerly, RI','F',NULL),('2570921522','Lydia','Fox',NULL,NULL,'F',NULL),('2580865796','Laura','Sullivan',NULL,NULL,'F',NULL),('2696104754','Tommy','Doubleday',2024,'Park Ridge, IL','M',NULL),('2711430262','Ben','Stadler',NULL,NULL,'M',NULL),('2775864644','Garrett','Kemmerly',NULL,NULL,'M',NULL),('3064803113','Trevor','Sorenson',2027,'Burke, VA','M',NULL),('3167832723','Quinten','Prieur',NULL,NULL,'M',NULL),('3261298872','Zachary','Kuhn',2027,'Richmond, VA','M',NULL),('3335343328','Catie','George',NULL,NULL,'F',NULL),('3353743306','Amelia','Gay',NULL,NULL,'F',NULL),('3453171754','Emma','Nylund',2027,NULL,'F',NULL),('3608739027','Maddy','McNiff',NULL,NULL,'F',NULL),('3734421932','Brice','Biediger',2026,NULL,'M',NULL),('3761084756','Antoni','Reynolds',2025,NULL,'M',NULL),('3937274148','Chase','Stabolepszy',2025,'Great Falls, VA','M',NULL),('4401287254','Tom','Serra',NULL,NULL,'M',NULL),('464538977','Jackson','Livanec',2024,'Williamsburg, VA','M',NULL),('4764654361','Spencer','McGehee',2025,'Blacksburg, VA','M',NULL),('4922385494','Julia','Placide',NULL,NULL,'F',NULL),('4968292801','Leo','Lombardi',2024,'Richmond, VA','M',NULL),('5113544648','Yash','Sharma',2024,'Woodbridge, NJ','M',NULL),('5119278768','Jaedyn','Williams',NULL,NULL,'M',NULL),('5313622719','Craig','Hamilton',NULL,NULL,'M',NULL),('5485772096','Kennon','Downes',2025,'Mechanicsville, VA','M',NULL),('5599555021','Phillip','Sullivan',NULL,NULL,'M',NULL),('5698812619','Emerson','Heaton',NULL,NULL,'M',NULL),('5702903750','Destin','Rodgers',NULL,NULL,'M',NULL),('5713059843','Matt','Stelmokas',2025,'Belchertown, MA','M','2003-01-01'),('5774333930','Ann-Sidney','Ragsdale',2027,'Richmond, VA','F',NULL),('5788073021','Hugh','Grennan',2026,'Morristown, NJ','M',NULL),('5836497424','Reilly','Krason',NULL,NULL,'F',NULL),('6420791129','Spencer','Kearns',2026,'Moneta, VA','M',NULL),('6443831339','Khadija','ElBouchti',2024,'Lovettsville, VA','F',NULL),('6508991546','Katy','Lobeda',NULL,NULL,'F',NULL),('6874599561','Andrew','Chen',NULL,NULL,'M',NULL),('6883275876','Matt','Padgett',NULL,NULL,'M',NULL),('6927596133','William','Cabell',NULL,NULL,'M',NULL),('6993059391','Drew','Conboy',2025,'Williamsburg, VA','M',NULL),('7025345402','Evan','Donohoe',2026,'McLean, VA','M',NULL),('7119825992','Christian','White',NULL,NULL,'M',NULL),('7239494167','Jonathan \"Joota\"','Ravid',2025,'Roswell, GA','M','2003-01-01'),('7661183485','Patrick','Hedger',NULL,NULL,'M',NULL),('7663564361','Cameron','Menzies',2027,'Roswell, GA','M',NULL),('7720063701','Isaac','Lerner',NULL,NULL,'M',NULL),('7726157074','Thomas','Davis',NULL,NULL,'M',NULL),('7731450680','Jennifer','Fleming',NULL,NULL,'F',NULL),('7820315500','Joey','Rodgers',NULL,NULL,'M',NULL),('8005234325','Ladson','Walls',NULL,NULL,'M',NULL),('8104140960','Sam','Northrup',2027,'North Kingstown, RI','M',NULL),('8123611192','Katrina','Lytle',NULL,NULL,'F',NULL),('8132729710','Kyle','Brown',NULL,NULL,'M',NULL),('8214033320','Samantha','McKinnon',NULL,NULL,'F',NULL),('8292746489','Nicholas','Gardella',NULL,NULL,'M',NULL),('8337824653','Andrew','Bickford',2025,'McLean, VA','M',NULL),('8620488679','Aonghus','McGuinness',NULL,NULL,'M',NULL),('8980209414','Anna','Sullivan',2024,'Vienna, VA','F',NULL),('8990326044','Hunter','McClelland',NULL,NULL,'M',NULL),('9095138819','Cooper','Dereszynski',2027,'Fayetteville, NY','M',NULL),('9146096775','Adaline','Bisese',2025,'Buchanan, VA','F',NULL),('9170718028','Tamir','Zharmagambetov',2026,'Almaty, Kazakhstan','M',NULL),('9201241845','Dave','Kaul',NULL,NULL,'M',NULL),('9307267646','Henry','Berger',2027,NULL,'M','2004-01-01'),('9364974840','Yanlin','Du',NULL,NULL,'M',NULL),('9523120725','Cason','TeVault',2024,'Winston Salem, NC','M','2002-01-01'),('9610978013','Bobby','Lytle',NULL,NULL,'M',NULL),('9671390081','Ray','Rady',NULL,NULL,'M',NULL),('9740530843','Kelly','Smith',2026,'Clemmons, NC','F',NULL),('9750397432','Kyle','Reeder',2027,NULL,'M',NULL);
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

-- Dump completed on 2024-03-15 22:52:40
