import { defineStore } from 'pinia';

export const useFileStore = defineStore('fileStore', {
  state: () => ({
	files: [], 
  }),
  actions: {
	addFiles(newFiles) {
		const filesWithId = newFiles.map(file => ({
		  id: Date.now() + Math.random(), // Генерация уникального ID
		  file, // Сохраняем сам файл
		}));
		this.files.push(...filesWithId); // Добавляем новые файлы в массив
	  },
	  addFile(file) {
		const fileWithId = {
		  id: Date.now() + Math.random(), // Генерация уникального ID
		  file, // Сохраняем сам файл
		};
		this.files.push(fileWithId); // Добавляем один файл в массив
	  },
	  removeFile(fileId) {
		this.files = this.files.filter(file => file.id !== fileId); // Удаляем файл по ID
	  },
	  clearFiles() {
		this.files = []; // Очищаем массив файлов
	  },
  },
});
