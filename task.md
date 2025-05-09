# Daily Planner AI Agent: Task List

This document serves as a comprehensive todo list for building the Daily Planner AI Agent. Tasks are organized by development phase and component.

## 1. Project Setup & Environment Configuration

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

## 2. Infrastructure & DevOps

- [x] Containerize n8n service and set up persistent volume
- [x] Document existing n8n configuration and volume setup
- [x] Set up Next.js deployment in Fly.io with persistent storage (Note: Persistent volume for Next.js app deferred as not currently required; primary data persistence via Google Drive)
- [x] Configure shared environment and secrets management in Fly.io (Next.js to use N8N_BASE_URL & N8N_WEBHOOK_API_KEY set via Fly.io secrets for n8n communication; .env.example updated)
- [x] Set up remote development environment configuration (Documented local dev setup with .env.local and Fly.io deployment for testing in DEVELOPMENT_SETUP.md)
- [x] Configure GitHub Actions CI for build, lint, and test workflows (Basic CI workflow created in .github/workflows/ci.yml for build and lint; test step placeholder added)
- [ ] Configure CD pipeline for Fly.io deployment of Next.js
- [ ] Set up automated version tagging and release notes

## 3. Google Cloud & Data Storage

- [ ] Create GCP project and enable Drive & Sheets APIs
- [ ] Create service account, generate key, and upload to Fly.io secrets
- [ ] Create "Life" folder structure in Google Drive, including:
    - [ ] `Inbox/`
    - [ ] `Long-Term Goals/` (for AI to reference for contextual suggestions)
    - [ ] `Projects/` (potentially structured project details for AI reference)
    - [ ] `Personal Documents/`
    - [ ] `values, interests, philosophies/`
    - [ ] `Memory/` containing:
        - [ ] `Instructions.md` (for personality type, explicit instructions, master rules, persistent schedule preferences like lunch time, work hours, preferred communication style elements)
        - [ ] `User_Info.gsheet` (for structured data: Project details/importance, Opinions, Relationships)
- [ ] Set up shared Master To-Do Google Sheet with required columns (link to Task Schema in README)
- [ ] Configure cloud-based backup and restore procedures
- [ ] Populate sample data for initial testing (including sample personality quiz data and instructions)

## 4. n8n Workflows

- [x] Deploy n8n instance
- [x] Export and document modular n8n workflows: `main_planner.json`, `life_folder.json`, `todo.json`, `calendar.json`
- [ ] Document existing n8n deployment configuration
- [ ] Set up version control for n8n workflows (JSON exports)
- [ ] Configure n8n REST API access for programmatic updates
- [ ] Build Morning Kickoff / Daily Planning workflow (triggered by user activity or time):
    - [ ] AI "Good morning" greeting.
    - [ ] Parse today's Google Calendar events (using defined strict format).
    - [ ] For each calendar block, pull relevant to-dos from To-Do DB.
    - [ ] Logic for Contextual Suggestions:
        - [ ] Propose secondary/low-priority tasks if schedule is light.
        - [ ] Remind of long-term goals (from `Life/Long-Term Goals/`) or pain-avoidance motivators based on personality profile.
    - [ ] Generate proposed visual time-blocked schedule, incorporating tasks, events, and persistent preferences (from `Memory/Instructions.md`).
    - [ ] Send schedule to front-end for display and user acceptance/adjustment.
- [ ] Build On-Edit GSheet workflow (for Master To-Do)
- [ ] Build Calendar Update webhook workflow (for real-time event changes)
- [ ] Build End-of-Day Retro workflow
- [ ] Build `Memory/Instructions.md` Ingestion Workflow:
    - [ ] Regularly parse `Instructions.md` for personality settings, master rules, preferences, and feedback.
    - [ ] Update AI's operational parameters/prompt elements.
    - [ ] Implement logic to merge new instructions and auto-resolve/flag conflicts.
- [ ] Implement Dynamic Rescheduling logic within relevant workflows:
    *   [ ] Handle free-form change requests from user chat (move, add, remove blocks).
    *   [ ] Detect deviations (task completion changes, new events) and propose updated plan.
    *   [ ] Conflict avoidance: check for double bookings, reprioritize based on urgency, project importance (`User_Info.gsheet`), and user preferences (`Memory/Instructions.md`).
- [ ] Implement Management Mode / Progress Check-in logic:
    *   [ ] Cadence and tone tuned to personality type (`Memory/Instructions.md`).
    *   [ ] Contextual progress prompts (e.g., "How's X going?").
    *   [ ] Celebrations for task/subtask completion.
    *   [ ] Logic for addressing off-task behavior: point out sacrifices, offer to reprioritize/reblock.
- [ ] Add unit tests / mock executions for all workflows
- [ ] Create workflow deployment script using n8n API
- [ ] Replace Slack Trigger in `main_planner.json` with a secured HTTP/Webhook trigger (e.g., Header Auth) for front-end integration, and document API key strategy.
- [ ] Update workflow documentation to reflect front-end integration

