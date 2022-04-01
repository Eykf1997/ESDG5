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
-- Database: `inventory`
--

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
CREATE TABLE IF NOT EXISTS `inventory` (
  `Item_Id` int NOT NULL AUTO_INCREMENT,
  `Quantity` int NOT NULL,
  `Details` varchar(64) DEFAULT NULL,
  `Expiry_Date` varchar(10) NOT NULL,
  `Item_Name` varchar(64) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`Item_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`Item_Id`, `Quantity`, `Details`, `Expiry_Date`, `Item_Name`, `Price`) VALUES
(1, -14, '99 rose bouquet', '2022-03-20', 'Willow Series ', '500.00'),
(2, -12, 'Blue Baby Breath', '2022-03-26', 'Blue Baby Breath Bouquet', '80.00'),
(3, 0, 'Canvas of Blooming Pastel Bouquet', '2022-04-20', 'Pastel Bouquet', '220.00'),
(4, 0, 'Cotton Dreams Bouquet', '2022-03-20', 'Cotton Dreams', '127.00'),
(5, 0, 'Emcatador Bouquet', '2022-04-05', 'Emcantador Bouquet', '118.00'),
(6, 0, 'Hydrangeas & Baby Breath Bouquet', '2022-03-26', 'Hydrangeas & Baby Breath Bouquet', '78.00'),
(7, 0, '18 pink and red roses', '2022-03-26', 'Jasper Bouquet', '250.00'),
(8, 0, 'Mixture of flowers', '2022-03-26', 'Condolence Stands', '230.00');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
