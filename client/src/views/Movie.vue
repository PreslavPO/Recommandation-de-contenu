<template>
	<h1>Movie</h1>
</template>

<script>
import { useRoute } from "vue-router";

export default {
	data() {
		return {
			id: "",
		}
	},
	mounted() {
		const route = useRoute();
		document.title = `${route.params.id} — TheMoviesualizer`;
		this.id = route.params.id;
	},
}
</script>