<template>
	<header class="sidebar">
		<ul class="menu">
			<SidebarLink to="/" text="Home"><HomeIcon /></SidebarLink>
			<SidebarLink to="/top" text="Top rating"><TicketIcon /></SidebarLink>
			<SidebarLink to="/recommended" text="Recommended for you"><CandlestickIcon /></SidebarLink>
			<hr />
			<SidebarLink to="/settings" text="Settings"><GearIcon /></SidebarLink>
		</ul>
		<div class="profile">
			<SidebarLink to="/profile" text="Profile">👤</SidebarLink>
		</div>
	</header>
</template>

<script>
import SidebarLink from "./SidebarLink.vue";
import HomeIcon from "../icons/HomeIcon.vue";
import TicketIcon from "../icons/TicketIcon.vue";
import CandlestickIcon from "../icons/CandlestickIcon.vue";
import GearIcon from "../icons/GearIcon.vue";

export default {
	components: {
		SidebarLink,
		HomeIcon,
		TicketIcon,
		CandlestickIcon,
		GearIcon,
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
	.menu {
		flex: 1 1 auto;
		margin: 0;
		padding: 0;
		overflow-x: scroll;
		overflow-y: hidden;
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
	.profile {
		display: flex;
		flex: 0 0 auto;
	}
}
</style>