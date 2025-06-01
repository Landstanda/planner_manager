import { NextRequest, NextResponse } from 'next/server'
import { supabase } from '../../../lib/supabase'

export async function GET(request: NextRequest) {
  // Check if environment variables are properly configured
  if (!process.env.NEXT_PUBLIC_SUPABASE_URL || !process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
    return NextResponse.json(
      { error: 'Supabase configuration missing' },
      { status: 500 }
    )
  }

  try {
    const { searchParams } = new URL(request.url)
    const sortBy = searchParams.get('sortBy') || 'created_at'
    const sortOrder = searchParams.get('sortOrder') || 'desc'
    
    // Build the query
    let query = supabase
      .from('tasks')
      .select(`
        *,
        projects (
          id,
          name,
          priority
        )
      `)
    
    // Apply sorting
    switch (sortBy) {
      case 'priority':
        query = query.order('priority', { ascending: sortOrder === 'asc' })
        break
      case 'status':
        query = query.order('task_status', { ascending: sortOrder === 'asc' })
        break
      case 'deadline':
        query = query.order('target_deadline', { ascending: sortOrder === 'asc', nullsFirst: false })
        break
      case 'title':
        query = query.order('title', { ascending: sortOrder === 'asc' })
        break
      case 'project':
        query = query.order('project_id', { ascending: sortOrder === 'asc', nullsFirst: false })
        break
      default:
        query = query.order('created_at', { ascending: sortOrder === 'asc' })
    }
    
    const { data: tasks, error } = await query
    
    if (error) {
      console.error('Error fetching tasks:', error)
      return NextResponse.json(
        { error: 'Failed to fetch tasks' },
        { status: 500 }
      )
    }
    
    return NextResponse.json({ tasks })
  } catch (error) {
    console.error('Unexpected error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
} 