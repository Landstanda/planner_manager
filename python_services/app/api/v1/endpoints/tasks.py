"""
Task management API endpoints.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_database_session
from app.services.task_service import TaskService
from app.services.ai_service import AIService
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    TaskCreateRequest, TaskCreateResponse, TaskSearchRequest, TaskSearchResponse
)
from app.models.database import TaskStatusType

logger = structlog.get_logger(__name__)
router = APIRouter()


def get_task_service(db: AsyncSession = Depends(get_database_session)) -> TaskService:
    """Dependency to get TaskService instance."""
    ai_service = AIService()
    return TaskService(db, ai_service)


# TODO: Add authentication dependency
def get_current_user_id() -> UUID:
    """Temporary mock user ID - replace with real authentication."""
    return UUID("00000000-0000-0000-0000-000000000001")


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id)
):
    """Create a new task."""
    try:
        task = await task_service.create_task(task_data, user_id)
        logger.info("Task created via API", task_id=str(task.id))
        return task
    except Exception as e:
        logger.error("Failed to create task via API", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create task")


@router.post("/from-text", response_model=TaskCreateResponse, status_code=201)
async def create_task_from_natural_language(
    request: TaskCreateRequest,
    task_service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id)
):
    """Create a task from natural language input using AI analysis."""
    try:
        result = await task_service.create_task_from_natural_language(request, user_id)
        logger.info("Task created from NL via API", task_id=str(result["task"].id))
        return TaskCreateResponse(
            task=result["task"],
            analysis=result["analysis"],
            suggestions=result["suggestions"]
        )
    except Exception as e:
        logger.error("Failed to create task from NL via API", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to analyze and create task")


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[TaskStatusType] = None,
    project_id: Optional[UUID] = None,
    priority: Optional[int] = Query(None, ge=1, le=5),
    task_service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id)
):
    """Get tasks with optional filtering."""
    try:
        tasks = await task_service.get_tasks(
            user_id=user_id,
            skip=skip,
            limit=limit,
            status=status,
            project_id=project_id,
            priority=priority
        )
        logger.info("Tasks retrieved via API", count=len(tasks))
        return tasks
    except Exception as e:
        logger.error("Failed to get tasks via API", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve tasks")


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    task_service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id)
):
    """Get a specific task by ID."""
    try:
        task = await task_service.get_task(task_id, user_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        logger.info("Task retrieved via API", task_id=str(task_id))
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get task via API", task_id=str(task_id), error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve task")


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id)
):
    """Update an existing task."""
    try:
        task = await task_service.update_task(task_id, task_update, user_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        logger.info("Task updated via API", task_id=str(task_id))
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update task via API", task_id=str(task_id), error=str(e))
        raise HTTPException(status_code=500, detail="Failed to update task")


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: UUID,
    task_service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id)
):
    """Delete a task."""
    try:
        success = await task_service.delete_task(task_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        
        logger.info("Task deleted via API", task_id=str(task_id))
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete task via API", task_id=str(task_id), error=str(e))
        raise HTTPException(status_code=500, detail="Failed to delete task")


@router.post("/search", response_model=TaskSearchResponse)
async def search_tasks(
    search_request: TaskSearchRequest,
    task_service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id)
):
    """Search tasks using semantic similarity."""
    try:
        results = await task_service.search_tasks(search_request, user_id)
        logger.info("Task search completed via API", 
                   query=search_request.query, 
                   results_count=len(results.results))
        return results
    except Exception as e:
        logger.error("Failed to search tasks via API", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to search tasks") 