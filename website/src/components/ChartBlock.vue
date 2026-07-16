<script setup lang="ts">
defineProps(['chartId', 'title', 'subtitle'])
</script>

<template>
  <div>
    <h2 class="chart-title">{{ title }}</h2>
    <h3 class="chart-subtitle">{{ subtitle }}</h3>
    <canvas :id="chartId" />
  </div>
</template>

<style scoped>
canvas {
  width: 100%;
  display: block;
  box-sizing: border-box;
}
div {
  padding: 1rem;
}
</style>
