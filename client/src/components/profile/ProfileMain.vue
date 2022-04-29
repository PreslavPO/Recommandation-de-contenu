<template>
	<div class="profile">
		<div class="profile__title">
			<h1>Your profile</h1>
			<button @click="logout">Logout</button>
		</div>
		<div class="profile__header">
			<div class="profile__details">
				<h3>{{ $store.state.user.username }}</h3>
				<p>{{ $store.state.user.email }}</p>
			</div>
		</div>
		<div class="profile__contribution">
			<h2>Contribution</h2>
			<div class="contribution">
				<div class="contribution__group">
					<span class="contribution__number">-</span>
					<span class="contribution__title">Movie rated</span>
				</div>
				<div class="contribution__group">
					<span class="contribution__number">-</span>
					<span class="contribution__title">Rating over 5</span>
				</div>
				<div class="contribution__group">
					<span class="contribution__number">-</span>
					<span class="contribution__title">Rating under 5</span>
				</div>
				<div class="contribution__group">
					<span class="contribution__number">-</span>
					<span class="contribution__title">Average rating</span>
				</div>
			</div>
		</div>
		<div class="profile__rated-movies">
			<h2>My movies</h2>
			<Suspense>
				<template #default>
					<ProfileMovieList />
				</template>
				<template #fallback>
					Loading...
				</template>
			</Suspense>
		</div>
	</div>
</template>

<script>
import ProfileMovieList from "@/components/profile/ProfileMovieList.vue";

export default {
	components: {
		ProfileMovieList,
	},
	methods: {
		async logout() {
			this.$store.dispatch("signout");
		}
	}
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";

.profile {
	margin: $margin-page;
	&__title {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		button {
			cursor: pointer;
			padding: 7px 15px;
			border-radius: 50px;
			border: none;
			background-color: $main-color;
			&:hover {
				background-color: $main2-color;
			}
		}
	}
	&__header {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 30px;
		border-radius: 20px;
		background: linear-gradient(180deg, $main-color 0%, transparent 100%);
		.profile__details {
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;
			h3 {
				margin: 0;
				font-weight: 700;
				font-size: 24px;
			}
			p {
				margin: 0;
				margin-top: 15px;
				font-weight: 400;
				font-size: 18px;
				color: $font2-color;
			}
		}
	}
	&__contribution {
		.contribution {
			display: flex;
			flex-direction: row;
			justify-content: space-around;
			margin-top: 5px;
			padding: 30px;
			border-radius: 20px;
			background-color: $back3-color;
			&__group {
				display: flex;
				flex-direction: column;
				justify-content: center;
				align-items: center;
			}
			&__number {
				font-weight: 800;
				font-size: 32px;
			}
			&__title {
				font-weight: 400;
				font-size: 14px;
				color: $font2-color;
			}
		}
	}
	&__rated-movies {
	}
}
</style>