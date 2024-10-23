-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for ssis_web
CREATE DATABASE IF NOT EXISTS `ssis_web` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ssis_web`;

-- Dumping structure for table ssis_web.college_table
CREATE TABLE IF NOT EXISTS `college_table` (
  `college_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `college_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`college_code`),
  UNIQUE KEY `college_code` (`college_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ssis_web.college_table: ~7 rows (approximately)
INSERT IGNORE INTO `college_table` (`college_code`, `college_name`) VALUES
	('CASS', 'College of Arts and Social Sciences'),
	('CCS', 'College of Computer Studies'),
	('CEBA', 'College of Economics, Business, and Accountancy'),
	('CED', 'College of Education'),
	('CHS', 'College of Health Sciences'),
	('COE', 'College of Engineering'),
	('CSM', 'College of Science and Mathematics');

-- Dumping structure for table ssis_web.course_table
CREATE TABLE IF NOT EXISTS `course_table` (
  `course_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `course_name` varchar(50) DEFAULT NULL,
  `course_college` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`course_code`),
  UNIQUE KEY `course_code` (`course_code`),
  KEY `course_college` (`course_college`),
  CONSTRAINT `course_college` FOREIGN KEY (`course_college`) REFERENCES `college_table` (`college_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ssis_web.course_table: ~2 rows (approximately)
INSERT IGNORE INTO `course_table` (`course_code`, `course_name`, `course_college`) VALUES
	('BSCA', 'Bachelor of Science in Computer Applications', 'CCS'),
	('BSCS', 'Bachelors of Science in Computer Science', 'CCS');

-- Dumping structure for table ssis_web.student_table
CREATE TABLE IF NOT EXISTS `student_table` (
  `student_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `student_firstname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `student_lastname` varchar(50) DEFAULT NULL,
  `student_year` varchar(50) DEFAULT NULL,
  `student_gender` varchar(50) DEFAULT NULL,
  `student_course` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_id` (`student_id`),
  KEY `student_course` (`student_course`),
  CONSTRAINT `student_course` FOREIGN KEY (`student_course`) REFERENCES `course_table` (`course_code`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ssis_web.student_table: ~3 rows (approximately)
INSERT IGNORE INTO `student_table` (`student_id`, `student_firstname`, `student_lastname`, `student_year`, `student_gender`, `student_course`) VALUES
	('2021-2525', 'John', 'Reddington', '4', 'Others', 'BSCS'),
	('2022-0001', 'Raymond', 'Reddington', '3', 'Male', 'BSCS'),
	('2023-0005', 'Jake', 'Peralta', '1', 'Male', 'BSCS');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
