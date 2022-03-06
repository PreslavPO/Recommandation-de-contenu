<template>
	<div class="hello">
		<h2>{{ msg }}</h2>
		<h3>Movies</h3>
		<ul>
			<li><router-link to="/movie/127564">Interstellar</router-link></li>
			<li><router-link to="/movie/787652">Blade Runner 2049</router-link></li>
			<li><router-link to="/movie/45624">Forrest Gump</router-link></li>
		</ul>
	</div>
</template>

<script>
export default {
	name: "HelloWorld",
	props: {
		msg: String,
	},
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
	margin: 40px 0 0;
}
ul {
	list-style-type: none;
	padding: 0;
}
li {
	display: inline-block;
	margin: 0 10px;
}
a {
	color: #42b983;
}
</style>
