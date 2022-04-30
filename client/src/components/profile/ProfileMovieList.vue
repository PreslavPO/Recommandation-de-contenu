<template>
	<div class="profile-movie-list-container">
		<ul class="profile-movie-list">
			<span class="no-movie" v-if="movieList.length == 0">No movie rated yet.</span>
			<li class="profile-movie-item" v-for="movie in movieList.result" :key="movie.id">
				<SmallCard v-if="movie" :movie="movie" :hasRating="true" />
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

		const movieListResponse = await store.dispatch(
			"getListRating",
			{ "page": 1, "sort_by": "last_rated" }
		);
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

.profile {
	&-movie-list-container {
		margin-top: 20px;
		.no-movie {
			color: $font2-color;
		}
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
	.profile-movie-list {
		grid-template-columns: repeat(6, 1fr);
	}
}
@media (max-width: 1500px) {
	.profile-movie-list {
		grid-template-columns: repeat(5, 1fr);
	}
}
@media (max-width: 1400px) {
	.profile-movie-list {
		grid-template-columns: repeat(4, 1fr);
	}
}
@media (max-width: 1200px) {
	.profile-movie-list {
		grid-template-columns: repeat(3, 1fr);
	}
}
</style>