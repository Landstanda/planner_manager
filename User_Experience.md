# User Experience Guide: Chief-of-Flow

## Overview

Chief-of-Flow is an intuitive AI-powered task management app designed specifically for solo founders, creators, and individuals managing complex projects with a tendency toward distraction. It combines the simplicity of pen-and-paper with robust automation and AI customization, so users can focus on their work and not on managing the tool.

The central vision is to serve as your personal AI “chief-of-staff,” one that genuinely understands your motivations, personality, and working style to keep you in a state of flow.

---

## User Journey

### 1. Onboarding & Personalization

- **Personality & Motivation Quiz (Optional to Skip):**
  - A 1–2 minute quiz identifies your core motivational drivers, preferred communication tone (e.g., sarcastic, upbeat, dead-pan), stress-management needs, and proactivity level.
  - You can skip the quiz and manually select personality and tone settings instead.
  - **Outcome:** Quiz results or chosen settings are saved in `Life/Memory/Instructions.md` and used to tailor every AI interaction.

- **Initial Setup (Optional Calendar Integration):**
  - Option to link your Google Calendar (non-MVP). When you do, calendar entries should be formatted as:  
    ```
    Title = ProjectName–WorkBlock  
    Tags = work / life / personal, etc.
    ```
  - This allows the AI to automatically parse and categorize calendar blocks by project.
  - During onboarding, you’re introduced to the “Life Folder” concept:
    - `Memory/Instructions.md`: Stores personality quiz results, explicit behavior rules (e.g., “Remind me 10 min before deadlines,” “No weekend blocks before 10 AM”), and stable preferences (lunch time, work hours).
    - `Memory/User_Info.gsheet` (if used): Holds structured data on projects, relationships, values.
    - `Inbox/`: Captures spontaneous notes and quick thoughts.
    - `Long-Term Goals/`: Houses your overarching aspirations.

---

### 2. Daily Planning Routine

- **Morning Kickoff & Greeting:**
  - At a pre-configured time or as soon as you become active, Chief-of-Flow sends a personalized “Good morning” message.
  - It reviews today’s calendar entries (including any calendar blocks you created in the prescribed format) and pulls relevant to-dos from your master task list.

- **Project Drill-Down & Contextual Suggestions:**
  - For each calendar block, the AI surfaces outstanding tasks from the Task DB.
  - If the day’s calendar is light or heavily skewed toward a single project, the AI suggests secondary or low-priority tasks:
    > “Your afternoon is wide open—would you like to chip away at your ‘Launch New Course’ goal?”  
    > “Looks like you’ve got time before that call; how about finishing the slides so you’re not stressed later?”
  - These suggestions incorporate your long-term goals and pain-avoidance motivators, presented in a tone matching your personality profile.

- **Proposed Schedule & Review/Accept/Adjust:**
  - Chief-of-Flow presents a time-blocked schedule in a clean, calendar-style UI (with blocks for lunch, meetings, focused work).
  - You can:
    - **Accept** the proposed plan as-is.
    - **Adjust** via natural-language chat (“Move my marketing block to 2 PM”) or by direct drag-and-drop.
  - As soon as you make a change, the system checks for conflicts (avoiding double bookings), reprioritizes if needed, and explains its rationale:
    > “I moved your writing block to 2 PM because your client call shifted. This ensures you still get two solid hours of uninterrupted focus.”

---

### 3. Task Capture & Structuring

- **Free-Form Input (Text/Voice):**
  - You can add tasks or ideas at any moment with simple phrases (e.g., “Remind me to call John tomorrow,” “I need to draft the project proposal by Friday,” “Buy groceries”).
  - The AI parses key details—task name, deadline, priority—and files them into the Master Task List (in Supabase or a Google Sheet).
  - If a task seems large or ambiguous, the AI may follow up:  
    > “That project proposal sounds big—want me to break it into subtasks (outline, first draft, review)?”
  - Urgent items trigger a quick “manager mode” prompt:
    > “This seems critical—should I schedule a 15-min focus block before your 3 PM meeting?”

