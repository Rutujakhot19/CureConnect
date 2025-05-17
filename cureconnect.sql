-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: doctors_db
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `apt_date` date NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `is_complete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (8,1,13,'2025-05-08','123 Demo St, Sample City','Test User A',1),(9,2,13,'2025-05-09','123 Demo St, Sample City','Test User B',1),(10,2,13,'2025-05-09','123 Demo St, Sample City','Test User B',1),(11,2,13,'2025-05-09','456 Example Rd, Exampletown','Test User C',0);
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bed_availability`
--

DROP TABLE IF EXISTS `bed_availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bed_availability` (
  `availability_id` int NOT NULL AUTO_INCREMENT,
  `hospital_id` int NOT NULL,
  `available_general_beds` int NOT NULL DEFAULT '0',
  `available_icu_beds` int NOT NULL DEFAULT '0',
  `available_private_rooms` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`availability_id`),
  KEY `hospital_id` (`hospital_id`),
  CONSTRAINT `bed_availability_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals_bed` (`hospital_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bed_availability`
--

LOCK TABLES `bed_availability` WRITE;
/*!40000 ALTER TABLE `bed_availability` DISABLE KEYS */;
INSERT INTO `bed_availability` VALUES (1,1,20,10,5),(2,2,15,8,6),(3,3,25,12,8),(4,4,30,15,10),(5,5,40,20,15),(6,6,35,18,12),(7,7,50,25,20),(8,8,45,22,18);
/*!40000 ALTER TABLE `bed_availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blood_bank`
--

DROP TABLE IF EXISTS `blood_bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_bank` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `timing` varchar(50) NOT NULL,
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood_bank`
--

LOCK TABLES `blood_bank` WRITE;
/*!40000 ALTER TABLE `blood_bank` DISABLE KEYS */;
INSERT INTO `blood_bank` VALUES (1,'Sangli Blood Bank','Sangli City','2225558888','9 AM - 6 PM',16.85240000,74.58150000),(2,'Miraj Blood Bank','Miraj','8899556644','8 AM - 5 PM',16.83380000,74.64100000),(3,'Kupwad Blood Bank','Kupwad MIDC','899999999','10 AM - 7 PM',16.83710000,74.61440000),(4,'Sahyadri Blood Bank','62/1, 1st Floor, Near Shivajinagar Bus Depot, Shivaji Nagar, Pune, Maharashtra, India','020-25457368','9:00 AM - 6:00 PM',18.52040000,73.85670000),(5,'Poona Blood Bank','2nd Floor, Near OPP. Nehru Stadium, Camp, Pune, Maharashtra, India','020-26139600','8:00 AM - 5:00 PM',18.51060000,73.86330000),(6,'KEM Hospital Blood Bank','1, Rasta Peth, Pune, Maharashtra, India','020-26353344','10:00 AM - 7:00 PM',18.52160000,73.86820000),(7,'Bharati Hospital Blood Bank','Bharati Vidyapeeth University, Pune-Satara Road, Pune, Maharashtra, India','020-24370151','9:00 AM - 5:00 PM',18.46720000,73.85290000),(8,'Ruby Hall Clinic Blood Bank','40, Sassoon Road, Pune, Maharashtra, India','020-26116020','24/7',18.52360000,73.85350000);
/*!40000 ALTER TABLE `blood_bank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blood_inventory`
--

DROP TABLE IF EXISTS `blood_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_inventory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `blood_bank_id` int NOT NULL,
  `blood_group` varchar(5) NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `blood_bank_id` (`blood_bank_id`),
  CONSTRAINT `blood_inventory_ibfk_1` FOREIGN KEY (`blood_bank_id`) REFERENCES `blood_bank` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood_inventory`
--

LOCK TABLES `blood_inventory` WRITE;
/*!40000 ALTER TABLE `blood_inventory` DISABLE KEYS */;
INSERT INTO `blood_inventory` VALUES (1,1,'A+',10),(2,1,'O+',5),(3,2,'B-',8),(4,2,'AB+',4),(5,3,'O-',12),(6,3,'A-',7),(7,1,'A+',15),(8,1,'B+',10),(9,1,'O+',8),(10,1,'AB+',5),(11,2,'A-',5),(12,2,'B-',7),(13,2,'O-',12),(14,2,'AB-',4),(15,3,'A+',20),(16,3,'B+',25),(17,3,'O+',15),(18,3,'AB+',10),(19,4,'A+',12),(20,4,'B+',10),(21,4,'O+',8),(22,4,'AB+',5),(23,5,'A+',10),(24,5,'B+',20),(25,5,'O+',18),(26,5,'AB+',12);
/*!40000 ALTER TABLE `blood_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bloodbank_users`
--

DROP TABLE IF EXISTS `bloodbank_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bloodbank_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `dob` date NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bloodbank_users`
--

LOCK TABLES `bloodbank_users` WRITE;
/*!40000 ALTER TABLE `bloodbank_users` DISABLE KEYS */;
INSERT INTO `bloodbank_users` VALUES (1,'abc','abc@gemail.com','abc','1236547890','2002-05-06','oms',NULL);
/*!40000 ALTER TABLE `bloodbank_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor_login`
--

DROP TABLE IF EXISTS `doctor_login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor_login` (
  `doctor_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`doctor_id`),
  CONSTRAINT `doctor_login_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors_table` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_login`
--

LOCK TABLES `doctor_login` WRITE;
/*!40000 ALTER TABLE `doctor_login` DISABLE KEYS */;
INSERT INTO `doctor_login` VALUES (13,'Dr. Neha Joshi','admin123','admin123');
/*!40000 ALTER TABLE `doctor_login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `contact` varchar(15) DEFAULT NULL,
  `bio` text,
  `rating` float DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (1,'Dr. John Doe','Cardiologist','1234567890','Expert in heart diseases.',4.5),(2,'Dr. Jane Smith','Pediatrician','2254578952','Specializes in children\'s health.',3.8),(3,'Dr. Emily Davis','Dermatologist','1122334455','Skin care and treatment specialist.',4),(4,'Dr. Michael Brown','Orthopedic','2233445566','Expert in bone and joint disorders.',4.7),(5,'Dr. Sarah Wilson','Neurologist','3344556677','Specializes in brain and nervous system.',4.2);
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors_table`
--

DROP TABLE IF EXISTS `doctors_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `specialization` varchar(255) NOT NULL,
  `rating` decimal(2,1) NOT NULL,
  `hospital_id` int DEFAULT NULL,
  `appointment_count` int DEFAULT '0',
  `appointment_price` decimal(10,2) DEFAULT NULL,
  `upi_id` varchar(255) DEFAULT NULL,
  `current_count` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `hospital_id` (`hospital_id`),
  CONSTRAINT `doctors_table_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors_table`
--

LOCK TABLES `doctors_table` WRITE;
/*!40000 ALTER TABLE `doctors_table` DISABLE KEYS */;
INSERT INTO `doctors_table` VALUES (1,'Dr. John Doe','Cardiologist',4.5,1,0,100.00,'demo@upi',0),(2,'Dr. Jane Smith','Dermatologist',4.0,1,0,100.00,'demo@upi',0),(3,'Dr. Emily Jones','Pediatrician',4.2,1,0,100.00,'demo@upi',0),(4,'Dr. John Gal','Cardiologist',4.5,2,1,100.00,'demo@upi',0),(5,'Dr. Janny Smith','Dermatologist',4.0,2,0,100.00,'demo@upi',0),(6,'Dr. Essa Jones','Pediatrician',4.2,2,0,100.00,'demo@upi',0),(7,'Dr. Anil Deshmukh','Cardiologist',4.8,3,0,100.00,'demo@upi',0),(8,'Dr. Priya Patil','Dermatologist',4.6,3,0,100.00,'demo@upi',0),(9,'Dr. Sanjay Kulkarni','Pediatrician',4.5,3,0,100.00,'demo@upi',0),(10,'Dr. Anil Deshmukh','Cardiologist',4.8,3,0,100.00,'demo@upi',0),(11,'Dr. Priya Patil','Dermatologist',4.6,3,0,100.00,'demo@upi',0),(12,'Dr. Sanjay Kulkarni','Pediatrician',4.5,3,0,100.00,'demo@upi',0),(13,'Dr. Neha Joshi','General Surgeon',4.7,4,3,100.00,'demo@upi',0),(14,'Dr. Rahul More','Orthopedic',4.6,4,0,100.00,'demo@upi',0),(15,'Dr. Sheetal Patil','Gynecologist',4.9,4,0,100.00,'demo@upi',0),(16,'Dr. Shweta Nair','General Surgeon',4.5,5,0,100.00,'demo@upi',0),(17,'Dr. Amit Bhosle','Dermatologist',4.4,5,0,100.00,'demo@upi',0),(18,'Dr. Neha Rao','Anesthesiologist',4.3,5,0,100.00,'demo@upi',0);
/*!40000 ALTER TABLE `doctors_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drivers`
--

DROP TABLE IF EXISTS `drivers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drivers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `dob` date NOT NULL,
  `password` varchar(255) NOT NULL,
  `latitude` decimal(10,7) NOT NULL,
  `longitude` decimal(10,7) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drivers`
--

LOCK TABLES `drivers` WRITE;
/*!40000 ALTER TABLE `drivers` DISABLE KEYS */;
INSERT INTO `drivers` VALUES (1,'neyax wills','abcd@gmail.com','testwills','5124655154','1515-12-25','$2b$12$9.e/oKJgjFa9sB/XcmxzcOrBIdn11tqnrfOBbWVTxCDDchpRtj4D2',0.0000000,0.0000000,1),(2,'abgd','abg1510@gmail.com','administrator','5551115544','2002-12-15','$2b$12$jhLMDwno/At3xdEQrOV4OONDtqHahKybQRYcbL8s9RKyhDtG4C1Ka',19.0840832,74.7896832,1),(3,'bhad','bhad@gmail.com','admin','5665452882','2002-12-15','$2b$12$X4z0XPQbAYQg1mWYoZE89OpKdlCQVrIK7c1zxXvSgzW8bUuHoN3xO',16.9399632,74.4173823,0);
/*!40000 ALTER TABLE `drivers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospital_users`
--

DROP TABLE IF EXISTS `hospital_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospital_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `dob` date NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospital_users`
--

LOCK TABLES `hospital_users` WRITE;
/*!40000 ALTER TABLE `hospital_users` DISABLE KEYS */;
INSERT INTO `hospital_users` VALUES (1,'avt','ava@gmail.com','a','8010969392','2025-05-01','scrypt:32768:8:1$ZHNXToZuzEEOicnq$e81a5f7f06f4bf6f0f20598323bafb5b9c7466974741e46616a42885961fbb7f35639d18f5d2b1590671f5aa0a08447da59d95695cac5027adc0e656fb0e7195',NULL),(3,'avta','avta008@gmail.com','avantika','08010969392','2025-05-01','avita',NULL);
/*!40000 ALTER TABLE `hospital_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospitals`
--

DROP TABLE IF EXISTS `hospitals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospitals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `rating` decimal(2,1) NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospitals`
--

LOCK TABLES `hospitals` WRITE;
/*!40000 ALTER TABLE `hospitals` DISABLE KEYS */;
INSERT INTO `hospitals` VALUES (1,'General Hospital','New York',4.5,40.71277600,-74.00597400),(2,'Grant Hospital','Mumbai',5.0,19.07609000,72.87742600),(3,'Pune General Hospital','Pune',4.3,18.51960000,73.85530000),(4,'Miraj Medical College Hospital','Miraj',4.7,16.79892000,74.66095000),(5,'Goa Hospital','Goa',4.2,15.29930000,74.12400000);
/*!40000 ALTER TABLE `hospitals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospitals_bed`
--

DROP TABLE IF EXISTS `hospitals_bed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospitals_bed` (
  `hospital_id` int NOT NULL AUTO_INCREMENT,
  `hospital_name` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `latitude` decimal(10,7) NOT NULL,
  `longitude` decimal(10,7) NOT NULL,
  `rating` float DEFAULT NULL,
  PRIMARY KEY (`hospital_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospitals_bed`
--

LOCK TABLES `hospitals_bed` WRITE;
/*!40000 ALTER TABLE `hospitals_bed` DISABLE KEYS */;
INSERT INTO `hospitals_bed` VALUES (1,'Horizon Multispeciality Hospital','Ganesh Nagar, Sangli','09665209210',16.8520000,74.5815000,3.6),(2,'Krishna Hospital and Medical Research Centre','Karad Sangli Road, Malkapur','02364241555',16.8550000,74.5640000,3.7),(3,'Bharati Hospital','Market Yard Road, Sangli','02332622293',16.8475000,74.5800000,4),(4,'Appasaheb Birnale Hospital','Sangli-Miraj Road','02332622800',16.8530000,74.5830000,4.4),(5,'Ruby Hall Clinic','Sassoon Road, Pune','02026163391',18.5289000,73.8767000,4.7),(6,'Jehangir Hospital','Bund Garden Road, Pune','02066811000',18.5362000,73.8750000,3.5),(7,'Deenanath Mangeshkar Hospital','Erandwane, Pune','02040151000',18.5085000,73.8070000,3.9),(8,'Sahyadri Super Specialty Hospital','Nagar Road, Pune','02067213300',18.5560000,73.9123000,4.6);
/*!40000 ALTER TABLE `hospitals_bed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notify`
--

DROP TABLE IF EXISTS `notify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notify` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `latitude` decimal(10,7) NOT NULL,
  `longitude` decimal(10,7) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `notify_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notify`
--

LOCK TABLES `notify` WRITE;
/*!40000 ALTER TABLE `notify` DISABLE KEYS */;
INSERT INTO `notify` VALUES (1,1,19.0795000,74.7700000,0),(19,2,18.5761792,73.9606528,0),(20,2,18.6384384,73.7705984,0),(21,2,18.6384384,73.7705984,0),(22,1,16.9400610,74.4174899,0),(23,1,16.9400670,74.4174987,0),(24,2,16.9399632,74.4173823,0);
/*!40000 ALTER TABLE `notify` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_history`
--

DROP TABLE IF EXISTS `patient_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `hospital_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `visit_date` date NOT NULL,
  `diagnostis` varchar(500) DEFAULT NULL,
  `medicines` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `hospital_id` (`hospital_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `patient_history_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `patient_history_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors_table` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `patient_history_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_history`
--

LOCK TABLES `patient_history` WRITE;
/*!40000 ALTER TABLE `patient_history` DISABLE KEYS */;
INSERT INTO `patient_history` VALUES (1,1,1,1,'2025-01-14','Cancer','NA'),(2,1,1,2,'2025-01-14','Cancer stage 4','NA'),(3,1,4,13,'2025-05-08','Cancer','NA'),(4,1,4,13,'2025-05-08','Cancer','NA'),(5,1,4,13,'2025-05-08','Cancer Stage 4','NA'),(6,1,4,13,'2025-05-08','Cancer Stage 4','NA'),(7,2,4,13,'2025-05-09','Cancer','NA'),(14,2,4,13,'2025-05-09','TB','NA');
/*!40000 ALTER TABLE `patient_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_rating`
--

DROP TABLE IF EXISTS `patient_rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_rating` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `hospital_id` int NOT NULL,
  `rating` float NOT NULL,
  `ph_id` int NOT NULL,
  `review` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `hospital_id` (`hospital_id`),
  KEY `ph_id` (`ph_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `patient_rating_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`),
  CONSTRAINT `patient_rating_ibfk_2` FOREIGN KEY (`ph_id`) REFERENCES `patient_history` (`id`),
  CONSTRAINT `patient_rating_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_rating`
--

LOCK TABLES `patient_rating` WRITE;
/*!40000 ALTER TABLE `patient_rating` DISABLE KEYS */;
/*!40000 ALTER TABLE `patient_rating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_driver`
--

DROP TABLE IF EXISTS `user_driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_driver` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `driver_id` int NOT NULL,
  `latitude` decimal(10,7) NOT NULL,
  `longitude` decimal(10,7) NOT NULL,
  `driver_lat` decimal(10,7) NOT NULL,
  `driver_long` decimal(10,7) NOT NULL,
  `is_complete` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `driver_id` (`driver_id`),
  CONSTRAINT `user_driver_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_driver_ibfk_2` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_driver`
--

LOCK TABLES `user_driver` WRITE;
/*!40000 ALTER TABLE `user_driver` DISABLE KEYS */;
INSERT INTO `user_driver` VALUES (1,2,3,19.0683000,74.7540000,16.8272291,74.6502208,1),(2,2,3,19.0683000,74.7540000,19.0840832,74.7896832,1),(3,2,3,19.1005000,74.8232000,19.0840832,74.7896832,1),(4,2,3,19.1005000,74.8232000,16.8272296,74.6502221,1),(5,2,3,19.1005000,74.8232000,16.8272244,74.6502102,1),(6,2,3,19.1005000,74.8232000,19.0840832,74.7896832,1),(7,2,3,19.0683000,74.7540000,19.0840832,74.7896832,1),(8,2,3,19.0683000,74.7540000,16.8272244,74.6502102,1),(9,1,1,19.0795000,74.7700000,19.0840832,74.7896832,1),(10,2,1,19.0683000,74.7540000,19.0840832,74.7896832,1),(11,1,3,19.0795000,74.7700000,17.0440436,74.2129800,1),(12,3,3,19.1005000,74.8232000,16.8460288,74.6029056,1),(13,3,3,19.1005000,74.8232000,16.8460288,74.6029056,1),(14,3,3,19.1005000,74.8232000,16.8460288,74.6029056,1),(15,1,3,19.0795000,74.7700000,17.0440436,74.2129800,1),(16,2,3,19.0683000,74.7540000,16.8460288,74.6029056,1),(17,1,3,19.0795000,74.7700000,16.8460288,74.6029056,1),(18,1,3,19.0795000,74.7700000,16.8460288,74.6029056,1),(19,2,1,19.1005000,74.8232000,19.0840832,74.7896832,1),(20,2,1,19.0683000,74.7540000,19.0840832,74.7896832,1),(21,2,1,19.0683000,74.7540000,16.8272224,74.6502308,1),(22,3,3,19.1005000,74.8232000,20.0081408,73.7640448,1),(23,2,1,19.0683000,74.7540000,20.0081408,73.7640448,1),(24,1,3,19.0795000,74.7700000,15.5123712,73.7607680,1),(25,2,1,16.8272211,74.6501959,18.6155008,73.7640448,1),(26,2,1,16.8272211,74.6501959,18.5729024,73.7411072,1),(27,2,1,16.8272211,74.6501959,16.8272211,74.6501959,1),(28,2,1,19.1005000,74.8232000,16.8272211,74.6501959,1),(29,2,1,16.8272242,74.6502268,16.8272242,74.6502268,1),(30,2,3,18.6155008,73.7640448,18.6155008,73.7640448,1),(31,2,3,18.6155008,73.7640448,18.5729024,73.7411072,1),(32,2,3,18.5729024,73.7411072,18.5729024,73.7411072,1),(33,2,3,18.5729024,73.7411072,18.5729024,73.7411072,1),(34,2,3,18.5729024,73.7411072,18.5729024,73.7411072,1),(35,2,3,16.8272325,74.6502284,16.8272325,74.6502284,1),(36,2,3,16.8272325,74.6502284,16.8272325,74.6502284,1),(37,2,3,18.5761792,73.9606528,18.5761792,73.9606528,1),(38,2,3,18.6384384,73.7705984,18.6384384,73.7705984,1),(39,2,3,18.6384384,73.7705984,18.6384384,73.7705984,1),(40,1,3,16.9400610,74.4174899,16.9400610,74.4174899,1),(41,1,3,16.9400670,74.4174987,16.9399632,74.4173823,1),(42,2,3,16.9399632,74.4173823,16.9399632,74.4173823,0);
/*!40000 ALTER TABLE `user_driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `dob` date NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'abc','abc1510@gmail.com','abc1234','02222222222','2002-10-15','$2b$12$kMbL6F2JWIUuZYjpZz48Tud1.jbKNlhyCZ/himKmKLQu4VfSoSpRK'),(2,'neyax wills','wiliti7184@ckuer.com','wiliti','+12018577757','2020-06-11','$2b$12$RM/2iX7pSyRs9xMBwACkg.H1rQMRFgSRnCIRmNP.O1xTSuJ18b.ua'),(3,'neyax wills','testwills@gmail.com','testwills','02222222444','2002-12-11','$2b$12$0B2yhC/9dO1Yvn1MVLX3yuU34gCAedsvK2uI.8E96VUEETimv.GEi');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-17 13:51:30
