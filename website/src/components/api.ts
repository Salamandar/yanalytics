
export function serverUrl(): string {
  const api_server = import.meta.env.VITE_API_SERVER
  if (api_server !== undefined && api_server !== '') {
    return api_server
  }

  const base = import.meta.env.BASE_URL
  let server = ''
  if (window.location.href.startsWith(base)) {
    server = base
  } else if (window.location.pathname.startsWith(base)) {
    server = `${window.location.origin}${base}`
  }
  return server
}

export interface AnalyticsStatsData {
  instances: [{ year: number; v12: number; v13: number }]
  apps_nb: [{ year: number; count: number }]
}

export async function getAnalyticsStats(): Promise<AnalyticsStatsData> {
  const server = serverUrl()
  const analyticsUrl = `${server}/api/v1/analytics/stats`.replace(/(?<!:)\/+/g, '/')
  return fetch(analyticsUrl).then(async (response) => {
    return response.json()
  })
}
