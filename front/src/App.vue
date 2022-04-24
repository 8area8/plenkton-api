<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/about">About</router-link>
    <button v-if="auth?.authenticated" @click="auth?.logout()">
      Déconnexion
    </button>
  </nav>
  <router-view />
</template>

<script lang="ts" setup>
  import { injectAuth } from 'vue-auth0-plugin'
  import { definePlugin, defaultPlugins, useClient } from 'villus'

  const auth = injectAuth()

  /**
   * Villus - add the token to the request
   * https://villus.logaretm.com/guide/plugins#example---adding-authorization-headers
   */
  const authPlugin = definePlugin(async ({ opContext }) => {
    const token = localStorage.getItem('token')
    opContext.headers.Authorization = token ? `Bearer ${token}` : ''
  })
  useClient({
    url: '/graphql',
    use: [authPlugin, ...defaultPlugins()],
  })
</script>
