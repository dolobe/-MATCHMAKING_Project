-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 16 avr. 2025 à 11:16
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `matchmaking_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `matchs`
--

CREATE TABLE `matchs` (
  `id` int(11) NOT NULL,
  `player1_ip` varchar(45) NOT NULL,
  `player1_port` int(11) NOT NULL,
  `player2_ip` varchar(45) NOT NULL,
  `player2_port` int(11) NOT NULL,
  `board_state` varchar(9) DEFAULT '         ',
  `is_finished` tinyint(1) DEFAULT 0,
  `result` enum('player1','player2','draw','none') DEFAULT 'none'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `matchs`
--

INSERT INTO `matchs` (`id`, `player1_ip`, `player1_port`, `player2_ip`, `player2_port`, `board_state`, `is_finished`, `result`) VALUES
(1, '127.0.0.1', 55082, '127.0.0.1', 55092, '         ', 0, 'none');

-- --------------------------------------------------------

--
-- Structure de la table `queue`
--

CREATE TABLE `queue` (
  `id` int(11) NOT NULL,
  `ip` varchar(45) NOT NULL,
  `port` int(11) NOT NULL,
  `pseudo` varchar(50) NOT NULL,
  `entry_time` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `queue`
--

INSERT INTO `queue` (`id`, `ip`, `port`, `pseudo`, `entry_time`) VALUES
(2, '127.0.0.1', 12345, 'PlayerOne', '2025-04-16 10:32:08'),
(3, '127.0.0.1', 55082, 'Herison', '2025-04-16 10:55:59'),
(4, '127.0.0.1', 55092, '', '2025-04-16 10:56:41'),
(5, '127.0.0.1', 55197, 'dolo', '2025-04-16 10:57:40'),
(6, '127.0.0.1', 55247, 'dolo', '2025-04-16 11:00:29');

-- --------------------------------------------------------

--
-- Structure de la table `turns`
--

CREATE TABLE `turns` (
  `id` int(11) NOT NULL,
  `match_id` int(11) NOT NULL,
  `player` enum('player1','player2') NOT NULL,
  `move_position` int(11) DEFAULT NULL CHECK (`move_position` between 0 and 8),
  `played_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `matchs`
--
ALTER TABLE `matchs`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `queue`
--
ALTER TABLE `queue`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `turns`
--
ALTER TABLE `turns`
  ADD PRIMARY KEY (`id`),
  ADD KEY `match_id` (`match_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `matchs`
--
ALTER TABLE `matchs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `queue`
--
ALTER TABLE `queue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `turns`
--
ALTER TABLE `turns`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `turns`
--
ALTER TABLE `turns`
  ADD CONSTRAINT `turns_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `matchs` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
