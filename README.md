# **Daily Planner AI Agent**

A streamlined personal assistant that plans your day intelligently, helps you prioritize, keeps you focused, and captures your ideas as they happen. Designed to support a fast-paced, nonlinear thought process, this agent makes it easy to offload mental clutter and build structure later. Each morning, it compiles a personalized daily schedule from your calendar and master task list, then checks in throughout the day with smart reminders and progress nudges. It handles spontaneous requests in natural language, converts them into structured tasks, and files everything neatly into your "Life Folder."

**It's envisioned as a personal AI "chief‑of‑staff" for solo founders and build‑in‑public creators, speaking the user's language by adapting its tone and communication style.** The key differentiator is the immediate feeling that "this AI gets me," unlike generic LLM assistants.

The backend is powered by **n8n** for automation and logic orchestration, **Next.js** and **Tailwind CSS** for a fast, responsive UI, and **Fly.io** for scalable deployment. Your **Google Drive** acts as both database and file system, keeping everything centralized, accessible, and versionable.

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

* **Personal AI "chief‑of‑staff":** Tailored for solo founders and build‑in‑public creators.
* **Speaks Your Language:** Adapts tone to personality, motivation (toward‑goals vs. away‑from‑pain), and communication style (sarcastic, upbeat, dead‑pan), driven by a personality quiz and ongoing feedback via `Life/Memory/Instructions.md`. This creates an immediate connection, differentiating it from generic LLM assistants.
* **Effortless Capture → Organized Execution:** Jot tasks anytime; the system auto‑structures them, schedules work blocks (respecting persistent preferences like lunch breaks from `Life/Memory/Instructions.md`), and nudges progress.
* **Dynamic Schedule Management:** Revises the day's plan in real time when tasks finish early/late, new priorities appear, or meetings shift. Handles free-form change requests and resolves conflicts based on urgency, importance, and user preferences.
* **Motivational Accountability:** Regular, context-aware check‑ins delivered in the user's preferred tone keep momentum. The AI can point out deviations from the plan and offer to reprioritize.

---

## **Key Features & MVP Feature Set**

The app aims for a comprehensive set of features, with the following identified as core to the Minimum Viable Product (MVP):

### General Features (Existing & Enhanced)
* Natural language to Master To-Do List (via chat or voice).
* **Morning Kickoff & Daily Planning Logic:**
    * Greets user and reviews today's calendar (expecting specific event formatting for project tagging).
    * Drills into project details, pulling relevant tasks from the To-Do DB for each calendar block.
    * Proposes a visual time-blocked schedule, considering persistent preferences (e.g., lunch, work hours) stored in `Life/Memory/Instructions.md`.
    * Offers contextual suggestions for light schedules or to align with long-term goals/motivators (also stored in Life Folder).
* Builds a time‑blocked schedule with buffers (configurable).
* **Smart Check-ins & Dynamic Pacing (Management Mode):**
    * Cadence and tone of check-ins tuned to personality type.
    * Progress prompts at appropriate intervals; celebrates subtask/task completion.
    * If user drifts, points out sacrifices vs. planned priorities and offers to reprioritize.
* Spontaneous requests and notes captured via chat interface to `Life/Inbox/`.
* **Instant Re-planning & Dynamic Rescheduling:**
    * Handles free-form change requests (move, add, remove blocks).
    * Automatically checks for conflicts and reprioritizes based on urgency, project importance, and user's stated preferences (from `Life/Memory/Instructions.md`).
* Unstructured notes and requests automatically logged to `Life/Inbox/`.

### MVP Feature Set

