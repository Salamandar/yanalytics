<script setup lang="ts">
import { onMounted, ref, type Ref } from 'vue'
import Chart, { type ChartConfiguration } from 'chart.js/auto'
import 'chartjs-adapter-moment';

import { getAnalyticsApps, type AnalyticsAppsDetail } from './api'
import ChartBlock from './ChartBlock.vue'

const apps: Ref<AnalyticsAppsDetail[]> = ref([])

onMounted(async () => {
  const analyticsJson = await getAnalyticsApps()
  apps.value = analyticsJson.details

  const instancesData = analyticsJson.count_history
  const history = Array.from(
    Object.entries(instancesData),
    ([k, v]) => ({x: k, y: v})
  )
  const instancesConfig: ChartConfiguration = {
    type: 'line',
    options: {
      animation: {
        duration: 0
      },
      scales: {
        x: {
          type: 'time',
          time: {
            displayFormats: {
              month: 'YYYY-MM-DD',
            },
          },
        },
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
      elements: {
        point: {
          pointStyle: false
        }
      }
    },
    data: {
      datasets: [
        {
          label: 'Number of apps',
          // @ts-expect-error data is wrongly typed and doesn't accept date as string
          data: history,
          cubicInterpolationMode: 'monotone',
        },
      ],
    },
  }
  new Chart('appsCountChart', instancesConfig)
})
</script>

<template>
  <div class="apps-container">
    <div class="apps-chart">
      <ChartBlock chartId="appsCountChart" title="Number of apps" />

    </div>
    <table class="apps-table">
      <thead>
        <tr>
          <th class="apps-idx"></th>
          <th class="apps-name">Name</th>
          <th class="apps-installations">Installations</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(app, idx) in apps" :key="`entity-${app.id}`">
          <td class="apps-idx">{{ idx + 1 }}</td>
          <td class="apps-name">
            <a
              title="Appstore page"
              :href="`https://apps.yunohost.org/app/${app.id}`"
              target="_blank"
            >
              <img
                :src="`https://raw.githubusercontent.com/YunoHost/apps/refs/heads/main/logos/${app.id}.png`"
              />
              <span>{{ app.name }}</span>
            </a>
          </td>
          <td class="apps-installations">{{ app.count }} ({{ app.percent }}%)</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.apps-container {
  display: flex;
  flex-wrap: wrap;
}

.apps-container > * {
  min-width: 400px;
  flex: 50%;
}

.apps-table {
  background-color: var(--color-background-mute);
  border-collapse: collapse;
}

.apps-table th {
  font-weight: bold;
}

.apps-table tbody tr {
  border-top: 1px solid black;
}

.apps-table th,
.apps-table td {
  padding: 16px;
}

.apps-idx {
  width: 32px;
  text-align: right;
}

.apps-name {
  text-align: left;
}

.apps-name a {
  text-decoration: none;
  color: var(--color-text);
}

.apps-name img {
  height: 1.6rem;
  width: 1.6rem;
  display: inline-block;
  vertical-align: center;
  margin-right: 1rem;
}

.apps-installations {
  text-align: right;
}
</style>
