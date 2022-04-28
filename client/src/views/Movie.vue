<template>
	<Suspense>
		<template #default>
			<MovieMain />
		</template>
		<template #fallback>
			Loading...
		</template>
	</Suspense>
	<Suspense>
		<template #default>
			<MovieCast />
		</template>
		<template #fallback>
			Loading...
		</template>
	</Suspense>
</template>

<script>
import MovieMain from "@/components/movieDetails/MovieMain.vue";
import MovieCast from "@/components/movieDetails/MovieCast.vue"

export default {
	name: "Movie",
	components: {
		MovieMain,
		MovieCast,
	},
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";

$element-space: 75px;
.background {
	display: flex;
	align-items: center;
	justify-content: center;
	margin: 30px;
	height: 400px;
	overflow: hidden;
	border-radius: 20px;
	img {
		filter: blur(2px);
		width: 100%;
	}
}

$poster-width: 350px;
.header {
	position: relative;
	margin: 0 $margin-content;
	margin-bottom: $element-space;
	&__poster {
		position: absolute;
		bottom: 0;
		overflow: hidden;
		border-radius: 20px;
		width: $poster-width;
		img {
			display: block;
			width: 100%;
		}
	}
	&__info {
		margin-left: $poster-width + 45px;
		h2 {
			margin: 0;
			font-size: 40px;
			font-weight: 600;
		}
		.subtitle {
			display: flex;
			align-items: center;
			flex-wrap: wrap;
			&__text {
				font-size: 16px;
				color: $font2-color;
				margin-right: 20px;
			}
			&__genre {
				display: flex;
				margin: 0;
				padding: 0;
				list-style: none;
				font-size: 16px;
				li {
					margin-right: 10px;
					padding: 5px 20px;
					border-radius: 50px;
					background-color: #2933FF;
				}
			}
		}
		.overview-text {
			margin: 0;
			margin-top: 20px;
			font-size: 16px;
		}
		.score-list {
			display: flex;
			grid-gap: 30px;
			margin-top: 30px;
		}
	}
}

$cast-spacing: 10px;
.cast {
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	margin: 0 $margin-content;
	margin-bottom: $element-space;
	.first-column {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		.cast__category:first-child {
			width: calc(percentage(1/3) - $cast-spacing);
		}
		.cast__category:last-child {
			width: percentage(2/3);
		}
	}
	&__category {
		width: 100%;
		&.one-column .cast__item {
			width: 100%;
		}
		&.two-column .cast__item {
			width: calc(percentage(1/2) - $cast-spacing);
		}
		&.three-column .cast__item {
			width: calc(percentage(1/3) - $cast-spacing);
		}
	}
	&__title {
		font-size: 20px;
		font-weight: 500;
		color: $font2-color;
	}
	&__list {
		display: flex;
		justify-content: space-between;
		flex-wrap: wrap;
		width: 100%;
		.cast__item {
			display: flex;
			flex-direction: row;
			margin-bottom: 20px;
			width: 100%;
			.cast__img {
				display: flex;
				align-items: center;
				justify-content: center;
				overflow: hidden;
				width: 85px;
				height: 85px;
				min-width: 85px;
				min-height: 85px;
				border-radius: 50%;
			}
			.cast__description {
				display: flex;
				flex-direction: column;
				justify-content: center;
				margin-left: 20px;
				.cast__name {
					font-size: 20px;
					color: $font-color;
				}
				.cast__subtitle {
					font-size: 16px;
					color: $font2-color;
				}
			}
		}
	}
}

@media (max-width: 1400px) {
	.background {
		height: 250px;
	}
	.header__poster {
		width: $poster-width/1.25;
	}
	.header__info {
		margin-left: $poster-width/1.25 + 45px;
	}

	.cast {
		.first-column {
			flex-direction: column;
			.cast__category {
				&:first-child, &:last-child {
					width: 100%;
				}
			}
		}
		&__category.three-column .cast__item {
			width: calc(percentage(1/2) - $cast-spacing);
		}
	}
}
@media (max-width: 1100px) {
	.cast__category {
		&.two-column, &.three-column {
			.cast__item {
				width: 100%;
			}
		}
	}
}
</style>