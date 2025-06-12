-- Enable UUID generation if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- For vector support in the tasks table.
-- 1. Run this line separately in the Supabase SQL editor if the extension is not yet enabled:
-- CREATE EXTENSION IF NOT EXISTS vector;
-- 2. Replace '''1536''' in the tasks table definition with the actual dimension of your embeddings.

-- Enum type for task status
CREATE TYPE public.task_status_type AS ENUM (
    '''dependent''',
    '''ready''',
    '''progressing''',
    '''done''',
    '''cancelled'''
);

-- Enum type for calendar event status
CREATE TYPE public.event_status_type AS ENUM (
    '''CONFIRMED''',
    '''TENTATIVE''',
    '''CANCELLED'''
);

-- Projects Table
CREATE TABLE public.projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    priority SMALLINT CHECK (priority >= 1 AND priority <= 5),
    goals TEXT,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE public.projects IS '''Stores information about user projects.''';
COMMENT ON COLUMN public.projects.priority IS '''Project priority, 1=critical, 5=someday.''';

-- Tasks Table
CREATE TABLE public.tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    project_id UUID REFERENCES public.projects(id) ON DELETE SET NULL,
    task_status public.task_status_type DEFAULT '''ready''',
    priority SMALLINT CHECK (priority >= 1 AND priority <= 5),
    est_duration INTEGER, -- Estimated duration in minutes
    dur_conf SMALLINT CHECK (dur_conf >= 1 AND dur_conf <= 5), -- Duration confidence (e.g., 1-5 scale)
    dependencies UUID[], -- Array of task IDs this task depends on
    target_deadline TIMESTAMPTZ,
    dl_hardness SMALLINT CHECK (dl_hardness >= 1 AND dl_hardness <= 5), -- Deadline hardness/flexibility (e.g., 1-5 scale)
    reoccuring TEXT, -- For RRULE strings or similar recurrence definitions
    description TEXT,
    notes TEXT,
    tags TEXT[],
    deferred INTEGER, -- Number of times task has been rescheduled
    embedding vector(1536), -- For semantic search; requires pgvector extension and dimension specification
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE public.tasks IS '''Stores all tasks for the planner.''';
COMMENT ON COLUMN public.tasks.est_duration IS '''Estimated duration of task in minutes.''';
COMMENT ON COLUMN public.tasks.dur_conf IS '''Confidence in est_duration, 1=high, 5=low.''';
COMMENT ON COLUMN public.tasks.target_deadline IS '''Desired completion date/time.''';
COMMENT ON COLUMN public.tasks.dl_hardness IS '''How firm the deadline is, 1=hard, 5=flexible.''';
COMMENT ON COLUMN public.tasks.reoccuring IS '''Recurrence rule (e.g., iCalendar RRULE string).''';
COMMENT ON COLUMN public.tasks.embedding IS '''Vector embedding for similarity searches.''';

