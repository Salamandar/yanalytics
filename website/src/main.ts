import './assets/main.css'

import '@fontsource-variable/source-sans-3/wght.css'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import AnalyticsView from './components/AnalyticsView.vue'
import AppsStatsView from './components/AppsStatsView.vue'
import PageNotFound from './components/PageNotFound.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: AnalyticsView },
    { path: '/apps', component: AppsStatsView },
    { path: '/:pathMatch(.*)*', component: PageNotFound },
  ],
})

const app = createApp(App)
app.use(router)
app.mount('#app')