- **Spontaneous Capture → Inbox Workflow:**
  - When you jot down random thoughts or new ideas, they go into `Inbox/` in the Life Folder.
  - If something in the Inbox looks like a task, the AI may ask clarifying questions or structure it immediately:
    > “I noticed you mentioned ‘research competitor pricing.’ Would you like me to turn that into a 30-minute task today?”

---

### 4. Dynamic Schedule Management: Adapting to Real Life

- **Free-Form Change Requests (Examples):**
  - You can say:  
    > “Push my 2 PM meeting to 3 PM.”  
    > “Cancel my writing block this afternoon.”  
    > “Add a 30-minute call with Sarah at 4 PM.”
  - The AI instantly verifies conflicts, reprioritizes, and updates your day.

- **Real-Time Adjustments & Rationale:**
  - Chief-of-Flow monitors task completion (either by your marking tasks as “done” or by inferring from check-ins).
  - If tasks finish early or run late, or if new high-priority events appear (from calendar sync), the AI proposes an updated plan and explains why:
    > “You completed your design review 30 minutes early. I’ve moved your next block up so you can get a break sooner. Sound good?”

- **Conflict Avoidance & Reprioritization Based on Preferences:**
  - Whenever a change is requested or detected, the AI checks for double bookings and resolves conflicts using:
    1. Task urgency  
    2. Project importance (from `User_Info.gsheet` or Supabase)  
    3. Your stable preferences in `Memory/Instructions.md` (e.g., “Keep 3 PM free for family calls” or “Never schedule meetings on Fridays after 3 PM”).  
  - It may notify you:  
    > “Your ‘Marketing Review’ task was low priority, so I pushed it to tomorrow. Let me know if you want to keep it today instead.”

---

### 5. Motivational Accountability: Management Mode & Focus Support

- **Progress Check-Ins (Tuned to Personality):**
  - Check-in cadence, tone, and phrasing follow your personality profile in `Instructions.md`.  
  - Examples:  
    - “How’s that [Task Name] going?” (gentle, warm style)  
    - “Two tasks down—let’s crush that presentation draft while you’re on a roll!” (upbeat, toward-goals style)  
    - “Your writing block ends in 15 minutes—anything you need before moving on?” (matter-of-fact, candid style)

- **On-the-Fly Adjustments & Focus Management:**
  - If you indicate you’re drifting off-task—or if a scheduled block ends with no status update—the AI intervenes:  
    > “I see you’re browsing social media—want to officially reschedule that writing block, or shall we refocus on it now?”  
  - This keeps you aware of what you’re sacrificing versus your planned priorities, giving you the choice to reprioritize or recommit.

- **Continuous Feedback Loop:**
  - You can refine the AI’s behavior by editing `Life/Memory/Instructions.md` or providing in-chat feedback:  
    > “Be more sarcastic” or “Check in less often around noon.”  
  - The system ingests these updates and adjusts tone, frequency, and check-in style accordingly.

---

### 6. End-of-Day Reflection & Long-Term Engagement

- **Daily Summary:**
  - At a set time (e.g., 5 PM), you receive a concise recap of:  
    - Tasks completed  
    - Incomplete items carried forward  
    - Suggestions for tomorrow’s priorities (linked to long-term goals)  
  - You can provide feedback on scheduling choices, which feeds into future plan adjustments.

- **Life Folder & Memory Integration:**
  - **Life Folder Contents (quick reference):**  
    - `Memory/Instructions.md`: Master instruction list for AI behavior (tone, scheduling preferences, buffers, etc.).  
    - `Memory/User_Info.gsheet`: Structured data on projects, values, opinions, relationships.  
    - `Inbox/`: Unstructured quick captures.  
    - `Long-Term Goals/`: Files outlining your overarching aspirations.  
    - Project-specific folders and documents.  
  - As you interact, Chief-of-Flow continuously refines its understanding of your preferences, creating a feedback loop that deepens personalization over time.

