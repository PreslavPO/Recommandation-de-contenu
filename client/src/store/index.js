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
		logout(context) {
			context.commit("LOGGED_OUT");
			axios.post("/user/logout");
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
		deleteRating(context, movieId) {
			return context.dispatch(
				"requestWithCredentials",
				axios.delete(`/user/rating/${movieId}?userId=${context.state.user._id}`)
			);
		},
		getListRating(context, { page, sort_by }) {
			if (!page) page = 1
			if (!sort_by) sort_by = "last_rated"
			
			return context.dispatch(
				"requestWithCredentials",
				axios.get(`/user/rating?userId=${context.state.user._id}&page=${page}&sort_by=${sort_by}`)
			);
		},
		getRecommendation(context, page) {
			if (!page) page = 1
			
			return context.dispatch(
				"requestWithCredentials",
				axios.get(`/user/recommendation?userId=${context.state.user._id}&page=${page}`)
			);
		},
		getInformation(context) {
			return context.dispatch(
				"requestWithCredentials",
				axios.get(`/user/information?userId=${context.state.user._id}`)
			);
		},
	},
	modules: {
	},
});