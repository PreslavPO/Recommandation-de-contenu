<template>
	<div id="main">
		<Sidebar />
		<main class="content">
			<div class="content__wrapper">
				<router-view/>
			</div>
		</main>
	</div>
</template>

<script>
import Sidebar from "@/components/sidebar/Sidebar.vue";

export default {
	components: { Sidebar }
}
</script>

<style lang="scss">
@import './assets/fonts.scss';
@import './assets/normalize.scss';
@import './assets/variables.scss';

* {
	box-sizing: border-box;
}

html,
body {
	display: block;
	background-color: $back-color;
	color: $font-color;
	fill: $font-color;
	font-size: 20px;
	font-family: $main-font;
	min-height: 100vh;
	height: 100%;
	overflow: auto;
}

div, textarea, table, td, th, code, pre, samp {
	word-wrap: break-word;
	-webkit-hyphens: auto;
	-moz-hyphens: auto;
	-ms-hyphens: auto;
	-o-hyphens: auto;
	hyphens: auto;
}

img, table, td, blockquote, code, pre, textarea, input, video {
    max-width: 100%;
}

a {
	color: inherit;
	text-decoration: none;
}
a img {
	border: 0;
}

h1, h2, h3, h4, h5, h6 {
	color: $font-color;
	word-break: break-word;
}

body, #app, #main {
	width: 100%;
	height: 100%;
}

#app {
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
}

#main {
	position: relative;
	display: flex;
	flex: 1 1 auto;
	.content {
		position: relative;
		display: flex;
		flex: 1 1 auto;	
		align-items: stretch;
		background-color: $back2-color;
		border-radius: 20px 0 0 0;
		min-width: 800px;
		&__wrapper {
			position: absolute;
			top: 0;
			bottom: 0;
			left: 0;
			right: 0;
			height: 100%;
			overflow-y: scroll;
			overflow-x: hidden;
			&::-webkit-scrollbar {
				width: 10px;
			}
			&::-webkit-scrollbar-thumb {
				min-height: 40px;
				border-radius: 20px;
				background-color: #5a5a5a;
			}
		}
	}
}
</style>