<template>
	<div class="top-movie">
		<h1>Top Rating</h1>
		<span>Which is the best rated movie?</span>
		<ul class="movie-list">
			<li class="movie-item" v-for="i in 10" :key="i">
				<BigCard />
			</li>
		</ul>
	</div>
</template>

<script>
import BigCard from "@/components/movieCards/BigCard.vue";

export default {
	name: "TopRating",
	components: {
		BigCard,
	},
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
.movie-list {
	margin: 0;
	margin-top: 50px;
	padding: 0;
	.movie-item {
		list-style: none;
		margin-bottom: 40px;
	}
}
</style>