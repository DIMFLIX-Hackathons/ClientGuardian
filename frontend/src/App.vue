<script setup>
</script>

<template>
  <router-view/>
</template>

<style lang="scss">

body {
  background-color: var(--bg-color); 
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  background-color: var(--bg-color); 
  height: 100vh;
  max-height: 100vh;
  margin: 0;
  padding: 0;
}

:root {
    --bg-color: #1E1E2E;
    --dark-sbg: #28283E;
    --sbg-color: #353550;
    --light-sbg: #45456A;
    --border-color: rgb(202, 150, 253);
    --button-background-color: rgb(202, 150, 253);
    --input-background-color: black;
    --input-text-color: white;
}
</style>