- **Long-Term Engagement & Growth:**
  - The AI celebrates milestones, tracks progress toward larger goals, and adjusts motivation tactics as you evolve (e.g., shifting from gentle encouragement to more candid nudges if you respond better that way).  
  - Over weeks and months, you’ll see an evolving “assistant” that truly feels like it knows how you think and work—reducing friction and preserving your mental energy.

---

## Interaction Examples

> **User Captures a Task (Voice/Text)**  
> **User:** “I need to follow up with Sarah about the budget by tomorrow afternoon.”  
> **AI:** “Got it—reminder set for tomorrow at 10 AM to check with Sarah on the budget. Anything else?”

> **Morning Kickoff (Contextual Suggestion)**  
> **AI:** “Good morning! Today you have a client call at 11 AM and a lunch break from 12:30 PM to 1:30 PM. You haven’t touched your ‘Launch Course’ project in two days—want to slot in 30 minutes on that right after your call so it doesn’t slip?”

> **Real-Time Adjustment with Rationale**  
> **User:** “Push my 2 PM writing block to 3 PM.”  
> **AI:** “Sure—your 3 PM project sync moved earlier, so I’ve swapped those. Now you’ll have a full hour from 2 PM to 3 PM to prep. Does that work?”

> **Progress Check-In (Focus Management)**  
> *(Task block runs over, user hasn’t updated)*  
> **AI (after 5 minutes of no update):** “Your design review block just ended a few minutes ago. I noticed no status—are you still on it or should I reschedule?”

---

## User Interface Principles

- **Simplicity & Clarity:**  
  A clean, minimalist layout with clearly labeled tasks, visual time blocks, and intuitive cues that minimize cognitive load.

- **Personal Connection:**  
  UI elements (phrasing, colors, even emojis) reflect the tone and style matching your personality profile. You should feel the interface “speaks your language.”

- **Efficiency:**  
  Seamless fluidity from capturing ideas to seeing them on your schedule. Drag-and-drop adjustments, one-tap voice input, and chat-based commands keep friction at a minimum.

---

## Key UI Elements

- **Swipeable Panels:**  
  1. **To-Do List** (Master Task DB view)  
  2. **Calendar/Daily Schedule** (Time-blocked, interactive)  
  3. **Life Folder** (Inbox, Long-Term Goals, Memory files)

- **Floating “Ask Me…” Pill:**  
  Always visible at the bottom—tap to type or hold to record a voice command. Instantly converts free-form input into tasks or notes.

- **Dynamic Navigation Bar:**  
  Bottom bar highlights the current panel. You can also swipe between panels.

- **Drag-and-Drop Schedule Editor:**  
  In the Calendar view, long-press a block to move it, or pull up a menu to add/​cancel blocks.

---

## Long-Term Engagement & Evolution

- **Continuous Learning:**  
  Chief-of-Flow adjusts its motivational style, check-in frequency, and scheduling logic based on your actions and explicit feedback in `Instructions.md`.

- **Milestone Celebrations & Gamification:**  
  As you hit major project milestones, the AI highlights achievements (“Congratulations—you’ve completed 5 subtasks on your new course!”) and may unlock small “rewards” (e.g., optional Pomodoro break reminders or encouraging badges).

- **Persistent Memory & Context:**  
  Over time, the assistant better anticipates your patterns—knowing, for instance, that you usually need a 15-min buffer between meetings or that you resist Tuesday morning brainstorming sessions. This deep familiarity reduces the need for manual corrections and keeps you in flow.

---

*This document should serve as the definitive guide for designers, developers, and stakeholders building Chief-of-Flow, ensuring every interaction feels effortless, personalized, and deeply supportive of the user’s goals.*  
