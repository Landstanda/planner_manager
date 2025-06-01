# Daily Planner AI Agent: Task List

This document serves as a comprehensive todo list for building the Daily Planner AI Agent. Tasks are organized by development phase and component, with current focus on **Task Interface UI Development**.

## 1. Project Setup & Environment Configuration ✅

- [x] Initialize Next.js project with TypeScript (in `nextjs_app`)
- [x] Set up Tailwind CSS configuration (via `create-next-app`)
- [x] Configure ESLint and Prettier
  - [x] ESLint (via `create-next-app`)
  - [x] Prettier (installed, configured with .prettierrc, .prettierignore, ESLint integration, package.json script)
- [x] Create project directory structure (initial `nextjs_app` created)
- [x] Set up Git repository (assumed already done by user)
- [x] Configure environment variables (.env) (created `.env.example`, `.env.local`; updated `.gitignore`)
- [x] Containerize Next.js app (`nextjs_app`) and configure for Fly.io deployment (Dockerfile, fly.toml)
- [x] Create `actions.md` for logging
- [x] Create `.cursor/rules/log_actions_rule.md` for logging reminders

## 2. Infrastructure & DevOps ✅

- [x] Containerize n8n service and set up persistent volume
- [x] Document existing n8n configuration and volume setup
- [x] Set up Next.js deployment in Fly.io with persistent storage (Volume `chief_of_staff_data` created; usage for caching by Next.js app to be determined)
- [x] Configure shared environment and secrets management in Fly.io (Next.js to use N8N_BASE_URL & N8N_WEBHOOK_API_KEY set via Fly.io secrets for n8n communication; .env.example updated)
- [x] Set up remote development environment configuration (Documented local dev setup with .env.local and Fly.io deployment for testing in DEVELOPMENT_SETUP.md)
- [x] Configure GitHub Actions CI for build, lint, and test workflows (Basic CI workflow created in .github/workflows/ci.yml for build and lint; test step placeholder added)
- [x] Configure CD pipeline for Fly.io deployment of Next.js (Initial manual launch followed by successful GitHub Action triggered deploy; volume to be created manually)
- [ ] Set up automated version tagging and release notes

## 3. Google Cloud & Supabase Storage ✅

- [x] Create GCP project and enable Drive API
- [x] Create Google Cloud service account, generate JSON key, and add key as a secret to the *n8n application* on Fly.io (for Google Drive access)
- [x] Set up Supabase project and configure database schema (for To-Dos, User_Info, etc.)
- [x] Add Supabase connection details (URL, anon key, service role key) as secrets to n8n and Next.js applications on Fly.io
- [x] Create "Life" folder structure in Google Drive, including:
    - [x] `Inbox/`
    - [x] `Goals/` (for AI to reference for contextual suggestions)
    - [x] `Projects/` (potentially structured project details for AI reference - consider if this moves to Supabase)
    - [x] `Instructions.md` (for personality type, explicit instructions, master rules, persistent schedule preferences like lunch time, work hours, preferred communication style elements)
- [x] Define and create Master To-Do table(s) in Supabase (link to Task Schema in README)
- [x] Define and create User_Info table(s) in Supabase (for structured data: Project details/importance, Opinions, Relationships)
- [ ] Configure cloud-based backup and restore procedures (for Google Drive & Supabase)
- [ ] Populate sample data for initial testing (including sample personality quiz data and instructions)

## 4. n8n Workflows 🔄

- [x] Deploy n8n instance
- [x] Export and document modular n8n workflows: `main_planner.json`, `life_folder.json`, `todo.json`, `calendar.json`
- [x] **Build task_creator workflow** (COMPLETED - can create tasks from natural language input)
- [x] Document existing n8n deployment configuration
- [x] Set up version control for n8n workflows (JSON exports)
- [ ] Configure n8n REST API access for programmatic updates
- [ ] Replace Slack Trigger in `main_planner.json` with a secured HTTP/Webhook trigger (e.g., Header Auth) for front-end integration, and document API key strategy
- [ ] Update workflow documentation to reflect front-end integration

