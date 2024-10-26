<script setup>
import good_status_svg from "../assets/svg/good_status_svg.vue"
import bad_status_svg from "../assets/svg/bad_status_svg.vue"
import wait_status_svg from "../assets/svg/wait_status_svg.vue"


// import read_svg from "../assets/svg/read_svg.vue"
import delete_svg from "../assets/svg/busket_svg.vue"
import ai_svg from "../assets/svg/ai_svg.vue"
import download_svg from "@/assets/svg/download_svg.vue"




const props = defineProps({
  
    status: String,
    filename: String,
    data: String
})
const emit = defineEmits([
    "remove"
])
function delete_task(){
    console.log("удалил")
    emit("remove");
    
}
</script>

<template>
    <div class="task">
        <div class="data">
            <div class="status">
                <good_status_svg v-if="props.status === 'completed'" />
                <bad_status_svg v-if="props.status === 'error'" />
                <wait_status_svg v-if="props.status === 'expectation'" />
            </div>
            <div class="filename_data_and_name">
                <div class="filename">
                    <span>{{ props.filename }}</span>
                </div>
                <div class="task_date">
                    <span v-if="props.status === 'completed'">Срок хранения: {{ data }}</span>
                    <span v-if="props.status === 'error'">Ошибка при обработке </span>
                </div>
            </div>
        </div>

        <div class="crud_task">
            <div class="original_download" v-if="props.status == 'completed'">
                <download_svg />
            </div>
            <div class="ai_download" v-if="props.status == 'completed'">
                <ai_svg />
            </div>

            <div @click="delete_task" class="delete_task" v-if="props.status == 'error' || props.status == 'completed'">
                <delete_svg />
            </div>
        </div>
    </div>
</template>

<style scoped>
.task {
    width: 92%;
    border-radius: 10px;
    min-height: 8vh;
    background-color: #353550;
    display: flex;
    justify-content: space-between;

}

.data {
    margin-left: 15px;
    display: flex;
    align-items: center;
    gap: 20px;
}

.filename_data_and_name {
    display: flex;
    flex-direction: column;
    /* gap: 3px; */
    align-items: flex-start
}

.filename {
    color: white;
    font-weight: 600;
    font-size: 19px;
}

.task_date {
    font-weight: 600;
    font-size: 12px;
    color: #B4BEFE;

}

.crud_task {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-right: 15px;

}

.original_download, .ai_download {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background-color: #B4BEFE;
    display: flex;
    align-items: center;
    justify-content: center;
}
.ai_download{
    background-color: #949edd;

}

.delete_task {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background-color: #F38BA8;
    display: flex;
    align-items: center;
    justify-content: center;

}
</style>