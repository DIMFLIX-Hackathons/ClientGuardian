import axios from 'axios'
import { useFileStore } from '@/store/files';
    
const apiClient = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    timeout: 1000,
    headers: {
        'Content-Type': 'application/json'
    }
});

export const createTask = async () => {
    const fileStore = useFileStore();
    const formData = new FormData();
    fileStore.files.forEach(file => {formData.append('files', file.file);});

    try {
        const response = await apiClient.post('/api/create_task', formData, {
            headers: {'Content-Type': 'multipart/form-data'},
        });
        console.log('Файлы успешно загружены:', response.data);
    } catch (error) {
        console.error('Ошибка при загрузке файлов:', error);
    }
};
    