## 5. **COMPLETED: Task Interface UI Development** ✅

### Phase 1: Setup & Infrastructure ✅
- [x] **Step 1: Create Supabase Client Configuration**
    - [x] Create `src/lib/supabase.ts` to configure the Supabase client
    - [x] Set up TypeScript types based on the database schema from `supabase_tables.sql`
    - [x] Create `src/types/database.ts` with proper TypeScript interfaces for tasks, projects, and related entities

- [x] **Step 2: Create API Routes for Task Management**
    - [x] Create `src/app/api/tasks/route.ts` for fetching tasks with sorting options
    - [x] Create `src/app/api/tasks/[id]/route.ts` for individual task details
    - [x] Implement proper error handling and data validation

- [x] **Step 3: Set Up Task-Specific Pages and Routing**
    - [x] Create `src/app/tasks/page.tsx` for the main task list view
    - [x] Create `src/app/tasks/[id]/page.tsx` for individual task detail view
    - [x] Update navigation in the main layout

### Phase 2: Core Components ✅
- [x] **Step 4: Build Task List Component**
    - [x] Create task list functionality in `src/app/tasks/page.tsx` with:
        - [x] Task cards showing title, priority, status, and project
        - [x] Responsive grid layout using Tailwind CSS
        - [x] Loading states and error handling
        - [x] Empty state when no tasks exist

- [x] **Step 5: Create Sort/Filter Controls**
    - [x] Implement sorting controls with dropdown for:
        - [x] Priority (1-5, critical to someday)
        - [x] Status (dependent, ready, progressing, done, cancelled)
        - [x] Target deadline (earliest first, latest first)
        - [x] Created date (newest first, oldest first)
        - [x] Project name (alphabetical)

- [x] **Step 6: Build Task Detail Page**
    - [x] Create `src/app/tasks/[id]/page.tsx` showing:
        - [x] All task fields from the schema
        - [x] Project information (if linked)
        - [x] Dependencies visualization with clickable links
        - [x] Smart dependency fetching with actual task titles
        - [x] Close button for navigation

### Phase 3: UI/UX Implementation ✅
- [x] **Step 7: Implement Modern UI Design**
    - [x] Use Tailwind CSS for styling with a clean, modern aesthetic
    - [x] Implement proper color coding for:
        - [x] Priority levels (1=red, 2=orange, 3=yellow, 4=blue, 5=gray)
        - [x] Task status (ready=green, progressing=blue, done=gray, etc.)
    - [x] Add hover effects and smooth transitions

- [x] **Step 8: Add Interactive Features**
    - [x] Implement click-to-expand task details (opens in new tab)
    - [x] Add clickable dependency links for task navigation
    - [x] Include visual indicators and badges for task properties
    - [x] Add proper loading states and error handling

- [x] **Step 9: Mobile Responsiveness**
    - [x] Ensure the interface works well on mobile devices
    - [x] Implement responsive design with proper breakpoints
    - [x] Optimize touch targets and spacing

### Phase 4: Integration & Polish ✅
- [x] **Step 10: Connect to Real Data**
    - [x] Test with actual Supabase database
    - [x] Implement proper error boundaries
    - [x] Add loading skeletons for better UX
    - [x] Handle edge cases (missing projects, malformed data)

- [x] **Step 11: Enhanced Features**
    - [x] Implement smart dependency task fetching and display
    - [x] Add comprehensive task detail view with all schema fields
    - [x] Include proper date formatting and status indicators
    - [x] Add graceful error handling for missing dependencies

- [x] **Step 12: Testing & Deployment**
    - [x] Test the interface thoroughly
    - [x] Ensure proper environment variable configuration
    - [x] Deploy to Fly.io and verify functionality
    - [x] Fix linting errors and ensure clean deployment

