<template>
	<div class="cast">
		<div class="first-column">
			<div class="cast__category one-column" v-if="haveJob(credits.person_crew, 'Director')">
				<h3 class="cast__title">Director</h3>
				<div class="cast__list">
					<div
						v-for="person in getPeopleByJob(credits.person_crew, 'Director')"
						class="cast__item"
						:key="person.id"
					>
						<div class="cast__img">
							<img
								:src="person.profile_path"
								:alt="'Picture of ' + person.name"
							>
						</div>
						<div class="cast__description">
							<div class="cast__name">{{ person.name }}</div>
						</div>
					</div>
				</div>
			</div>
			<div class="cast__category two-column" v-if="haveJob(credits.person_crew, 'Writer')">
				<h3 class="cast__title">Writer</h3>
				<div class="cast__list">
					<div
						v-for="person in getPeopleByJob(credits.person_crew, 'Writer')"
						class="cast__item"
						:key="person.id"
					>
						<div class="cast__img">
							<img
								:src="person.profile_path"
								:alt="'Picture of ' + person.name"
							>
						</div>
						<div class="cast__description">
							<div class="cast__name">{{ person.name }}</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="second-column">
			<div class="cast__category three-column" v-if="credits.person_cast.length > 0">
				<h3 class="cast__title">Starring</h3>
				<div class="cast__list">
					<div
						v-for="person in credits.person_cast"
						class="cast__item"
						:key="person.id"
					>
						<div class="cast__img">
							<img
								:src="person.profile_path"
								:alt="'Picture of ' + person.name"
							>
						</div>
						<div class="cast__description">
							<div class="cast__name">{{ person.name }}</div>
							<div class="cast__subtitle">as {{ person.character }}</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { ref } from "vue";
import axios from "@/../config/axios";
import { useRoute } from "vue-router";

export default {
	methods: {
		/** @return {boolean} */
		haveJob(list, job) {
			return list.some(person => person.job === job);
		},
		/** @return {[{id: number, name: String, job: String, profile_path: String}]} */
		getPeopleByJob(list, job) {
			return list.filter(person => person.job === job);
		},
	},
	async setup() {
		const base_url = "https://image.tmdb.org/t/p";

		/**
		 * Get image if correct path or else get default image
		 */
		const getThumbnail = (name, imgDefault) => {
			return new Promise((resolve, reject) => {
				let imageUrl = `${base_url}/w500${name}`;
				let image = new Image();

				image.onload = () => resolve(imageUrl);
				image.onerror = () => resolve(imgDefault);
				image.src = imageUrl;
			});
		}

		const route = useRoute();
		let credits = ref(null);
		const creditsResponse = await axios.get(`/api/movie/${route.params.id}/credits`);
		const creditsData = creditsResponse.data;

		let creditsComputed = {};
		creditsComputed.person_cast = creditsData.cast;
		creditsComputed.person_crew = creditsData.crew;
		
		creditsComputed.person_cast = creditsData.cast.map(async p => {
			let newPerson = p;
			newPerson.profile_path = await getThumbnail(
				p.profile_path,
				"/no-image.png"
			);

			return newPerson;
		});
		creditsComputed.person_cast = await Promise.all(creditsComputed.person_cast);
		
		creditsComputed.person_crew = creditsData.crew.map(async p => {
			let newPerson = p;
			newPerson.profile_path = await getThumbnail(
				p.profile_path,
				"/no-image.png"
			);

			return newPerson;
		});
		creditsComputed.person_crew = await Promise.all(creditsComputed.person_crew);
		
		credits.value = creditsComputed;
		return {
			credits,
		};
	},
}
</script>

<style>
</style>