<template>
	<Suspense>
		<template #default>
			<MovieMain />
		</template>
		<template #fallback>
			Loading...
		</template>
	</Suspense>
	<Suspense>
		<template #default>
			<MovieCast />
		</template>
		<template #fallback>
			Loading...
		</template>
	</Suspense>
</template>

<script>
import MovieMain from "@/components/movieDetails/MovieMain.vue";
import MovieCast from "@/components/movieDetails/MovieCast.vue"
import { useRoute } from "vue-router";
import axios from "/config/axios";

export default {
	name: "Movie",
	components: {
		MovieMain,
		MovieCast,
	},
	// data() {
	// 	return {
	// 		id: "",
	// 		title: "Loading ...",
	// 		poster_path: "/no-poster.png",
	// 		background_path: "",
	// 		date: "--/--/----",
	// 		duration: "- mins",
	// 		overview: "Loading ...",
	// 		score: -1,
	// 		vote_count: -1,
	// 		genres: [{id: -1, name: "Loading ..."}],
	// 		person_crew: [
	// 			{id: 12, name: "Loading ...", job: "Director", profile_path: "/no-image.png"},
	// 			{id: 12, name: "Loading ...", job: "Writer", profile_path: "/no-image.png"},
	// 		],
	// 		person_cast: [
	// 			{id: 125, order: 0, character: "---", name: "Loading ...", profile_path: "/no-image.png"},
	// 		],
	// 		userScore: -1,
	// 	}
	// },
	// methods: {
	// 	/** @return {boolean} */
	// 	haveJob(list, job) {
	// 		return list.some(person => person.job === job);
	// 	},
	// 	/** @return {[{id: number, name: String, job: String, profile_path: String}]} */
	// 	getPeopleByJob(list, job) {
	// 		return list.filter(person => person.job === job);
	// 	},
	// 	/** @return {string} */
	// 	getThumbnail(name, imgDefault, c) {
	// 		let image_url = "https://image.tmdb.org/t/p/w500" + name;
	// 		let image = new Image();

	// 		image.onload = function() {
	// 			c(image_url);
	// 		}
	// 		image.onerror = function() {
	// 			c(imgDefault);
	// 		}

	// 		image.src = image_url;
	// 	}
	// },
	// async mounted() {
	// 	const route = useRoute();
	// 	document.title = `${route.params.id} — TheMoviesualizer`;
	// 	this.id = route.params.id;
	// 	const base_url = "https://image.tmdb.org/t/p";

	// 	try {
	// 		let resMovie = await axios.get(`/api/movie/${this.id}`);
	// 		// TODO : Si 404 on affiche rien, sinon on affiche tout
	// 		// Actuellement cela va dans le catch peu importe l'erreur (normal de pas trouver le plan d'arrière plan)
	// 		// Exemple id = 88844
	// 		let dataMovie = resMovie.data;
			
	// 		this.title = dataMovie.title;
	// 		this.poster_path = dataMovie.poster_path;
	// 		this.background_path = dataMovie.backdrop_path;
	// 		this.score = dataMovie.vote_average;
	// 		this.vote_count = dataMovie.vote_count;
	// 		this.duration = dataMovie.runtime;
	// 		this.overview = dataMovie.overview;
	// 		this.date = new Date(dataMovie.release_date);
	// 		this.genres = dataMovie.genres;

	// 		// Convert date
	// 		this.date = this.date.toLocaleDateString();

	// 		// Convert duration
	// 		this.duration = Math.floor(this.duration/60) + "h " + this.duration%60 + "mins";

	// 		// Images Path
	// 		this.poster_path = `${base_url}/w500${this.poster_path}`;
	// 		if (this.background_path)
	// 			this.background_path = `${base_url}/original${this.background_path}`;

	// 		this.getThumbnail(
	// 			this.poster_path,
	// 			"/no-poster.png",
	// 			(url) => { this.poster_path = url; }
	// 		);
			
	// 		let resCredits = await axios.get(`/api/movie/${this.id}/credits`)
	// 		let dataCredits = resCredits.data;
	// 		this.person_cast = dataCredits.cast;
	// 		this.person_crew = dataCredits.crew;

	// 		this.person_crew.forEach(p => {
	// 			this.getThumbnail(
	// 				p.profile_path,
	// 				"/no-image.png",
	// 				(url) => { p.profile_path = url; }
	// 			);
	// 		});
	// 		this.person_cast.forEach(p => {
	// 			this.getThumbnail(
	// 				p.profile_path,
	// 				"/no-image.png",
	// 				(url) => { p.profile_path = url; }
	// 			);
	// 		});
	// 	}
	// 	catch (error) {
	// 		console.error(error);
	// 	}
	// },
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";

$element-space: 75px;
.background {
	display: flex;
	align-items: center;
	justify-content: center;
	margin: 30px;
	height: 400px;
	overflow: hidden;
	border-radius: 20px;
	img {
		filter: blur(2px);
		width: 100%;
	}
}

$poster-width: 350px;
.header {
	position: relative;
	margin: 0 $margin-content;
	margin-bottom: $element-space;
	&__poster {
		position: absolute;
		bottom: 0;
		overflow: hidden;
		border-radius: 20px;
		width: $poster-width;
		img {
			display: block;
			width: 100%;
		}
	}
	&__info {
		margin-left: $poster-width + 45px;
		h2 {
			margin: 0;
			font-size: 40px;
			font-weight: 600;
		}
		.subtitle {
			display: flex;
			align-items: center;
			flex-wrap: wrap;
			&__text {
				font-size: 16px;
				color: $font2-color;
				margin-right: 20px;
			}
			&__genre {
				display: flex;
				margin: 0;
				padding: 0;
				list-style: none;
				font-size: 16px;
				li {
					margin-right: 10px;
					padding: 5px 20px;
					border-radius: 50px;
					background-color: #2933FF;
				}
			}
		}
		.overview-text {
			margin: 0;
			margin-top: 20px;
			font-size: 16px;
		}
		.score-list {
			display: flex;
			grid-gap: 30px;
			margin-top: 30px;
		}
	}
}

$cast-spacing: 10px;
.cast {
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	margin: 0 $margin-content;
	margin-bottom: $element-space;
	.first-column {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		.cast__category:first-child {
			width: calc(percentage(1/3) - $cast-spacing);
		}
		.cast__category:last-child {
			width: percentage(2/3);
		}
	}
	&__category {
		width: 100%;
		&.one-column .cast__item {
			width: 100%;
		}
		&.two-column .cast__item {
			width: calc(percentage(1/2) - $cast-spacing);
		}
		&.three-column .cast__item {
			width: calc(percentage(1/3) - $cast-spacing);
		}
	}
	&__title {
		font-size: 20px;
		font-weight: 500;
		color: $font2-color;
	}
	&__list {
		display: flex;
		justify-content: space-between;
		flex-wrap: wrap;
		width: 100%;
		.cast__item {
			display: flex;
			flex-direction: row;
			margin-bottom: 20px;
			width: 100%;
			.cast__img {
				display: flex;
				align-items: center;
				justify-content: center;
				overflow: hidden;
				width: 85px;
				height: 85px;
				min-width: 85px;
				min-height: 85px;
				border-radius: 50%;
			}
			.cast__description {
				display: flex;
				flex-direction: column;
				justify-content: center;
				margin-left: 20px;
				.cast__name {
					font-size: 20px;
					color: $font-color;
				}
				.cast__subtitle {
					font-size: 16px;
					color: $font2-color;
				}
			}
		}
	}
}

@media (max-width: 1400px) {
	.background {
		height: 250px;
	}
	.header__poster {
		width: $poster-width/1.25;
	}
	.header__info {
		margin-left: $poster-width/1.25 + 45px;
	}

	.cast {
		.first-column {
			flex-direction: column;
			.cast__category {
				&:first-child, &:last-child {
					width: 100%;
				}
			}
		}
		&__category.three-column .cast__item {
			width: calc(percentage(1/2) - $cast-spacing);
		}
	}
}
@media (max-width: 1100px) {
	.cast__category {
		&.two-column, &.three-column {
			.cast__item {
				width: 100%;
			}
		}
	}
}
</style>