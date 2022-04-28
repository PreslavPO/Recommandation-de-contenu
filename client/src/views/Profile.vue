<template>
	<Authenticate v-if="!$store.state.isLogged" />
	<ProfileDetails v-else />
</template>

<script>
import Authenticate from "@/components/profile/Authenticate.vue";
import ProfileDetails from "@/components/profile/ProfileDetails.vue";

export default {
	name: "Profile",
	components: {
		Authenticate,
		ProfileDetails,
	},
}
</script>