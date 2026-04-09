import { useQuery } from '@tanstack/react-query'
import { tokenAPI } from '../services/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function Tokens() {
  const { data: tokenUsage, isLoading } = useQuery({
    queryKey: ['tokens'],
    queryFn: async () => {
      const res = await tokenAPI.getUsage({ days: 7 })
      return res.data
    },
  })

  // 按日期聚合数据
  const chartData = tokenUsage
    ? tokenUsage.reduce((acc, item) => {
        const date = item.date
        if (!acc[date]) {
          acc[date] = { date, total: 0, cost: 0 }
        }
        acc[date].total += item.total_tokens
        acc[date].cost += item.estimated_cost
        return acc
      }, {})
    : []

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Token 用量统计</h2>
      
      {/* 图表 */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">近 7 天用量趋势</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={Object.values(chartData)}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="total" stroke="#8884d8" name="Token 数" />
            <Line type="monotone" dataKey="cost" stroke="#82ca9d" name="成本 ($)" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* 详细列表 */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b">
          <h3 className="text-lg font-semibold text-gray-900">详细记录</h3>
        </div>
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                日期
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Agent
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                输入 Token
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                输出 Token
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                总计
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                估算成本
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {tokenUsage && tokenUsage.map((item, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {item.date}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {item.agent_name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {item.input_tokens.toLocaleString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {item.output_tokens.toLocaleString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                  {item.total_tokens.toLocaleString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">
                  ${item.estimated_cost.toFixed(4)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
