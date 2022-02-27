<template>
  <div class="admin">
      This is the admin dashboard (supercharge the home dashboard with custom slots)
  </div>
</template>

<script lang="ts" setup>
import { injectAuth } from 'vue-auth0-plugin'

const auth = injectAuth();

if (auth) {
  if (!auth.authenticated) {
      auth.loginWithRedirect();
  }
}
</script>
