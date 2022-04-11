<template>
	<li class="movie-item" v-for="movie in movieList.result" :key="movie.id">
		<BigCard v-if="movie" :movie="movie" />
	</li>
</template>

<script>
import { ref } from "vue";
import axios from "@/../config/axios";
import BigCard from "@/components/movieCards/BigCard.vue";

export default {
	components: {
		BigCard,
	},
	props: {
		page: Number,
	},
	async setup(props) {
		let movieList = ref(null);

		const movieListResponse = await axios.get(`/api/movie/top_rating?page=${props.page}`);
		const movieListData = movieListResponse.data;

		let movieListComputed = {};
		movieListComputed.page = movieListData.page;
		movieListComputed.result = movieListData.result;

		movieList.value = movieListComputed;
		return {
			movieList
		};
	},
}
</script>