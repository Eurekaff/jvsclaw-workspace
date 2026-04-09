import axios from 'axios'

const API_BASE = '/api'

export const dashboardAPI = {
  getSummary: () => axios.get(`${API_BASE}/dashboard`),
}

export const workflowAPI = {
  list: (params) => axios.get(`${API_BASE}/workflows`, { params }),
  get: (runId) => axios.get(`${API_BASE}/workflows/${runId}`),
}

export const agentAPI = {
  list: () => axios.get(`${API_BASE}/agents`),
  get: (name) => axios.get(`${API_BASE}/agents/${name}`),
  update: (name, status) => axios.post(`${API_BASE}/agents/${name}/update`, status),
}

export const tokenAPI = {
  getUsage: (params) => axios.get(`${API_BASE}/tokens`, { params }),
  record: (usage) => axios.post(`${API_BASE}/tokens/record`, usage),
}
