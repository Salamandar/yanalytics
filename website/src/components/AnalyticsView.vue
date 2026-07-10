<script setup lang="ts">
import { onMounted } from 'vue'
import Chart from 'chart.js/auto'

import ChartBlock from './ChartBlock.vue'

import analyticsJson from '../assets/analytics.json'


onMounted(async () => {
  // const base = import.meta.env.BASE_URL


  const instancesData = analyticsJson.instances
  new Chart('instancesChart', {
    type: 'line',
    // options: {
    //   parsing: false,
    //   responsive: false,
    //   scales: {
    //     x: {
    //       type: 'time',
    //     }
    //   }
    // },
    data: {
      labels: instancesData.map((row) => row.year),
      datasets: [
        {
          label: 'Total instances',
          data: instancesData.map((row) => row.count),
        },
      ],
    },
  })

  const appsNbData = analyticsJson.apps_nb
  new Chart('appsNbChart', {
    type: 'bar',
    data: {
      labels: appsNbData.map((row) => row.year),
      datasets: [
        {
          label: 'Total apps',
          data: appsNbData.map((row) => row.count),
        },
      ],
    },
  })
})
// customElements.define('analytics-block', Analytics);

</script>

<template>
  <span id="analytics" data-analyticsdata="{analyticsData}">
    <ChartBlock chartId="instancesChart" title="Active instances" />
    <ChartBlock chartId="appsNbChart" title="Number of apps" />
  </span>
</template>

<style scoped>
@media screen and (max-height: 368px) {
  #news {
    display: none;
  }
}

@media screen and (max-width: 768px) {
  #container {
    display: flex;
    flex-direction: column;
  }

  #hero {
    display: block;
    padding-top: 10%;
  }

  #links {
    flex-wrap: wrap;
  }

  #links a.button {
    padding: 14px 18px;
  }

  #news {
    right: 16px;
    left: 16px;
    bottom: 2.5rem;
    max-width: 100%;
  }

  h1 {
    line-height: 1.5;
  }
}
</style>
