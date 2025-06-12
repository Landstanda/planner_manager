# **Daily Planner AI Agent: Chief-of_Flow**

A streamlined personal assistant that plans your day intelligently, helps you prioritize, keeps you focused, and captures your ideas as they happen. Designed to support a fast-paced, nonlinear thought process, this agent makes it easy to offload mental clutter and build structure later. Each morning, it compiles a personalized daily schedule from your master task list, then checks in throughout the day with smart reminders and progress nudges. It handles spontaneous requests in natural language, converts them into structured tasks, and files everything neatly into your "Life Folder."

**It's envisioned as a personal AI Task-Management Assistant for solo founders and build‑in‑public creators, speaking the user's language by adapting its tone and communication style.** The key differentiator is the immediate feeling that "this AI gets me," unlike generic LLM assistants. And unlike most task management software, this is designed to be as easy to use as a pen and paper, with AI doing all of the detailed busy work so you could stay focused.

The backend is powered by **Python FastAPI** for AI logic and automation services, **Next.js** and **Tailwind CSS** for a fast, responsive UI, and **Fly.io** for scalable deployment. **Supabase** serves as the primary database for structured data like tasks and user information, keeping everything centralized, accessible, and versionable.

---

## **Table of Contents**

1. **Product Vision & Core Value**
2. Key Features & **MVP Feature Set**
3. Architecture
4. Folder / Data Layout
5. Task Schema
6. Workflow Triggers
7. Scheduling & Conflict Logic
8. Adaptive Tone & Feedback Loop
9. Spontaneous Natural-Language Capture
10. Management Styles & Personality Tuning
11. Front‑End
12. Deployment
13. Future Add-Ons
14. Contributing
15. License
16. **Detailed User Experience (See `User_Experience.md`)**
17. **Detailed Front-End Description (See `Front_End_Details.md`)**

---

## **Product Vision & Core Value**

* **Personal AI "chief‑of‑flow":** Tailored for solo founders and build‑in‑public creators (‘Flow’ = in the hyper-productive creater zone/focus)
* **Speaks Your Language:** Adapts tone to personality, motivation (toward‑goals vs. away‑from‑pain), and communication style (sarcastic, upbeat, dead‑pan), driven by a personality quiz and ongoing feedback. This creates an immediate connection, differentiating it from generic LLM assistants.
* **Effortless Capture → Organized Execution:** Jots down tasks anytime; the system auto‑structures them, schedules work blocks (respecting persistent preferences like lunch breaks), and nudges progress.
* **Dynamic Schedule Management:** Revises the day's plan in real time when tasks finish early/late, new priorities appear, or meetings shift. Handles free-form change requests and resolves conflicts based on urgency, importance, and user preferences.
* **Motivational Accountability:** Regular, context-aware check‑ins delivered in the user's preferred tone keep momentum. The AI can point out deviations from the plan and offer to reprioritize.

---

## **Key Features & MVP Feature Set**

The app aims for a comprehensive set of features, with the following identified as core to the Minimum Viable Product (MVP):

### General Features (Existing & Enhanced)
* Natural language to Master Task List (via chat or voice).
* **Morning Kickoff & Daily Planning Logic:**
    * Greets user and reviews today's schedule
    * Drills into project details, pulling relevant tasks from the Task DB for each calendar block.
    * Proposes a visual time-blocked schedule, considering persistent preferences (e.g., lunch, work hours) stored in the schedule template.
    * Offers contextual suggestions for light schedules or to align with long-term goals/motivators.
* Builds a time‑blocked schedule  from the schedule template and current tasks.
* **Smart Check-ins & Dynamic Pacing (Management Mode):**
    * Cadence and tone of check-ins tuned to personality type.
    * Progress prompts at appropriate intervals; celebrates subtask/task completion.
    * If user drifts, points out sacrifices vs. planned priorities and offers to reprioritize/reschedule.
* Spontaneous requests and notes captured via chat interface to `Life/Inbox/`.
* **Instant Re-planning & Dynamic Rescheduling:**
    * Handles free-form change requests (move, add, remove blocks).
    * Automatically checks for conflicts and reprioritizes based on urgency, project importance, and user's stated preferences (from `Life/Memory/Instructions.md`).
* Unstructured notes and requests automatically logged to `Life/Inbox/`.

## MVP Feature Set

### Personality On‑Ramp
-**1–2 minute quiz** to tag user's personality archetype and motivation style.
- Drives all language tailoring.
- Marketable as: "Take the free test to meet your perfect AI assistant."
---