-- Daily Schedule Table
CREATE TABLE public.daily_schedule (
    uid TEXT PRIMARY KEY, -- Unique ID from the calendar system (e.g., Google Calendar event ID)
    dtstart TIMESTAMPTZ NOT NULL,
    dtend TIMESTAMPTZ,
    summary TEXT,
    description TEXT,
    location TEXT,
    rrule TEXT, -- Recurrence rule (e.g., iCalendar RRULE string)
    exdate TIMESTAMPTZ[], -- Array of exclusion dates for recurring events
    event_status public.event_status_type,
    last_modified TIMESTAMPTZ, -- When the event was last modified in the source system
    check_in TEXT, -- Status of user check-in for this event, e.g., '''pending''', '''attended''', '''skipped'''
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE public.daily_schedule IS '''Scheduled tasks & activities stored as calendar events.''';
COMMENT ON COLUMN public.daily_schedule.uid IS '''Unique ID from the source calendar system.''';
COMMENT ON COLUMN public.daily_schedule.check_in IS '''Time the manager is to check in with user.''';

-- Schedule Template Table
CREATE TABLE public.schedule_template (
    block_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    day_type TEXT NOT NULL, -- e.g., '''weekday''', '''monday''', '''weekend''', or a specific date '''YYYY-MM-DD'''
    start_time TIME NOT NULL, -- Start time of the block
    end_time TIME NOT NULL, -- End time of the block
    block_type TEXT, -- e.g., '''work_deep''', '''planning''', '''morning''', '''personal''', '''break'''
    flexible BOOLEAN DEFAULT FALSE, -- Whether this block can be easily moved or has tasks that can be
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE public.schedule_template IS '''Defines reusable blocks for scheduling the day.''';
COMMENT ON COLUMN public.schedule_template.day_type IS '''User defined day type. eg ''weekday'' or ''mondays'' or ''work'' or ''vacation''.''';
COMMENT ON COLUMN public.schedule_template.block_type IS '''Type of activity for this time-block.''';

-- User LLM Instructions Table
CREATE TABLE public.user_llm_instructions (
    instruction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- user_id UUID REFERENCES public.users(id) ON DELETE CASCADE, -- Uncomment if you have a users table and want to link instructions to specific users
    instruction_text TEXT NOT NULL CHECK (char_length(instruction_text) > 0),
    category TEXT,
    priority INTEGER DEFAULT 0, -- For ordering or conflict resolution
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE public.user_llm_instructions IS '''Stores user-defined instructions to customize the LLM''s behavior and responses.''';
COMMENT ON COLUMN public.user_llm_instructions.instruction_text IS '''The actual instruction text provided by the user.''';
COMMENT ON COLUMN public.user_llm_instructions.category IS '''Optional category for the instruction (e.g., tone, response_format).''';
COMMENT ON COLUMN public.user_llm_instructions.priority IS '''Optional priority for ordering or resolving conflicting instructions.''';

-- Core personality dimensions and scores
CREATE TABLE public.user_personality_profile (
    profile_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- user_id UUID REFERENCES public.users(id) ON DELETE CASCADE, -- Uncomment if you have a users table
    
    -- Core criteria/values that drive the user's motivation
    criteria TEXT[] NOT NULL, -- Array of user's key motivational criteria (e.g., ['autonomy', 'impact', 'learning'])
    
    -- Motivation Direction (NLP) - simplified to single score
    motivation_direction SMALLINT DEFAULT 0 CHECK (motivation_direction >= -5 AND motivation_direction <= 5), -- -5=strongly away-from, 0=balanced, +5=strongly toward
    
    -- Communication Tone Preference
    warm_candid SMALLINT DEFAULT 0 CHECK (warm_candid >= -5 AND warm_candid <= 5), -- -5=very candid/direct, 0=balanced, +5=very warm/encouraging
    
    -- Behavioral Style
    proactive_reactive SMALLINT DEFAULT 0 CHECK (proactive_reactive >= -5 AND proactive_reactive <= 5), -- -5=very reactive, 0=balanced, +5=very proactive
    
    -- Stress/Reassurance Needs (simplified neuroticism)
    reassurance_needs SMALLINT DEFAULT 0 CHECK (reassurance_needs >= -5 AND reassurance_needs <= 5), -- -5=low need for reassurance, 0=moderate, +5=high need for reassurance
    
    -- Language Diversity Preference (openness-related)
    language_variety SMALLINT DEFAULT 0 CHECK (language_variety >= -5 AND language_variety <= 5), -- -5=prefer consistent language, 0=balanced, +5=prefer varied/creative language
    
    -- Assessment metadata
    assessment_version TEXT DEFAULT 'v1.0',
    last_assessment_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE public.user_personality_profile IS '''Stores the user''s psychological profile for AI personalization, focused on core motivational patterns.''';
COMMENT ON COLUMN public.user_personality_profile.criteria IS '''Array of user''s key motivational criteria/values (e.g., autonomy, impact, learning).''';
COMMENT ON COLUMN public.user_personality_profile.motivation_direction IS '''Motivation direction: -5=strongly away-from problems, +5=strongly toward goals.''';
COMMENT ON COLUMN public.user_personality_profile.warm_candid IS '''Communication preference: -5=candid/direct, +5=warm/encouraging.''';
COMMENT ON COLUMN public.user_personality_profile.proactive_reactive IS '''Behavioral style: -5=reactive (responds to situations), +5=proactive (initiates action).''';
COMMENT ON COLUMN public.user_personality_profile.reassurance_needs IS '''Stress management needs: -5=low reassurance needed, +5=high reassurance needed.''';
COMMENT ON COLUMN public.user_personality_profile.language_variety IS '''Language preference: -5=consistent/predictable, +5=varied/creative language.''';

-- Optional Indexes (examples)
CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON public.tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_task_status ON public.tasks(task_status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON public.tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_target_deadline ON public.tasks(target_deadline);
CREATE INDEX IF NOT EXISTS idx_tasks_tags ON public.tasks USING GIN(tags);
-- Example: Index for vector embeddings (requires pgvector extension)
CREATE INDEX IF NOT EXISTS idx_tasks_embedding ON public.tasks USING hnsw (embedding vector_cosine_ops); -- Choose opclass (e.g., vector_cosine_ops, vector_ip_ops, vector_l2_ops) and ensure dimension is set in table DDL

CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON public.tasks(created_at DESC);

-- Example Compound Indexes for more specific query patterns:
-- If you frequently query for tasks by project and then status:
-- CREATE INDEX IF NOT EXISTS idx_tasks_project_status ON public.tasks(project_id, task_status);
-- Note: The index below (project_status_deadline) would also cover (project_id, task_status) queries efficiently.

-- If you frequently query for tasks by project, then status, then filter/sort by deadline:
CREATE INDEX IF NOT EXISTS idx_tasks_project_status_deadline ON public.tasks(project_id, task_status, target_deadline);

CREATE INDEX IF NOT EXISTS idx_daily_schedule_dtstart ON public.daily_schedule(dtstart);
-- Example Compound Index for daily_schedule if you often query ranges or sort by dtstart then dtend:
-- CREATE INDEX IF NOT EXISTS idx_daily_schedule_dtstart_dtend ON public.daily_schedule(dtstart, dtend);

CREATE INDEX IF NOT EXISTS idx_schedule_template_day_type ON public.schedule_template(day_type);
CREATE INDEX IF NOT EXISTS idx_schedule_template_block_type ON public.schedule_template(block_type);

-- CREATE INDEX IF NOT EXISTS idx_user_llm_instructions_user_id ON public.user_llm_instructions(user_id); -- Uncomment if user_id is added
CREATE INDEX IF NOT EXISTS idx_user_llm_instructions_category ON public.user_llm_instructions(category);

-- Function to update '''updated_at''' column
CREATE OR REPLACE FUNCTION public.trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers to automatically update '''updated_at''' on row modification
CREATE TRIGGER set_projects_timestamp
BEFORE UPDATE ON public.projects
FOR EACH ROW
EXECUTE FUNCTION public.trigger_set_timestamp();

CREATE TRIGGER set_tasks_timestamp
BEFORE UPDATE ON public.tasks
FOR EACH ROW
EXECUTE FUNCTION public.trigger_set_timestamp();

CREATE TRIGGER set_daily_schedule_timestamp
BEFORE UPDATE ON public.daily_schedule
FOR EACH ROW
EXECUTE FUNCTION public.trigger_set_timestamp();

CREATE TRIGGER set_schedule_template_timestamp
BEFORE UPDATE ON public.schedule_template
FOR EACH ROW
EXECUTE FUNCTION public.trigger_set_timestamp();

CREATE TRIGGER set_user_llm_instructions_timestamp
BEFORE UPDATE ON public.user_llm_instructions
FOR EACH ROW
EXECUTE FUNCTION public.trigger_set_timestamp();

CREATE TRIGGER set_user_personality_profile_timestamp
BEFORE UPDATE ON public.user_personality_profile
FOR EACH ROW
EXECUTE FUNCTION public.trigger_set_timestamp(); 