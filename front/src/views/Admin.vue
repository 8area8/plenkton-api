<template>
  <div class="admin">
    <div>Loading...</div>
  </div>
</template>

<script lang="ts" setup>
  import { injectAuth } from 'vue-auth0-plugin'

  const auth = injectAuth()
  if (auth) {
    if (!auth.authenticated) {
      await auth?.client?.loginWithRedirect()
    }
  }
</script>
