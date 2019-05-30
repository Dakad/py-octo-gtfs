/*  

Script contributed by Michael Perkins

example usage:
cat load_all.sql | mysql -u root
(assumes user is in same directory as GTFS source files)

*/

-- DROP TABLE IF EXISTS agency;

-- CREATE TABLE `agency` (
--     agency_id int(11) PRIMARY KEY,
--     agency_name VARCHAR(255),
--     agency_url VARCHAR(255),
--     agency_timezone VARCHAR(50)
-- );


-- DROP TABLE IF EXISTS routes;

-- CREATE TABLE `routes` (
--     route_id INT(11) PRIMARY KEY,
-- 	agency_id INT(11),
-- 	route_short_name VARCHAR(150),
-- 	route_long_name VARCHAR(255),
-- 	route_type INT(2),
-- 	KEY `agency_id` (agency_id),
-- 	KEY `route_type` (route_type)
-- );

-- DROP TABLE IF EXISTS stop_times;

-- CREATE TABLE `stop_times` (
--     trip_id INT(11),
-- 	arrival_time VARCHAR(8),
-- 	departure_time VARCHAR(8),
-- 	stop_id INT(11),
-- 	stop_sequence INT(11),
-- 	pickup_type INT(2),
-- 	drop_off_type INT(2),
-- 	KEY `trip_id` (trip_id),
-- 	KEY `stop_id` (stop_id),
-- 	KEY `stop_sequence` (stop_sequence),
-- 	KEY `pickup_type` (pickup_type),
-- 	KEY `drop_off_type` (drop_off_type)
-- );

-- DROP TABLE IF EXISTS stops;

-- CREATE TABLE `stops` (
--     stop_id INT(11) PRIMARY KEY,
-- 	stop_name VARCHAR(255),
-- 	stop_desc VARCHAR(255),
-- 	stop_lat DECIMAL(8,6),
-- 	stop_lon DECIMAL(8,6),
-- 	zone_id INT(11),
-- 	KEY `zone_id` (zone_id),
-- 	KEY `stop_lat` (stop_lat),
-- 	KEY `stop_lon` (stop_lon)
-- );

-- DROP TABLE IF EXISTS trips;

-- CREATE TABLE `trips` (
--     route_id INT(11),
-- 	service_id INT(11),
-- 	trip_id INT(11) PRIMARY KEY,
-- 	trip_headsign VARCHAR(255),
-- 	direction_id TINYINT(1),
-- 	block_id INT(11),
-- 	KEY `route_id` (route_id),
-- 	KEY `service_id` (service_id),
-- 	KEY `direction_id` (direction_id),
-- 	KEY `block_id` (block_id)
-- );

.IMPORT 'agency.txt' agency;

.IMPORT 'routes.txt' routes;

.IMPORT 'stop_times.txt' stop_times;

.IMPORT 'stops.txt' stops;

.IMPORT 'trips.txt' trips;