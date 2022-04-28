<template>
	<Transition name="modal">
		<div v-if="show" class="modal__mask">
			<div class="modal__wrapper">
				<div class="modal__container">
					<div class="modal__header">
						<slot name="header"></slot>
					</div>

					<div class="modal__body">
						<slot name="body"></slot>
					</div>

					<div class="modal__footer">
						<slot name="footer">
							<button
								class="modal-default-button"
								@click="$emit('close')"
							>
								OK
							</button>
						</slot>
					</div>
				</div>
			</div>
			<div class="modal__click-outside" @click="$emit('close')"></div>
		</div>
	</Transition>
</template>

<script>
export default {
	props: {
		show: Boolean,
	}
}
</script>

<style lang="scss">
@import "@/assets/variables.scss";

.modal {
	&__mask {
		position: fixed;
		z-index: 9998;
		display: flex;
		flex-direction: column;
		overflow-x: auto;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		transition: opacity 0.3s ease;
	}
	&__wrapper {
		position: relative;
		margin: auto;
		min-width: 300px;
		max-width: 600px;
	}
	&__container {
		position: relative;
		z-index: 997;
		margin: 10px;
		padding: 20px;
		border-radius: 10px;
		background-color: $back3-color;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
		transition: all 0.2s ease;
	}
	&__header {
		h2, h3, h4, h5 {
			margin: 0;
			margin-bottom: 15px;
			color: $main-color;
		}
	}
	&__body {
		margin: 10px 0;
		p {
			margin: 0;
		}
	}
	&__footer {
		display: flex;
		justify-content: end;
		button {
			cursor: pointer;
			margin-left: 10px;
			padding: 5px 15px;
			border: none;
			border-radius: 50px;
			background-color: $main-color;
			font-weight: 600;
			font-size: 16px;
			&:hover {
				background-color: $main2-color;
			}
		}
	}
	&__click-outside {
		position: absolute;
		z-index: 996;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
	}
}

/* Transition */
.modal-enter-from {
	opacity: 0;
}
.modal-leave-to {
	opacity: 0;
}
.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
	-webkit-transform: scale(1.1);
	transform: scale(1.1);
}
</style>