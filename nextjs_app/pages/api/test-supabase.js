import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
)

export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    // Test connection by fetching projects
    const { data: projects, error } = await supabase
      .from('projects')
      .select('*')
      .limit(5)

    if (error) {
      console.error('Supabase error:', error)
      return res.status(500).json({ error: 'Database connection failed', details: error.message })
    }

    // Test personality profile table exists
    const { error: profileError } = await supabase
      .from('user_personality_profile')
      .select('profile_id')
      .limit(1)

    if (profileError) {
      console.error('Profile table error:', profileError)
      return res.status(500).json({ error: 'Profile table access failed', details: profileError.message })
    }

    return res.status(200).json({ 
      success: true, 
      message: 'Supabase connection successful!',
      projectCount: projects.length,
      profileTableExists: true,
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('Connection test failed:', error)
    return res.status(500).json({ error: 'Connection test failed', details: error.message })
  }
} 