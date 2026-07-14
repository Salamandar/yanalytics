<script setup lang="ts">
import ynhLogo from '../assets/ynh_logo_white.svg'
</script>

<template>
  <span class="site-title">
    <img :src="ynhLogo" alt="YunoHost Logo" />
    YunoHost Analytics
  </span>
</template>

<style scoped>
header {
  margin-bottom: 2rem;
}

.site-title {
  gap: 1rem;
  display: flex;
  align-items: center;
  font-weight: 700;
  font-size: 2em;
}

.site-title img {
  height: 2em;
}

@media (prefers-color-scheme: light) {
  .site-title > img {
    filter: invert(1);
  }
}
</style>
