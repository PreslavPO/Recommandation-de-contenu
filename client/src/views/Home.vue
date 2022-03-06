<template>
	<div class="home">
		<div class="logo__wrapper">
			<img alt="TheMoviesualizer logo" src="../assets/logo.svg">
			<h1>The<span>Movie</span>sualizer</h1>
		</div>
		<HelloWorld :msg="title" />
	</div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import axios from "/config/axios";

export default {
	name: "Home",
	components: {
		HelloWorld
	},
	data() {
		return {
			title: "Chargement...",
		}
	},
	mounted() {
		axios
			.get("/api/hello")
			.then(res => this.title = res.data.message)
			.catch(err => console.error(err))
	},
}
</script>

<style lang="scss">
@import "../assets/variables.scss";

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
</style>