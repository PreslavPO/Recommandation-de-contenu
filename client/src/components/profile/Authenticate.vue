<template>
	<div class="authenticate">
		<div class="authenticate__global">
			<div class="authenticate__container">
				<form class="authenticate__form" name="login_form">
					<h2>Login</h2>

					<label for="login-username">Username</label>
					<input v-model="login.username" type="text" name="login-username" required />

					<label for="login-password">Password</label>
					<input v-model="login.password" type="password" name="login-password" required />

					<p class="error">{{ login.error }}</p>

					<input type="button" value="Login" @click="loginSubmit" />
				</form>
			</div>
			<div class="authenticate__container">
				<form class="authenticate__form" name="signup_form">
					<h2>Create an account</h2>
					<label for="signup-username">Username</label>
					<input v-model="signup.username" type="text" name="signup-username" required />

					<label for="signup-email">Email</label>
					<input v-model="signup.email" type="email" name="signup-email" required />

					<label for="signup-password">Password</label>
					<input v-model="signup.password" type="password" name="signup-password" required />

					<p class="error">{{ signup.error }}</p>

					<input type="button" value="Sign Up" @click="signupSubmit" /> <!--TODO : Validation and transform into submit-->
				</form>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "/config/axios";

export default {
	data() {
		return {
			login: {
				username: "",
				password: "",
				error: "",
			},
			signup: {
				username: "",
				email: "",
				password: "",
				error: "",
			},
		}
	},
	methods: {
		async signupSubmit() {
			console.log("signup");
			try {
				const res = await axios.post("/user/signup", {
					username: this.signup.username,
					email: this.signup.email,
					password: this.signup.password,
				})
				if (res.data.status === "success") {
					console.log(res);
				}
			}
			catch (err) {
				if (err.response)
					this.signup.error = err.response.data.message;
				else if (err.request)
					console.error(err.request);
				else
					console.error("Error", err.message);
			}
		},
		async loginSubmit() {
			// TODO : Temporary to test connexion -> Remove it
			console.log("login");
			const resGet = await axios.get("/user");
			console.log(resGet);
			/*try {
				const res = await axios.post("/user/login", {
					username: this.login.username,
					password: this.login.password,
				})
				console.log(res.data)
			}
			catch (err) {
				if (err.response)
					this.login.error = err.response.data.message;
				else if (err.request)
					console.error(err.request);
				else
					console.error("Error", err.message);
			}*/
		},
	},
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";

.authenticate {
	display: flex;
	justify-content: center;
	align-items: center;
	width: 100%;
	height: 100%;
	&__global {
		display: flex;
		width: 100%;
		max-width: 1000px;
	}
	&__container {
		width: 50%;
		height: 100%;
	}
	&__form {
		display: flex;
		flex-direction: column;
		justify-content: center;
		padding: 0 50px;
		h2 {
			text-align: center;
			font-size: 30px;
			font-weight: 800;
		}
		.error {
			margin: 10px 0 5px 0;
			text-align: center;
			font-size: 14px;
			color: red;
		}
		label {
			margin-top: 8px;
			margin-bottom: 5px;
			color: $font2-color;
			font-weight: 300;
			font-size: 16px;
		}
		input {
			margin-bottom: 8px;
			padding: 12px 15px;
			font-size: 16px;
			border-radius: 8px;
			border: none;
			background-color: $back3-color;
			color: $font-color;
			&:focus {
				outline: none;
				box-shadow:
					0 0 0 2px $main-color,
					0 0 0 5px $main3-color;
			}
			&[type="button"] {
				cursor: pointer;
				margin-top: 15px;
				border-radius: 50px;
				background-color: $main-color;
				color: $back2-color;
				font-size: 18px;
				font-weight: 600;
				&:hover {
					background-color: $main2-color;
				}
			}
			// Remove default autofill style
			&:-webkit-autofill {
				-webkit-box-shadow: 0 0 0 1000px $back3-color inset !important;
				box-shadow: 0 0 0 1000px $back3-color inset !important;
				-webkit-text-fill-color: $font-color !important;
			}
			&:-webkit-autofill,
			&:-webkit-autofill:focus {
				transition: background-color 600000s 0s, color 600000s 0s;
			}
			&[data-autocompleted] {
				background-color: transparent !important;
			}
		}
	}
}
</style>