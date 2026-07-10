<script setup lang="ts">
import Header from './components/Header.vue'
import Analytics from './components/Analytics.vue'
</script>

<template>
  <div id="container">
    <Header />
    <div id="summary">
      YunoHost allows users to share their data. It helps developers where to direct their efforts.
    </div>

    <Analytics />
  </div>
</template>

<style scoped>
#container {
  height: 100%;
  padding: 2rem;
  max-width: 1000px;
  margin: auto;
}

#summary {
  padding: 1rem;
}

main {
  height: 100%;
  display: flex;
  justify-content: center;
}
</style>
