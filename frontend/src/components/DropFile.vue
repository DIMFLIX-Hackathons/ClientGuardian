<script setup>
import { useDropzone } from 'vue3-dropzone';
import { useFileStore } from '@/store/files';
import { ref } from 'vue';

const fileStore = useFileStore();
const files = ref([]);

const { getRootProps, getInputProps, isDragActive } = useDropzone({
	onDrop: (acceptedFiles) => {
		console.log('Accepted files:', acceptedFiles);
		const validExtensions = ['xlsx', 'docx', 'pdf', "csv"];

		acceptedFiles.forEach(file => {
			const extension = file.name.split('.').pop();
			if (validExtensions.includes(extension)) {
				files.value.push(file);
				fileStore.addFile(file)
			} else {
				console.log("не то расширение");
			}
		});
	},
});
</script>

<template>
	<div class="dropzone" v-bind="getRootProps()">
		<input v-bind="getInputProps()" />
		<div class="dropzone-message" v-if="isDragActive">
			Release to drop files here.
		</div>
		<div class="dropzone-message" v-else>
			Drag & drop files here, <br>or click to select files.
		</div>
	</div>
</template>


<style scoped>
.dropzone {
	height: 100%;
	border: 2px dashed #B4BEFE;
	border-radius: 8px;
	text-align: center;
	transition: border-color 0.3s ease;
	display: flex;
	align-items: center;
	justify-content: center;
}

.dropzone:hover {
	border-color: #4a90e2;
}

.dropzone-message {
	font-size: 20px;
	font-weight: 400;
	color: white;

}

input[type='file'] {
	display: none;
}
</style>