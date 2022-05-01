<template>
	<header class="sidebar">
		<ul class="menu">
			<SidebarLink to="/" text="Home"><HomeIcon /></SidebarLink>
			<SidebarLink to="/top" text="Top rating"><TicketIcon /></SidebarLink>
			<hr />
			<SidebarLink to="/recommended" text="Recommended for you"><CandlestickIcon /></SidebarLink>
		</ul>
		<div class="bottom">
			<SidebarLink to="/profile" :text="$store.state.user.username || 'Login or Sign Up'"><UserBoxIcon /></SidebarLink>
		</div>
	</header>
</template>

<script>
import SidebarLink from "./SidebarLink.vue";
import HomeIcon from "../icons/HomeIcon.vue";
import TicketIcon from "../icons/TicketIcon.vue";
import CandlestickIcon from "../icons/CandlestickIcon.vue";
import GearIcon from "../icons/GearIcon.vue";
import UserBoxIcon from "../icons/UserBoxIcon.vue";

export default {
	components: {
		SidebarLink,
		HomeIcon,
		TicketIcon,
		CandlestickIcon,
		GearIcon,
		UserBoxIcon,
	}
}
</script>

<style lang="scss">
@import '../../assets/variables.scss';

.sidebar {
	display: flex;
	flex-direction: column;
	height: 100%;
	width: 275px;
	min-width: 275px;
	.menu {
		flex: 1 1 auto;
		margin: 0;
		padding: 0;
		overflow-x: hidden;
		overflow-y: scroll;
		-ms-overflow-style: none;
		scrollbar-width: none;
		hr {
			border: 1px solid $back2-color;
		}
		&::-webkit-scrollbar {
			display: none;
			background: transparent;
		}
	}
	.bottom {
		display: flex;
		flex: 0 0 auto;
	}
}
</style>