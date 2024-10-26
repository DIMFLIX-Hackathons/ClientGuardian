<script setup>
// import {check_token} from "@/modules/api";
</script>


<template>
    <div class="container">
       <div class="form">
         <div class="auth_token_inputs">
           <input type="text" placeholder="Введите токен" />
          
         </div>
         <div class="btn_check_token">
           <button>Проверить токен</button>
         </div>
       </div>
    </div>
   </template>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: var(--background-color);
}

.form {
    display: flex;
    flex-direction: column; 
    align-items: center; 
    padding: 30px;
    border: 1px solid #B4BEFE;
    border-radius: 12px; 
    background-color:#45456A;
    height: 10vh;
    background-color:var(--sbg-color);
}

.auth_token_inputs input {
    padding: 10px;
    padding-right: 40px; 
    margin-bottom: 15px;
    border: 1px solid #B4BEFE;
    border-radius: 4px; 
    width: 250px; 
    background-image: url('../assets/svg/protection.svg'); 
    background-size: 20px; 
    background-repeat: no-repeat; 
    background-position: right 10px center; 
    background-color:#45456A;
    outline: none;
    color: var(--input-text-color);
}

.btn_check_token button {
    padding: 10px 20px; 
    background-color: #B4BEFE; 
    color: var(--input-text-color); 
    border: none; 
    border-radius: 4px; 
    cursor: pointer;
    width: 300px;
}


</style>