export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  public: {
    Tables: {
      projects: {
        Row: {
          id: string
          name: string
          priority: number | null
          goals: string | null
          description: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          name: string
          priority?: number | null
          goals?: string | null
          description?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          name?: string
          priority?: number | null
          goals?: string | null
          description?: string | null
          created_at?: string
          updated_at?: string
        }
        Relationships: []
      }
      tasks: {
        Row: {
          id: string
          title: string
          project_id: string | null
          task_status: 'dependent' | 'ready' | 'progressing' | 'done' | 'cancelled'
          priority: number | null
          est_duration: number | null
          dur_conf: number | null
          dependencies: string[] | null
          target_deadline: string | null
          dl_hardness: number | null
          reoccuring: string | null
          description: string | null
          notes: string | null
          tags: string[] | null
          deferred: number | null
          embedding: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          title: string
          project_id?: string | null
          task_status?: 'dependent' | 'ready' | 'progressing' | 'done' | 'cancelled'
          priority?: number | null
          est_duration?: number | null
          dur_conf?: number | null
          dependencies?: string[] | null
          target_deadline?: string | null
          dl_hardness?: number | null
          reoccuring?: string | null
          description?: string | null
          notes?: string | null
          tags?: string[] | null
          deferred?: number | null
          embedding?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          title?: string
          project_id?: string | null
          task_status?: 'dependent' | 'ready' | 'progressing' | 'done' | 'cancelled'
          priority?: number | null
          est_duration?: number | null
          dur_conf?: number | null
          dependencies?: string[] | null
          target_deadline?: string | null
          dl_hardness?: number | null
          reoccuring?: string | null
          description?: string | null
          notes?: string | null
          tags?: string[] | null
          deferred?: number | null
          embedding?: string | null
          created_at?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "tasks_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          }
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      task_status_type: 'dependent' | 'ready' | 'progressing' | 'done' | 'cancelled'
      event_status_type: 'CONFIRMED' | 'TENTATIVE' | 'CANCELLED'
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

// Convenience types for easier use
export type Task = Database['public']['Tables']['tasks']['Row']
export type Project = Database['public']['Tables']['projects']['Row']
export type TaskInsert = Database['public']['Tables']['tasks']['Insert']
export type TaskUpdate = Database['public']['Tables']['tasks']['Update'] 