<template>
	<div class="bigCard">
		<router-link :to="'/movie/' + id" class="bigCard__poster">
			<img :src="poster_path" :alt="'poster of ' + title">
		</router-link>
		<div class="bigCard__info">
			<router-link :to="'/movie/' + id" class="bigCard__link--title">
				<h3>{{ title }}</h3>
			</router-link>
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
				<RatingStar :is-global="true" :score="8.2" :vote-count="16234" />
				<RatingStar :is-global="false" :score="9" />
			</div>
		</div>
	</div>
</template>

<script>
import RatingStar from "@/components/RatingStar.vue";

export default {
	name: "BigCard",
	components: {
		RatingStar,
	},
	data() {
		return {
			id: "183",
			title: "Interstellar",
			poster_path: "",
			date: new Date(),
			duration: 171,
			overview: "Laboris laborum ex ullamco labore fugiat tempor nisi veniam consectetur. Sint nulla ut tempor ut cillum in qui eu labore do irure eiusmod. Sunt nostrud labore consectetur sint occaecat elit consectetur do.",
			score: 8.2,
			genres: [{id: 35, name: "Sci-Fi"}, {id: 18, name: "Comedy"}],
		}
	},
	mounted() {
		// Convert date
		this.date = this.date.toLocaleDateString();

		// Convert duration
		this.duration = Math.floor(this.duration/60) + "h " + this.duration%60 + "mins";

		// Images Path
		const base_url = "https://image.tmdb.org/t/p";
		this.poster_path = `${base_url}/w500/1pnigkWWy8W032o9TKDneBa3eVK.jpg`;
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