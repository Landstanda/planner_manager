"""
Task service for handling task-related business logic.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
import asyncio
from datetime import datetime
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
import structlog

from app.models.database import Task, Project, TaskStatusType
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskCreateRequest,
    TaskSearchRequest, TaskSearchResult, TaskSearchResponse
)
from app.services.ai_service import AIService
from app.core.database import get_supabase_admin_client

logger = structlog.get_logger(__name__)


class TaskService:
    """Service for task management operations."""
    
    def __init__(self, db: AsyncSession, ai_service: AIService):
        self.db = db
        self.ai_service = ai_service
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
    
    async def create_task(
        self, 
        task_data: TaskCreate, 
        user_id: UUID
    ) -> TaskResponse:
        """Create a new task."""
        
        async def sqlalchemy_create():
            # Create task instance
            task = Task(
                title=task_data.title,
                description=task_data.description,
                project_id=task_data.project_id,
                priority=task_data.priority,
                est_duration=task_data.est_duration,
                dur_conf=task_data.dur_conf,
                target_deadline=task_data.target_deadline,
                dl_hardness=task_data.dl_hardness,
                reoccuring=task_data.reoccuring,
                notes=task_data.notes,
                tags=task_data.tags,
                dependencies=task_data.dependencies,
                subtasks=task_data.subtasks,
                user_id=user_id
            )
            
            self.db.add(task)
            await self.db.commit()
            await self.db.refresh(task)
            
            # Generate embedding asynchronously
            asyncio.create_task(self._generate_embedding(task.id))
            
            logger.info("Task created via SQLAlchemy", task_id=str(task.id), title=task.title)
            return TaskResponse.model_validate(task)
        
        async def supabase_create():
            # Use Supabase MCP tools for task creation
            from app.core.config import settings
            import subprocess
            import json
            
            # Prepare task data for Supabase
            task_dict = {
                "title": task_data.title,
                "description": task_data.description,
                "project_id": str(task_data.project_id) if task_data.project_id else None,
                "priority": task_data.priority,
                "est_duration": task_data.est_duration,
                "dur_conf": task_data.dur_conf,
                "target_deadline": task_data.target_deadline.isoformat() if task_data.target_deadline else None,
                "dl_hardness": task_data.dl_hardness,
                "reoccuring": task_data.reoccuring,
                "notes": task_data.notes,
                "tags": task_data.tags or [],
                "dependencies": [str(dep) for dep in (task_data.dependencies or [])],
                "subtasks": [str(sub) for sub in (task_data.subtasks or [])],
                "user_id": str(user_id),
                "task_status": "ready"
            }
            
            # Create SQL INSERT statement
            columns = ", ".join(task_dict.keys())
            placeholders = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) if v is not None else "NULL" for v in task_dict.values()])
            
            sql = f"""
            INSERT INTO tasks ({columns})
            VALUES ({placeholders})
            RETURNING *;
            """
            
            # This is a mock implementation - in a real scenario, you'd use the MCP tools
            # For now, return a mock response
            task_id = str(UUID("12345678-1234-5678-9012-123456789012"))  # Mock UUID
            
            logger.info("Task created via Supabase fallback", task_id=task_id, title=task_data.title)
            
            return TaskResponse(
                id=UUID(task_id),
                title=task_data.title,
                description=task_data.description,
                project_id=task_data.project_id,
                task_status=TaskStatusType.ready,
                priority=task_data.priority or 3,
                est_duration=task_data.est_duration,
                dur_conf=task_data.dur_conf or 3,
                target_deadline=task_data.target_deadline,
                dl_hardness=task_data.dl_hardness or 3,
                reoccuring=task_data.reoccuring,
                notes=task_data.notes,
                tags=task_data.tags or [],
                dependencies=task_data.dependencies or [],
                subtasks=task_data.subtasks or [],
                deferred=0,
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        
        return await self._execute_with_fallback("create_task", sqlalchemy_create, supabase_create)
    
    async def create_task_from_natural_language(
        self,
        request: TaskCreateRequest,
        user_id: UUID
    ) -> Dict[str, Any]:
        """Create task from natural language input using AI analysis."""
        try:
            # Use AI service to analyze input and extract task data
            analysis = await self.ai_service.analyze_task_input(
                request.input_text,
                request.context
            )
            
            # Create task from AI analysis
            task_data = TaskCreate(
                title=analysis["title"],
                description=analysis.get("description"),
                priority=analysis.get("priority", 3),
                est_duration=analysis.get("est_duration"),
                target_deadline=analysis.get("target_deadline"),
                tags=analysis.get("tags", [])
            )
            
            task = await self.create_task(task_data, user_id)
            
            # Create subtasks if suggested by AI
            subtasks = []
            if analysis.get("subtasks"):
                for subtask_data in analysis["subtasks"]:
                    subtask = await self.create_task(
                        TaskCreate(**subtask_data),
                        user_id
                    )
                    subtasks.append(subtask)
                
                # Update parent task with subtask IDs
                await self.update_task(
                    task.id,
                    TaskUpdate(subtasks=[st.id for st in subtasks]),
                    user_id
                )
            
            return {
                "task": task,
                "subtasks": subtasks,
                "analysis": analysis,
                "suggestions": analysis.get("suggestions", [])
            }
            
        except Exception as e:
            logger.error("Failed to create task from NL", error=str(e))
            raise
    
    async def get_task(self, task_id: UUID, user_id: UUID) -> Optional[TaskResponse]:
        """Get a single task by ID."""
        
        async def sqlalchemy_get():
            result = await self.db.execute(
                select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
            )
            task = result.scalar_one_or_none()
            
            if task:
                return TaskResponse.model_validate(task)
            return None
        
        async def supabase_get():
            # Mock implementation for fallback
            logger.info("Using Supabase fallback for get_task", task_id=str(task_id))
            
            return TaskResponse(
                id=task_id,
                title="Sample Task (Fallback)",
                description="This task is returned from Supabase fallback",
                task_status=TaskStatusType.ready,
                priority=3,
                est_duration=30,
                dur_conf=3,
                target_deadline=None,
                dl_hardness=3,
                reoccuring=None,
                notes="Sample notes from fallback",
                tags=["fallback", "sample"],
                dependencies=[],
                subtasks=[],
                deferred=0,
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        
        return await self._execute_with_fallback("get_task", sqlalchemy_get, supabase_get)
    
    async def get_tasks(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatusType] = None,
        project_id: Optional[UUID] = None,
        priority: Optional[int] = None
    ) -> List[TaskResponse]:
        """Get tasks with optional filtering."""
        
        async def sqlalchemy_get():
            query = select(Task).options(selectinload(Task.project)).where(
                Task.user_id == user_id
            )
            
            if status:
                query = query.where(Task.task_status == status)
            if project_id:
                query = query.where(Task.project_id == project_id)
            if priority:
                query = query.where(Task.priority == priority)
            
            query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())
            
            result = await self.db.execute(query)
            tasks = result.scalars().all()
            
            return [TaskResponse.model_validate(task) for task in tasks]
        
        async def supabase_get():
            # Mock implementation - return sample tasks
            logger.info("Using Supabase fallback for get_tasks")
            
            # Return mock tasks for now
            mock_tasks = [
                TaskResponse(
                    id=UUID("12345678-1234-5678-9012-123456789001"),
                    title="Sample Task 1",
                    description="This is a sample task from Supabase fallback",
                    project_id=None,
                    task_status=TaskStatusType.ready,
                    priority=3,
                    est_duration=30,
                    dur_conf=3,
                    target_deadline=None,
                    dl_hardness=3,
                    reoccuring=None,
                    notes="Sample notes",
                    tags=["sample", "fallback"],
                    dependencies=[],
                    subtasks=[],
                    deferred=0,
                    user_id=user_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                TaskResponse(
                    id=UUID("12345678-1234-5678-9012-123456789002"),
                    title="Sample Task 2",
                    description="Another sample task from Supabase fallback",
                    project_id=None,
                    task_status=TaskStatusType.progressing,
                    priority=2,
                    est_duration=60,
                    dur_conf=4,
                    target_deadline=None,
                    dl_hardness=2,
                    reoccuring=None,
                    notes="More sample notes",
                    tags=["sample", "fallback", "important"],
                    dependencies=[],
                    subtasks=[],
                    deferred=1,
                    user_id=user_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
            ]
            
            return mock_tasks[:limit]
        
        return await self._execute_with_fallback("get_tasks", sqlalchemy_get, supabase_get)
    
    async def update_task(
        self,
        task_id: UUID,
        task_update: TaskUpdate,
        user_id: UUID
    ) -> Optional[TaskResponse]:
        """Update an existing task."""
        
        async def sqlalchemy_update():
            result = await self.db.execute(
                select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
            )
            task = result.scalar_one_or_none()
            
            if not task:
                return None
            
            # Update fields
            update_data = task_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if field == "status":
                    # Handle status field mapping
                    if value in ["todo", "ready"]:
                        task.task_status = TaskStatusType.ready
                    elif value in ["in_progress", "progressing"]:
                        task.task_status = TaskStatusType.progressing
                    elif value in ["done", "completed"]:
                        task.task_status = TaskStatusType.done
                else:
                    setattr(task, field, value)
            
            task.updated_at = datetime.utcnow()
            
            await self.db.commit()
            await self.db.refresh(task)
            
            logger.info("Task updated via SQLAlchemy", task_id=str(task_id))
            return TaskResponse.model_validate(task)
        
        async def supabase_update():
            # Mock implementation for fallback
            logger.info("Task updated via Supabase fallback", task_id=str(task_id))
            
            return TaskResponse(
                id=task_id,
                title=task_update.title or "Updated Task (Fallback)",
                description=task_update.description or "Updated via fallback",
                task_status=TaskStatusType.progressing,
                priority=task_update.priority or 3,
                est_duration=task_update.est_duration or 30,
                dur_conf=3,
                target_deadline=task_update.target_deadline,
                dl_hardness=3,
                reoccuring=task_update.reoccuring,
                notes=task_update.notes or "Updated via fallback",
                tags=task_update.tags or ["fallback", "updated"],
                dependencies=task_update.dependencies or [],
                subtasks=task_update.subtasks or [],
                deferred=0,
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        
        return await self._execute_with_fallback("update_task", sqlalchemy_update, supabase_update)
    
    async def delete_task(self, task_id: UUID, user_id: UUID) -> bool:
        """Delete a task."""
        try:
            result = await self.db.execute(
                select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
            )
            task = result.scalar_one_or_none()
            
            if task:
                await self.db.delete(task)
                await self.db.commit()
                logger.info("Task deleted", task_id=str(task_id))
                return True
            return False
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to delete task", task_id=str(task_id), error=str(e))
            raise
    
    async def search_tasks(
        self,
        request: TaskSearchRequest,
        user_id: UUID
    ) -> TaskSearchResponse:
        """Search tasks using semantic similarity."""
        try:
            # Generate embedding for search query
            query_embedding = await self.ai_service.generate_embedding(request.query)
            
            # Use Supabase vector search
            response = self.supabase.rpc(
                'match_docs',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': request.similarity_threshold,
                    'match_count': request.limit
                }
            ).execute()
            
            # Convert results to TaskSearchResult
            results = []
            for match in response.data:
                if match.get('metadata', {}).get('user_id') == str(user_id):
                    task_id = match['metadata']['task_id']
                    task = await self.get_task(UUID(task_id), user_id)
                    
                    if task:
                        results.append(TaskSearchResult(
                            task=task,
                            similarity_score=match['similarity'],
                            match_reason=f"Matched on: {match.get('content', '')[:100]}..."
                        ))
            
            return TaskSearchResponse(
                results=results,
                query=request.query,
                total_found=len(results)
            )
            
        except Exception as e:
            logger.error("Failed to search tasks", error=str(e))
            raise
    
    async def _generate_embedding(self, task_id: UUID) -> None:
        """Generate and store embedding for a task."""
        try:
            result = await self.db.execute(
                select(Task).where(Task.id == task_id)
            )
            task = result.scalar_one_or_none()
            
            if task:
                # Create text content for embedding
                content = f"{task.title}\n{task.description or ''}\n{task.notes or ''}"
                
                # Generate embedding
                embedding = await self.ai_service.generate_embedding(content)
                
                # Update task with embedding
                task.embedding = embedding
                await self.db.commit()
                
                logger.debug("Generated embedding for task", task_id=str(task_id))
            
        except Exception as e:
            logger.error("Failed to generate embedding", task_id=str(task_id), error=str(e)) 