<template>
	<div class="movie-list-container">
		<ul class="movie-list">
			<li class="movie-item" v-for="movie in movieList.result" :key="movie.id">
				<BigCard v-if="movie" :movie="movie" />
			</li>
		</ul>
		<div class="pagination">
			<ul class="pagination__list">
				<div v-if="movieList.page > 1" class="pagination__button">
					<router-link
						class="pagination__content link"
						:to="{ query: { ...this.$route.query, page: parseInt(movieList.page)-1 } }"
					>
						Prev
					</router-link>
				</div>
				<li
					v-for="index in paginationList"
					class="pagination__item"
					:class="{separator: !index}"
					:key="index"
				>
					<span
						v-if="index && movieList.page == index"
						class="pagination__content active"
					>
						{{ index }}
					</span>
					<router-link
						v-else-if="index"
						class="pagination__content link"
						:to="{ query: { ...this.$route.query, page: index } }"
					>
						{{ index }}
					</router-link>
					<span class="pagination__content separator" v-else>...</span>
				</li>
				<div v-if="movieList.page < movieList.total_pages" class="pagination__button">
						<!--@click="changePage(parseInt(movieList.page)+1)"-->
					<router-link
						class="pagination__content link"
						:to="{ query: { ...this.$route.query, page: parseInt(movieList.page)+1 } }"
					>
						Next
					</router-link>
				</div>
			</ul>
		</div>
	</div>
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
		language: String,
		genres: Array,
		startDate: String,
		endDate: String,
	},
	async setup(props) {
		let movieList = ref(null);
		let paginationList = ref(null);

		let languageQuery = "";
		if (props.language && props.language != "") languageQuery = "&original_language=" + props.language;
		let genresQuery = "";
		if (props.genres && props.genres.length != 0) genresQuery = "&genres=" + props.genres.join(",");
		let startDateQuery = "";
		if (props.startDate && props.startDate != "") startDateQuery = "&release_date.gte=" + props.startDate;
		let endDateQuery = "";
		if (props.endDate && props.endDate != "") endDateQuery = "&release_date.lte=" + props.endDate;

		const movieListResponse = await axios.get(
			`/api/movie/list?page=${props.page}${languageQuery}${genresQuery}${startDateQuery}${endDateQuery}`
		);
		const movieListData = movieListResponse.data;

		let movieListComputed = {};
		movieListComputed.page = movieListData.page;
		movieListComputed.result = movieListData.result;
		movieListComputed.total_pages = movieListData.total_pages;
		movieListComputed.total_results = movieListData.total_results;

		// Pagination en bas de page
		let pagination = 
			[...Array(movieListData.total_pages).keys()]
			.map(i => i+1)
			.filter(index => Math.abs(index - movieListData.page) < 3 || index == movieListData.total_pages || index == 1);

		// On ajoute la séparation entre les parties
		let paginationComputed = [...pagination];
		let nbAdded = 0;
		for (let i = 0; i < pagination.length; i++) {
			const curr = pagination[i];
			const next = pagination[i+1];
			if (next != null && curr + 1 != next) {
				paginationComputed.splice(i+nbAdded+1, 0, null);
				nbAdded++;
			}
		}

		paginationList.value = paginationComputed;
		movieList.value = movieListComputed;
		return {
			movieList,
			paginationList,
		};
	},
}
</script>

<style lang="scss">
@import "../../assets/variables.scss";

.movie-list-container {
	margin-left: 30px;
	width: 100%;
}
.movie-list {
	margin: 0;
	padding: 0;
	width: 100%;
}
.pagination {
	&__list {
		display: flex;
		flex-flow: wrap;
		justify-content: center;
		align-items: center;
		padding: 0;
	}
	&__item {
		display: inline-block;
		list-style: none;
		margin-left: 10px;
		&:first-of-type {
			margin-left: 0;
		}
		&.active {
			background-color: $main-color;
			color: $back2-color;
		}
	}
	&__button {
		margin: 0 15px;
	}
	&__content {
		display: block;
		padding: 10px 15px;
		border-radius: 5px;
		background-color: $back3-color;
		color: $font-color;
		font-size: 20px;
		font-weight: 500;
		&.active {
			background-color: $main-color;
			color: $back2-color;
		}
		&.link {
			&:hover {
				background-color: $back3-color;
				color: $main-color;
			}
		}
		&.separator {
			cursor: default;
			background-color: transparent;
		}
	}
}
</style>