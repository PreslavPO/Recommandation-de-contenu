<template>
	<div class="bigCard">
		<router-link :to="'/movie/' + movie.id" class="bigCard__poster">
			<img :src="movie.poster_path" :alt="'poster of ' + movie.title">
		</router-link>
		<div class="bigCard__info">
			<router-link :to="'/movie/' + movie.id" class="bigCard__link--title">
				<h3>{{ movie.title }}</h3>
			</router-link>
			<div class="subtitle">
				<span class="subtitle__text">{{ movie.release_date }} — {{ movie.runtime }}</span>
				<ul class="subtitle__genre">
					<li v-for="genre in movie.genres" :key="genre.id">
						{{ genre.name }}
					</li>
				</ul>
			</div>
			<p class="overview-text">{{ movie.overview }}</p>
			<div class="score-list">
				<RatingStar :is-global="true" :score="movie.vote_average" :vote-count="movie.vote_count" />
				<RatingStar :is-global="false" :score="-1" />
			</div>
		</div>
	</div>
</template>

<script>
import RatingStar from "@/components/RatingStar.vue";

export default {
	name: "BigCard",
	props: {
		movie: {
			id: Number,
			title: String,
			poster_path: String,
			release_date: Date,
			runtime: Number,
			overview: String,
			vote_average: Number,
			vote_count: Number,
			genres: Array,
		}
	},
	components: {
		RatingStar,
	},
	data() {
		return {
		}
	},
	async created() {
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
		
		// Convert date
		this.movie.release_date = new Date(this.movie.release_date).toLocaleDateString();

		// Convert duration
		this.movie.runtime = `${~~(this.movie.runtime/60)}h ${this.movie.runtime%60}mins`;

		// Images Path
		this.movie.poster_path = await getThumbnail(
			this.movie.poster_path,
			"/no-poster.png"
		);
	},
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";

.bigCard {
	display: flex;
	&__poster {
		overflow: hidden;
		border-radius: 20px;
		width: 200px;
		min-width: 200px;
		img {
			display: block;
			width: 100%;
		}
	}
	&__info {
		margin-left: 30px;
		h3 {
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
	&__link--title:hover h3 {
		color: $main-color;
	}
}
</style>