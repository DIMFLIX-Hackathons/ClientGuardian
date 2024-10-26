import axios from 'axios'
import { useFileStore } from '@/store/files';
// import { router } from '@/router/index';
    
const apiClient = axios.create({
    baseURL: process.env.VUE_APP_API_URL + '/api',
    
    headers: {
        'Content-Type': 'application/json'
    }
});

export const createTask = async () => {
    const fileStore = useFileStore();
    const formData = new FormData();
    fileStore.files.forEach(file => {formData.append('files', file.file);});

    try {
        const response = await apiClient.post('/create_task', formData, {
            headers: {'Content-Type': 'multipart/form-data'},
        });
        console.log('Файлы успешно загружены:', response.data);
    } catch (error) {
        console.error('Ошибка при загрузке файлов:', error);
    }
};
    

export const auth = async (token, router) => {
    try {
        let a = await apiClient.post('/auth', {token: token}, {withCredentials: true, headers: {"Content-Type": "application/json"}})
        console.log(a)
        router.push("/");
    } catch (error) {
        console.log("ятутабля")
        console.error('Ошибка при проверке токена:', error);
    }
}

export const checkToken = async () => {
    try {
        console.log("Проверяю токен")
        let a = await apiClient.post('/is_authenticated', null, {withCredentials: true, headers: {"Content-Type": "application/json"}});
        console.log(a)
        return true;
    } catch (error) {
        console.error('Ошибка при проверке токена:', error);
        return false;
    }
}