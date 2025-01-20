/* Tecnologia de Base de Dados - PG ANALYTICS & DATA SCIENCE EMPRESARIAL 2024/2025
This is a simple aviation database with information about some airports, airplanes and their models and about the flights */

-- CREATE THE DATABASE AND TABLES

CREATE DATABASE aviation;

CREATE TABLE airport (
idAirport int NOT NULL,
name varchar(50) NOT NULL,
city varchar(50) NOT NULL,
country varchar(50) NOT NULL
);

CREATE TABLE airplane (
idAirplane int NOT NULL,
name varchar(50) NOT NULL,
idModel int NOT NULL
);

CREATE TABLE model (
idModel int NOT NULL,
manufacturer varchar(50) NOT NULL,
version varchar(50) NOT NULL,
numEngines int NOT NULL
);

CREATE TABLE flight (
idFlight int NOT NULL,
idAirportDeparture int NOT NULL,
idAirportArrival int NOT NULL,
airline varchar(50) NOT NULL,
duration int NOT NULL,
idAirplane int NOT NULL
);

-- IMPORT DATA

INSERT INTO airport (idAirport, name, city, country) VALUES
(1, 'Sa Carneiro', 'Porto', 'Portugal'),
(2, 'Madeira', 'Funchal', 'Portugal'),
(3, 'Portela', 'Lisboa', 'Portugal'),
(4, 'Ponta Delgada', 'S. Miguel', 'Portugal'),
(5, 'Faro', 'Faro', 'Portugal'),
(8, 'Charles de Gaule', 'Paris', 'France'),
(9, 'Orly', 'Paris', 'France'),
(11, 'Heathrow', 'Londres', 'United Kingdom'),
(12, 'Gatwick', 'Londres', 'United Kingdom');

INSERT INTO airplane (idAirplane, name, idModel) VALUES
(1, 'Scott Adams', 1),
(2, 'Milo Manara', 1),
(3, 'Serpieri', 5),
(4, 'Henki Bilal', 3),
(5, 'Gary Larson', 4),
(6, 'Bill Waterson', 4),
(7, 'J R R Tolkien', 3),
(8, 'Franquin', 3),
(9, 'Douglas Adams', 1);

INSERT INTO model (idModel, manufacturer, version, numEngines) VALUES
(1, 'Douglas', 'DC-10', 3),
(2, 'Boeing', '737', 2),
(3, 'Boeing', '747', 4),
(4, 'Airbus', 'A300', 2),
(5, 'Airbus', 'A340', 4);

INSERT INTO flight (idFlight, idAirportDeparture, idAirportArrival, airline, duration, idAirplane)
VALUES
(1001, 1, 2, 'TAP', 2, 1),
(1002, 2, 3, 'TAP', 1, 2),
(1003, 2, 12, 'BA', 2, 5),
(1004, 4, 3, 'SATA', 3, 6),
(1005, 9, 2, 'AirFrance', 2, 3),
(1006, 8, 11, 'BA', 1, 5),
(1007, 5, 1, 'TAP', 1, 5),
(1008, 3, 12, 'Portugalia', 3, 4),
(1009, 1, 3, 'Portugalia', 1, 2),
(1010, 12, 4, 'BA', 3, 3),
(1111, 1, 3, 'TAP', 2, 3);