### Task Ingest & Structuring
- **Free-form input** (chat or voice) added to Task DB.
- Large tasks are **automatically broken into subtasks** with dependency links.
- Urgent items trigger immediate scheduling questions or manager mode.
---

### Daily Planning Mode
- **Morning routine** merges calendar events and Task DB.
- Creates proposed day blocks for user to accept/adjust.
- Includes contextual suggestions and respects persistent preferences from `Life/Memory/Instructions.md`.
- Visual schedule interface is key.
---

### Live Schedule Adjust
- Detects deviations (done early/late, cancellations, new events).
- Proposes updated day plan.
- Handles user-initiated free-form changes with conflict resolution.
- AI checks for double bookings and reprioritizes based on urgency, importance, and user preferences.
---

### Progress Check‑Ins
- Timed or context-based pings ask for status updates in user-tailored tone.
- Offers to reprioritize if off-task.
- Cadence and tone driven by personality profile in Instructions.
---

### Master Instruction List

- Single source of truth in Instructions for high-level behavior rules, personality settings, and stable preferences (e.g., "Remind me 10 min before deadlines," lunch time).
- System ingests, merges, and attempts to auto-resolve conflicts.
- User can view/edit.                                                                      |
---

## **Architecture**

┌────────────┐    REST/WS    ┌───────────────┐    REST    ┌──────────────┐
│  Next.js   │◀─────────────▶│ Python FastAPI│◀──────────▶│   Supabase   │
│  Front‑End │   JSON        │  AI Services  │    SQL/ORM │  (To‑Dos &   │
└────────────┘                └─────▲─────────┘           │  User_Info)  │
      ▲ HTTP/PWA                     │  Drive API           └──────────────┘
      │                              │
┌─────┴─────┐    HTTP/REST        ┌──┴──────────┐
│ Fly.io VM │◀───────────────────▶│ Google Drive│ (Life Folder Docs)
└───────────┘                     └──────────────┘

---

## **Folder / Data Layout**

**Primary Database: Supabase**
*   **projects:** Stores information about user projects.
*   **tasks:** Master To-Do List for all tasks, following the Task Schema.
*   **daily_schedule:** Stores calendar events, typically synced from an external calendar.
*   **schedule_template:** Defines reusable blocks for structuring the day.
*   **user_llm_instructions:** Stores user-defined instructions to customize the LLM's behavior, responses, and personality. (See User LLM Instructions Schema below).
*   **user_personality_profile:** Stores psychological profile data for AI personalization (See Personality Assessment System below).
*   **User_Info:** Table(s) for structured user data: Project details/importance, Opinions, Relationships (Consider consolidating or ensuring clear purpose if distinct from `projects` and `user_llm_instructions`). [Post-MVP Feature]

**File System: Google Drive (Life Folder)**
Life/
├─ Inbox/                     ← default dump for new items, spontaneous thoughts
├─ Long‑Term Goals/           ← User's long-term aspirations, referenced for contextual suggestions
├─ Projects/                    ← Details about ongoing projects
├─ Personal Documents/
├─ values, interests, philosophies/
└─ Memory/
   ├─ Instructions.md          ← DEPRECATED: High-level AI behavior rules, personality settings, stable preferences. Replaced by user_llm_instructions table in Supabase for core LLM behavioral instructions. May still be used for non-LLM specific preferences or general notes for the AI.
   └─ improvement_requests.md  ← (Consider merging into a structured feedback system or specific instructions) specific feedback on AI tone/behavior.

---

## **Task Schema**

id: string  
title: string -- Renamed from 'name' for clarity
project_id: string -- Foreign key to projects table
task_status: dependent | ready | progressing | done | cancelled -- Reflects task_status_type ENUM
priority: 1‑5  # 1 = critical, 5 = someday
est_duration: int  # Estimated duration in minutes
dur_conf: 1-5 # Confidence in estimated duration (e.g., 1=high, 5=low - as per SQL comment)
dependencies: [id,…]  # Array of task IDs that must be done before preceding with this task
target_deadline: datetime | null # Desired completion date/time
dl_hardness: 1-5 # How firm the deadline is (e.g., 1=hard, 5=flexible - as per SQL comment)
reoccuring: string # Recurrence rule (e.g., iCalendar RRULE string)
description: string # Detailed description of the task
notes: string # Additional notes or comments about the task
tags: [string, ...] # Array of tags for categorization and filtering
deferred: int # Number of times the task has been rescheduled. Used by the AI to gauge if the user is avoiding or struggling with the task, potentially triggering more persuasive or supportive interactions.
embedding: vector # Vector embedding for similarity searches
Subtasks: child-tasks that must be completed for this parent-task to be complete

---

## Workflow Triggers
---

