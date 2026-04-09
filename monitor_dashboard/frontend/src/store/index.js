import { create } from 'zustand'

export const useAgentStore = create((set) => ({
  agents: [],
  setAgents: (agents) => set({ agents }),
}))

export const useWorkflowStore = create((set) => ({
  workflows: [],
  currentWorkflow: null,
  setWorkflows: (workflows) => set({ workflows }),
  setCurrentWorkflow: (workflow) => set({ currentWorkflow: workflow }),
}))

export const useDashboardStore = create((set) => ({
  summary: null,
  setSummary: (summary) => set({ summary }),
}))
