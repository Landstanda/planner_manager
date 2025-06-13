/**
 * API Client for Chief-of-Flow Python FastAPI Backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://chief-of-flow-api.fly.dev';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

interface Task {
  id: string;
  title: string;
  description?: string;
  task_status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  priority: number;
  project_id?: string;
  target_deadline?: string;
  created_at: string;
  updated_at: string;
  subtasks?: string[];
  dependencies?: string[];
}

interface Project {
  id: string;
  name: string;
  description?: string;
  priority: number;
  status: 'active' | 'completed' | 'on_hold';
  created_at: string;
  updated_at: string;
}

interface ScheduleEntry {
  id: string;
  title: string;
  start_time: string;
  end_time: string;
  task_id?: string;
  task_type: 'task' | 'appointment' | 'meeting';
  priority?: number;
}

interface AvailableSlot {
  start_time: string;
  end_time: string;
  duration_minutes: number;
}

interface WeekSchedule {
  [date: string]: ScheduleEntry[];
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          error: errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }

  // Health Check
  async healthCheck(): Promise<ApiResponse<{ status: string; service: string }>> {
    return this.request('/api/v1/health/');
  }

  // Tasks API
  async getTasks(params?: {
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
    status?: string;
    project_id?: string;
  }): Promise<ApiResponse<Task[]>> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value) searchParams.append(key, value);
      });
    }
    
    const endpoint = `/api/v1/tasks/${searchParams.toString() ? `?${searchParams}` : ''}`;
    return this.request(endpoint);
  }

  async createTask(task: {
    title: string;
    description?: string;
    priority?: number;
    project_id?: string;
    target_deadline?: string;
  }): Promise<ApiResponse<Task>> {
    return this.request('/api/v1/tasks/', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async createTaskFromText(text: string): Promise<ApiResponse<Task>> {
    return this.request('/api/v1/tasks/from-text', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
  }

  async updateTask(id: string, updates: Partial<Task>): Promise<ApiResponse<Task>> {
    return this.request(`/api/v1/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async deleteTask(id: string): Promise<ApiResponse<{ message: string }>> {
    return this.request(`/api/v1/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async searchTasks(query: string, limit?: number): Promise<ApiResponse<Task[]>> {
    return this.request('/api/v1/tasks/search', {
      method: 'POST',
      body: JSON.stringify({ query, limit }),
    });
  }

  // Projects API
  async getProjects(): Promise<ApiResponse<Project[]>> {
    return this.request('/api/v1/projects/');
  }

  async createProject(project: {
    name: string;
    description?: string;
    priority?: number;
  }): Promise<ApiResponse<Project>> {
    return this.request('/api/v1/projects/', {
      method: 'POST',
      body: JSON.stringify(project),
    });
  }

  // Schedule API
  async getSchedule(targetDate?: string): Promise<ApiResponse<ScheduleEntry[]>> {
    const endpoint = targetDate 
      ? `/api/v1/schedule/?target_date=${targetDate}`
      : '/api/v1/schedule/';
    return this.request(endpoint);
  }

  async getAvailableSlots(targetDate: string, durationMinutes: number): Promise<ApiResponse<AvailableSlot[]>> {
    return this.request(
      `/api/v1/schedule/available-slots?target_date=${targetDate}&duration_minutes=${durationMinutes}`
    );
  }

  async getWeekSchedule(): Promise<ApiResponse<WeekSchedule>> {
    return this.request('/api/v1/schedule/week');
  }

  // AI API
  async chatWithAI(message: string): Promise<ApiResponse<{ response: string }>> {
    return this.request('/api/v1/ai/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  async getAIStatus(): Promise<ApiResponse<{ openai_available: boolean; status: string }>> {
    return this.request('/api/v1/ai/status');
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
export default apiClient;

// Export types
export type { Task, Project, ScheduleEntry, AvailableSlot, WeekSchedule, ApiResponse }; 