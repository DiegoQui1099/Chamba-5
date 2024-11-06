-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-11-2024 a las 16:49:10
-- Versión del servidor: 10.4.25-MariaDB
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `pruebajd`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `multas_jurados`
--

CREATE TABLE `multas_jurados` (
  `Nombres` varchar(25) DEFAULT NULL,
  `Apellidos` varchar(25) DEFAULT NULL,
  `Cedula` varchar(25) DEFAULT NULL,
  `Departamento` varchar(25) DEFAULT NULL,
  `Multa_p` int(50) DEFAULT NULL,
  `Motivo` varchar(225) DEFAULT NULL,
  `observaciones` varchar(225) DEFAULT NULL,
  `Id_Jurado` int(25) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `multas_jurados`
--

INSERT INTO `multas_jurados` (`Nombres`, `Apellidos`, `Cedula`, `Departamento`, `Multa_p`, `Motivo`, `observaciones`, `Id_Jurado`) VALUES
('Diego Alexander', 'Quiñones Sanabria', '1013691626', 'Cundinamarca', 1000000000, 'No Asistió a la mesa de jurado.', 'Al momento de comunicarse con el ciudadano este dijo.  ! eso chúpenme la monda ¡ \r\n\r\n', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `multas_jurados`
--
ALTER TABLE `multas_jurados`
  ADD PRIMARY KEY (`Id_Jurado`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `multas_jurados`
--
ALTER TABLE `multas_jurados`
  MODIFY `Id_Jurado` int(25) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
