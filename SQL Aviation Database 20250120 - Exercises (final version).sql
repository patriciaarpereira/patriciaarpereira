/* Tecnologia de Base de Dados - PG ANALYTICS & DATA SCIENCE EMPRESARIAL 2024/2025
This is a simple aviation database with information about some airports, airplanes and their models and about the flights */

/* EXERCISES
Topics:
	- WHERE AND ORDER BY
	- GROUP BY AND HAVING
	- JOIN
	- SUBQUERIES
	- CTE
	- WINDOW FUNCTIONS
	- CASE WHEN
*/

-- 1) Project the name and city of all existing airports in Portugal.
SELECT
	name AS airport,
	city
FROM airport
WHERE country = 'Portugal'
ORDER BY name;


-- 2) Project the name of the planes whose model version is DC-10.
SELECT
	name AS airplane
FROM airplane
LEFT JOIN model
	USING (idmodel)
WHERE version = 'DC-10';


-- 3) Project the number of engines for each plane
SELECT
	name AS airplane,
	numengines AS number_engines
FROM airplane
LEFT JOIN model
	USING (idmodel)
ORDER BY numengines;


/* 4) Project the total number of flights lasting two or three hours.
(Must include the number of different planes on flights lasting 2 to 3 hours). */
SELECT
	duration,
	COUNT(DISTINCT idairplane) as number_airplanes,
	COUNT(idflight) as number_flights
FROM flight
GROUP BY duration
HAVING duration IN (2,3);


-- 5) Project the idModel and version of the airplane model whose version starts with ‘A3’.
SELECT
	idmodel,
	version
FROM model
WHERE version LIKE 'A3%';


-- 6) Project the code and duration of all flights. Sort by longest flight to shortest.
SELECT
	idflight,
	duration
FROM flight
ORDER BY duration DESC, idflight;


/* 7) Knowing that there are no direct flights from Porto to London, plan the flights that allow this connection. Tip: Use the airport codes (1 and 12) instead of the airport name. */

-- Different replies
-- Join
SELECT
	idflight,
	idairportdeparture as departure,
	ap_departure.name AS airport_departure,
	idairportarrival,
	ap_arrival.name AS airport_arrival
FROM flight
LEFT JOIN airport AS ap_departure
	ON flight.idairportdeparture = ap_departure.idairport
LEFT JOIN airport AS ap_arrival
	ON flight.idairportarrival = ap_arrival.idairport
WHERE idairportdeparture = 1
	OR idairportarrival = 12
ORDER BY idairportdeparture, idairportarrival;

-- Subquery
SELECT
	idflight,
	idairportdeparture,
	(SELECT name AS airport_departure FROM airport WHERE idairportdeparture = idairport),
	idairportarrival,
	(SELECT name AS airport_arrival FROM airport WHERE idairportarrival = idairport)
FROM flight
WHERE idairportdeparture = 1
	OR idairportarrival = 12
ORDER BY idairportdeparture, idairportarrival;

-- CTE
WITH ap_porto_london AS (
	SELECT 
		idflight,
		idairportdeparture,
		idairportarrival
	FROM flight
	WHERE idairportdeparture = 1
		OR idairportarrival = 12
	ORDER BY idairportdeparture, idairportarrival	
)
SELECT
	idflight,
	idairportdeparture,
	(SELECT name AS airport_departure FROM airport WHERE idairportdeparture = idairport),
	idairportarrival,
	(SELECT name AS airport_arrival FROM airport WHERE idairportarrival = idairport)
FROM ap_porto_london;


-- 8) Project the total number of airports by country. Order from lowest to highest number.
SELECT
	country,
	COUNT(idairport) AS total_airports
FROM airport
GROUP BY country
ORDER BY COUNT(idairport);


-- 9) Project each flight code with the origin city and destination city of each flight.

-- Join
SELECT
	idflight,
	ap_departure.city AS city_departure,
	ap_arrival.city AS city_arrival
FROM flight
LEFT JOIN airport AS ap_departure
	ON flight.idairportdeparture = ap_departure.idairport
LEFT JOIN airport AS ap_arrival
	ON flight.idairportarrival = ap_arrival.idairport

-- Subquery
SELECT
	idflight,
	(SELECT city AS city_departure FROM airport WHERE idairport = idairportdeparture),
	(SELECT city AS city_arrival FROM airport WHERE idairport = idairportarrival)
FROM flight;

-- CTE
WITH c_departure AS (
	SELECT idairport, city AS city_departure 
	FROM airport 
),
c_arrival AS (
	SELECT idairport, city AS city_arrival 
	FROM airport 
)
SELECT
	idflight,
	city_departure,
	city_arrival
FROM flight
LEFT JOIN c_departure
	ON idairportdeparture = c_departure.idairport
LEFT JOIN c_arrival
	ON idairportarrival = c_arrival.idairport;


/* 10) Project the codes of flights departing from Porto to Lisbon. 
Tip: Use the names of the cities instead of the airport codes. */

-- Subquery
SELECT 
	idflight
FROM flight
WHERE idairportdeparture IN (
		SELECT idairport
		FROM airport
		WHERE city = 'Porto')
	AND idairportarrival IN (
		SELECT idairport 
		FROM airport
		WHERE city = 'Lisboa');

-- CTE
WITH departure_porto AS (
	SELECT idairport
	FROM airport
	WHERE city = 'Porto'
),
arrival_lisbon AS (
	SELECT idairport 
	FROM airport
	WHERE city = 'Lisboa'
)
SELECT
	idflight
