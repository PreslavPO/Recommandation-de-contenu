<template>
	<h1>You're logged in</h1>
	<button @click="$store.commit('LOGGED_OUT')">Logout</button>
	<button @click="test">Testing</button>
	<h2>Bienvenue {{ $store.state.user.username }}</h2>
	<h3>Votre email : {{ $store.state.user.email }}</h3>
</template>

<script>
export default {
	methods: {
		async test() {
			this.$store.dispatch("getRating")
				.then((res) => console.log(res))
				.catch((err) => console.error(err));
		}
	}
}
</script>