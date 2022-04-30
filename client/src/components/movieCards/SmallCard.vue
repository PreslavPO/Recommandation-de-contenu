<template>
	<div class="smallCard">
		<router-link :to="'/movie/' + movie.id" class="smallCard__poster">
			<img :src="movie.poster_path" :alt="'poster of ' + movie.title">
		</router-link>
		<div class="smallCard__info">
			<div class="smallCard__subtitle">
				<template v-if="!hasRating">
					<div class="smallCard__score">
						<StarFillIcon />
						<span>{{ movie.vote_average }}</span>
					</div>
					<span>{{ date }}</span>
				</template>
				<template v-else>
					<RatingStars
						:score="userRating || -1"
						:smallStar="true"
						@set-score="setNewScore"
					/>
				</template>
			</div>
			<router-link :to="'/movie/' + movie.id" class="smallCard__link--title">
				<h5>{{ movie.title }}</h5>
			</router-link>
		</div>
	</div>
</template>

<script>
import StarFillIcon from "@/components/icons/StarFillIcon.vue";
import RatingStars from "@/components/rating/RatingStars.vue";

export default {
	name: "SmallCard",
	props: {
		hasRating: Boolean,
		movie: {
			id: Number,
			title: String,
			poster_path: String,
			release_date: Date,
			vote_average: Number,
		},
	},
	components: {
		StarFillIcon,
		RatingStars,
	},
	data() {
		return {
			userRating: -1,
			date: "----",
		}
	},
	methods: {
		async setNewScore(score) {
			this.$store.dispatch("setRating", { "movieId": this.movie.id, score })
				.then((res) => {
					console.log(res.message);
					this.userRating = score;
				})
				.catch((err) => console.error(err));
		},
		isValidDate(d) {
			return d instanceof Date && !isNaN(d);
		},
		convertDigitIn(str){
			return str.split('/').reverse().join('/');
		},
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
		const tempDate = new Date(this.movie.release_date);
		if (this.isValidDate(tempDate)) {
			this.date = tempDate.getFullYear();
		}
		else {
			this.date = new Date(this.convertDigitIn(this.movie.release_date)).getFullYear();
		}

		// Images Path
		this.movie.poster_path = await getThumbnail(
			this.movie.poster_path,
			"/no-poster.png"
		);

		// User Rating
		if (this.$store.state.isLogged) {
			this.$store.dispatch("getRating", this.movie.id)
				.then((res) => {
					if (res.rating)
						this.userRating = res.rating;
				})
				.catch(() => this.userRating = -1);
		}
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