<template>
  <div class="home">
    {{ auth?.user }}
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
  </div>
</template>

<script lang="ts" setup>
import HelloWorld from "@/components/HelloWorld.vue"; // @ is an alias to /src
import { injectAuth } from 'vue-auth0-plugin'
const auth = injectAuth();
</script>
