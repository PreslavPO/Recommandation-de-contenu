CREATE DATABASE IF NOT EXISTS recommandation_de_contenu;

CREATE TABLE `movie` (
  `id` int PRIMARY KEY,
  `title` varchar(255),
  `vote_average` float,
  `vote_count` int,
  `tagline` text,
  `status` varchar(255),
  `video` boolean,
  `runtime` int,
  `revenue` int,
  `release_date` date,
  `poster_path` varchar(255),
  `popularity` float,
  `overview` text,
  `original_title` varchar(255),
  `original_language` varchar(255),
  `imdb_id` int,
  `homepage` varchar(255),
  `budget` int,
  `adult` boolean
);

CREATE TABLE `movies_genres` (
  `movie_id` int,
  `genre_id` int
);

CREATE TABLE `genre` (
  `id` int PRIMARY KEY,
  `name` varchar(255)
);

CREATE TABLE `movies_keywords` (
  `movie_id` int,
  `keyword_id` int
);

CREATE TABLE `keyword` (
  `id` int PRIMARY KEY,
  `name` int
);

CREATE TABLE `belong_to_collection` (
  `movie_id` int,
  `collection_id` int
);

CREATE TABLE `collection` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `poster_path` varchar(255),
  `backdrop_path` varchar(255)
);

CREATE TABLE `movies_production_companies` (
  `movie_id` int,
  `production_company_id` int
);

CREATE TABLE `production_company` (
  `id` int PRIMARY KEY,
  `name` varchar(255)
);

CREATE TABLE `movies_production_countries` (
  `movie_id` int,
  `production_country_id` int
);

CREATE TABLE `production_country` (
  `iso_3166_1` char(2) PRIMARY KEY,
  `name` varchar(255)
);

CREATE TABLE `movies_spoken_languages` (
  `movie_id` int,
  `spoken_language_id` int
);

CREATE TABLE `spoken_language` (
  `iso_639_1` char(2) PRIMARY KEY,
  `name` varchar(255)
);

CREATE TABLE `movies_cast` (
  `movie_id` int,
  `cast_id` int,
  `order` int,
  `cast_member_id` int
);

CREATE TABLE `cast_member` (
  `id` int PRIMARY KEY,
  `character` varchar(255),
  `name` varchar(255),
  `genre` int,
  `profile_path` varchar(255)
);

CREATE TABLE `movies_crew` (
  `movie_id` int,
  `order` int,
  `crew_member_id` int
);

CREATE TABLE `crew_member` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `genre` int,
  `job` varchar(255),
  `department` varchar(255),
  `profile_path` varchar(255)
);

CREATE TABLE `ratings` (
  `user_id` int,
  `movie_id` int,
  `rating` int,
  `timestamp` bigint
);

CREATE TABLE `links` (
  `movie_id` int,
  `imdb_id` int,
  `tmdb_id` int
);

ALTER TABLE `movies_genres` ADD FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`);

ALTER TABLE `movies_genres` ADD FOREIGN KEY (`genre_id`) REFERENCES `genre` (`id`);

ALTER TABLE `movies_keywords` ADD FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`);

ALTER TABLE `movies_keywords` ADD FOREIGN KEY (`keyword_id`) REFERENCES `keyword` (`id`);

ALTER TABLE `belong_to_collection` ADD FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`);

ALTER TABLE `belong_to_collection` ADD FOREIGN KEY (`collection_id`) REFERENCES `collection` (`id`);

ALTER TABLE `movies_production_companies` ADD FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`);

ALTER TABLE `movies_production_companies` ADD FOREIGN KEY (`production_company_id`) REFERENCES `production_company` (`id`);

ALTER TABLE `movies_production_countries` ADD FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`);

ALTER TABLE `movies_production_countries` ADD FOREIGN KEY (`production_country_id`) REFERENCES `production_country` (`iso_3166_1`);

ALTER TABLE `movies_spoken_languages` ADD FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`);

ALTER TABLE `movies_spoken_languages` ADD FOREIGN KEY (`spoken_language_id`) REFERENCES `spoken_language` (`iso_639_1`);

ALTER TABLE `movies_cast` ADD FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`);

ALTER TABLE `movies_cast` ADD FOREIGN KEY (`cast_member_id`) REFERENCES `cast_member` (`id`);

ALTER TABLE `movies_crew` ADD FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`);

ALTER TABLE `movies_crew` ADD FOREIGN KEY (`crew_member_id`) REFERENCES `crew_member` (`id`);

ALTER TABLE `ratings` ADD FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`);

ALTER TABLE `links` ADD FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`);
