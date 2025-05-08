# **Daily Planner AI Agent**

A streamlined personal assistant that plans your day intelligently, helps you prioritize, keeps you focused, and captures your ideas as they happen. Designed to support a fast-paced, nonlinear thought process, this agent makes it easy to offload mental clutter and build structure later. Each morning, it compiles a personalized daily schedule from your calendar and master task list, then checks in throughout the day with smart reminders and progress nudges. It handles spontaneous requests in natural language, converts them into structured tasks, and files everything neatly into your "Life Folder."

The backend is powered by **n8n** for automation and logic orchestration, **Next.js** and **Tailwind CSS** for a fast, responsive UI, and **Fly.io** for scalable deployment. Your **Google Drive** acts as both database and file system, keeping everything centralized, accessible, and versionable.

---

## **Table of Contents**

1. Key Features  
2. Architecture  
3. Folder / Data Layout  
4. Task Schema  
5. Workflow Triggers  
6. Scheduling & Conflict Logic  
7. Adaptive Tone & Feedback Loop  
8. Spontaneous Natural-Language Capture  
9. Management Styles & Personality Tuning
10. Front‑End  
11. Deployment  
12. Future Add-Ons
13. Contributing  
14. License

---

## **Key Features**

* Natural language to Master To-Do List  
* Morning planning logic: parses today’s Google Calendar events and tasks at 07:45  
* Builds a time‑blocked schedule with buffers  
* Smart check-ins and dynamic pacing throughout the day  
* Spontaneous requests captured via chat interface  
* Instant re-planning if new constraints arise  
* Unstructured notes and requests automatically logged to Life/Inbox

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
├─ Long‑Term Goals/  
├─ values, interests, philosophies/  
├─ Projects/  
├─ improvement\_requests.md   ← tone & feedback to system prompt   
├─ Inbox/             ← default dump for new items  
└─ Personal Documents/

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

* **File:** `Life/Important Info/improvement_requests.md`  
* **Format:** free text per line  
* **Effect:** most recent N lines appended to prompt  
* **Example:**

2025-05-07 09:32 | Please be more passive-aggressive in your encouragement.

* The next nudge might sound like: *"You could keep procrastinating... or just order that HDMI cord now."*

---

## **Spontaneous Natural-Language Capture**

You can quickly say or type things like:

"I need to buy a new HDMI cord on Amazon before the end of the day\!"

The system infers:

title: Buy HDMI cord  
description: Buy HDMI cord by end of day.  
estimated\_duration: 5  \# minutes  
priority: 1  \# High  
scheduled\_datetime: today by 5pm

It may respond:

"Why don’t you just do it now?"

If you give a reason (e.g., "I'm on a call"), it'll:

* Predict when you'll be free  
* Schedule a reminder (e.g., in 15 minutes)  
* Confirm with something like: *"I’ll remind you in 15\. Good luck surviving Amazon search."*

\---

## **Management Styles & Personality Tuning**

The planner supports a range of management styles to match your motivation type. You can pick one manually or take a short personality quiz to get matched. Styles include:

* Tough Love – blunt and committed, calls you out when you ignore your plan.  
* Encouraging Coach – kind and motivating, celebrates progress and nudges gently.  
* Passive-Aggressive Californian – breezy and polite with pointed reminders.  
* Quiet Observer – minimal interruptions, ideal for self-directed workflows.

Change styles anytime or shape tone gradually by adding notes like “be more assertive” to improvement\_requests.md.

---

## **Front‑End UI**

* Three swipeable panels: **To-Do List**, **Calendar**, **Life Folder**  
* Bottom nav has three icons: tap or swipe to switch views  
* Input field at bottom launches a GPT-style chat  
  * Swipes up into a chat bubble overlay  
  * Swipe down to collapse and return to previous view  
* **Top left:** Chat history  
* **Top right:** Settings menu

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

The planner is built to be extensible, allowing for optional features and modules that support broader aspects of daily life and long-term growth. These add-ons can be activated or toggled through the settings panel and integrate seamlessly with your core workflow.

* Pomodoro Timer – Stay focused with timed work sessions and short breaks  
* Habit Tracker – Reinforce daily habits with streaks, reminders, and analytics  
* Meal Planner – Plan meals for the week, integrate with grocery lists and time blocks  
* Gamified To-Do System – Completing tasks helps grow a virtual tree or earn points toward personalized goals  
* Advanced Task Tracking – Visualize task momentum, effort estimation accuracy, and rollover trends  
* Long-Term Goal Tracking – Break major life goals into actionable steps and milestones  
* Life Coach Mode – Offers reflective questions, vision prompts, and weekly reviews  
* Astrologer Plugin – Inject a lighthearted astrological lens on scheduling and moods  
* Psychologist Assistant – Optional prompts for journaling, CBT-style check-ins, or emotional tagging of tasks

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