### Morning‑Plan Service

- **Trigger:** Cron job at 07:45 America/Chicago, daily
- **Action:** Python service builds daily schedule and updates dashboard via API
–

### Check-ins Service

- **Trigger:** Background scheduler according to user preferences 
- **Action:** Python service sends status update prompts and motivational reminders
---

### End‑of‑Day Retro Service

- **Trigger:** Cron job at 17:00, daily
- **Action:** Python service updates task statuses, analyzes productivity, suggests schedule template changes
---


## **Scheduling & Conflict Logic**

1. **Order of Precedence**  
    `priority` → earliest `scheduled_datetime` → shorter `estimated_duration` → FIFO

2. **Time Blocking**  
    Tasks fill open slots around calendar events with a 5-minute buffer (configurable).

3. **Collision Resolution**

   * Push low-priority tasks to the next feasible window  
   * Add 1 in deferred column of scheduled but uncomplete tasks at the end of the day

4. **Dynamic Check-ins**  
    Adjusts reminder timing based on task urgency and your past response behavior

---

## **Adaptive Tone & Feedback Loop**

* **File:** `Instructions` is the primary file. It stores personality quiz results/settings, explicit instructions from the user (e.g., "be more sarcastic," "don't schedule meetings on Friday afternoons"), and persistent preferences (like default lunch times).
* **Effect:** The system ingests `Instructions.md` to tailor its communication style and check-in cadence. New instructions are merged, and the system attempts to resolve conflicts or flags them for user review.


---

## **Spontaneous Natural-Language Capture**

You can quickly say or type things like:

"I need to buy a new HDMI cord on Amazon before the end of the day!"

The system infers:

title: Buy HDMI cord  
description: Buy HDMI cord by end of day.  
estimated\_duration: 5  \# minutes  
priority: 1  \# High  
scheduled\_datetime: today by 5pm

It may respond:

"Why don't you just do it now?"

If you give a reason (e.g., "I'm on a call"), it'll:

* Predict when you'll be free  
* Schedule a reminder (e.g., in 15 minutes)  
* Confirm with something like: *"I'll remind you in 15. Good luck surviving Amazon search."*

\---

## **Management Styles & Personality Tuning**

The planner supports a range of management styles to match your motivation type. These are initially set via a personality quiz (results stored in `Life/Memory/Instructions.md`) and can be fine-tuned by the user adding direct instructions or feedback into the same file. Styles include:

* Tough Love – blunt and committed, calls you out when you ignore your plan or drift off-task.
* Encouraging Coach – kind and motivating, celebrates progress and gently nudges towards goals.
* Passive-Aggressive Californian – breezy and polite with pointed reminders about what might be getting sacrificed.
* Quiet Observer – minimal interruptions, ideal for self-directed workflows, intervenes mostly on request or critical conflicts.

Change styles anytime or shape tone gradually by adding notes like "be more assertive" or "check in less frequently" to Instructions.

---

## **Front‑End UI**

* Three swipeable panels: **To-Do List**, **Calendar/Daily Schedule View**, **Life Folder**.
    *   The Calendar/Daily Schedule View is highly interactive, showing time blocks with project labels, and allowing drag-and-drop rescheduling.
* Bottom nav has three icons: tap or swipe to switch views.

Chief Of Flow features a clean, modern mobile UI styled with Tailwind CSS and the Inter font family for all text. For example, the Task phone UI will have color-coded project blocks (soft orange, blue, and lavender) distinguish different areas of your to-do list, with smooth rounded corners, subtle drop-shadows, and crisp, high-contrast headings. The header uses a bold, large font for brand presence, while task items and section titles use lighter, readable weights and sizes for clarity. The layout leverages generous padding, white space, and consistent vertical rhythm to ensure a focused, calm user experience. At the bottom, a simple navigation bar enables quick switching between ToDo, Schedule, and Life views, highlighting the current section.

A floating "Ask me…" field overlays above the navigation bar, styled as a rounded, shadowed input pill with a blue microphone icon for voice commands or text queries. All design tokens (custom color shades, font sizes, border radii, and box shadows) are managed in the Tailwind config for easy theming and extension. The end result is a familiar, intuitive interface that feels at home on any modern Android or iOS device, while remaining uniquely recognizable for the Chief Of Flow brand.
---

## **Deployment**

1. Clone the repo & configure `.env` with required API keys and database URLs
2. **Backend Services**: Deploy Python FastAPI services to Fly.io:

```bash
# Deploy each service
flyctl deploy --dockerfile Dockerfile.scheduling-service
flyctl deploy --dockerfile Dockerfile.task-service  
flyctl deploy --dockerfile Dockerfile.ai-service
```