| Area                          | Must‑Have Capability                                                                                                                                     | Notes                                                                                             |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Personality On‑Ramp**       | 1–2‑minute quiz → tag user's personality archetype & motivation style                                                                                    | Drives all language tailoring; marketable "Take the free test to meet your perfect AI assistant." |
| **Task Ingest & Structuring** | Free‑form input (chat or voice) added to **To‑Do DB**. Large tasks auto‑broken into subtasks with dependency links.                                      | Urgent items trigger immediate scheduling questions or manager mode.                              |
| **Daily Planning Mode**       | Morning routine that merges calendar events + To‑Do DB; creates proposed day blocks for user to accept/adjust. Includes contextual suggestions and respects persistent preferences from `Life/Memory/Instructions.md`. | Visual schedule interface is key.                                                                  |
| **Live Schedule Adjust**      | Detects deviations (done early/late, cancellations, new events) and proposes updated day plan. Handles user-initiated free-form changes with conflict resolution. | AI checks for double bookings & reprioritizes based on urgency, importance, & user preferences. |
| **Progress Check‑Ins**        | Timed or context‑based pings asking for status updates in user‑tailored tone. Offers to reprioritize if off-task.                                      | Cadence & tone driven by personality profile in `Life/Memory/Instructions.md`.                   |
| **Master Instruction List**   | Single source of truth in `Life/Memory/Instructions.md` for high‑level behavior rules, personality settings, and stable preferences (e.g., "Remind me 10 min before deadlines," lunch time). System ingests, merges, and attempts to auto-resolve conflicts. | User can view/edit.                                                                              |

---

## **Architecture**

┌────────────┐    Webhooks   ┌───────────────┐    REST    ┌──────────────┐  
│  Next.js   │◀─────────────▶│    n8n        │◀──────────▶│ Google Sheets│  
│  Front‑End │   JSON/WS     │  Workflows    │    GSheets │   (To‑Dos)   │  
└────────────┘                └─────▲─────────┘           └──────────────┘  
      ▲ HTTP/PWA                 │  Drive API                                 
      │                           │                                            
┌─────┴─────┐    gRPC / REST   ┌──┴──────────┐                                
│ Fly.io VM │◀───────────────▶│ Google Drive│ (Life Folder)                  
└───────────┘                 └──────────────┘

---

## **Folder / Data Layout**

Life/
├─ Inbox/                     ← default dump for new items, spontaneous thoughts
├─ Long‑Term Goals/           ← User's long-term aspirations, referenced for contextual suggestions
├─ Projects/                    ← Details about ongoing projects
├─ Personal Documents/
├─ values, interests, philosophies/
└─ Memory/
   ├─ Instructions.md          ← Personality type, explicit AI instructions, master rules, persistent schedule preferences (lunch, work hours), communication style tweaks.
   └─ User_Info.gsheet         ← Structured user data: Project details/importance, Opinions, Relationships (name/title | fact format)
   └─ improvement_requests.md  ← (Consider merging into Instructions.md) specific feedback on AI tone/behavior.

---

## **Task Schema**

id: string  
name: string  
description: string  
project: string  
status: delayed | ready | in‑progress | done | cancelled  
priority: 1‑5  \# 1 \= critical, 5 \= someday  
estimated\_duration: int  \# minutes  
dependencies: \[id,…\]  
scheduled\_datetime: datetime|null  
actual\_start: datetime|null  
actual\_end: datetime|null

---

## **Workflow Triggers**

| Trigger | Schedule / Event | Action |
| ----- | ----- | ----- |
| Morning‑Plan | 07:45 America/Chicago daily | Build Daily Schedule; display in dashboard |
| On‑Edit (GSheet) | Row change in Master To‑Do | Re-check dependencies, update plan if impacted |
| Calendar Update | Google Calendar webhook | If change affects today, re-check schedule |
| End‑of‑Day Retro | 17:00 daily | Track actual durations, update statuses |
| Feedback File | New line in improvement\_requests.md | Reload prompt style with latest suggestions |

---

## **Scheduling & Conflict Logic**

1. **Order of Precedence**  
    `priority` → earliest `scheduled_datetime` → shorter `estimated_duration` → FIFO

2. **Time Blocking**  
    Tasks fill open slots around calendar events with a 5-minute buffer (configurable).

