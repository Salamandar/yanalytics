<script setup lang="ts">
import { onMounted, ref, type Ref } from 'vue'
import { getAnalyticsApps, type AnalyticsAppsData } from './api'

const apps: Ref<[AnalyticsAppsData]> = ref([] as AnalyticsAppsData[])

onMounted(async () => {
  const analyticsJson = await getAnalyticsApps()
  apps.value = analyticsJson
})
</script>

<template>
  <table class="apps-table">
    <tr>
      <th class="apps-idx" />
      <th class="apps-name">Name</th>
      <th class="apps-installations">Installations</th>
    </tr>
    <tr v-for="(app, idx) in apps" :key="`entity-${app.id}`">
      <td class="apps-idx">{{ idx + 1 }}</td>
      <td class="apps-name">
        <a title="Appstore page" :href="`https://apps.yunohost.org/app/${app.id}`" target="_blank">
          <img
            :src="`https://raw.githubusercontent.com/YunoHost/apps/refs/heads/main/logos/${app.id}.png`"
          />
          <span>{{ app.name }}</span>
        </a>
      </td>
      <td class="apps-installations">{{ app.count }} ({{ app.percent }}%)</td>
    </tr>
  </table>
</template>

<style scoped>
.apps-table {
  background-color: var(--color-background-mute);
  width: 100%;
}

.apps-table th {
  font-weight: bold;
}

.apps-table > tr > th,
.apps-table > tr > td {
  padding: 8px;
}

.apps-idx {
  width: 32px;
}

.apps-name {
  text-align: left;
}

.apps-name a {
  text-decoration: none;
  color: var(--color-text);
}

.apps-name img {
  height: 2rem;
  width: 2rem;
  display: inline-block;
  vertical-align: center;
  margin-right: 1rem;
}

.apps-installations {
  text-align: right;
}
</style>