3. **Frontend**: Deploy Next.js app:

```bash
flyctl deploy --dockerfile Dockerfile.frontend
```

4. Configure Google Cloud:
* Service account with Drive access
* Share your "Life" folder with the service account
5. Configure Supabase:
* Set up project, tables, and RLS policies
* Enable pgvector extension for semantic search
* Add Supabase URL and API keys to service environment variables
6. Configure domain and SSL via:

```bash
fly certs add <your domain>
```

### Development Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run services locally
uvicorn main:app --reload --port 8000  # Main API gateway
uvicorn scheduling_service:app --reload --port 8001
uvicorn task_service:app --reload --port 8002

# Run frontend
cd frontend && npm run dev
```

---

## **Future Add-Ons**

Beyond the MVP, the planner can be extended with features like:

* **Life Folder (Expanded):** Automated extractor scans daily chats to populate/update entries in the `User_Info` Supabase table and other relevant documents in Google Drive.
* **Secure Vault:** For important numbers, passwords, docs (requires solid crypto design).
* Pomodoro Timer – Stay focused with timed work sessions and short breaks
* Habit Tracker – Reinforce daily habits with streaks, reminders, and analytics
* Screenshot or pic to import schedule/tasks
* → instead of connecting your Google calenda or other task app, you can just take a screenshot or three and an OCR will read it and add it to the system.

These modules are designed to be modular and optional—so you can shape the system to be as minimalist or full-featured as you want.

---

## **Contributing**

Pull requests are welcome\! For major changes, please open an issue first.

\# lint & test  
npm run lint  
npm test

---

## **License**

MIT © 2025 Jeff Steele

## **Python Service Architecture**

The automation and orchestration backbone of the Daily Planner AI Agent is powered by a set of modular Python FastAPI services, deployed on Fly.io. The system has evolved into a sophisticated **5-service architecture** that handles different aspects of task and schedule management:

### Core Service Components

* **SchedulingDecider Service** (`scheduling_decider.py`): The decision engine that determines whether and when to schedule a task based on priority, dependencies, available time blocks, and current schedule density. Returns either a specific time slot (HH:MM format) or None for no scheduling.

* **TimeblockAllocator Service** (`timeblock_allocator.py`): Finds the optimal time slot for tasks that have been approved for scheduling. Analyzes available time windows from the schedule template, considers task duration + buffers, and creates schedule entries in the database.

* **TaskCreator Service** (`task_creator.py`): Enhanced task creation service with AI-powered analysis that breaks down complex requests into structured tasks with subtasks, estimates durations, detects dependencies, and generates vector embeddings for semantic search.

* **TaskUpdater Service** (`task_updater.py`): Handles task status updates, completion tracking, and modifications with vector search capabilities to find specific tasks mentioned by users. Includes sophisticated parsing for natural language update requests.

* **Rescheduler Service** (`rescheduler.py`): Manages cascade rescheduling when changes occur (tasks running late, completing early, new urgent tasks, or cancellations). Minimizes disruption while preserving priorities and respecting schedule template boundaries.

### Database Integration

All services use **SQLAlchemy ORM with Supabase PostgreSQL** for better performance, security, and real-time capabilities:

- **Primary Tables**: `tasks`, `projects`, `daily_schedule`, `schedule_template`, `user_llm_instructions`, `user_personality_profile`
- **Vector Search**: Uses Supabase's vector capabilities with OpenAI embeddings for semantic task matching
- **Real-time Updates**: Leverages Supabase's real-time subscriptions for immediate UI updates

### Enhanced AI Integration

The Python services now include sophisticated AI agents with:
- **Vector Search Tools**: Find similar tasks and dependencies using semantic similarity via pgvector
- **Personality-Driven Responses**: Adapt communication style based on user personality profile
- **Dependency Detection**: Automatically identify blocking relationships between tasks using LangChain
- **Subtask Automation**: Break complex tasks into manageable subtasks with proper sequencing
- **Duration Estimation**: AI-powered duration predictions based on similar historical tasks

### Service Integration

- **API Architecture**: RESTful APIs with FastAPI for all service communication
- **Background Tasks**: Celery with Redis for scheduled jobs and async processing  
- **Monitoring**: Structured logging and health check endpoints for each service
- **Testing**: Comprehensive unit and integration tests with pytest

**Development Workflow:**
- Services are developed as independent Python modules with clear interfaces
- Docker containers for consistent development and deployment environments
- CI/CD pipeline automatically tests and deploys services to Fly.io

---

*For a detailed description of the user's interaction with the app, see `User_Experience.md`.*
*For a detailed description of the front-end layout, feel, and components, see `Front_End_Details.md`.*

## **User LLM Instructions Schema (Supabase Table: `user_llm_instructions`)**

instruction_id: UUID (Primary Key)
user_id: UUID (Foreign Key - if implementing multi-user, otherwise can be omitted for single-user context)
instruction_text: TEXT (The actual instruction provided by the user)
is_active: BOOLEAN (Defaults to TRUE, allows disabling instructions without deleting)
category: TEXT (Optional: e.g., "tone", "response_format", "scheduling_preference")
priority: INTEGER (Optional: For ordering or conflict resolution if multiple instructions apply)
created_at: TIMESTAMPTZ
updated_at: TIMESTAMPTZ

**Purpose:** Allows users to dynamically tailor the AI's behavior by adding specific instructions. The AI will be programmed to recognize when a user utterance is intended as a new instruction and use a tool to save it to this table via an n8n workflow. These active instructions will be retrieved and incorporated into the LLM's system prompt or context for subsequent interactions.

---

## **Personality Assessment System**

The Daily Planner AI uses a focused personality assessment to understand how to best motivate and communicate with each user. This MVP system targets the most impactful psychological patterns for daily planning and task management.

### **Assessment Framework (MVP: 5 Core Indicators)**

**1. Criteria (Core Values)**
- **What it measures**: The user's fundamental motivational drivers and values (e.g., "autonomy," "impact," "learning," "stability")
- **How it's captured**: Open-ended question asking what makes work/projects most engaging for them
- **Why it matters**: These criteria become the lens through which the AI frames all communication and suggestions

**2. Motivation Direction (NLP-based)**
- **What it measures**: Whether the user is primarily motivated by moving *toward* goals and achievements or *away from* problems and risks
- **Scale**: -5 (strongly away-from) to +5 (strongly toward)
- **How it's identified**: Using the user's criteria, ask "Why is [criterion] important to you?" and listen for goal-oriented vs. problem-avoidance language
- **Why it matters**: Fundamentally shapes motivational language - "Let's achieve this milestone!" vs. "Let's avoid missing this deadline"

**3. Communication Tone: Warm vs. Candid**
- **What it measures**: Preference for encouraging, supportive communication vs. direct, no-nonsense feedback
- **Scale**: -5 (very candid/direct) to +5 (very warm/encouraging)
- **Why it matters**: Prevents the "AI ass-kisser" problem by matching the user's respect for authenticity vs. warmth

**4. Proactive vs. Reactive Style**
- **What it measures**: Whether the user prefers to initiate action and drive situations vs. respond to circumstances as they arise
- **Scale**: -5 (very reactive) to +5 (very proactive)
- **Why it matters**: Affects check-in timing, task presentation, and how the AI approaches the user ("Here's what you should tackle next" vs. "How are you feeling about your current task?")

**5. Reassurance Needs (Stress Management)**
- **What it measures**: How much reassurance, buffer time warnings, and stress management support the user needs
- **Scale**: -5 (low reassurance needed) to +5 (high reassurance needed)
- **Why it matters**: Critical for deadline anxiety, overwhelm prevention, and appropriate check-in frequency

**Bonus: Language Variety Preference**
- **What it measures**: Preference for consistent, predictable language vs. varied, creative communication
- **Scale**: -5 (consistent language) to +5 (varied/creative language)
- **Technical note**: This can influence the AI's temperature/k-parameter for more or less linguistic diversity

### **Assessment Process**

**Initial Assessment**: 5-7 minute questionnaire:
1. **Criteria Discovery**: "When you think about work or projects where you feel most engaged, what are the 3-5 most important things that make them that way?"
2. **Motivation Direction**: For each criterion: "Why is [criterion] important to you? What does having [criterion] do for you?"
3. **Communication & Style Preferences**: Scenario-based questions to identify tone, proactivity, and reassurance preferences

**Ongoing Refinement**: The system learns from:
- User responses to different communication styles
- Task completion patterns and stress indicators
- Feedback on AI interactions
- Language patterns in user messages

### **AI Personalization Examples**

**High Toward + Candid + Proactive + Low Reassurance:**
> "You're crushing it today. Two tasks down, one big win left. Want to knock out that presentation draft while you're in the zone?"

**High Away-From + Warm + Reactive + High Reassurance:**
> "I noticed the client meeting is tomorrow and wanted to check in. You've got plenty of time to prepare, and I can help break it into smaller steps if that would feel more manageable."

**Criteria-Based Framing** (if "autonomy" is a key criterion):
> "I have a few suggestions for your afternoon, but you know your energy best. What feels right to you?"