3. **Collision Resolution**

   * Try to extend the day (up to 1 hr)  
   * Push low-priority tasks to the next feasible window  
   * Mark unplaced tasks as `delayed` and resurface next morning  
4. **Dynamic Check-ins**  
    Adjusts reminder timing based on task urgency and your past response behavior

---

## **Adaptive Tone & Feedback Loop**

* **File:** `Life/Memory/Instructions.md` is the primary file. It stores personality quiz results/settings, explicit instructions from the user (e.g., "be more sarcastic," "don't schedule meetings on Friday afternoons"), and persistent preferences (like default lunch times).
* **Format:** Structured data for personality scores and preferences; free text per line for feedback or direct instructions.
* **Effect:** The system ingests `Instructions.md` to tailor its communication style, scheduling behavior, and check-in cadence. New instructions are merged, and the system attempts to resolve conflicts or flags them for user review.
* **Example (Instruction in `Instructions.md`):**
  `preference: lunch_time=12:30`
  `feedback: 2025-05-08 | Your morning greeting was a bit too cheerful.`

* The next nudge might sound less cheerful, and lunch will be pre-blocked at 12:30 PM.

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

Change styles anytime or shape tone gradually by adding notes like "be more assertive" or "check in less frequently" to `Life/Memory/Instructions.md`.

---

## **Front‑End UI**

* Three swipeable panels: **To-Do List**, **Calendar/Daily Schedule View**, **Life Folder**.
    *   The Calendar/Daily Schedule View is highly interactive, showing time blocks with project labels, and allowing drag-and-drop rescheduling.
* Bottom nav has three icons: tap or swipe to switch views.

---

## **Deployment**

1. Clone the repo & configure `.env`  
2. Launch via Fly.io:

flyctl launch \--dockerfile Dockerfile.multi

3. Configure Google Cloud:  
* Service account with Drive & Sheets access  
* Share your "Life" folder and To-Do list sheet  
4. Configure domain and SSL via:

fly certs add \<your domain\>

---

## **Future Add-Ons**

Beyond the MVP, the planner can be extended with features like:

* **Life Folder (Expanded):** Automated extractor scans daily chats to populate/update entries in `User_Info.gsheet` and other relevant documents.
* **Secure Vault:** For important numbers, passwords, docs (requires solid crypto design).
* Pomodoro Timer – Stay focused with timed work sessions and short breaks
* Habit Tracker – Reinforce daily habits with streaks, reminders, and analytics

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

## **n8n Workflow Architecture**

The automation and orchestration backbone of the Daily Planner AI Agent is powered by a set of modular n8n workflows, deployed on Fly.io. The main workflow, `main_planner.json`, acts as the central router and orchestrator, delegating user requests to specialized tool workflows:

* **Life Folder Tool** (`life_folder.json`): Handles user details (from `Life/Memory/User_Info.gsheet`), project info, document management (Google Drive), and AI instructions/feedback (from `Life/Memory/Instructions.md`).
* **Todo Tool** (`todo.json`): Manages the master to-do list, project metadata, and task updates using Google Sheets.
* **Calendar Tool** (`calendar.json`): Manages Google Calendar events, including creation, updates, and deletions.

### Workflow Integration

- **Current State:** The `main_planner.json` workflow is triggered by Slack messages (via Slack Trigger node) and responds in Slack.
- **Planned Update:** The Slack integration will be replaced with a direct connection to the custom Next.js front-end. The front-end will send user requests to n8n via HTTP/webhook, and receive responses for display in the UI chat overlay.

**How to Update Workflows:**
- Export the relevant workflow JSON from n8n running on Fly.io.
- Edit the workflow as needed (e.g., update trigger nodes, tool connections).
- Re-import or update the workflow in the n8n instance.

**Note:** The n8n Dockerfile and deployment are managed separately on Fly.io, so workflow updates can be made independently by copying/pasting JSON.

---

*For a detailed description of the user's interaction with the app, see `User_Experience.md`.*
*For a detailed description of the front-end layout, feel, and components, see `Front_End_Details.md`.*

