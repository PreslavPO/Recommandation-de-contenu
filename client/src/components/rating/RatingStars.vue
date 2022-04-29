<template>
	<div
		class="rating-stars"
		@click="$emit('setScore', this.scoreHover)"
		@mouseleave="onMouseLeave"
		@mouseover="onMouseOver"
		ref="ratingStars"
	>
		<div class="empty-stars">
			<span v-for="i in 5" :key="i" class="star" :style="{'width': smallStar ? '30px' : ''}">
				<StarEmptyIcon />
			</span>
		</div>
		<div
			class="filled-stars"
			:style="{
				'width': 
					(percentageSize > 0 ? percentageSize : (score > 0 ? getPercentageByScore(score) : 0)) + '%'
			}"
		>
			<span v-for="i in 5" :key="i" class="star" :style="{'width': smallStar ? '30px' : ''}">
				<StarFillIcon />
			</span>
		</div>
	</div>
	<p v-if="!smallStar">
		{{ [
		"",
		"Awful",
		"Really bad",
		"Bad",
		"Not great",
		"Meh",
		"Not bad",
		"Good",
		"Really good",
		"Excellent",
		"Masterpiece"
		][this.scoreHover]
		}}
	</p>
</template>

<script>
import StarFillIcon from "@/components/icons/StarFillIcon.vue";
import StarEmptyIcon from "@/components/icons/StarEmptyIcon.vue";

export default {
	components: {
		StarFillIcon,
		StarEmptyIcon,
	},
	props: {
		score: Number,
		smallStar: Boolean,
	},
	emits: ["setScore"],
	data() {
		return {
			NB_HALF_STAR: 10,
			percentageSize: 0,
			scoreHover: 0,
			width: 0,
		}
	},
	mounted() {
		this.width = this.$refs.ratingStars.clientWidth;
	},
	methods: {
		getXPosition(event) {
			const rect = event.currentTarget.getBoundingClientRect();
			return event.clientX - rect.left;
		},
		getPercentageByScore(score) {
			const sizeContainer = this.width;
			const halfStarValuePx = sizeContainer / this.NB_HALF_STAR;

			const currValuePxRounded = score * halfStarValuePx;
			return (currValuePxRounded * 100) / sizeContainer;
		},
		onMouseLeave() {
			this.percentageSize = 0;
			this.scoreHover = 0;
		},
		onMouseOver(event) {
			const sizeContainer = this.width;
			const halfStarValuePx = sizeContainer / this.NB_HALF_STAR;
			const mousePos = this.getXPosition(event) + halfStarValuePx;
			
			this.scoreHover = ~~(mousePos / halfStarValuePx)
			const currValuePxRounded = this.scoreHover * halfStarValuePx;
			this.percentageSize = (currValuePxRounded * 100) / sizeContainer;
		}
	},
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";

.rating-stars {
	cursor: pointer;
	position: relative;
	display: inline-block;
	overflow: hidden;
	white-space: nowrap;
	.empty-stars {
		display: inline-block;
		color: $font-color;
	}
	.filled-stars {
		position: absolute;
		display: inline-block;
		overflow: hidden;
		top: 0;
		left: 0;
		color: $main-color;
	}
	.star {
		display: inline-block;
		width: 40px;
		//height: 40px;
		svg {
			width: 100%;
			height: 100%;
		}
	}
}
</style>