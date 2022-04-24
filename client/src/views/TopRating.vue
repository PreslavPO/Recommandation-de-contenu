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
						<label for="start-date">From</label>
						<input type="date" id="start-date" v-model="startDateSelected" placeholder="xxxx-xx-xx" />
						<label for="end-date">To</label>
						<input type="date" id="end-date" v-model="endDateSelected" placeholder="xxxx-xx-xx" />
					</div>
					<div class="filter__group">
						<h3>By language</h3>
						<select v-model="languageSelected" name="languages" id="languages-select" class="filter__input">
							<option value="">No selection</option>
							<option
								v-for="genre in languages"
								:key="genre._id"
								:value="genre._id"
							>
								{{ genre.name }} ({{ genre.total }})
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
						<input type="button" value="Rechercher" @click="search">
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
		"$route.query": () => {
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
			}).then(() => location.reload()); // Force refresh
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

$element-space: 75px;
.top-movie {
	margin: $element-space;
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
	width: 200px;
	min-width: 200px;
	&__list {
	}
	&__group {
		h3 {
			color: $font2-color;
			font-weight: 500;
			font-size: 18px;
		}
	}
	&__input {
		width: 100%;
	}
}
select {
	border-radius: 10px;
}
</style>