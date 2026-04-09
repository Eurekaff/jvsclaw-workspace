import { Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Workflows from './pages/Workflows'
import WorkflowDetail from './pages/WorkflowDetail'
import Agents from './pages/Agents'
import Tokens from './pages/Tokens'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* 顶部导航 */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">🤖 Agent 工作流监控</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/" className="text-gray-600 hover:text-gray-900 px-3 py-2">
                仪表板
              </Link>
              <Link to="/workflows" className="text-gray-600 hover:text-gray-900 px-3 py-2">
                工作流
              </Link>
              <Link to="/agents" className="text-gray-600 hover:text-gray-900 px-3 py-2">
                Agents
              </Link>
              <Link to="/tokens" className="text-gray-600 hover:text-gray-900 px-3 py-2">
                Token 用量
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* 主内容区 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/workflows" element={<Workflows />} />
          <Route path="/workflows/:runId" element={<WorkflowDetail />} />
          <Route path="/agents" element={<Agents />} />
          <Route path="/tokens" element={<Tokens />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
