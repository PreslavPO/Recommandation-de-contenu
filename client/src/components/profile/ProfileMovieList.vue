<template>
	<div class="profile-movie-list-container">
		<div class="profile-movie-list-filter">
			<select v-model="sortBySelected" name="languages" @change="onSortChange">
				<option value="last_rated">Last rated</option>
				<option value="rating.desc">Descending rating</option>
				<option value="rating.asc">Ascending rating</option>
			</select>
		</div>
		<ul class="profile-movie-list">
			<span class="no-movie" v-if="movieList.length == 0">No movie rated yet.</span>
			<li class="profile-movie-item" v-for="movie in movieList.result" :key="movie.id">
				<SmallCard v-if="movie" :movie="movie" :hasRating="true" />
			</li>
		</ul>
		<div class="profile-movie-list-filter">
			<input class="profile-see-more" type="button" value="See more" @click="seeMore">
		</div>
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
	data() {
		return {
			sortBySelected: "last_rated",
			page: 1,
		}
	},
	methods: {
		async onSortChange() {
			const movieListResponse = await this.$store.dispatch(
				"getListRating",
				{ "page": 1, "sort_by": this.sortBySelected }
			);

			this.movieList = movieListResponse;
		},
		async seeMore() {
			this.page++;
			const movieListResponse = await this.$store.dispatch(
				"getListRating",
				{ "page": this.page, "sort_by": this.sortBySelected }
			);

			this.movieList.result.push(...movieListResponse.result);
		},
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

.profile-movie-list-filter {
	display: flex;
	margin-bottom: 30px;
	select {
		padding: 8px;
		width: 100%;
		max-width: 250px;
		font-size: 16px;
		border-radius: 10px;
		border: 1px solid $font-color;
		background-color: $back2-color;
		color: $font-color;
		fill: $font-color;
		color-scheme: dark;
	}
	.profile-see-more {
		cursor: pointer;
		margin: auto;
		margin-top: 25px;
		padding: 7px 25px;
		border-radius: 50px;
		border: none;
		background-color: $main-color;
		&:hover {
			background-color: $main2-color;
		}
	}
}
</style>