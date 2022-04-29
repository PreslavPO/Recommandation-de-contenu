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
		signout(context) {
			context.commit("LOGGED_OUT");
			axios.post("/user/signout");
		},
		requestWithCredentials(context, axiosReq) {
			return new Promise((resolve, reject) => {
				axiosReq
					.then((res) => {
						resolve(res.data);
					})
					.catch((err) => {
						if (err.response) {
							if (err.response.status === 401)
								context.commit("LOGGED_OUT");
							reject(err.response.data);
						}
						else if (err.request)
							console.error(err.request);
						else
							console.error("Error", err.message);
					});
			});
		},
		getRating(context, movieId) {
			return context.dispatch(
				"requestWithCredentials",
				axios.get(`/user/rating/${movieId}?userId=${context.state.user._id}`)
			);
		},
		setRating(context, { movieId, score }) {
			return context.dispatch(
				"requestWithCredentials",
				axios.post(`/user/rating/${movieId}?userId=${context.state.user._id}`, { score })
			);
		},
		getListRating(context, { page, sort_by }) {
			if (!page) page = 1
			if (!sort_by) sort_by = "last_rated"
			
			return context.dispatch(
				"requestWithCredentials",
				axios.get(`/user/rating/?userId=${context.state.user._id}&page=${page}&sort_by=${sort_by}`)
			);
		},
	},
	modules: {
	},
});