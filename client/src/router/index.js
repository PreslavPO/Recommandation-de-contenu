import { createRouter, createWebHistory, createWebHashHistory } from "vue-router"
import Home from "../views/Home.vue"

const routes = [
	{
		path: "/",
		name: "Home",
		component: Home,
		meta: {
			title: "TheMoviesualizer",
			titleShowName: false,
		},
	},
	{
		path: "/about",
		name: "About",
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () => import(/* webpackChunkName: "about" */ "../views/About.vue"),
		meta: {
			title: "About — TheMoviesualizer",
		},
	},
	{
		path: "/top",
		name: "Top",
		component: () => import("../views/TopRating.vue"),
		meta: {
			title: "Top Rating — TheMoviesualizer",
		},
	},
	{
		path: "/movie/:id(\\d+)",
		name: "Movie",
		component: () => import("../views/Movie.vue"),
		meta: {
			title: "Movie — TheMoviesualizer",
		},
	},
	{
		path: "/profile",
		name: "Profile",
		component: () => import("../views/Profile.vue"),
		meta: {
			title: "Profile — TheMoviesualizer",
		},
	},
	{
		path: "/:catchAll(.*)",
		component: () => import("../views/NotFound.vue"),
		meta: {
			title: "Page Not Found — TheMoviesualizer",
		},
	},
]

const router = createRouter({
	history: process.env.IS_ELECTRON ? createWebHashHistory() : createWebHistory(),
	routes
})

router.beforeEach((to, from, next) => {
	document.title = `${to.meta.title}`;
	next();
});

export default router;
