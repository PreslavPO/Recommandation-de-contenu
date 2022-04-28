import { createStore } from "vuex";
import axios from "/config/axios";

export default createStore({
	state: {
		isLogged: false,
		user: {},
	},
	mutations: {
		LOGGED_IN(state, user) {
			state.isLogged = true;
			state.user = user;
		},
		LOGGED_OUT(state) {
			state.isLogged = false;
			state.user = {};
		},
	},
	actions: {
		requestWithCredentials(context, axiosReq) {
			return new Promise((resolve, reject) => {
				axiosReq
					.then((res) => {
						resolve(res.data);
					})
					.catch((err) => {
						context.commit("LOGGED_OUT");
						if (err.response.data)
							reject(err.response.data);
						else if (err.request)
							console.error(err.request);
						else
							console.error("Error", err.message);
					});
			});
		},
		getRating(context) {
			return context.dispatch(
				"requestWithCredentials",
				axios.get("/user/rating")
			);
		}
	},
	modules: {
	},
});