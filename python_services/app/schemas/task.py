"""
Pydantic schemas for task-related API operations.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from app.models.database import TaskStatusType


class TaskBase(BaseModel):
    """Base task schema with common fields."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    priority: int = Field(default=3, ge=1, le=5)
    est_duration: Optional[int] = Field(None, gt=0)  # minutes
    dur_conf: int = Field(default=3, ge=1, le=5)
    target_deadline: Optional[datetime] = None
    dl_hardness: int = Field(default=3, ge=1, le=5)
    reoccuring: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    project_id: Optional[UUID] = None
    dependencies: List[UUID] = Field(default_factory=list)
    subtasks: List[UUID] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    project_id: Optional[UUID] = None
    task_status: Optional[TaskStatusType] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    est_duration: Optional[int] = Field(None, gt=0)
    dur_conf: Optional[int] = Field(None, ge=1, le=5)
    dependencies: Optional[List[UUID]] = None
    subtasks: Optional[List[UUID]] = None
    target_deadline: Optional[datetime] = None
    dl_hardness: Optional[int] = Field(None, ge=1, le=5)
    reoccuring: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class TaskInDB(TaskBase):
    """Schema representing a task as stored in the database."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    project_id: Optional[UUID] = None
    task_status: TaskStatusType
    dependencies: List[UUID]
    subtasks: List[UUID]
    deferred: int
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None


class TaskResponse(TaskInDB):
    """Schema for task API responses."""
    pass


class TaskWithProject(TaskResponse):
    """Task response including project information."""
    project_name: Optional[str] = None
    project_importance: Optional[int] = None


class TaskListResponse(BaseModel):
    """Schema for paginated task list responses."""
    tasks: List[TaskResponse]
    total: int
    page: int
    per_page: int
    has_more: bool


class TaskCreateRequest(BaseModel):
    """Schema for natural language task creation requests."""
    input_text: str = Field(..., min_length=1, max_length=2000)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TaskCreateResponse(BaseModel):
    """Schema for task creation response with AI analysis."""
    task: TaskResponse
    analysis: Dict[str, Any]
    suggestions: List[str] = Field(default_factory=list)


class TaskSearchRequest(BaseModel):
    """Schema for semantic task search requests."""
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=50)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)


class TaskSearchResult(BaseModel):
    """Schema for individual task search result."""
    task: TaskResponse
    similarity_score: float
    match_reason: str


class TaskSearchResponse(BaseModel):
    """Schema for task search response."""
    results: List[TaskSearchResult]
    query: str
    total_found: int


# Project schemas
class ProjectCreate(BaseModel):
    """Schema for creating a new project."""
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    description: Optional[str] = Field(None, max_length=1000, description="Project description")
    importance: int = Field(..., ge=1, le=5, description="Project importance (1-5)")


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Project name")
    description: Optional[str] = Field(None, max_length=1000, description="Project description")
    importance: Optional[int] = Field(None, ge=1, le=5, description="Project importance (1-5)")


class ProjectResponse(BaseModel):
    """Schema for project response."""
    id: UUID
    name: str
    description: Optional[str]
    importance: int
    created_at: str
    updated_at: Optional[str]
    task_stats: Dict[str, int]
    tasks: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True


# Schedule schemas
class ScheduleEntryCreate(BaseModel):
    """Schema for creating a schedule entry."""
    task_id: UUID = Field(..., description="Task ID to schedule")
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    start_time: str = Field(..., description="Start time in HH:MM format")
    duration_minutes: int = Field(..., ge=1, le=1440, description="Duration in minutes")


class ScheduleEntryResponse(BaseModel):
    """Schema for schedule entry response."""
    id: UUID
    date: str
    start_time: str
    end_time: str
    title: str
    description: Optional[str]
    task_id: Optional[UUID]
    priority: Optional[int]
    task_type: str
    scheduled_by: str

    class Config:
        from_attributes = True 