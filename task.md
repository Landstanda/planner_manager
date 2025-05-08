# Book-Builder Project: Task List

This document serves as a comprehensive todo list for building the Book-Builder application. Tasks are organized by development phase and component.

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

## 2. Database Implementation (Supabase)

- [ ] Create Supabase project
- [ ] Install and configure required PostgreSQL extensions:
  - [ ] pgvector for embeddings
  - [ ] ltree for hierarchical data
- [ ] Implement database schema:
  - [ ] sections table (with ltree position)
  - [ ] formulas table (with mood_id)
  - [ ] moods table
  - [ ] entities table
  - [ ] facts table
  - [ ] embeddings table
- [ ] Set up Row-Level Security (RLS) policies
- [ ] Create database indexes:
  - [ ] ltree index on sections.position
  - [ ] Full-text index on sections.text
  - [ ] pgvector index on embeddings.vector
  - [ ] JSONB GIN index on entities.attributes
- [ ] Configure Supabase Auth
- [ ] Set up Supabase Realtime channels
- [ ] Generate and export TypeScript types

## 3. Backend Infrastructure

- [ ] Implement Supabase Edge Functions:
  - [ ] Authentication handlers
  - [ ] Section CRUD operations 
  - [ ] Entity CRUD operations
  - [ ] Proxy functions for n8n workflows
- [ ] Configure Next.js API routes:
  - [ ] Authentication endpoints
  - [ ] Section endpoints
  - [ ] Entity endpoints
  - [ ] LLM proxy endpoints
- [ ] Set up error handling and monitoring

## 4. n8n Workflow Implementation

- [ ] Set up n8n instance (local or cloud)
- [ ] Create World-Builder workflow:
  - [ ] Design webhook entry point
  - [ ] Implement entity upsert logic
  - [ ] Create detailed prompts for LLM triple extraction
  - [ ] Build fact extraction and storage nodes
  - [ ] Add response formatting
- [ ] Create Outline Generator workflow:
  - [ ] Design webhook entry point
  - [ ] Implement context fetching from parent sections
  - [ ] Create detailed prompts for each formula step
  - [ ] Build section merge and storage logic
  - [ ] Add response formatting
- [ ] Create Draft Writer workflow:
  - [ ] Design webhook entry point
  - [ ] Implement comprehensive context builder from sections/formulas/moods
  - [ ] Create detailed prompts for draft generation
  - [ ] Design iterative feedback mechanism
  - [ ] Build final text commit logic
  - [ ] Add notification nodes (Slack/email)

## 5. Frontend Development

- [ ] Build layout components:
  - [ ] Mobile-first responsive layout
  - [ ] Swipeable TOC drawer
  - [ ] Settings drawer
- [ ] Implement authentication UI:
  - [ ] Login/signup forms
  - [ ] User profile settings
- [ ] Create World-Building interface:
  - [ ] Entity creation forms
  - [ ] Entity browsing and visualization
  - [ ] Fact extraction UI
- [ ] Develop Outlining interface:
  - [ ] Tree view for outline structure
  - [ ] Formula selection UI
  - [ ] Outline editing tools
- [ ] Build Draft Writing interface:
  - [ ] Section editor with feedback loop
  - [ ] Draft preview
  - [ ] Revision interface
- [ ] Implement React Query for data fetching and caching
- [ ] Add real-time updates with Supabase subscription

## 6. LLM Integration (GPT-4.1)

- [ ] Set up secure API key management
- [ ] Develop prompt engineering framework:
  - [ ] Base prompt templates
  - [ ] Context injection utilities
  - [ ] Token optimization tools
- [ ] Design and test detailed prompts for:
  - [ ] Entity triple extraction
  - [ ] Outline generation based on formulas
  - [ ] Draft writing with mood/style control
- [ ] Implement LLM response parsing and handling
- [ ] Add error handling and fallback strategies

## 7. Testing and Quality Assurance

- [ ] Write unit tests:
  - [ ] React component tests
  - [ ] Database operation tests
  - [ ] API endpoint tests
- [ ] Implement integration tests:
  - [ ] n8n workflow tests (with mock LLM)
  - [ ] Full user journey tests
- [ ] Perform end-to-end testing
- [ ] Conduct security review:
  - [ ] Authentication
  - [ ] RLS policies
  - [ ] API endpoints
- [ ] Perform performance testing
- [ ] Test on various mobile devices

## 8. Deployment

- [ ] Set up Fly.io configuration:
  - [ ] Next.js app deployment
  - [ ] n8n deployment (if self-hosted)
- [ ] Configure production environment variables
- [ ] Set up CI/CD pipeline
- [ ] Deploy to staging environment
- [ ] Conduct production environment tests
- [ ] Configure monitoring and logging
- [ ] Set up backup strategies

## 9. Documentation and Final Touches

- [ ] Complete inline code documentation
- [ ] Create user guide:
  - [ ] World-building workflow
  - [ ] Outlining workflow
  - [ ] Draft writing workflow
- [ ] Write technical documentation:
  - [ ] Architecture overview
  - [ ] API documentation
  - [ ] Database schema
- [ ] Create sample project tutorial
- [ ] Implement analytics
- [ ] Finalize README and contribution guidelines

## 10. Post-Launch Tasks

- [ ] Monitor performance and user feedback
- [ ] Address initial bugs and issues
- [ ] Begin work on roadmap items:
  - [ ] Visual timeline Gantt chart
  - [ ] Embedding-powered "similar scene" suggestions
- [ ] Consider expansion features based on user feedback 