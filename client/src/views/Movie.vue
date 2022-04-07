<template>
	<div class="background">
		<img :src="background_path" :alt="'background of ' + title">
	</div>
	<div class="header">
		<div class="header__poster">
			<img :src="poster_path" :alt="'poster of ' + title">
		</div>
		<div class="header__info">
			<h2>{{ title }}</h2>
			<div class="subtitle">
				<span class="subtitle__text">{{ date }} — {{ duration }}</span>
				<ul class="subtitle__genre">
					<li v-for="genre in genres" :key="genre.id">
						{{ genre.name }}
					</li>
				</ul>
			</div>
			<p class="overview-text">{{ overview }}</p>
			<div class="score-list">
				<RatingStar :is-global="true" :score="score" :vote-count="vote_count" />
				<RatingStar :is-global="false" :score="userScore" />
			</div>
		</div>
	</div>
	<div class="cast">
		<div class="first-column">
			<div class="cast__category one-column" v-if="haveJob(person_crew, 'Director')">
				<h3 class="cast__title">Director</h3>
				<div class="cast__list">
					<div
						v-for="person in getPeopleByJob(person_crew, 'Director')"
						class="cast__item"
						:key="person.id"
					>
						<div class="cast__img">
							<img
								:src="person.profile_path"
								:alt="'Picture of ' + person.name"
							>
						</div>
						<div class="cast__description">
							<div class="cast__name">{{ person.name }}</div>
						</div>
					</div>
				</div>
			</div>
			<div class="cast__category two-column" v-if="haveJob(person_crew, 'Writer')">
				<h3 class="cast__title">Writer</h3>
				<div class="cast__list">
					<div
						v-for="person in getPeopleByJob(person_crew, 'Writer')"
						class="cast__item"
						:key="person.id"
					>
						<div class="cast__img">
							<img
								:src="person.profile_path"
								:alt="'Picture of ' + person.name"
							>
						</div>
						<div class="cast__description">
							<div class="cast__name">{{ person.name }}</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="second-column">
			<div class="cast__category three-column" v-if="person_cast.length > 0">
				<h3 class="cast__title">Starring</h3>
				<div class="cast__list">
					<div
						v-for="person in person_cast"
						class="cast__item"
						:key="person.id"
					>
						<div class="cast__img">
							<img
								:src="person.profile_path"
								:alt="'Picture of ' + person.name"
							>
						</div>
						<div class="cast__description">
							<div class="cast__name">{{ person.name }}</div>
							<div class="cast__subtitle">as {{ person.character }}</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import RatingStar from "@/components/RatingStar.vue";
import { useRoute } from "vue-router";
import axios from "/config/axios";

export default {
	name: "Movie",
	components: {
		RatingStar,
	},
	data() {
		return {
			id: "",
			title: "Interstellar",
			poster_path: "/no-poster.png",
			background_path: "",
			date: "--/--/----",
			duration: "- mins",
			overview: "Loading ...",
			score: -1,
			vote_count: -1,
			genres: [{id: 35, name: "Sci-Fi"}, {id: 18, name: "Comedy"}],
			person_crew: [
				{id: 12, name: "Loading ...", job: "Director", profile_path: "/no-image.png"},
				{id: 12, name: "Loading ...", job: "Writer", profile_path: "/no-image.png"},
			],
			person_cast: [
				{id: 125, order: 0, character: "---", name: "Loading ...", profile_path: "/no-image.png"},
			],
			userScore: -1,
		}
	},
	methods: {
		/** @return {boolean} */
		haveJob(list, job) {
			return list.some(person => person.job === job);
		},
		/** @return {[{id: number, name: String, job: String, profile_path: String}]} */
		getPeopleByJob(list, job) {
			return list.filter(person => person.job === job);
		},
		/** @return {string} */
		getThumbnail(name, imgDefault, c) {
			let image_url = "https://image.tmdb.org/t/p/w500" + name;
			let image = new Image();

			image.onload = function() {
				c(image_url);
			}
			image.onerror = function() {
				c(imgDefault);
			}

			image.src = image_url;
		}
	},
	mounted() {
		const route = useRoute();
		document.title = `${route.params.id} — TheMoviesualizer`;
		this.id = route.params.id;
		const base_url = "https://image.tmdb.org/t/p";

		axios
			.get(`/api/movie/${this.id}`)
			.then(res => res.data)
			.then(data => {
				this.title = data.title;
				this.poster_path = data.poster_path;
				this.score = data.vote_average;
				this.vote_count = data.vote_count;
				this.duration = data.runtime;
				this.overview = data.overview;
				this.date = new Date(data.release_date);

				// Convert date
				this.date = this.date.toLocaleDateString();

				// Convert duration
				this.duration = Math.floor(this.duration/60) + "h " + this.duration%60 + "mins";

				// Images Path
				this.poster_path = `${base_url}/w500${this.poster_path}`;
				this.background_path = `${base_url}/original/xJHokMbljvjADYdit5fK5VQsXEG.jpg`;

				this.getThumbnail(
					this.poster_path,
					"/no-poster.png",
					(url) => { this.poster_path = url; }
				);
			})
			.catch(err => console.error(err))
		
		axios
			.get(`/api/movie/${this.id}/credits`)
			.then(res => res.data)
			.then(data => {
				this.person_cast = data.cast;
				this.person_crew = data.crew;

				this.person_crew.forEach(p => {
					this.getThumbnail(
						p.profile_path,
						"/no-image.png",
						(url) => { p.profile_path = url; }
					);
				});
				this.person_cast.forEach(p => {
					this.getThumbnail(
						p.profile_path,
						"/no-image.png",
						(url) => { p.profile_path = url; }
					);
				});
			})
	},
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