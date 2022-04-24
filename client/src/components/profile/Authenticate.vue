<template>
	<form class="authenticate" name="signup_form">
		<label for="name">Name</label>
		<input v-model="name" type="text" name="name" class="authenticate__field" required />

		<label for="signup-email">Email</label>
		<input v-model="email" type="email" name="signup-email" class="authenticate__field" required />

		<label for="signup-password">Password</label>
		<input v-model="password" type="password" name="signup-password" class="authenticate__field" required />

		<input type="button" value="Save" @click="signup" /> <!--TODO : Validation and transform into submit-->
	</form>
</template>

<script>
import axios from "/config/axios";

export default {
	data() {
		return {
			name: "",
			email: "",
			password: "",
		}
	},
	methods: {
		signup() {
			console.log("signup");
			axios
				.post("/user/signup", { 
					name: this.name,
					email: this.email,
					password: this.password,
				})
				.then(res => console.log(res.data))
				.catch(err => console.error(err))
		}
	},
}
</script>

<style lang="scss">
</style>