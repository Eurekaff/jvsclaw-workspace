import { useQuery } from '@tanstack/react-query'
import { dashboardAPI, workflowAPI, agentAPI } from '../services/api'
import { Link } from 'react-router-dom'

function StatCard({ title, value, subtitle, color = 'blue' }) {
  const colors = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    purple: 'bg-purple-500',
  }
  
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center">
        <div className={`${colors[color]} rounded-md p-3 mr-4`}>
          <span className="text-white text-2xl">{value}</span>
        </div>
        <div>
          <p className="text-gray-500 text-sm">{title}</p>
          <p className="text-gray-900 font-semibold">{subtitle}</p>
        </div>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const { data: summary, isLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: async () => {
      const res = await dashboardAPI.getSummary()
      return res.data
    },
  })

  if (isLoading) {
    return <div className="text-center py-12">加载中...</div>
  }

  if (!summary) {
    return <div className="text-center py-12 text-gray-500">暂无数据</div>
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">仪表板概览</h2>
      
      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="总运行数"
          value={summary.total_runs}
          subtitle="所有工作流"
          color="blue"
        />
        <StatCard
          title="进行中"
          value={summary.active_runs}
          subtitle="当前活跃"
          color="yellow"
        />
        <StatCard
          title="Agent 总数"
          value={summary.total_agents}
          subtitle="已注册"
          color="green"
        />
        <StatCard
          title="今日 Token"
          value={summary.total_tokens_today.toLocaleString()}
          subtitle={`$${summary.estimated_cost_today.toFixed(2)}`}
          color="purple"
        />
      </div>

      {/* 最近运行 */}
      <div className="bg-white rounded-lg shadow mb-8">
        <div className="px-6 py-4 border-b">
          <h3 className="text-lg font-semibold text-gray-900">最近运行</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  运行 ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  项目名
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  状态
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  当前阶段
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  更新时间
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {summary.recent_runs.map((run) => (
                <tr key={run.run_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <Link
                      to={`/workflows/${run.run_id}`}
                      className="text-blue-600 hover:text-blue-900 font-mono text-sm"
                    >
                      {run.run_id}
                    </Link>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {run.project_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        run.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {run.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {run.current_stage}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(run.updated_at).toLocaleString('zh-CN')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Agent 状态 */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b flex justify-between items-center">
          <h3 className="text-lg font-semibold text-gray-900">Agent 状态</h3>
          <Link to="/agents" className="text-blue-600 hover:text-blue-900 text-sm">
            查看全部 →
          </Link>
        </div>
        <AgentStatusList />
      </div>
    </div>
  )
}

function AgentStatusList() {
  const { data: agents } = useQuery({
    queryKey: ['agents'],
    queryFn: async () => {
      const res = await agentAPI.list()
      return res.data
    },
  })

  if (!agents || agents.length === 0) {
    return <div className="px-6 py-4 text-gray-500">暂无 Agent 数据</div>
  }

  return (
    <div className="p-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => (
          <div
            key={agent.name}
            className="border rounded-lg p-4 flex items-center justify-between"
          >
            <div>
              <p className="font-semibold text-gray-900">{agent.name}</p>
              <p className="text-sm text-gray-500">{agent.stage}</p>
            </div>
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
        ))}
      </div>
    </div>
  )
}
