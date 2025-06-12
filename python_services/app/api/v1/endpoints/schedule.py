"""
Schedule management API endpoints.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.services.schedule_service import ScheduleService
from app.services.ai_service import AIService
from app.schemas.task import ScheduleEntryCreate, ScheduleEntryResponse

logger = structlog.get_logger(__name__)
router = APIRouter()

# Mock user ID for development (TODO: Replace with actual authentication)
MOCK_USER_ID = uuid4()


@router.get("/")
async def get_daily_schedule(
    target_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    db: AsyncSession = Depends(get_db)
):
    """Get the daily schedule for a specific date."""
    try:
        # Parse date or use today
        if target_date:
            schedule_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        else:
            schedule_date = date.today()
        
        schedule_service = ScheduleService(db, AIService())
        schedule = await schedule_service.get_daily_schedule(MOCK_USER_ID, schedule_date)
        
        return {
            "date": schedule_date.isoformat(),
            "entries": schedule,
            "total_entries": len(schedule)
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}"
        )
    except Exception as e:
        logger.error("Failed to get daily schedule", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve daily schedule"
        )


@router.get("/template")
async def get_schedule_template(
    day_of_week: str = Query(..., description="Day of week (monday, tuesday, etc.)"),
    db: AsyncSession = Depends(get_db)
):
    """Get the schedule template for a specific day of the week."""
    try:
        schedule_service = ScheduleService(db, AIService())
        template = await schedule_service.get_schedule_template(MOCK_USER_ID, day_of_week)
        
        return {
            "day_of_week": day_of_week.lower(),
            "template": template,
            "total_blocks": len(template)
        }
        
    except Exception as e:
        logger.error("Failed to get schedule template", day_of_week=day_of_week, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve schedule template"
        )


@router.get("/available-slots")
async def get_available_time_slots(
    target_date: str = Query(..., description="Date in YYYY-MM-DD format"),
    duration_minutes: int = Query(..., description="Required duration in minutes"),
    db: AsyncSession = Depends(get_db)
):
    """Find available time slots for scheduling a task."""
    try:
        schedule_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        
        schedule_service = ScheduleService(db, AIService())
        available_slots = await schedule_service.find_available_time_slots(
            user_id=MOCK_USER_ID,
            target_date=schedule_date,
            duration_minutes=duration_minutes
        )
        
        return {
            "date": schedule_date.isoformat(),
            "duration_needed": duration_minutes,
            "available_slots": available_slots,
            "slots_found": len(available_slots)
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}"
        )
    except Exception as e:
        logger.error("Failed to find available time slots", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to find available time slots"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_schedule_entry(
    schedule_entry: ScheduleEntryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new schedule entry (manual scheduling)."""
    try:
        schedule_service = ScheduleService(db, AIService())
        
        # Parse the target date
        target_date = datetime.strptime(schedule_entry.date, "%Y-%m-%d").date()
        
        result = await schedule_service.schedule_task(
            user_id=MOCK_USER_ID,
            task_id=schedule_entry.task_id,
            target_date=target_date,
            start_time=schedule_entry.start_time,
            duration_minutes=schedule_entry.duration_minutes
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to create schedule entry", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create schedule entry"
        )


@router.post("/intelligent-schedule")
async def intelligent_schedule_task(
    task_id: UUID,
    preferences: Optional[Dict[str, Any]] = None,
    db: AsyncSession = Depends(get_db)
):
    """Use AI to intelligently schedule a task."""
    try:
        ai_service = AIService()
        schedule_service = ScheduleService(db, ai_service)
        
        result = await schedule_service.intelligent_schedule_task(
            user_id=MOCK_USER_ID,
            task_id=task_id,
            preferences=preferences or {}
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to intelligently schedule task", task_id=str(task_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to intelligently schedule task"
        )


@router.get("/week")
async def get_weekly_schedule(
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    db: AsyncSession = Depends(get_db)
):
    """Get the schedule for a full week."""
    try:
        # Parse start date or use current week
        if start_date:
            week_start = datetime.strptime(start_date, "%Y-%m-%d").date()
        else:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())  # Monday of current week
        
        schedule_service = ScheduleService(db, AIService())
        weekly_schedule = {}
        
        # Get schedule for each day of the week
        for i in range(7):
            current_date = week_start + timedelta(days=i)
            daily_schedule = await schedule_service.get_daily_schedule(MOCK_USER_ID, current_date)
            weekly_schedule[current_date.isoformat()] = daily_schedule
        
        return {
            "week_start": week_start.isoformat(),
            "schedule": weekly_schedule,
            "total_days": 7
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}"
        )
    except Exception as e:
        logger.error("Failed to get weekly schedule", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve weekly schedule"
        )


@router.get("/stats")
async def get_schedule_stats(
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
    db: AsyncSession = Depends(get_db)
):
    """Get schedule statistics for a date range."""
    try:
        # Default to current week if no dates provided
        if not start_date:
            today = date.today()
            start_date = (today - timedelta(days=today.weekday())).isoformat()
        if not end_date:
            end_date = (datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=6)).isoformat()
        
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        schedule_service = ScheduleService(db, AIService())
        
        # Collect statistics
        total_entries = 0
        total_scheduled_time = 0
        task_types = {"task": 0, "appointment": 0, "meeting": 0}
        priorities = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        current_date = start_dt
        while current_date <= end_dt:
            daily_schedule = await schedule_service.get_daily_schedule(MOCK_USER_ID, current_date)
            
            for entry in daily_schedule:
                total_entries += 1
                
                # Calculate duration
                start_time = datetime.strptime(entry["start_time"], "%H:%M")
                end_time = datetime.strptime(entry["end_time"], "%H:%M")
                duration = (end_time - start_time).total_seconds() / 60
                total_scheduled_time += duration
                
                # Count task types
                task_type = entry.get("task_type", "task")
                if task_type in task_types:
                    task_types[task_type] += 1
                
                # Count priorities
                priority = entry.get("priority", 3)
                if priority in priorities:
                    priorities[priority] += 1
            
            current_date += timedelta(days=1)
        
        return {
            "date_range": {
                "start": start_date,
                "end": end_date
            },
            "statistics": {
                "total_entries": total_entries,
                "total_scheduled_hours": round(total_scheduled_time / 60, 2),
                "average_entries_per_day": round(total_entries / ((end_dt - start_dt).days + 1), 1),
                "task_types": task_types,
                "priority_distribution": priorities
            }
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}"
        )
    except Exception as e:
        logger.error("Failed to get schedule stats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve schedule statistics"
        ) 