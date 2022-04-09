<template>
	<div class="background">
		<img v-if="movie.background_path" :src="movie.background_path" :alt="'background of ' + movie.title">
	</div>
	<div class="header">
		<div class="header__poster">
			<img :src="movie.poster_path" :alt="'poster of ' + movie.title">
		</div>
		<div class="header__info">
			<h2>{{ movie.title }}</h2>
			<div class="subtitle">
				<span class="subtitle__text">{{ movie.date }} — {{ movie.duration }}</span>
				<ul class="subtitle__genre">
					<li v-for="genre in movie.genres" :key="genre.id">
						{{ genre.name }}
					</li>
				</ul>
			</div>
			<p class="overview-text">{{ movie.overview }}</p>
			<div class="score-list">
				<RatingStar :is-global="true" :score="movie.score" :vote-count="movie.vote_count" />
				<RatingStar :is-global="false" :score="movie.userScore" />
			</div>
		</div>
	</div>
</template>

<script>
import { ref } from "vue";
import axios from "@/../config/axios";
import { useRoute } from "vue-router";
import RatingStar from "@/components/RatingStar.vue";

export default {
	components: {
		RatingStar,
	},
	async setup() {
		const base_url = "https://image.tmdb.org/t/p";

		/**
		 * Get image if correct path or else get default image
		 */
		const getThumbnail = (name, imgDefault) => {
			return new Promise((resolve, reject) => {
				let imageUrl = `${base_url}/w500${name}`;
				let image = new Image();

				image.onload = () => resolve(imageUrl);
				image.onerror = () => resolve(imgDefault);
				image.src = imageUrl;
			});
		}

		const route = useRoute();
		let movie = ref(null);
		const movieResponse = await axios.get(`/api/movie/${route.params.id}`);
		const movieData = movieResponse.data;

		document.title = `${movieData.title} — TheMoviesualizer`;

		let movieComputed = {};
		movieComputed.title = movieData.title;
		movieComputed.score = movieData.vote_average;
		movieComputed.vote_count = movieData.vote_count;
		movieComputed.overview = movieData.overview;
		movieComputed.genres = movieData.genres;
		// Converting date
		movieComputed.date = new Date(movieData.release_date).toLocaleDateString();
		// Converting duration XXh XXmins
		movieComputed.duration = `${~~(movieData.runtime/60)}h ${movieData.runtime%60}mins`;

		// Images Path
		if (movieData.backdrop_path)
			movieComputed.background_path = `${base_url}/original${movieData.backdrop_path}`;

		movieComputed.poster_path = await getThumbnail(
			movieData.poster_path,
			"/no-poster.png"
		);

		movie.value = movieComputed;
		return {
			movie,
		};
	},
}
</script>