<template>
	<div class="home">
		<div class="logo__wrapper">
			<img alt="TheMoviesualizer logo" src="../assets/logo.svg">
			<h1>The<span>Movie</span>sualizer</h1>
		</div>
		<h3>Might interest you</h3>
		<ul class="interest-list">
			<li class="interest-item" v-for="i in 7" :key="i">
				<!--<SmallCard />-->
			</li>
		</ul>
	</div>
</template>

<script>
// @ is an alias to /src
import SmallCard from "@/components/movieCards/SmallCard.vue";
import axios from "/config/axios";

export default {
	name: "Home",
	components: {
		SmallCard,
	},
}
</script>

<style lang="scss">
@import "../assets/variables.scss";

.home {
	margin: $margin-page;
	h3 {
		margin: 0;
	}
}

.logo__wrapper {
	display: flex;
	flex-direction: column;
	margin: auto;
	margin-top: 25px;
	width: fit-content;
	img {
		margin-left: 78px;
		width: 115px;
	}
	h1 {
		margin: 0;
		font-size: 40px;
		span {
			color: $main-color;
		}
	}
}

.interest-list {
	display: flex;
	justify-content: space-between;
	margin: 0;
	margin-top: 30px;
	padding: 0;
	.interest-item {
		list-style: none;
		margin-bottom: 40px;
	}
}
</style>