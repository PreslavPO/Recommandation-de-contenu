<template>
	<div class="recommended">
		<h1>Recommended for you</h1>
		<span>Which movie will you like?</span>
		<div>
			<Suspense>
				<template #default>
					<RecommendedMovieList />
				</template>
				<template #fallback>
					Loading...
				</template>
			</Suspense>
		</div>
	</div>
</template>

<script>
import RecommendedMovieList from "@/components/recommended/RecommendedMovieList.vue";

export default {
	name: "Recommended",
	components: {
		RecommendedMovieList,
	},
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";

.recommended {
	margin: $margin-page;
	h1 {
		margin: 0;
		margin-bottom: 15px;
	}
	& > span {
		color: $font2-color;
		font-size: 18px;
	}
}
</style>