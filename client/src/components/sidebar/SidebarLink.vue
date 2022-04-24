<template>
	<li class="link-layout">
		<router-link :to="to" class="link">
			<slot />
			<span>{{ text }}</span>
		</router-link>
	</li>
</template>

<script>
export default {
	props: {
		to: { type: String, required: true },
		text: { type: String, required: true }
	},
}
</script>

<style lang="scss">
@import '../../assets/variables.scss';

.sidebar {
	.link-layout {
		display: block;
		width: 100%;
		padding: 0 10px;
		margin-top: 10px;
	}
	.link {
		position: relative;
		display: flex;
		align-items: center;
		padding: 15px;
		width: 100%;
		border-radius: 10px;
		color: $font2-color;
		svg {
			margin-right: 20px;
			width: 30px;
			height: 30px;
		}
		span {
			font-size: 16px;
		}
		&:hover {
			background-color: $back2-color;
		}
		&.router-link-exact-active {
			color: $font-color;
			&::before {
				position: absolute;
				content: " ";
				left: 0;
				width: 5px;
				height: 20px;
				border-radius: 25px;
				background-color: $main-color;
			}
		}
	}
}
</style>