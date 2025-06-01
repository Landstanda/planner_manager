'use client'

import React, { useState, useEffect, useCallback } from 'react'
import type { Task } from '../../types/database'

interface TaskWithProject extends Task {
  projects?: {
    id: string
    name: string
    priority: number | null
  } | null
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<TaskWithProject[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [sortBy, setSortBy] = useState('created_at')
  const [sortOrder, setSortOrder] = useState('desc')

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/tasks?sortBy=${sortBy}&sortOrder=${sortOrder}`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch tasks')
      }
      
      const data = await response.json()
      setTasks(data.tasks || [])
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }, [sortBy, sortOrder])

  useEffect(() => {
    fetchTasks()
  }, [fetchTasks])

  const getPriorityColor = (priority: number | null) => {
    switch (priority) {
      case 1: return 'bg-red-100 text-red-800 border-red-200'
      case 2: return 'bg-orange-100 text-orange-800 border-orange-200'
      case 3: return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 4: return 'bg-blue-100 text-blue-800 border-blue-200'
      case 5: return 'bg-gray-100 text-gray-800 border-gray-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ready': return 'bg-green-100 text-green-800 border-green-200'
      case 'progressing': return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'done': return 'bg-gray-100 text-gray-800 border-gray-200'
      case 'cancelled': return 'bg-red-100 text-red-800 border-red-200'
      case 'dependent': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-6xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-24 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-6xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Tasks</h2>
            <p className="text-red-600">{error}</p>
            <button 
              onClick={fetchTasks}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
          
          {/* Sort Controls */}
          <div className="flex gap-4">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="created_at">Created Date</option>
              <option value="priority">Priority</option>
              <option value="status">Status</option>
              <option value="deadline">Deadline</option>
              <option value="title">Title</option>
              <option value="project">Project</option>
            </select>
            
            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>
        </div>

        {/* Task List */}
        {tasks.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📝</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No tasks found</h3>
            <p className="text-gray-500">Create your first task to get started!</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg hover:border-gray-300 transition-all duration-200 cursor-pointer group"
                onClick={() => window.open(`/tasks/${task.id}`, '_blank')}
              >
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors leading-tight">
                    {task.title}
                  </h3>
                  <div className="flex gap-2 flex-shrink-0 ml-4">
                    {task.priority && (
                      <span className={`px-2 py-1 text-xs font-medium rounded border ${getPriorityColor(task.priority)}`}>
                        P{task.priority}
                      </span>
                    )}
                    <span className={`px-2 py-1 text-xs font-medium rounded border ${getStatusColor(task.task_status)}`}>
                      {task.task_status}
                    </span>
                  </div>
                </div>
                
                {task.description && (
                  <p className="text-gray-600 line-clamp-2 mb-4 leading-relaxed">
                    {task.description}
                  </p>
                )}
                
                <div className="flex justify-between items-center text-sm">
                  <div className="flex gap-4 flex-wrap">
                    {task.projects && (
                      <span className="text-gray-600 font-medium">📁 {task.projects.name}</span>
                    )}
                    {task.est_duration && (
                      <span className="text-gray-600">⏱️ {task.est_duration}m</span>
                    )}
                    {task.target_deadline && (
                      <span className="text-gray-600">📅 {new Date(task.target_deadline).toLocaleDateString()}</span>
                    )}
                  </div>
                  <span className="text-gray-400 text-xs">
                    {new Date(task.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
} 