'use client'

import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import type { Task, Project } from '../../../types/database'

interface TaskWithProject extends Task {
  projects?: Project | null
}

interface DependencyTask {
  id: string
  title: string
  task_status: string
}

interface TaskDetailPageProps {
  params: Promise<{ id: string }>
}

export default function TaskDetailPage({ params }: TaskDetailPageProps) {
  const [task, setTask] = useState<TaskWithProject | null>(null)
  const [dependencyTasks, setDependencyTasks] = useState<DependencyTask[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [resolvedParams, setResolvedParams] = useState<{ id: string } | null>(null)
  const router = useRouter()

  useEffect(() => {
    const resolveParams = async () => {
      const resolved = await params
      setResolvedParams(resolved)
    }
    resolveParams()
  }, [params])

  useEffect(() => {
    if (!resolvedParams?.id) return

    const fetchTask = async () => {
      try {
        setLoading(true)
        const response = await fetch(`/api/tasks/${resolvedParams.id}`)
        
        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('Task not found')
          }
          throw new Error('Failed to fetch task')
        }
        
        const data = await response.json()
        setTask(data.task)
        
        // Fetch dependency task details if they exist
        if (data.task.dependencies && data.task.dependencies.length > 0) {
          await fetchDependencyTasks(data.task.dependencies)
        }
        
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred')
      } finally {
        setLoading(false)
      }
    }

    fetchTask()
  }, [resolvedParams])

  const fetchDependencyTasks = async (dependencyIds: string[]) => {
    try {
      const dependencyPromises = dependencyIds.map(async (id) => {
        try {
          const response = await fetch(`/api/tasks/${id}`)
          if (response.ok) {
            const data = await response.json()
            return {
              id: data.task.id,
              title: data.task.title,
              task_status: data.task.task_status
            }
          }
          return {
            id,
            title: `Task ${id}`,
            task_status: 'unknown'
          }
        } catch {
          return {
            id,
            title: `Task ${id}`,
            task_status: 'unknown'
          }
        }
      })
      
      const dependencies = await Promise.all(dependencyPromises)
      setDependencyTasks(dependencies)
    } catch (error) {
      console.error('Error fetching dependency tasks:', error)
    }
  }

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

  const formatDateShort = (dateString: string | null) => {
    if (!dateString) return 'Not set'
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-4 sm:p-8">
        <div className="max-w-4xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
            <div className="bg-white rounded-lg border border-gray-200 p-6 sm:p-8">
              <div className="space-y-4">
                <div className="h-8 bg-gray-200 rounded w-3/4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                <div className="h-32 bg-gray-200 rounded"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-4 sm:p-8">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center mb-6">
            <button
              onClick={() => router.back()}
              className="flex items-center text-gray-600 hover:text-gray-900 font-medium transition-colors"
            >
              <span className="text-xl mr-2">✕</span>
              <span className="hidden sm:inline">Back</span>
            </button>
          </div>
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Task</h2>
            <p className="text-red-600 mb-4">{error}</p>
            <Link 
              href="/tasks"
              className="inline-block px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
            >
              Return to Tasks
            </Link>
          </div>
        </div>
      </div>
    )
  }

  if (!task) {
    return (
      <div className="min-h-screen bg-gray-50 p-4 sm:p-8">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center mb-6">
            <button
              onClick={() => router.back()}
              className="flex items-center text-gray-600 hover:text-gray-900 font-medium transition-colors"
            >
              <span className="text-xl mr-2">✕</span>
              <span className="hidden sm:inline">Back</span>
            </button>
          </div>
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📝</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Task not found</h3>
            <p className="text-gray-600 mb-4">The task you&apos;re looking for doesn&apos;t exist or has been deleted.</p>
            <Link 
              href="/tasks"
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              Return to Tasks
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header with Close Button */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={() => router.back()}
            className="flex items-center text-gray-600 hover:text-gray-900 font-medium transition-colors"
          >
            <span className="text-xl mr-2">✕</span>
            <span className="hidden sm:inline">Back to Tasks</span>
            <span className="sm:hidden">Back</span>
          </button>
          
          {/* Quick Actions */}
          <div className="flex gap-2">
            {task.priority && (
              <span className={`px-2 sm:px-3 py-1 text-xs sm:text-sm font-medium rounded border ${getPriorityColor(task.priority)}`}>
                <span className="hidden sm:inline">Priority </span>P{task.priority}
              </span>
            )}
            <span className={`px-2 sm:px-3 py-1 text-xs sm:text-sm font-medium rounded border ${getStatusColor(task.task_status)}`}>
              {task.task_status.charAt(0).toUpperCase() + task.task_status.slice(1)}
            </span>
          </div>
        </div>

        {/* Task Detail Card */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
          {/* Task Header */}
          <div className="p-6 sm:p-8 border-b border-gray-200">
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4 leading-tight">{task.title}</h1>
            
            {task.description && (
              <div className="prose prose-gray max-w-none">
                <p className="text-gray-700 text-base sm:text-lg leading-relaxed">{task.description}</p>
              </div>
            )}
          </div>

          {/* Task Details */}
          <div className="p-6 sm:p-8">
            <div className="grid gap-6 lg:grid-cols-2 lg:gap-8">
              {/* Left Column */}
              <div className="space-y-6">
                {/* Project */}
                {task.projects && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">Project</h3>
                    <div className="flex items-start">
                      <span className="text-lg text-gray-900 font-medium">📁 {task.projects.name}</span>
                      {task.projects.priority && (
                        <span className="ml-2 text-sm text-gray-500 mt-1">(P{task.projects.priority})</span>
                      )}
                    </div>
                    {task.projects.description && (
                      <p className="text-gray-600 mt-2 text-sm">{task.projects.description}</p>
                    )}
                  </div>
                )}

                {/* Duration & Deadline Row */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Duration */}
                  {task.est_duration && (
                    <div className="bg-blue-50 rounded-lg p-4">
                      <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-2">Duration</h3>
                      <p className="text-lg font-semibold text-gray-900">⏱️ {task.est_duration}m</p>
                      {task.dur_conf && (
                        <p className="text-sm text-gray-500">Confidence: {task.dur_conf}%</p>
                      )}
                    </div>
                  )}

                  {/* Deadline */}
                  {task.target_deadline && (
                    <div className="bg-orange-50 rounded-lg p-4">
                      <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-2">Deadline</h3>
                      <p className="text-lg font-semibold text-gray-900">📅 {formatDateShort(task.target_deadline)}</p>
                      {task.dl_hardness && (
                        <p className="text-sm text-gray-500">Hardness: {task.dl_hardness}/10</p>
                      )}
                    </div>
                  )}
                </div>

                {/* Recurring */}
                {task.reoccuring && (
                  <div className="bg-purple-50 rounded-lg p-4">
                    <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-2">Recurring</h3>
                    <p className="text-lg font-semibold text-gray-900">🔄 {task.reoccuring}</p>
                  </div>
                )}
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                {/* Dependencies */}
                {dependencyTasks.length > 0 && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">Dependencies</h3>
                    <div className="space-y-2">
                      {dependencyTasks.map((dep) => (
                        <Link
                          key={dep.id}
                          href={`/tasks/${dep.id}`}
                          className="block p-3 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors group"
                        >
                          <div className="flex items-center justify-between">
                            <span className="text-blue-700 font-medium group-hover:text-blue-800">
                              🔗 {dep.title}
                            </span>
                            <span className={`px-2 py-1 text-xs rounded ${getStatusColor(dep.task_status)}`}>
                              {dep.task_status}
                            </span>
                          </div>
                          <span className="text-blue-600 text-sm">Click to view details</span>
                        </Link>
                      ))}
                    </div>
                  </div>
                )}

                {/* Tags */}
                {task.tags && task.tags.length > 0 && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">Tags</h3>
                    <div className="flex flex-wrap gap-2">
                      {task.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full font-medium"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Status Info */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">Status Info</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Created:</span>
                      <span className="font-medium">{formatDateShort(task.created_at)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Updated:</span>
                      <span className="font-medium">{formatDateShort(task.updated_at)}</span>
                    </div>
                    {task.deferred && task.deferred > 0 && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Deferred:</span>
                        <span className="font-medium text-orange-600">{task.deferred} time(s)</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Notes */}
            {task.notes && (
              <div className="mt-8 pt-6 border-t border-gray-200">
                <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-4">Notes</h3>
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{task.notes}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
} 