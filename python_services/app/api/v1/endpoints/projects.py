"""
Project management API endpoints.
"""

from typing import List, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.services.project_service import ProjectService
from app.schemas.task import ProjectCreate, ProjectUpdate, ProjectResponse

logger = structlog.get_logger(__name__)
router = APIRouter()

# Mock user ID for development (TODO: Replace with actual authentication)
MOCK_USER_ID = uuid4()


@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all projects for the current user."""
    try:
        project_service = ProjectService(db)
        projects = await project_service.get_projects(
            user_id=MOCK_USER_ID,
            skip=skip,
            limit=limit
        )
        
        # Convert to response format
        return [
            ProjectResponse(
                id=UUID(project["id"]),
                name=project["name"],
                description=project["description"],
                importance=project["importance"],
                created_at=project["created_at"],
                updated_at=project["updated_at"],
                task_stats=project["task_stats"]
            )
            for project in projects
        ]
        
    except Exception as e:
        logger.error("Failed to get projects", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve projects"
        )


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new project."""
    try:
        project_service = ProjectService(db)
        created_project = await project_service.create_project(
            name=project.name,
            description=project.description,
            importance=project.importance,
            user_id=MOCK_USER_ID
        )
        
        return ProjectResponse(
            id=UUID(created_project["id"]),
            name=created_project["name"],
            description=created_project["description"],
            importance=created_project["importance"],
            created_at=created_project["created_at"],
            updated_at=created_project["updated_at"],
            task_stats={"total": 0}  # New project has no tasks
        )
        
    except Exception as e:
        logger.error("Failed to create project", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project"
        )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific project by ID."""
    try:
        project_service = ProjectService(db)
        project = await project_service.get_project(project_id, MOCK_USER_ID)
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        return ProjectResponse(
            id=UUID(project["id"]),
            name=project["name"],
            description=project["description"],
            importance=project["importance"],
            created_at=project["created_at"],
            updated_at=project["updated_at"],
            task_stats=project["task_stats"],
            tasks=project.get("tasks", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get project", project_id=str(project_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve project"
        )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_update: ProjectUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing project."""
    try:
        project_service = ProjectService(db)
        updated_project = await project_service.update_project(
            project_id=project_id,
            user_id=MOCK_USER_ID,
            name=project_update.name,
            description=project_update.description,
            importance=project_update.importance
        )
        
        if not updated_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        return ProjectResponse(
            id=UUID(updated_project["id"]),
            name=updated_project["name"],
            description=updated_project["description"],
            importance=updated_project["importance"],
            created_at=updated_project["created_at"],
            updated_at=updated_project["updated_at"],
            task_stats=updated_project["task_stats"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update project", project_id=str(project_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project"
        )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a project."""
    try:
        project_service = ProjectService(db)
        deleted = await project_service.delete_project(project_id, MOCK_USER_ID)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete project", project_id=str(project_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project"
        )


@router.get("/{project_id}/progress")
async def get_project_progress(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed progress information for a project."""
    try:
        project_service = ProjectService(db)
        progress = await project_service.get_project_progress(project_id, MOCK_USER_ID)
        
        return progress
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to get project progress", project_id=str(project_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve project progress"
        ) 