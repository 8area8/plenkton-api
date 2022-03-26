<template>
  <nav>
    <router-link to="/">Home</router-link>|
    <router-link to="/about">About</router-link>|
    <button v-if="auth?.authenticated" @click="auth?.logout()">Déconnexion</button>
  </nav>
  <router-view />
</template>

<script lang="ts" setup>
import { injectAuth } from "vue-auth0-plugin";
import { createClient, definePlugin, defaultPlugins, useClient } from "villus";

const auth = injectAuth();

/**
 * Villus - add the token to the request
 * https://villus.logaretm.com/guide/plugins#example---adding-authorization-headers
 */
const authPlugin = definePlugin(async ({ opContext }) => {
  const token = localStorage.getItem("token");
  opContext.headers.Authorization = token ? `Bearer ${token}` : "";
  console.log("token in middleware", token)
});
useClient({
  url: "/graphql",
  use: [authPlugin, ...defaultPlugins()],
});
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a,
  button {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
