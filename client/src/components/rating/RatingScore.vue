<template>
	<div class="score" @click="openTab">
		<div class="score__icon" :class="{ gold: isGlobal }">
			<StarFillIcon />
		</div>
		<component
			:is="showClickRating ? 'a' : 'div'"
			v-on="showClickRating ? { click: { prevent: openTab } } : {}"
			:class="'score__details ' + (showClickRating ? 'score__click' : '')"
		>
			<div class="details__title">
				<template v-if="rating && rating != -1">{{ rating }}</template>
				<template v-else>-</template>
				<span v-if="isGlobal">/10</span>
			</div>
			<div v-if="isGlobal" class="details__subtitle">
				<template v-if="voteCount && voteCount != -1">{{ voteCount }} reviews</template>
				<template v-else>- reviews</template>
			</div>
			<div v-else class="details__subtitle">Your review</div>
		</component>
	</div>

	<Teleport to="div#main" v-if="showClickRating">
		<Modal :show="showModal" @close="showModal = false">
			<template #header>
				<h3>{{ movieTitle }}</h3>
			</template>
			<template #body>
				<RatingStars
					:score="rating"
					@set-score="setNewScore"
					@delete-score="deleteScore"
				/>
			</template>
		</Modal>
	</Teleport>
</template>

<script>
import StarFillIcon from "@/components/icons/StarFillIcon.vue";
import Modal from "@/components/Modal.vue";
import RatingStars from "@/components/rating/RatingStars.vue";

export default {
	components: {
		StarFillIcon,
		Modal,
		RatingStars,
	},
	props: {
		isGlobal: Boolean,
		score: Number,
		voteCount: Number,
		movieId: Number,
		movieTitle: String,
	},
	data() {
		return {
			showModal: false,
			rating: -1,
			showClickRating: false,
		}
	},
	methods: {
		openTab() {
			this.showModal = true;
		},
		async setNewScore(score) {
			this.$store.dispatch("setRating", { "movieId": this.$props.movieId, score })
				.then((res) => {
					console.log(res.message);
					this.rating = score;
				})
				.catch((err) => console.error(err));
		},
		async deleteScore() {
			this.$store.dispatch("deleteRating", this.$props.movieId)
				.then((res) => {
					console.log(res.message);
					this.rating = 0;
				})
				.catch((err) => console.error(err));
		},
	},
	created() {
		this.showClickRating = !this.isGlobal && this.$store.state.isLogged;

		// User Rating
		if (!this.isGlobal && this.$store.state.isLogged) {
			this.$store.dispatch("getRating", this.movieId)
				.then((res) => {
					if (res.rating)
						this.rating = res.rating;
				})
				.catch(() => this.rating = -1);
		}
		else {
			this.rating = this.score;
		}
	},
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";

.score {
	display: flex;
	&__icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 50px;
		height: 50px;
		min-width: 50px;
		min-height: 50px;
		border-radius: 50%;
		background-color: $back3-color;
		svg {
			color: $font-color;
		}

		&.gold {
			background-color: $main-color;
			svg {
				color: $back2-color;
			}
		}
	}
	&__details {
		margin-left: 15px;
		.details__title {
			font-size: 32px;
			font-weight: 600;
			span {
				font-size: 16px;
				color: $font2-color;
			}
		}
		.details__subtitle {
			font-size: 16px;
			color: $font2-color;
		}
		&.score__click {
			cursor: pointer;
			&:hover {
				text-decoration: underline;
			}
		}
	}
}
</style>