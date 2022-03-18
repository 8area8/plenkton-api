<template>
  <div class="home">
    <div v-if="auth?.user">{{ auth?.user.name }} - {{ auth?.user.sub }}</div>
    <br />
    {{ auth?.authenticated }}
    <br />
    <div v-if="isFetching">Loading...</div>
    <div v-else-if="data">
      This is the admin dashboard (supercharge the home dashboard with custom
      slots)
    </div>
    <div v-else-if="error">{{ error }}</div>
    <br />

    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
  </div>
</template>

<script lang="ts" setup>
import HelloWorld from "@/components/HelloWorld.vue"; // @ is an alias to /src

import { injectAuth } from 'vue-auth0-plugin'
import { useQuery } from "villus";
import { watchEffect } from "vue";

const auth = injectAuth();
const { data, error, isFetching, execute } = useQuery({
  query: `query ShowAdminPanel { privateAdmin }`
})
watchEffect(async () => {
  if (auth) {
    const token = await auth?.client?.getTokenSilently()
    localStorage.setItem("token", token || '')
    await execute()
  }
})
</script>
