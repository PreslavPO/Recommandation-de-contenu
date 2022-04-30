<template>
	<div class="recommended-movie-list-container">
		<ul class="recommended-movie-list">
			<li class="recommended-movie-item" v-for="movie in movieList.result" :key="movie.id">
				<SmallCard v-if="movie" :movie="movie" :hasRating="false" />
			</li>
		</ul>
	</div>
</template>

<script>
import { ref } from "vue";
import { useStore } from 'vuex'
import axios from "@/../config/axios";
import SmallCard from "@/components/movieCards/SmallCard.vue";

export default {
	components: {
		SmallCard,
	},
	async setup() {
		const store = useStore();
		let movieList = ref(null);

		const movieListResponse = await store.dispatch( "getRecommendation", 1 );
		const movieListData = movieListResponse;

		let movieListComputed = {};
		movieListComputed.page = movieListData.page;
		movieListComputed.result = movieListData.result;
		movieListComputed.total_pages = movieListData.total_pages;
		movieListComputed.total_results = movieListData.total_results;

		movieList.value = movieListComputed;
		return {
			movieList,
		};
	},
}
</script>

<style lang="scss">
@import "../../assets/variables.scss";

.recommended {
	&-movie-list-container {
		margin-top: 20px;
	}
	&-movie-list {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		margin: 0;
		padding: 0;
		list-style: none;
	}
	&-movie-item {
		margin: 0 auto;
	}
}

@media (max-width: 1600px) {
	.recommended-movie-list {
		grid-template-columns: repeat(6, 1fr);
	}
}
@media (max-width: 1500px) {
	.recommended-movie-list {
		grid-template-columns: repeat(5, 1fr);
	}
}
@media (max-width: 1400px) {
	.recommended-movie-list {
		grid-template-columns: repeat(4, 1fr);
	}
}
@media (max-width: 1200px) {
	.recommended-movie-list {
		grid-template-columns: repeat(3, 1fr);
	}
}
</style>