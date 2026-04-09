import { useQuery } from '@tanstack/react-query'
import { agentAPI } from '../services/api'

export default function Agents() {
  const { data: agents, isLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: async () => {
      const res = await agentAPI.list()
      return res.data
    },
  })

  if (isLoading) {
    return <div className="text-center py-12">加载中...</div>
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Agent 列表</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents && agents.map((agent) => (
          <div key={agent.name} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">{agent.name}</h3>
              <span
                className={`px-2 py-1 text-xs rounded-full ${
                  agent.status === 'running'
                    ? 'bg-green-100 text-green-800'
                    : agent.status === 'error'
                    ? 'bg-red-100 text-red-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {agent.status}
              </span>
            </div>
            
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">阶段</span>
                <span className="text-gray-900">{agent.stage}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Token 用量</span>
                <span className="text-gray-900">{agent.token_usage.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">消息数</span>
                <span className="text-gray-900">{agent.message_count}</span>
              </div>
              {agent.current_task && (
                <div className="mt-3 pt-3 border-t">
                  <span className="text-gray-500">当前任务</span>
                  <p className="text-gray-900 text-xs mt-1">{agent.current_task}</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
