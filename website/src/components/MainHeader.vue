<script setup lang="ts">
import ynhLogo from '../assets/ynh_logo_white.svg'
</script>

<template>
  <header class="header-bar">
    <span class="site-title">
      <img :src="ynhLogo" alt="YunoHost Logo" />
      YunoHost Analytics
    </span>
    <nav class="site-nav">
      <ul>
        <li><router-link to="/">Installations</router-link></li>
        <li><router-link to="/apps">Applications</router-link></li>
      </ul>
    </nav>
  </header>
</template>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.site-nav ul {
  list-style: none;
  display: flex;
}

.site-nav li {
  padding: 4px;
}

.site-nav li a {
  padding: 0 4px;
  text-decoration: none;
  color: var(--color-text);
}

.router-link-exact-active {
  border-bottom: 2px solid var(--ynh-blue);
}
</style>
