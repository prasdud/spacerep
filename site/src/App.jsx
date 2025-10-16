import { useState } from 'react'
import './App.css' // only for Tailwind imports

function App() {
  const [topic, setTopic] = useState('')
  const [importance, setImportance] = useState('moderate')
  const [topics, setTopics] = useState([])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!topic.trim()) return
    const entry = {
      topic,
      importance,
      timestamp: new Date().toISOString(),
    }
    setTopics([entry, ...topics])
    setTopic('')
    setImportance('moderate')
  }

  // Map importance to colors
  const importanceColors = {
    low: 'bg-green-200 text-green-800',
    moderate: 'bg-yellow-200 text-yellow-800',
    high: 'bg-red-200 text-red-800',
  }

  return (
    <div className="min-h-screen bg-gradient-to-tr from-blue-100 via-purple-100 to-pink-100 flex items-center justify-center p-6">
      <div className="w-full max-w-md backdrop-blur-md bg-white/30 rounded-3xl p-6 shadow-lg">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
          What are you studying?
        </h2>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4 mb-6">
          <input
            type="text"
            placeholder="Enter topic"
            value={topic}
            onChange={e => setTopic(e.target.value)}
            className="px-4 py-3 rounded-xl bg-white/50 backdrop-blur-sm border border-white/30 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
          />
          <select
            value={importance}
            onChange={e => setImportance(e.target.value)}
            className="px-4 py-3 rounded-xl bg-white/50 backdrop-blur-sm border border-white/30 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
          >
            <option value="low">Low</option>
            <option value="moderate">Moderate</option>
            <option value="high">High</option>
          </select>
          <button
            type="submit"
            className="bg-white/50 backdrop-blur-sm hover:bg-white/70 text-gray-800 font-semibold py-3 rounded-xl shadow-md transition"
          >
            Add Topic
          </button>
        </form>

        {topics.length > 0 && (
          <div className="topic-list">
            <h3 className="text-xl font-medium text-gray-700 mb-4 text-center">Topics</h3>
            <ul className="flex flex-col gap-4">
              {topics.map((t, idx) => (
                <li
                  key={idx}
                  className={`p-4 rounded-2xl shadow-md backdrop-blur-sm bg-white/40 border border-white/30 flex flex-col transition hover:scale-105`}
                >
                  <span className="font-semibold text-gray-900">{t.topic}</span>
                  <span className={`inline-block mt-1 px-2 py-1 text-sm rounded-full ${importanceColors[t.importance]}`}>
                    {t.importance}
                  </span>
                  <small className="text-gray-600 mt-2">{new Date(t.timestamp).toLocaleString()}</small>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
