-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 15, 2026 at 11:27 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chickenarium`
--

-- --------------------------------------------------------

--
-- Table structure for table `detection_history`
--

CREATE TABLE `detection_history` (
  `id` int(11) NOT NULL,
  `log_date` datetime DEFAULT current_timestamp(),
  `health_status` varchar(50) DEFAULT NULL,
  `symptoms` varchar(255) DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `zone` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detection_history`
--

INSERT INTO `detection_history` (`id`, `log_date`, `health_status`, `symptoms`, `remarks`, `zone`) VALUES
(1, '2026-02-10 23:04:08', 'Critical', 'Coughing', 'TESTING NEW TIME', 'A'),
(2, '2026-02-10 23:04:08', 'Warning', 'Sneezing', 'TEST RECORD 2', 'B');

-- --------------------------------------------------------

--
-- Table structure for table `farm_settings`
--

CREATE TABLE `farm_settings` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `farm_name` varchar(100) NOT NULL,
  `farm_id` varchar(50) DEFAULT NULL,
  `owner_name` varchar(100) NOT NULL,
  `owner_phone` varchar(30) NOT NULL,
  `owner_email` varchar(100) NOT NULL,
  `farm_location` text DEFAULT NULL,
  `farm_type` varchar(50) DEFAULT NULL,
  `number_of_chickens` int(11) DEFAULT 0,
  `units` varchar(20) DEFAULT NULL,
  `notify_sms` tinyint(1) DEFAULT 0,
  `notify_email` tinyint(1) DEFAULT 0,
  `notify_push` tinyint(1) DEFAULT 0,
  `enable_alerts` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farm_settings`
--

INSERT INTO `farm_settings` (`id`, `user_id`, `farm_name`, `farm_id`, `owner_name`, `owner_phone`, `owner_email`, `farm_location`, `farm_type`, `number_of_chickens`, `units`, `notify_sms`, `notify_email`, `notify_push`, `enable_alerts`, `created_at`) VALUES
(4, 1, 'aldrin', 'FARM-2026-AJP3', 'awitin', '09509578226', 'aldrinte26@gmail.com', 'adsdasd', 'Broiler', 500, NULL, 0, 0, 0, 0, '2026-02-10 14:12:45'),
(5, 2, 'wendyeee', 'FARM-2026-LDS2', 'wendol', '09509578227', 'wendol@gmail.com', 'adaddw', 'Layer', 3232, 'metric', 1, 1, 1, 1, '2026-02-10 14:20:29');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fullname`, `email`, `username`, `password`, `created_at`) VALUES
(1, 'aldrin te', 'aldrinte26@gmail.com', 'aldrinte27', '$2y$10$UwdEAPfvbl24xA5Em0mozehaNxWktsVzsftT4pQuIYuYo5KwKPvwO', '2026-02-10 13:27:17'),
(2, 'wendy', 'wendy@gmail.com', 'wendol', '$2y$10$R0JIeNxhzfpTOw1BiPYxIOxVXBjDErKtYbs1B104dzsOPenglOH7S', '2026-02-10 14:19:58');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detection_history`
--
ALTER TABLE `detection_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `farm_settings`
--
ALTER TABLE `farm_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detection_history`
--
ALTER TABLE `detection_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `farm_settings`
--
ALTER TABLE `farm_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
