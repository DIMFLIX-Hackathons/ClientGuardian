<script setup>
import DropFile from "../components/DropFile.vue";
import FileToServer from "../components/FileToServer.vue"
import Task from "../components/Task.vue"
import { ref, onMounted } from 'vue';
import { useFileStore } from '@/store/files';
import { createTask, getTasks } from '@/modules/api'

const fileStore = useFileStore();
const tasks_object = ref([])
const tasks = ref([])

onMounted(async()=>{
    tasks_object.value = await getTasks()
    // console.log(tasks_object.value["data"]["tasks"][0])
    tasks.value = tasks_object.value["data"]["tasks"]
    
})

function removeTask(index){
    tasks.value.splice(index,1);
    console.log(index)
}

function createTaskProcess() {
    createTask()
    fileStore.clearFiles()
}
</script>

<template>
    <div class="container">
        <div class="task_form">
            <div class="drop_file">
                <DropFile/>
            </div>
            <div class="files_to_server" :class="{invisible:fileStore.files.length<1}">
                <FileToServer :file="file.file" :file_id="file.id" v-for="file in fileStore.files" class="file"/>
            </div>
            <div class="create_task" @click="createTaskProcess">
                <span onselectstart="return false" onmousedown="return false">Создать задачу</span>
            </div>
        </div>
        <div class="history_task">
            <div class="title">
                <span>История Ваших задач</span>
            </div>
            <div class="list_of_task">
                <Task 
                    v-for="(task, index) in tasks" 
                    :key="index" 
                    :task_id="task.id"
                    :status="task.status" 
                    :filename="task.original_filename"
                    :data="task.created_at" 
                    @remove="removeTask(index)"
                />
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.invisible{
    display:none !important;
}
::-webkit-scrollbar {
    display: none;
}
.container {
    display: flex;
    background-color: rgb(30, 30, 46);
    max-height: 100%;
    height: 100%;
    justify-content: center;
    align-items: center;
    gap: 30px;
}

.task_form {
    width: 25%;
    max-height: 70%;
    height: 70%;
    padding: 30px 30px;
    background-color: #28283E;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    
    gap: 20px;
    

    .drop_file {
        width: 100%;
        height: 100%;
    }
    

    .files_to_server {
        width: 100%;
        max-height: 25%;
        background-color: #353550;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        
        overflow-y: auto;
        gap: 10px;
        padding: 10px;
        box-sizing: border-box;
        
        .file {
            height: 50px;
        }
    }

    .create_task {
        width: 100%;
        min-height: 80px;
        background-color: #B4BEFE;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;

        span {
            font-size: 24px;
            font-weight: 600;
            color: white;
        }
    }
}





.history_task {
    width: 40%;
    max-height: 76%;
    height: 76%;
    background-color: #28283E;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;

    .title {
        margin: 4%;

        span {
            font-size: 32px;
            font-weight: 600;
            color: white;
        }
    }

    .list_of_task {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        overflow-y: auto;
        padding-bottom: 15px;
    }

    .list_of_task::-webkit-scrollbar {
        display: none;
    }
}
</style>