## 5. Scheduling Engine (Business Logic)

- [ ] Design time-blocking algorithm with buffers and collision resolution (core of dynamic rescheduling and daily planning)
- [ ] Implement algorithm as TypeScript library consumed by n8n & Next.js
    - [ ] Consider inputs: tasks (with priority, duration, dependencies), calendar events, user preferences from `Memory/Instructions.md` (e.g. work hours, lunch breaks, meeting buffers), project importance from `User_Info.gsheet`.
- [ ] Write unit tests covering edge cases (dependencies, delays, priority, conflicting preferences)

## 6. Next.js Front-End

- [ ] Set up Next.js project with TypeScript and Tailwind
- [ ] Configure cloud-based development environment
- [ ] Scaffold base layout with Tailwind & responsive design
- [ ] Implement swipeable panels (To-Do List, Calendar/Daily Schedule, Life Folder) (as per `Front_End_Details.md`)
- [ ] Implement bottom navigation bar (as per `Front_End_Details.md`)
- [ ] Build To-Do List component consuming Google Sheets data (MVP for task display & quick add)
- [ ] Build Calendar/Daily Schedule component:
    - [ ] Display time-blocked schedule from n8n (MVP).
    - [ ] Show events from Google Calendar (distinctly styled).
    - [ ] Visually represent persistent preferences (e.g., lunch block).
    - [ ] Allow direct manipulation (drag & drop reschedule, duration change) with changes sent to n8n for confirmation/conflict resolution.
- [ ] Build Life Folder explorer powered by Drive API (MVP for `Memory/Instructions.md`, `Inbox`, `Long-Term Goals` viewing; basic editing of `Instructions.md`).
- [ ] Implement chat overlay (as per `Front_End_Details.md`)
    - [ ] Free-form text/voice input to n8n for task ingest, schedule changes, feedback (MVP).
    - [ ] Display AI responses, including proposed schedule adjustments.
    - [ ] Interactive elements for confirming changes, snoozing reminders.
- [ ] Implement Personality On-Ramp Quiz (MVP)
    - [ ] Develop quiz questions and scoring for personality archetype & motivation style.
    - [ ] Store results in `Life/Memory/Instructions.md`.
    - [ ] Allow skipping quiz and manual setting of personality parameters.
- [ ] Implement settings panel:
    - [ ] View/Retake/Manually adjust personality settings (modifies `Memory/Instructions.md`).
    - [ ] Manage common persistent preferences (lunch time, work hours - modifies `Memory/Instructions.md`).
    - [ ] Notification preferences.
    - [ ] Google Account connection.
- [ ] Add PWA support and push notifications for reminders.
- [ ] Integrate authentication (Google OAuth).

## 7. Personality & Feedback Loop

- [ ] Implement `Memory/Instructions.md` reader and prompt augmentation system (MVP - core to AI behavior)
    - [ ] Ingest personality archetype, motivation style, explicit rules, preferences, and feedback from `Instructions.md`.
    - [ ] Dynamically construct system prompts or update AI operational parameters.
    - [ ] Implement conflict resolution logic for instructions within `Instructions.md` (attempt auto-resolve, else flag to user).
- [ ] Implement management style selection & initial set of tone templates based on archetypes (MVP).
    - [ ] These templates are further customized by specific instructions/feedback in `Memory/Instructions.md`.
- [ ] Implement parsing of free-form input (chat/voice) for task structuring (MVP)
    - [ ] Identify task name, potential deadlines, project tags, break down large tasks (basic heuristics).
- [ ] Logic for AI to propose breaking large tasks into subtasks with dependency links (post-MVP refinement).
- [ ] AI logic for contextual suggestions during morning planning (referencing `Long-Term Goals/` and personality profile).
- [ ] AI logic for focus management/off-task intervention (Management Mode).

## 8. API Layer

- [ ] Create Next.js API routes for tasks, schedule, and chat
- [ ] Secure endpoints with JWT/session & CSRF protection
- [ ] Integrate rate limiting and logging middleware

## 9. Testing & Quality Assurance

- [ ] Add Jest & React Testing Library tests for UI components
- [ ] Add integration tests for API routes
- [ ] Add E2E tests with Playwright or Cypress

## 10. Documentation

- [x] Extend README with detailed setup & usage instructions (initial pass done, will need ongoing updates)
- [x] Create architecture diagram assets (initial ASCII in README, can be improved)
- [ ] Document n8n workflows and API endpoints
- [x] Create User Experience (`User_Experience.md`) document
- [x] Create Front-End Details (`Front_End_Details.md`) document

## 11. Optional Add-Ons (Post-MVP)

- [ ] Implement Automated Life Folder Extractor (scans chats to update `User_Info.gsheet` etc.)
- [ ] Implement Secure Vault (requires crypto design)
- [ ] Implement Pomodoro Timer module
- [ ] Implement Habit Tracker module
- [ ] Implement Gamified To-Do module
- [ ] Implement Life Coach Mode
- [ ] Implement Astrologer Plugin

## 12.
   