**🎉 ACHIEVEMENT UNLOCKED: Complete Task Interface UI**
- ✅ Fully functional task management interface
- ✅ Modern, responsive design with Tailwind CSS
- ✅ Complete CRUD operations for viewing tasks
- ✅ Smart sorting and filtering capabilities
- ✅ Comprehensive task detail pages with dependency navigation
- ✅ Successfully deployed to production at https://chief-of-staff.fly.dev/

## 6. Next.js Front-End - Additional Components (Post Task Interface)

- [x] Set up Next.js project with TypeScript and Tailwind
- [x] Configure cloud-based development environment
- [ ] Implement Next.js direct integration with Supabase:
    - [x] Install and configure Supabase JS client (`@supabase/supabase-js`)
    - [x] Secure environment variables for Supabase URL and anon key
    - [ ] Implement user authentication (sign-up, login, session management) using Supabase Auth
    - [ ] Refactor data fetching for reads (e.g., tasks, projects) to use direct Supabase queries (server-side or client-side with RLS)
    - [ ] Implement real-time subscriptions for UI updates where beneficial (e.g., task list changes)
    - [ ] Define and apply Row Level Security (RLS) policies in Supabase for data accessed directly by Next.js
- [ ] Scaffold base layout with Tailwind & responsive design
- [ ] Implement swipeable panels (To-Do List, Calendar/Daily Schedule, Life Folder) (as per `Front_End_Details.md`)
- [ ] Implement bottom navigation bar (as per `Front_End_Details.md`)
- [ ] Build Calendar/Daily Schedule component
- [ ] Build Life Folder explorer powered by Drive API
- [ ] Implement chat overlay (as per `Front_End_Details.md`)
- [ ] Implement Personality On-Ramp Quiz (MVP)
- [ ] Implement settings panel
- [ ] Add PWA support and push notifications for reminders
- [ ] Integrate authentication (Google OAuth)

## 7. Scheduling Engine (Business Logic) - Future

- [ ] Design time-blocking algorithm with buffers and collision resolution (core of dynamic rescheduling and daily planning)
- [ ] Implement algorithm as TypeScript library consumed by n8n & Next.js
- [ ] Write unit tests covering edge cases (dependencies, delays, priority, conflicting preferences)

## 8. Personality & Feedback Loop - Future

- [ ] Implement `user_llm_instructions` reader and prompt augmentation system (MVP - core to AI behavior)
- [ ] Implement management style selection & initial set of tone templates based on archetypes (MVP)
- [x] Implement Personality Assessment System (MVP):
    - [x] Design and implement initial personality questionnaire (5-7 minutes)
    - [x] Create scoring algorithm for questionnaire responses (5-point scales)
    - [ ] Build assessment UI component in Next.js
    - [ ] Implement assessment results storage in `user_personality_profile` table
    - [ ] Create personality profile display/editing interface
- [ ] Implement ongoing behavioral analysis for profile refinement
- [ ] Integrate personality profile with AI prompt generation
- [ ] Implement parsing of free-form input (chat/voice) for task structuring (MVP)
- [ ] Logic for AI to propose breaking large tasks into subtasks with dependency links (post-MVP refinement)
- [ ] AI logic for contextual suggestions during morning planning
- [ ] AI logic for focus management/off-task intervention (Management Mode)

## 9. API Layer - Future

- [ ] Create Next.js API routes for schedule and chat (tasks routes covered in current focus)
- [ ] Secure endpoints with JWT/session & CSRF protection
- [ ] Integrate rate limiting and logging middleware

## 10. Testing & Quality Assurance - Future

- [ ] Add Jest & React Testing Library tests for UI components
- [ ] Add integration tests for API routes
- [ ] Add E2E tests with Playwright or Cypress

## 11. Documentation ✅

