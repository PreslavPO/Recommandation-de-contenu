<template>
	<Authenticate v-if="!$store.state.isLogged" />
	<ProfileMain v-else />
</template>

<script>
import Authenticate from "@/components/profile/Authenticate.vue";
import ProfileMain from "@/components/profile/ProfileMain.vue";

export default {
	name: "Profile",
	components: {
		Authenticate,
		ProfileMain,
	},
}
</script>