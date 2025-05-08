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
- [ ] Containerize Next.js app (`nextjs_app`) and configure for Fly.io deployment (Dockerfile, fly.toml)
- [x] Create `actions.md` for logging
- [x] Create `.cursor/rules/log_actions_rule.md` for logging reminders

## 2. Infrastructure & DevOps

- [x] Containerize n8n service and set up persistent volume
- [ ] Document existing n8n configuration and volume setup
- [ ] Set up Next.js deployment in Fly.io with persistent storage
- [ ] Configure shared environment and secrets management in Fly.io
- [ ] Set up remote development environment configuration
- [ ] Configure GitHub Actions CI for build, lint, and test workflows
- [ ] Configure CD pipeline for Fly.io deployment of Next.js
- [ ] Set up automated version tagging and release notes

## 3. Google Cloud & Data Storage

- [ ] Create GCP project and enable Drive & Sheets APIs
- [ ] Create service account, generate key, and upload to Fly.io secrets
- [ ] Create "Life" folder structure in Google Drive
- [ ] Set up shared Master To-Do Google Sheet with required columns
- [ ] Configure cloud-based backup and restore procedures
- [ ] Populate sample data for initial testing

## 4. n8n Workflows

- [x] Deploy n8n instance
- [x] Export and document modular n8n workflows: `main_planner.json`, `life_folder.json`, `todo.json`, `calendar.json`
- [ ] Document existing n8n deployment configuration
- [ ] Set up version control for n8n workflows (JSON exports)
- [ ] Configure n8n REST API access for programmatic updates
- [ ] Build Morning-Plan workflow (07:45 daily scheduler)
- [ ] Build On-Edit GSheet workflow
- [ ] Build Calendar Update webhook workflow
- [ ] Build End-of-Day Retro workflow
- [ ] Build Feedback File workflow
- [ ] Add unit tests / mock executions for all workflows
- [ ] Create workflow deployment script using n8n API
- [ ] Replace Slack Trigger in `main_planner.json` with HTTP/Webhook trigger for front-end integration
- [ ] Update workflow documentation to reflect front-end integration

## 5. Scheduling Engine (Business Logic)

- [ ] Design time-blocking algorithm with buffers and collision resolution
- [ ] Implement algorithm as TypeScript library consumed by n8n & Next.js
- [ ] Write unit tests covering edge cases (dependencies, delays, priority)

## 6. Next.js Front-End

- [ ] Set up Next.js project with TypeScript and Tailwind
- [ ] Configure cloud-based development environment
- [ ] Scaffold base layout with Tailwind & responsive design
- [ ] Implement swipeable panels (To-Do List, Calendar, Life Folder)
- [ ] Implement bottom navigation bar
- [ ] Build To-Do List component consuming Google Sheets data
- [ ] Build Calendar component showing events & schedule
- [ ] Build Life Folder explorer powered by Drive API
- [ ] Implement chat overlay with OpenAI integration
- [ ] Implement settings panel (management style selection, module toggles)
- [ ] Add PWA support and push notifications for reminders
- [ ] Integrate authentication (Google OAuth)

## 7. Personality & Feedback Loop

- [ ] Implement improvement_requests.md reader and prompt augmentation
- [ ] Implement management style selection & tone templates

## 8. API Layer

- [ ] Create Next.js API routes for tasks, schedule, and chat
- [ ] Secure endpoints with JWT/session & CSRF protection
- [ ] Integrate rate limiting and logging middleware

## 9. Testing & Quality Assurance

- [ ] Add Jest & React Testing Library tests for UI components
- [ ] Add integration tests for API routes
- [ ] Add E2E tests with Playwright or Cypress

## 10. Documentation

- [ ] Extend README with detailed setup & usage instructions
- [ ] Create architecture diagram assets
- [ ] Document n8n workflows and API endpoints

## 11. Optional Add-Ons

- [ ] Implement Pomodoro Timer module
- [ ] Implement Habit Tracker module
- [ ] Implement Gamified To-Do module
- [ ] Implement Life Coach Mode
- [ ] Implement Astrologer Plugin

## 12.
   