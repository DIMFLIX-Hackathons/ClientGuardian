<script setup>
import file_svg from "../assets/svg/file_svg.vue"
import busket_svg from "../assets/svg/busket_svg.vue"
import { useFileStore } from '@/store/files';
import { ref } from 'vue';

const fileStore = useFileStore();
const props = defineProps({
   file_id: Number,
   file: File,
})

</script>

<template>
   <div class="file">
      <div class="file_info">
         <file_svg class="svg_file"/>
         <div class="filename">
            <span>{{ file.name }}</span>
         </div>
      </div>
      <busket_svg class="delete_task" @click="() => {fileStore.removeFile(props.file_id)}"/>
   </div>
</template>

<style scoped lang="scss">
.file {
   width: 100%;
   border-radius: 10px;
   background-color: #45456A;
   display: flex;
   align-items: center;
   justify-content: space-between;
   min-height: 50px;

   .file_info {
      display: flex;
      gap: 15px;
      align-items: center;
      
      .svg_file {
         margin-left: 15px;
      }

      .filename span {
         font-weight: 600;
         color: white;
         font-size: 13px;
      }
   }

   .delete_task {
      height: 30px;
      width: 30px;
      background-color: #F38BA8;
      border-radius: 10px;
      margin-right: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
   }
}
</style>