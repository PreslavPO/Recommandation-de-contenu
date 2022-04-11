<template>
	<div class="top-movie">
		<h1>Top Rating</h1>
		<span>Which is the best rated movie?</span>
		<ul class="movie-list">
			<Suspense>
				<template #default>
					<TopList :page="page" />
				</template>
				<template #fallback>
					Loading...
				</template>
			</Suspense>
		</ul>
	</div>
</template>

<script>
import { useRoute } from 'vue-router'
import TopList from "@/components/topRating/TopList.vue";

export default {
	name: "TopRating",
	components: {
		TopList,
	},
	data() {
		return {
			page: 1,
		};
	},
	beforeMount() {
		const route = useRoute()
		if (route.query.page)
			this.page = parseInt(route.query.page);
	}
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