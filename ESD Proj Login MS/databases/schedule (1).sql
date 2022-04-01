-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 01, 2022 at 05:03 PM
-- Server version: 8.0.21
-- PHP Version: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `schedule`
--

-- --------------------------------------------------------

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
CREATE TABLE IF NOT EXISTS `schedule` (
  `Schedule_ID` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `timeslot` datetime NOT NULL,
  `Customer_ID` varchar(99) NOT NULL,
  `Email` varchar(99) NOT NULL,
  PRIMARY KEY (`Schedule_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `schedule`
--

INSERT INTO `schedule` (`Schedule_ID`, `order_id`, `timeslot`, `Customer_ID`, `Email`) VALUES
(1, 1, '2022-04-10 09:30:00', '02', 'yi@gmail'),
(2, 1, '2022-04-10 09:30:00', '02', 'yi@gmail'),
(3, 1, '2022-04-10 09:30:00', '02', 'yi@gmail'),
(4, 1, '2022-04-10 09:30:00', '02', 'yi@gmail'),
(5, 1, '2022-04-10 09:30:00', '02', 'yi@gmail');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
