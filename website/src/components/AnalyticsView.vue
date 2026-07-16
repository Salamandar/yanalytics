<script setup lang="ts">
import { onMounted } from 'vue'
import Chart, { type ChartConfiguration } from 'chart.js/auto'

import ChartBlock from './ChartBlock.vue'
import { getAnalyticsStats } from './api'

onMounted(async () => {
  const analyticsJson = await getAnalyticsStats()

  const instancesData = analyticsJson.instances
  const instancesConfig: ChartConfiguration = {
    type: 'line',
    options: {
      animation: {
        duration: 0
      },
      plugins: {
        tooltip: {
          mode: 'index',
        },
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false,
      },
      responsive: true,
    },
    data: {
      labels: instancesData.map((row) => row.year),
      datasets: [
        {
          label: 'Yunohost 12 (Debian Bookworm)',
          data: instancesData.map((row) => row.v12),
          cubicInterpolationMode: 'monotone',
        },
        {
          label: 'Yunohost 13 (Debian Trixie)',
          data: instancesData.map((row) => row.v13),
          cubicInterpolationMode: 'monotone',
        },
      ],
    },
  }
  new Chart('instancesChart', instancesConfig)

  const appsNbData = analyticsJson.apps_nb
  const appsNbConfig: ChartConfiguration = {
    type: 'bar',
    options: {
      animation: {
        duration: 0
      }
    },
    data: {
      labels: appsNbData.map((row) => row.year),
      datasets: [
        {
          label: 'Total apps',
          data: appsNbData.map((row) => row.count),
        },
      ],
    },
  }
  new Chart('appsNbChart', appsNbConfig)
})
</script>

<template>
  <span class="analytics-container" data-analyticsdata="{analyticsData}">
    <ChartBlock chartId="instancesChart" title="Active instances" />
    <ChartBlock chartId="appsNbChart" title="Number of apps" />
  </span>
</template>

<style scoped>

.analytics-container {
  display: flex;
  flex-wrap: wrap;
}

.analytics-container > * {
  min-width: 600px;
  flex: 50%;
}

@media screen and (max-width: 768px) {
  #analytics {
    display: flex;
    flex-direction: column;
  }
}
</style>
