<template>
	<div class="smallCard">
		<router-link :to="'/movie/' + id" class="smallCard__poster">
			<img :src="poster_path" :alt="'poster of ' + title">
		</router-link>
		<div class="smallCard__info">
			<div class="smallCard__subtitle">
				<div class="smallCard__score">
					<StarFillIcon />
					<span>{{ score }}</span>
				</div>
				<span>{{ date }}</span>
			</div>
			<router-link :to="'/movie/' + id" class="smallCard__link--title">
				<h5>{{ title }}</h5>
			</router-link>
		</div>
	</div>
</template>

<script>
import StarFillIcon from "@/components/icons/StarFillIcon.vue";

export default {
	name: "SmallCard",
	components: {
		StarFillIcon,
	},
	data() {
		return {
			id: "183",
			title: "Interstellar",
			poster_path: "",
			date: new Date(),
			score: 8.2,
		}
	},
	mounted() {
		// Convert date
		this.date = this.date.getFullYear();

		// Images Path
		const base_url = "https://image.tmdb.org/t/p";
		this.poster_path = `${base_url}/w500/1pnigkWWy8W032o9TKDneBa3eVK.jpg`;
	},
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";
.smallCard {
	display: flex;
	flex-direction: column;
	width: 150px;
	&__poster {
		border-radius: 20px;
		overflow: hidden;
	}
	&__info {
		margin-top: 5px;
		.smallCard__subtitle {
			display: flex;
			justify-content: space-between;
			align-items: center;
			.smallCard__score {
				display: flex;
				align-items: center;
				svg {
					color: $main-color;
					width: 22px;
					height: 22px;
				}
				span {
					font-size: 16px;
				}
			}
			& > span {
				font-size: 16px;
				color: $font2-color;
				font-weight: 300;
			}
		}
		h5 {
			margin: 0;
			margin-top: 5px;
			font-size: 18px;
			font-weight: 300;
		}
	}
	&__link--title h5:hover {
		color: $main-color;
	}
}
</style>