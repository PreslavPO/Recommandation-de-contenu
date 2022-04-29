<template>
	<div class="top-movie">
		<h1>Top Rating</h1>
		<span>Which is the best rated movie?</span>
		<div class="main-movie">
			<div class="filter">
				<h3>Filters</h3>
				<div class="filter__list">
					<div class="filter__group">
						<h3>By date</h3>
						<div class="filter-date">
							<label for="start-date">From</label>
							<input class="filter__input" type="date" id="start-date" v-model="startDateSelected" placeholder="xxxx-xx-xx" />
						</div>
						<div class="filter-date">
							<label for="end-date">To</label>
							<input class="filter__input" type="date" id="end-date" v-model="endDateSelected" placeholder="xxxx-xx-xx" />
						</div>
					</div>
					<div class="filter__group">
						<h3>By language</h3>
						<select v-model="languageSelected" name="languages" id="languages-select" class="filter__input">
							<option value="">No selection</option>
							<option
								v-for="language in languages"
								:key="language._id"
								:value="language._id"
							>
								{{ language.name }} ({{ language.total }})
							</option>
						</select>
					</div>
					<div class="filter__group">
						<h3>By genres</h3>
						<ul class="filter-genres">
							<li v-for="genre in genres" :key="genre._id" :value="genres.name" class="filter-genres__item">
								<input
									class="genres-input"
									type="checkbox"
									:id="'genres-' + genre._id"
									:value="genre._id"
									v-model="genresSelected"
								>
								<label
									class="genres-label"
									:for="'genres-' + genre._id"
								>
									{{ genre.name }}
								</label>
							</li>
						</ul>
					</div>
					<div class="filter__group">
						<input class="filter-search" type="button" value="Search" @click="search">
					</div>
				</div>
			</div>
			<Suspense>
				<template #default>
					<TopList
						:page="page"
						:language="languageSelected"
						:genres="genresSelected"
						:start-date="startDateSelected"
						:end-date="endDateSelected"
					/>
				</template>
				<template #fallback>
					Loading...
				</template>
			</Suspense>
		</div>
	</div>
</template>

<script>
import { useRoute } from 'vue-router'
import axios from "@/../config/axios";
import TopList from "@/components/topRating/TopList.vue";

export default {
	name: "TopRating",
	components: {
		TopList,
	},
	data() {
		return {
			page: 1,
			genres: [],
			languages: [],
			languageSelected: "",
			genresSelected: [],
			startDateSelected: "",
			endDateSelected: "",
		};
	},
	watch: {
		"$route": (to, from) => {
			if (to.path === from.path && JSON.stringify(to.query) !== JSON.stringify(from.query))
				location.reload();
		}
	},
	methods: {
		search() {
			let queries = {
				language: this.languageSelected,
				genres: this.genresSelected.join(","),
				"start-date": this.startDateSelected,
				"end-date": this.endDateSelected,
			};
			// If one query is empty, we remove it
			Object.keys(queries).forEach(key => {
				if (queries[key] === "") delete queries[key];
			});

			// Push query in url
			this.$router.push({
				name: this.$route.name,
				query: queries,
			});
		}
	},
	async beforeMount() {
		const route = useRoute()
		if (route.query.page) this.page = parseInt(route.query.page);
		if (route.query.language) this.languageSelected = route.query.language;
		if (route.query.genres) this.genresSelected = route.query.genres.split(",");
		if (route.query["start-date"]) this.startDateSelected = route.query["start-date"];
		if (route.query["end-date"]) this.endDateSelected = route.query["end-date"];
		
		const genresListResponse = await axios.get("/api/movie/genres");
		this.genres = genresListResponse.data

		const languagesListResponse = await axios.get("/api/movie/languages");
		this.languages = languagesListResponse.data;
	}
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";

.top-movie {
	margin: $margin-page;
	h1 {
		margin: 0;
		margin-bottom: 15px;
	}
	& > span {
		color: $font2-color;
		font-size: 18px;
	}
}
.main-movie {
	display: flex;
	margin: 0;
	margin-top: 50px;
	padding: 0;
	.movie-item {
		list-style: none;
		margin-bottom: 40px;
	}
}
.filter {
	width: 300px;
	min-width: 300px;
	padding: 30px;
	border-radius: 20px;
	border: 1px solid $main-color;
	background-color: $back-color;
	height: fit-content;
	> h3 {
		margin: 0;
		margin-bottom: 20px;
		font-size: 26px;
	}
	&__list {
	}
	&__group {
		margin-top: 20px;
		h3 {
			color: $font-color;
			font-weight: 500;
			font-size: 18px;
		}
	}
	&__input {
		padding: 8px;
		width: 100%;
		font-size: 16px;
		border-radius: 10px;
		border: 1px solid $font-color;
		background-color: $back2-color;
		color: $font-color;
		fill: $font-color;
		color-scheme: dark;
	}

	&-search {
		cursor: pointer;
		margin-top: 15px;
		padding: 8px;
		width: 100%;
		background-color: $main-color;
		border-radius: 50px;
		border: none;
		color: $back2-color;
		font-weight: 700;
		font-size: 19px;
		&:hover {
			background-color: $main2-color;
		}
	}
	&-date {
		display: flex;
		flex-direction: column;
		margin-top: 10px;
		label {
			display: inline-flex;
			align-items: center;
			margin-right: 10px;
			margin-bottom: 5px;
			width: 40px;
			min-width: 40px;
			color: $font2-color;
			font-size: 16px;
		}
	}
	&-genres {
		display: flex;
		flex-wrap: wrap;
		margin: 0;
		padding: 0;
		&__item {
			display: block;
			margin: 0 6px 8px 0;
			list-style: none;
			.genres-input {
				display: none;
				&:checked + .genres-label {
					background-color: $second-color;
					border-color: $second-color;
					color: $font-color;
				}
			}
			.genres-label {
				cursor: pointer;
				display: block;
				padding: 4px 12px;
				border: 1px solid $font2-color;
				border-radius: 50px;
				color: $font2-color;
				font-size: 14px;
				font-weight: 200;
			}
		}
	}
}
</style>