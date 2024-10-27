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
        const response = await apiClient.post('/create_task', formData, {withCredentials: true,
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
      
        console.error('Ошибка при проверке токена:', error);
    }
}

export const checkToken = async () => {
    try {
        
        let a = await apiClient.post('/is_authenticated', null, {withCredentials: true, headers: {"Content-Type": "application/json"}});
        console.log(a)
        return true;
    } catch (error) {
        console.error('Ошибка при проверке токена:', error);
        return false;
    }
}

export const getTasks = async () => {
    try {
     
        let a = await apiClient.post('/get_my_tasks', null, {withCredentials: true, headers: {"Content-Type": "application/json"}});
 
        return a;
    } catch (error) {
        console.error('Ошибка при получении:', error);
        return false;
    }
}


export const getOriginalFile = async (task_id, filename) =>{
    try {
     
        let response = await apiClient.post('/get_original_file', {"task_id":task_id}, {withCredentials: true, headers: {"Content-Type": "application/json"},responseType: 'blob'});
        
        const url = window.URL.createObjectURL(new Blob([response.data]));


        const contentDisposition = response.headers['content-disposition'];
       

        if (contentDisposition && contentDisposition.indexOf('attachment') !== -1) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
            if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, ''); 
            }
        }

        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename); 
        document.body.appendChild(link);
        link.click();
        link.remove();
        
        return a;
    } catch (error) {
        console.error('Ошибка при получении:', error);
        return false;
    }

}

export const getProccesedlFile = async (task_id) =>{
    try {
     
        let a = await apiClient.post('/get_my_tasks',{"task_id":task_id}, {withCredentials: true, headers: {"Content-Type": "application/json"}});
      
        return a;
    } catch (error) {
        console.error('Ошибка при получении:', error);
        return false;
    }

}


export const deleteTask = async (task_id) =>{
    try {
     
        let a = await apiClient.post('/delete_task',{"task_id":task_id}, {withCredentials: true, headers: {"Content-Type": "application/json"}});
    
        return true;
    } catch (error) {
        console.error('Ошибка при удалении:', error);
        return false;
    }


}