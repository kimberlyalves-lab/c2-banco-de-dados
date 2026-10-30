CREATE DATABASE IF NOT EXISTS acessibilidade;
USE acessibilidade;

DROP TABLE IF EXISTS recursos;
DROP TABLE IF EXISTS locais;


CREATE TABLE `locais` (
  `id_local` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `endereco` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cidade` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_local`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE `recursos` (
  `id_recurso` int NOT NULL AUTO_INCREMENT,
  `id_local` int NOT NULL,
  `nome` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo_deficiencia` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `situacao` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `data_verificacao` date NOT NULL,
  PRIMARY KEY (`id_recurso`),
  KEY `fk_recurso_local` (`id_local`),
  CONSTRAINT `fk_recurso_local` FOREIGN KEY (`id_local`) REFERENCES `locais` (`id_local`),
  CONSTRAINT `chk_situacao` CHECK ((`situacao` in (_utf8mb4'FUNCIONANDO',_utf8mb4'EM MANUTENCAO',_utf8mb4'INEXISTENTE')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
