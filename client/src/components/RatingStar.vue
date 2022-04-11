<template>
	<div class="score">
		<div class="score__icon" :class="{ gold: isGlobal }">
			<StarFillIcon />
		</div>
		<div class="score__details">
			<div class="details__title">
				<template v-if="score && score != -1">{{ score }}</template>
				<template v-else>-</template>
				<span v-if="isGlobal">/10</span>
			</div>
			<div v-if="isGlobal" class="details__subtitle">
				<template v-if="voteCount && voteCount != -1">{{ voteCount }} reviews</template>
				<template v-else>- reviews</template>
			</div>
			<div v-else class="details__subtitle">Your review</div>
		</div>
	</div>
</template>

<script>
import StarFillIcon from "@/components/icons/StarFillIcon.vue";

export default {
	name: "RatingStar",
	components: {
		StarFillIcon,
	},
	props: {
		isGlobal: Boolean,
		score: Number,
		voteCount: Number,
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
	}
}
</style>