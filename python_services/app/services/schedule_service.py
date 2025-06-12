"""
Schedule service for handling daily schedule management and time blocking.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, date, time, timedelta
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
import structlog

from app.models.database import DailySchedule, ScheduleTemplate, Task, BlockType
from app.services.ai_service import AIService
from app.core.database import get_supabase_client

logger = structlog.get_logger(__name__)


class ScheduleService:
    """Service for schedule management operations."""
    
    def __init__(self, db: AsyncSession, ai_service: AIService):
        self.db = db
        self.ai_service = ai_service
        self.supabase = get_supabase_client()
    
    async def get_daily_schedule(
        self, 
        user_id: UUID, 
        target_date: date
    ) -> List[Dict[str, Any]]:
        """Get the daily schedule for a specific date."""
        try:
            # Convert date to datetime for database query
            start_datetime = datetime.combine(target_date, time.min)
            end_datetime = datetime.combine(target_date, time.max)
            
            result = await self.db.execute(
                select(DailySchedule)
                .where(and_(
                    DailySchedule.user_id == user_id,
                    DailySchedule.date >= start_datetime,
                    DailySchedule.date <= end_datetime
                ))
                .order_by(DailySchedule.start_time)
            )
            
            schedule_entries = result.scalars().all()
            
            # Convert to dict format
            schedule = []
            for entry in schedule_entries:
                schedule.append({
                    "id": str(entry.id),
                    "date": entry.date.isoformat(),
                    "start_time": entry.start_time,
                    "end_time": entry.end_time,
                    "title": entry.title,
                    "description": entry.description,
                    "task_id": str(entry.task_id) if entry.task_id else None,
                    "priority": entry.priority,
                    "task_type": entry.task_type,
                    "scheduled_by": entry.scheduled_by
                })
            
            logger.info("Daily schedule retrieved", 
                       user_id=str(user_id), 
                       date=str(target_date),
                       entries_count=len(schedule))
            return schedule
            
        except Exception as e:
            logger.error("Failed to get daily schedule", 
                        user_id=str(user_id), 
                        date=str(target_date), 
                        error=str(e))
            raise
    
    async def get_schedule_template(
        self, 
        user_id: UUID, 
        day_of_week: str
    ) -> List[Dict[str, Any]]:
        """Get the schedule template for a specific day of the week."""
        try:
            result = await self.db.execute(
                select(ScheduleTemplate)
                .where(and_(
                    ScheduleTemplate.user_id == user_id,
                    ScheduleTemplate.day_of_week == day_of_week.lower()
                ))
                .order_by(ScheduleTemplate.start_time)
            )
            
            template_entries = result.scalars().all()
            
            template = []
            for entry in template_entries:
                template.append({
                    "id": str(entry.id),
                    "day_of_week": entry.day_of_week,
                    "start_time": entry.start_time,
                    "end_time": entry.end_time,
                    "block_type": entry.block_type.value,
                    "label": entry.label,
                    "description": entry.description
                })
            
            logger.info("Schedule template retrieved", 
                       user_id=str(user_id), 
                       day_of_week=day_of_week,
                       entries_count=len(template))
            return template
            
        except Exception as e:
            logger.error("Failed to get schedule template", 
                        user_id=str(user_id), 
                        day_of_week=day_of_week, 
                        error=str(e))
            raise
    
    async def find_available_time_slots(
        self,
        user_id: UUID,
        target_date: date,
        duration_minutes: int,
        preferred_times: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Find available time slots for scheduling a task."""
        try:
            # Get existing schedule for the day
            existing_schedule = await self.get_daily_schedule(user_id, target_date)
            
            # Get schedule template for the day of week
            day_name = target_date.strftime('%A').lower()
            template = await self.get_schedule_template(user_id, day_name)
            
            # Find available blocks from template
            available_slots = []
            for block in template:
                if block["block_type"] == "available":
                    # Check if this time slot conflicts with existing schedule
                    start_time = datetime.strptime(block["start_time"], "%H:%M").time()
                    end_time = datetime.strptime(block["end_time"], "%H:%M").time()
                    
                    # Calculate duration of available block
                    start_datetime = datetime.combine(target_date, start_time)
                    end_datetime = datetime.combine(target_date, end_time)
                    block_duration = (end_datetime - start_datetime).total_seconds() / 60
                    
                    if block_duration >= duration_minutes:
                        # Check for conflicts
                        has_conflict = False
                        for scheduled in existing_schedule:
                            scheduled_start = datetime.strptime(scheduled["start_time"], "%H:%M").time()
                            scheduled_end = datetime.strptime(scheduled["end_time"], "%H:%M").time()
                            
                            # Check for overlap
                            if (start_time < scheduled_end and end_time > scheduled_start):
                                has_conflict = True
                                break
                        
                        if not has_conflict:
                            available_slots.append({
                                "start_time": block["start_time"],
                                "end_time": block["end_time"],
                                "duration_available": int(block_duration),
                                "label": block["label"]
                            })
            
            logger.info("Available time slots found", 
                       user_id=str(user_id), 
                       date=str(target_date),
                       duration_needed=duration_minutes,
                       slots_found=len(available_slots))
            return available_slots
            
        except Exception as e:
            logger.error("Failed to find available time slots", 
                        user_id=str(user_id), 
                        date=str(target_date), 
                        error=str(e))
            raise
    
    async def schedule_task(
        self,
        user_id: UUID,
        task_id: UUID,
        target_date: date,
        start_time: str,
        duration_minutes: int,
        scheduling_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Schedule a task at a specific time."""
        try:
            # Get task details
            task_result = await self.db.execute(
                select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
            )
            task = task_result.scalar_one_or_none()
            
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            # Calculate end time
            start_datetime = datetime.strptime(start_time, "%H:%M")
            end_datetime = start_datetime + timedelta(minutes=duration_minutes)
            end_time = end_datetime.strftime("%H:%M")
            
            # Create schedule entry
            schedule_entry = DailySchedule(
                date=datetime.combine(target_date, datetime.min.time()),
                start_time=start_time,
                end_time=end_time,
                title=task.title,
                description=task.description,
                task_id=task_id,
                priority=task.priority,
                task_type="task",
                scheduled_by="manual",
                user_id=user_id
            )
            
            self.db.add(schedule_entry)
            await self.db.commit()
            await self.db.refresh(schedule_entry)
            
            result = {
                "id": str(schedule_entry.id),
                "task_id": str(task_id),
                "date": target_date.isoformat(),
                "start_time": start_time,
                "end_time": end_time,
                "title": task.title,
                "duration_minutes": duration_minutes,
                "scheduled_by": "manual"
            }
            
            logger.info("Task scheduled successfully", 
                       task_id=str(task_id), 
                       schedule_id=str(schedule_entry.id))
            return result
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to schedule task", 
                        task_id=str(task_id), 
                        error=str(e))
            raise
    
    async def intelligent_schedule_task(
        self,
        user_id: UUID,
        task_id: UUID,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Use AI to intelligently schedule a task."""
        try:
            # Get task details
            task_result = await self.db.execute(
                select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
            )
            task = task_result.scalar_one_or_none()
            
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            # Prepare task data for AI analysis
            task_data = {
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "est_duration": task.est_duration or 30,
                "target_deadline": task.target_deadline.isoformat() if task.target_deadline else None,
                "dl_hardness": task.dl_hardness
            }
            
            # Get schedule context for next few days
            today = date.today()
            schedule_context = {}
            for i in range(7):  # Look ahead 7 days
                check_date = today + timedelta(days=i)
                daily_schedule = await self.get_daily_schedule(user_id, check_date)
                available_slots = await self.find_available_time_slots(
                    user_id, 
                    check_date, 
                    task_data["est_duration"]
                )
                schedule_context[check_date.isoformat()] = {
                    "existing_schedule": daily_schedule,
                    "available_slots": available_slots
                }
            
            # Use AI to make scheduling decision
            user_preferences = preferences or {}
            decision = await self.ai_service.analyze_scheduling_decision(
                task_data,
                schedule_context,
                user_preferences
            )
            
            # If AI recommends scheduling, do it
            if decision.get("action") == "schedule":
                suggested_date = decision.get("suggested_date", today.isoformat())
                suggested_time = decision.get("suggested_time", "09:00")
                
                target_date = datetime.fromisoformat(suggested_date).date()
                
                result = await self.schedule_task(
                    user_id,
                    task_id,
                    target_date,
                    suggested_time,
                    task_data["est_duration"]
                )
                
                result["ai_decision"] = decision
                result["scheduled_by"] = "ai_scheduler"
                
                return result
            else:
                # Return the AI decision without scheduling
                return {
                    "action": decision.get("action"),
                    "reasoning": decision.get("reasoning"),
                    "ai_decision": decision,
                    "scheduled": False
                }
            
        except Exception as e:
            logger.error("Failed to intelligently schedule task", 
                        task_id=str(task_id), 
                        error=str(e))
            raise 