FROM flight
RIGHT JOIN departure_porto
	ON departure_porto.idairport = idairportdeparture
RIGHT JOIN arrival_lisbon
	ON arrival_lisbon.idairport = idairportarrival;


-- 11) Project country name and total airports of countries where there are more than 2 airports.
SELECT
	country,
	COUNT(idairport) AS total_airports
FROM airport
GROUP BY country
HAVING COUNT(idairport) > 2;


-- 12) Project the country or countries that have the fewest airports.

-- Subquery
SELECT 
	country
FROM airport
GROUP BY country
HAVING COUNT(idairport) = (
	SELECT MIN(total_airports)
	FROM (
		SELECT COUNT(idairport) AS total_airports
		FROM airport
		GROUP BY country
	)
)


-- 13) Project the country or countries that have the largest number of airports.

-- Subquery
SELECT
	country
FROM airport
GROUP BY country
HAVING COUNT(idairport) = (
	SELECT MAX(total_airports)
	FROM (
		SELECT COUNT(idairport) AS total_airports
		FROM airport
		GROUP BY country
	)
)


-- 14) Project the total number of existing aircrafts for each model.

-- Join
SELECT 
	idmodel,
	version AS model,
	COUNT(idairplane) AS total_airplane
FROM airplane
LEFT JOIN model -- select only idmodelo where there are idaviao (i.e., > 0)
	USING (idmodel)
GROUP BY idmodel, version
ORDER BY COUNT(idairplane);


/* 15) Project the total number of existing airplanes for each model. 
Include airplane models even if there are no existing airplanes. */

-- Join
SELECT 
	version AS model,
	COUNT(idairplane) AS total_airplanes
FROM airplane
RIGHT JOIN model -- select idmodelo even if there is no idaviao (= 0)
	USING (idmodel)
GROUP BY version
ORDER BY COUNT(idairplane);

-- CTE
WITH count_airplane AS (
	SELECT idmodel, COUNT(idairplane) AS tot_airplanes
	FROM airplane
	GROUP BY idmodel
)
SELECT 
	idmodel,
	version AS model,
	COALESCE(tot_airplanes, 0) AS total_airplanes -- tranform NULL as 0
FROM model
LEFT JOIN count_airplane
	USING (idmodel)
ORDER BY total_airplanes;


/* 16) Assuming that more projections can still be made for this database, present 6
new exercise proposals and the respective solution. */

-- 16.a) Which manufacturers produce the airplanes that make the longest trips??

-- Join and Subquery
SELECT 
	DISTINCT manufacturer,
	duration
FROM model
LEFT JOIN airplane
	USING (idmodel)
LEFT JOIN flight
	USING (idairplane)
WHERE duration = (
	SELECT MAX(duration)
	FROM flight
)

-- CTE
WITH man_aviao AS (
	SELECT manufacturer, idairplane
	FROM model
	LEFT JOIN airplane
		USING (idmodel)
)
SELECT
	DISTINCT manufacturer,
	duration
FROM man_aviao
LEFT JOIN flight
	USING (idairplane)
WHERE duration = (
	SELECT MAX(duration)
	FROM flight
);


-- 16.b) What is the ranking of the companies with the highest number of flights?
SELECT 
	airline,
	COUNT(idflight) AS number_flights,
	DENSE_RANK()
		OVER (ORDER BY COUNT(idflight) DESC) AS ranking_flights
FROM flight
GROUP BY airline


-- 16.c) What is the total travel time each model takes per flight??
WITH model_duration AS (
	SELECT 
		version AS model,
		idflight,
		duration
	FROM model
	LEFT JOIN airplane
		USING (idmodel)
	LEFT JOIN flight
		USING (idairplane)
	WHERE duration IS NOT NULL
	ORDER BY model, duration
)
SELECT 
	model,
	idflight,
	duration,
	SUM(duration) OVER (PARTITION BY model ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total_duration_flight
FROM model_duration
ORDER BY model;


-- 16.d) What are the flights with the respective airports that the A300 model makes?
SELECT
	version,
	idflight,
	(SELECT name FROM airport WHERE idairport = idairportdeparture) AS airport_departure,
	(SELECT name FROM airport WHERE idairport = idairportarrival) AS airport_arrival
FROM flight
JOIN airplane
	USING (idairplane)
JOIN model
	USING (idmodel)
WHERE version = 'A300';


-- 16.e) How many flights does each plane make per company and what is the total?
WITH voos_al AS (
	SELECT
		name,
		airline,
		COUNT(idflight) AS sum_flight_airline
	FROM flight
	JOIN airplane
		USING (idairplane)
	GROUP BY name, airline
	ORDER BY name, sum_flight_airline
)
SELECT
	name, 
	airline,
	sum_flight_airline,
	SUM(sum_flight_airline) OVER (PARTITION BY name ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total_flights
FROM voos_al;

-- 16.f) Creates a new column with "Direct flight" or "Possible stopover" between Sa Carneiro (id = 1) and Portela (id = 3) airports.
SELECT
	idflight,
	(SELECT name AS airport_departure FROM airport WHERE idairportdeparture = idairport),
	(SELECT name AS airport_arrival FROM airport WHERE idairportarrival = idairport),
	CASE 
		WHEN idairportdeparture = 1 AND idairportarrival = 3 THEN 'Direct flight'
		WHEN idairportdeparture = 1 OR idairportarrival = 3 THEN 'Possible stopover'
		ELSE 'NA' END AS Voos
FROM flight
WHERE idairportdeparture = 1
	OR idairportarrival = 3
ORDER BY idairportarrival;
