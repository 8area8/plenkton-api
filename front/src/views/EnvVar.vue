<template>
  <div class="container flex flex-col mx-auto">
    <div
      class="text-left"
      v-for="(env, index) in envars"
      :key="'envar-' + index"
    >
      {{ env.name }} {{ env.name ? '(defined)' : '(not defined)' }} :
      {{ env.value }}
    </div>
  </div>
</template>

<script lang="ts" setup>
  const envars: { name: string; value: string }[] = []
  for (const envar in process.env) {
    envars.push({ name: envar, value: process.env[envar] })
  }
</script>
