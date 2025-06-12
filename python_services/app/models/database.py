"""
SQLAlchemy models for the Chief-of-Flow database schema.
Corresponds to the Supabase tables defined in supabase_tables.sql.
"""

from sqlalchemy import (
    Column, String, Integer, DateTime, Boolean, Text, 
    ForeignKey, ARRAY, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

# Import pgvector for vector columns
try:
    from pgvector.sqlalchemy import Vector
    VECTOR_AVAILABLE = True
except ImportError:
    # Fallback for testing without pgvector
    VECTOR_AVAILABLE = False
    Vector = Text  # Use Text as fallback

from app.core.database import Base


class TaskStatusType(enum.Enum):
    """Task status enumeration."""
    dependent = "dependent"
    ready = "ready"
    progressing = "progressing" 
    done = "done"
    cancelled = "cancelled"


class BlockType(enum.Enum):
    """Schedule block type enumeration."""
    available = "available"
    personal = "personal"


class Project(Base):
    """Projects table model."""
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    importance = Column(Integer, default=3)  # 1-5 scale
    user_id = Column(UUID(as_uuid=True), nullable=False)  # ForeignKey reference to auth.users
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    """Tasks table model."""
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    task_status = Column(SQLEnum(TaskStatusType), default=TaskStatusType.ready)
    priority = Column(Integer, default=3)  # 1-5 scale (1=critical, 5=someday)
    est_duration = Column(Integer)  # Duration in minutes
    dur_conf = Column(Integer, default=3)  # Duration confidence 1-5
    dependencies = Column(ARRAY(UUID(as_uuid=True)), default=[])
    subtasks = Column(ARRAY(UUID(as_uuid=True)), default=[])
    target_deadline = Column(DateTime(timezone=True))
    dl_hardness = Column(Integer, default=3)  # Deadline hardness 1-5
    reoccuring = Column(String)  # iCalendar RRULE string
    description = Column(Text)
    notes = Column(Text)
    tags = Column(ARRAY(String), default=[])
    deferred = Column(Integer, default=0)
    # Use Vector if available, otherwise Text for embedding
    embedding = Column(Vector(1536) if VECTOR_AVAILABLE else Text)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # ForeignKey reference to auth.users
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="tasks")


class DailySchedule(Base):
    """Daily schedule table model."""
    __tablename__ = "daily_schedule"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime(timezone=True), nullable=False)
    start_time = Column(String, nullable=False)  # HH:MM format
    end_time = Column(String, nullable=False)    # HH:MM format
    title = Column(String, nullable=False)
    description = Column(Text)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    priority = Column(Integer)
    task_type = Column(String(50))  # task/appointment/meeting
    scheduled_by = Column(String(100))  # manual/ai_scheduler/rescheduler
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ScheduleTemplate(Base):
    """Schedule template table model."""
    __tablename__ = "schedule_template"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day_of_week = Column(String(10), nullable=False)  # monday, tuesday, etc.
    start_time = Column(String, nullable=False)  # HH:MM format
    end_time = Column(String, nullable=False)    # HH:MM format
    block_type = Column(SQLEnum(BlockType), nullable=False)
    label = Column(String, nullable=False)
    description = Column(Text)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserLLMInstructions(Base):
    """User LLM instructions table model."""
    __tablename__ = "user_llm_instructions"
    
    instruction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    instruction_text = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    category = Column(Text)  # tone, response_format, scheduling_preference
    priority = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserPersonalityProfile(Base):
    """User personality profile table model."""
    __tablename__ = "user_personality_profile"
    
    profile_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    criteria = Column(Text)  # JSON string of core values/motivators
    motivation_direction = Column(Integer, default=0)  # -5 to +5 (away-from to toward)
    warm_candid = Column(Integer, default=0)  # -5 to +5 (candid to warm)
    proactive_reactive = Column(Integer, default=0)  # -5 to +5 (reactive to proactive)
    reassurance_needs = Column(Integer, default=0)  # -5 to +5 (low to high reassurance)
    language_variety = Column(Integer, default=0)  # -5 to +5 (consistent to varied)
    assessment_completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 