- [x] Extend README with detailed setup & usage instructions (initial pass done, will need ongoing updates)
- [x] Create architecture diagram assets (initial ASCII in README, can be improved)
- [x] Create User Experience (`User_Experience.md`) document
- [x] Create Front-End Details (`Front_End_Details.md`) document
- [ ] Document n8n workflows and API endpoints

## 12. Optional Add-Ons (Post-MVP)

- [ ] Implement Automated Life Folder Extractor (scans chats to update Supabase `User_Info` table etc.)
- [ ] Implement Secure Vault (requires crypto design)
- [ ] Implement Pomodoro Timer module
- [ ] Implement Habit Tracker module
- [ ] Implement Gamified To-Do module
- [ ] Implement Life Coach Mode
- [ ] Implement Astrologer Plugin

### Future n8n Workflows (Post-MVP)
- [ ] Build Morning Kickoff / Daily Planning workflow
- [ ] Build Database Trigger/Webhook workflow (for Master To-Do changes in Supabase)
- [ ] Build Calendar Update webhook workflow (for real-time event changes)
- [ ] Build End-of-Day Retro workflow
- [ ] Build `Memory/Instructions.md` Ingestion Workflow
- [ ] Implement Dynamic Rescheduling logic within relevant workflows
- [ ] Implement Management Mode / Progress Check-in logic
- [ ] Add unit tests / mock executions for all workflows
- [ ] Create workflow deployment script using n8n API

---

## **COMPLETED SPRINT: Task Interface UI Development** ✅

**🎯 GOAL ACHIEVED:** Complete the Task Interface UI (Section 5) to provide users with a functional way to view, sort, and interact with tasks stored in the Supabase database.

**✅ SUCCESS CRITERIA MET:**
- ✅ Users can view all tasks from Supabase database
- ✅ Tasks can be sorted by multiple criteria via dropdown
- ✅ Clicking a task shows full details with enhanced dependency navigation
- ✅ Interface is responsive and follows modern UI principles
- ✅ Successfully deployed to Fly.io at https://chief-of-staff.fly.dev/

---

## **NEXT SPRINT OPTIONS** 🚀

Choose your next development focus:

### Option A: Task Creation & Management 📝
**Goal:** Add the ability to create, edit, and manage tasks directly from the UI
- [ ] Build task creation form with all schema fields
- [ ] Implement task editing capabilities
- [ ] Add task deletion with confirmation
- [ ] Create project management interface
- [ ] Add bulk task operations

### Option B: Real-time Features & Advanced UI 🔄
**Goal:** Enhance the user experience with real-time updates and advanced features
- [ ] Implement Supabase real-time subscriptions for live task updates
- [ ] Add search functionality across tasks
- [ ] Implement advanced filtering (by tags, date ranges, etc.)
- [ ] Add drag-and-drop task reordering
- [ ] Create task templates and quick actions

### Option C: Calendar & Scheduling Integration 📅
**Goal:** Build the calendar/daily schedule component for time-blocking
- [ ] Create calendar view component
- [ ] Implement time-blocking algorithm
- [ ] Add task scheduling to calendar slots
- [ ] Build daily planning interface
- [ ] Integrate with Google Calendar API

### Option D: AI Integration & Chat Interface 🤖
**Goal:** Connect the front-end to n8n workflows and add AI-powered features
- [ ] Build chat overlay for natural language task creation
- [ ] Integrate with n8n task_creator workflow
- [ ] Add AI-powered task suggestions
- [ ] Implement voice input for task creation
- [ ] Create AI assistant personality interface

### Option E: Authentication & User Management 👤
**Goal:** Add user authentication and multi-user support
- [ ] Implement Supabase Auth (Google OAuth)
- [ ] Add user registration and login flows
- [ ] Implement Row Level Security (RLS) policies
- [ ] Create user profile management
- [ ] Add user-specific task filtering

**Recommended Next Step:** Option A (Task Creation & Management) - This would complete the core CRUD operations and make the app fully functional for task management.
   