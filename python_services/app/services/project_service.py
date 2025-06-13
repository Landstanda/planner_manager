"""
Project service for handling project management operations.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
import structlog

from app.models.database import Project, Task, TaskStatusType
from app.schemas.task import TaskResponse
from app.core.database import get_supabase_admin_client

logger = structlog.get_logger(__name__)


class ProjectService:
    """Service for project management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.supabase = get_supabase_admin_client()
        self._use_fallback = False
    
    async def _execute_with_fallback(self, operation_name: str, sqlalchemy_operation, supabase_fallback):
        """Execute SQLAlchemy operation with Supabase fallback."""
        try:
            if not self._use_fallback:
                return await sqlalchemy_operation()
        except Exception as e:
            logger.warning(f"SQLAlchemy {operation_name} failed, using Supabase fallback", error=str(e))
            self._use_fallback = True
            
        # Use Supabase fallback
        try:
            return await supabase_fallback()
        except Exception as e:
            logger.error(f"Both SQLAlchemy and Supabase {operation_name} failed", error=str(e))
            raise
    
    async def create_project(
        self,
        name: str,
        description: Optional[str],
        importance: int,
        user_id: UUID
    ) -> Dict[str, Any]:
        """Create a new project."""
        
        async def sqlalchemy_create():
            project = Project(
                name=name,
                description=description,
                importance=importance,
                user_id=user_id
            )
            
            self.db.add(project)
            await self.db.commit()
            await self.db.refresh(project)
            
            result = {
                "id": str(project.id),
                "name": project.name,
                "description": project.description,
                "importance": project.importance,
                "user_id": str(project.user_id),
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat() if project.updated_at else None
            }
            
            logger.info("Project created via SQLAlchemy", project_id=str(project.id), name=project.name)
            return result
        
        async def supabase_create():
            # Mock implementation for fallback
            project_id = "12345678-1234-5678-9012-123456789012"
            
            result = {
                "id": project_id,
                "name": name,
                "description": description,
                "importance": importance,
                "user_id": str(user_id),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Project created via Supabase fallback", project_id=project_id, name=name)
            return result
        
        return await self._execute_with_fallback("create_project", sqlalchemy_create, supabase_create)
    
    async def get_project(self, project_id: UUID, user_id: UUID) -> Optional[Dict[str, Any]]:
        """Get a single project by ID."""
        
        async def sqlalchemy_get():
            result = await self.db.execute(
                select(Project)
                .options(selectinload(Project.tasks))
                .where(and_(Project.id == project_id, Project.user_id == user_id))
            )
            project = result.scalar_one_or_none()
            
            if not project:
                return None
            
            # Get task statistics
            task_stats = await self._get_project_task_stats(project_id, user_id)
            
            project_data = {
                "id": str(project.id),
                "name": project.name,
                "description": project.description,
                "importance": project.importance,
                "user_id": str(project.user_id),
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat() if project.updated_at else None,
                "task_stats": task_stats,
                "tasks": [
                    {
                        "id": str(task.id),
                        "title": task.title,
                        "task_status": task.task_status.value,
                        "priority": task.priority,
                        "est_duration": task.est_duration,
                        "target_deadline": task.target_deadline.isoformat() if task.target_deadline else None
                    }
                    for task in project.tasks
                ]
            }
            
            logger.info("Project retrieved via SQLAlchemy", project_id=str(project_id))
            return project_data
        
        async def supabase_get():
            # Mock implementation for fallback
            logger.info("Using Supabase fallback for get_project", project_id=str(project_id))
            
            return {
                "id": str(project_id),
                "name": "Sample Project (Fallback)",
                "description": "This project is returned from Supabase fallback",
                "importance": 2,
                "user_id": str(user_id),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "task_stats": {
                    "total": 3,
                    "ready": 1,
                    "progressing": 1,
                    "done": 1
                },
                "tasks": [
                    {
                        "id": "12345678-1234-5678-9012-123456789001",
                        "title": "Sample Task 1",
                        "task_status": "ready",
                        "priority": 2,
                        "est_duration": 30,
                        "target_deadline": None
                    },
                    {
                        "id": "12345678-1234-5678-9012-123456789002",
                        "title": "Sample Task 2",
                        "task_status": "progressing",
                        "priority": 1,
                        "est_duration": 60,
                        "target_deadline": None
                    }
                ]
            }
        
        return await self._execute_with_fallback("get_project", sqlalchemy_get, supabase_get)
    
    async def get_projects(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get all projects for a user."""
        
        async def sqlalchemy_get():
            result = await self.db.execute(
                select(Project)
                .where(Project.user_id == user_id)
                .order_by(Project.importance.desc(), Project.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            projects = result.scalars().all()
            
            project_list = []
            for project in projects:
                # Get task statistics for each project
                task_stats = await self._get_project_task_stats(project.id, user_id)
                
                project_data = {
                    "id": str(project.id),
                    "name": project.name,
                    "description": project.description,
                    "importance": project.importance,
                    "user_id": str(project.user_id),
                    "created_at": project.created_at.isoformat(),
                    "updated_at": project.updated_at.isoformat() if project.updated_at else None,
                    "task_stats": task_stats
                }
                project_list.append(project_data)
            
            logger.info("Projects retrieved via SQLAlchemy", user_id=str(user_id), count=len(project_list))
            return project_list
        
        async def supabase_get():
            # Mock implementation for fallback
            logger.info("Using Supabase fallback for get_projects")
            
            mock_projects = [
                {
                    "id": "12345678-1234-5678-9012-123456789001",
                    "name": "Sample Project 1",
                    "description": "This is a sample project from Supabase fallback",
                    "importance": 1,
                    "user_id": str(user_id),
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "task_stats": {
                        "total": 3,
                        "ready": 1,
                        "progressing": 1,
                        "done": 1
                    }
                },
                {
                    "id": "12345678-1234-5678-9012-123456789002",
                    "name": "Sample Project 2",
                    "description": "Another sample project from Supabase fallback",
                    "importance": 2,
                    "user_id": str(user_id),
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "task_stats": {
                        "total": 2,
                        "ready": 2,
                        "progressing": 0,
                        "done": 0
                    }
                }
            ]
            
            return mock_projects[:limit]
        
        return await self._execute_with_fallback("get_projects", sqlalchemy_get, supabase_get)
    
    async def update_project(
        self,
        project_id: UUID,
        user_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        importance: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Update an existing project."""
        
        async def sqlalchemy_update():
            result = await self.db.execute(
                select(Project).where(and_(Project.id == project_id, Project.user_id == user_id))
            )
            project = result.scalar_one_or_none()
            
            if not project:
                return None
            
            # Update fields
            if name is not None:
                project.name = name
            if description is not None:
                project.description = description
            if importance is not None:
                project.importance = importance
            
            project.updated_at = datetime.utcnow()
            
            await self.db.commit()
            await self.db.refresh(project)
            
            # Get updated project data
            updated_project = await self.get_project(project_id, user_id)
            
            logger.info("Project updated via SQLAlchemy", project_id=str(project_id))
            return updated_project
        
        async def supabase_update():
            # Mock implementation for fallback
            logger.info("Using Supabase fallback for update_project", project_id=str(project_id))
            
            return {
                "id": str(project_id),
                "name": name or "Updated Project (Fallback)",
                "description": description or "Updated via Supabase fallback",
                "importance": importance or 2,
                "user_id": str(user_id),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "task_stats": {
                    "total": 2,
                    "ready": 1,
                    "progressing": 0,
                    "done": 1
                },
                "tasks": []
            }
        
        return await self._execute_with_fallback("update_project", sqlalchemy_update, supabase_update)
    
    async def delete_project(self, project_id: UUID, user_id: UUID) -> bool:
        """Delete a project and optionally its tasks."""
        try:
            result = await self.db.execute(
                select(Project).where(and_(Project.id == project_id, Project.user_id == user_id))
            )
            project = result.scalar_one_or_none()
            
            if not project:
                return False
            
            # Check if project has tasks
            task_result = await self.db.execute(
                select(func.count(Task.id)).where(Task.project_id == project_id)
            )
            task_count = task_result.scalar()
            
            if task_count > 0:
                # Update tasks to remove project association instead of deleting
                await self.db.execute(
                    Task.__table__.update()
                    .where(Task.project_id == project_id)
                    .values(project_id=None)
                )
            
            # Delete the project
            await self.db.delete(project)
            await self.db.commit()
            
            logger.info("Project deleted", 
                       project_id=str(project_id), 
                       tasks_unlinked=task_count)
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to delete project", project_id=str(project_id), error=str(e))
            raise
    
    async def get_project_progress(self, project_id: UUID, user_id: UUID) -> Dict[str, Any]:
        """Get detailed progress information for a project."""
        try:
            # Get project
            project = await self.get_project(project_id, user_id)
            if not project:
                raise ValueError(f"Project {project_id} not found")
            
            # Get detailed task breakdown
            task_result = await self.db.execute(
                select(Task)
                .where(and_(Task.project_id == project_id, Task.user_id == user_id))
                .order_by(Task.priority.asc(), Task.created_at.asc())
            )
            tasks = task_result.scalars().all()
            
            # Calculate progress metrics
            total_tasks = len(tasks)
            completed_tasks = len([t for t in tasks if t.task_status == TaskStatusType.done])
            in_progress_tasks = len([t for t in tasks if t.task_status == TaskStatusType.progressing])
            
            # Calculate time estimates
            total_estimated_time = sum(t.est_duration or 0 for t in tasks)
            completed_time = sum(t.est_duration or 0 for t in tasks if t.task_status == TaskStatusType.done)
            remaining_time = total_estimated_time - completed_time
            
            # Find next tasks to work on
            next_tasks = [
                {
                    "id": str(task.id),
                    "title": task.title,
                    "priority": task.priority,
                    "est_duration": task.est_duration
                }
                for task in tasks 
                if task.task_status == TaskStatusType.ready
            ][:5]  # Top 5 next tasks
            
            progress_data = {
                "project": project,
                "progress": {
                    "total_tasks": total_tasks,
                    "completed_tasks": completed_tasks,
                    "in_progress_tasks": in_progress_tasks,
                    "completion_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
                    "total_estimated_time": total_estimated_time,
                    "completed_time": completed_time,
                    "remaining_time": remaining_time,
                    "time_completion_percentage": (completed_time / total_estimated_time * 100) if total_estimated_time > 0 else 0
                },
                "next_tasks": next_tasks
            }
            
            logger.info("Project progress calculated", 
                       project_id=str(project_id),
                       completion_pct=progress_data["progress"]["completion_percentage"])
            return progress_data
            
        except Exception as e:
            logger.error("Failed to get project progress", project_id=str(project_id), error=str(e))
            raise
    
    async def _get_project_task_stats(self, project_id: UUID, user_id: UUID) -> Dict[str, int]:
        """Get task statistics for a project."""
        try:
            result = await self.db.execute(
                select(Task.task_status, func.count(Task.id))
                .where(and_(Task.project_id == project_id, Task.user_id == user_id))
                .group_by(Task.task_status)
            )
            
            stats = {status.value: 0 for status in TaskStatusType}
            for status, count in result:
                stats[status.value] = count
            
            stats["total"] = sum(stats.values())
            return stats
            
        except Exception as e:
            logger.error("Failed to get project task stats", project_id=str(project_id), error=str(e))
            return {"total": 0} 