<template>
	<div class="home">
		<img alt="Vue logo" src="../assets/logo.png">
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
</style>