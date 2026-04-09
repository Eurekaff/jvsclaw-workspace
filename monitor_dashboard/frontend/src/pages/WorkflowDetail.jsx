import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { workflowAPI } from '../services/api'

export default function WorkflowDetail() {
  const { runId } = useParams()
  
  const { data: workflow, isLoading } = useQuery({
    queryKey: ['workflow', runId],
    queryFn: async () => {
      const res = await workflowAPI.get(runId)
      return res.data
    },
  })

  if (isLoading) {
    return <div className="text-center py-12">加载中...</div>
  }

  if (!workflow) {
    return <div className="text-center py-12 text-gray-500">工作流不存在</div>
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">{workflow.project_name}</h2>
        <p className="text-gray-500 font-mono text-sm">{workflow.run_id}</p>
      </div>

      {/* 状态概览 */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-gray-500 text-sm">状态</p>
            <p className="text-lg font-semibold">
              <span
                className={`px-2 py-1 rounded-full text-sm ${
                  workflow.status === 'completed'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}
              >
                {workflow.status}
              </span>
            </p>
          </div>
          <div>
            <p className="text-gray-500 text-sm">当前阶段</p>
            <p className="text-lg font-semibold">{workflow.current_stage}</p>
          </div>
          <div>
            <p className="text-gray-500 text-sm">Token 用量</p>
            <p className="text-lg font-semibold">{workflow.total_tokens.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-gray-500 text-sm">消息数</p>
            <p className="text-lg font-semibold">{workflow.total_messages}</p>
          </div>
        </div>
      </div>

      {/* 阶段流程可视化 */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">阶段流程</h3>
        <div className="flex items-center space-x-4 overflow-x-auto pb-4">
          {workflow.stages.map((stage, index) => (
            <div key={stage.name} className="flex items-center">
              <div
                className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center ${
                  stage.status === 'completed'
                    ? 'bg-green-500 text-white'
                    : stage.status === 'running'
                    ? 'bg-yellow-500 text-white'
                    : 'bg-gray-200 text-gray-500'
                }`}
              >
                {index + 1}
              </div>
              <div className="ml-3 min-w-[120px]">
                <p className="text-sm font-semibold text-gray-900">{stage.name}</p>
                <p className="text-xs text-gray-500">
                  {stage.completed_at
                    ? new Date(stage.completed_at).toLocaleDateString('zh-CN')
                    : '-'}
                </p>
              </div>
              {index < workflow.stages.length - 1 && (
                <div className="ml-4 w-8 h-0.5 bg-gray-300"></div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 产出物列表 */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">产出物</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {workflow.stages.flatMap((stage) =>
            stage.artifacts.map((artifact) => (
              <div
                key={artifact}
                className="border rounded-lg p-3 hover:bg-gray-50 cursor-pointer"
              >
                <p className="text-sm font-mono text-gray-700 truncate">{artifact}</p>
                <p className="text-xs text-gray-500 mt-1">{stage.name}</p>
              </div>
            )),
          )}
        </div>
      </div>
    </div>
  )
}
