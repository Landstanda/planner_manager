# User Experience: Planner-Manager App

This document outlines the user's interaction journey with the Planner-Manager App, emphasizing its role as a personalized AI "chief-of-staff."

## 1. Onboarding: Meeting Your AI Assistant

*   **Personality & Motivation Quiz:**
    *   The user's first interaction is a short (1-2 minute) quiz.
    *   Questions are designed to identify their personality archetype, primary motivation style (e.g., toward-goals vs. away-from-pain), and preferred communication tone (sarcastic, upbeat, dead-pan, etc.).
    *   Optionally, the user can skip the quiz choose their personality settings.
    *   **Outcome:** The system tags the user's profile, which tailors all future AI communication. Results and explicit instructions are stored in `Life/Memory/Instructions.md`.
*   **Initial Setup (Optional):**
    *   Link to your Google Calendar (non-MVP feature). Calendar entries are expected to follow a format for easy parsing: Title = Project name (e.g., "SaaS–Work Block"), with duration and tags (work, life, personal, etc.).
    *   Introduction to the "Life Folder" concept and the `Memory/Instructions.md` file for ongoing personalization and storing persistent preferences (e.g., lunch at 12:30 PM; no weekends before 10 AM).

## 2. Daily Interaction: Effortless Capture & Organized Execution

*   **Task Ingest:**
    *   Users can add tasks via a free-form chat interface (text or voice).
    *   Examples: "Remind me to call John tomorrow afternoon," "I need to draft the project proposal by Friday," "Buy groceries."
    *   The AI parses the input, identifies key details (task name, deadline, priority if mentioned), and adds it to the To-Do DB (Google Sheet).
    *   For large or complex tasks, the AI might ask clarifying questions or automatically suggest breaking them into subtasks with dependency links.
    *   Urgent items can trigger immediate scheduling questions or a more directive "manager mode" from the AI.
*   **Morning Kickoff & Planning:**
    *   The AI provides a "Good morning" greeting once it detects the user is active or at a set time.
    *   **Calendar Review:** It reviews today's calendar events (auto-created & tagged by project, or manually entered by the user following the specified format).
    *   **Project Drill-Down:** For each calendar block/project, the AI pulls relevant to-dos from the To-Do DB.
    *   **Contextual Suggestions:**
        *   If the day's calendar is light or heavily skewed to one project, the AI may propose secondary or low-priority tasks from the To-Do DB.
        *   It can also remind the user of long-term goals (from `Life/Long-Term Goals/`) or pain-avoidance motivators, tailoring the suggestion to their personality profile (e.g., "Want to chip away at that 'Launch New Course' goal?" or "Let's knock out this report so you don't have that looming over your weekend.").
    *   **Proposed Schedule:** The AI presents a time-blocked schedule in a clean, calendar-style UI, incorporating calendar events, tasks, and persistent preferences (e.g., pre-blocked lunch).
    *   The user can review, accept, or adjust the schedule via chat or direct manipulation on the visual schedule.
*   **Spontaneous Capture:**
    *   Throughout the day, users can note random thoughts, ideas, or new tasks into the chat that'll be noted in the `Inbox` doc.
    *   The system captures these into a designated "Inbox" within the Life Folder or attempts to structure them if they seem like tasks, potentially asking for clarification.

## 3. Dynamic Schedule Management: Adapting to Real Life

*   **Free-form Change Requests:**
    *   User can ask to move, add, or remove time blocks via chat (e.g., "Push my 2 PM meeting to 3 PM," "Cancel my writing block this afternoon," "Add a 30-minute call with Sarah at 4 PM").
*   **Real-Time Adjustments (Automated & Proposed):**
    *   The system monitors task completion (user marks as done, or AI infers from check-ins).
    *   If tasks finish early or run late, or if new high-priority items/meetings appear (e.g., from calendar sync), the AI detects these deviations.
    *   It proactively proposes an updated day plan, explaining the rationale.
*   **Conflict Avoidance & Reprioritization:**
    *   The AI automatically checks for double bookings when changes are made or proposed.
    *   Reprioritization considers: task urgency, project importance (potentially from `User_Info.gsheet`), and user's stated preferences (e.g., "Keep 3 PM free for family calls," stored in `Memory/Instructions.md`).

## 4. Motivational Accountability: Your Personalized Nudge (Management Mode)

*   **Progress Check-Ins:**
    *   Cadence and tone are tuned to the user's personality type (e.g., gentle reminders vs. tough love) as defined in `Memory/Instructions.md`.
    *   Prompts occur at appropriate intervals or contextually (e.g., before a block ends).
    *   Examples: "How's that [Task Name] going?", "Just a heads-up, your block for [Project Name] ends in 15 minutes."
    *   Celebrates when subtasks or major tasks are completed.
*   **On-the-Fly Adjustments & Focus Management:**
    *   If the user indicates they are drifting off-task, or if a scheduled block passes with no update, the AI might gently intervene.
    *   It might point out what they're sacrificing (based on the planned priorities) vs. their current activity (if known).
    *   Offers to officially reprioritize or reblock time: "Looks like you're focusing on [Other Activity]. Want to adjust the schedule to make room for that, or shall we try to get back to [Planned Task]?"
*   **Feedback Loop:**
    *   Users can continuously refine the AI's tone, check-in frequency, and behavior by adding or modifying notes in `Life/Memory/Instructions.md`.

## 5. Master Instruction List & Memory Integration

*   **Master Instruction List (`Life/Memory/Instructions.md`):**
    *   This file is the single source of truth for high-level behavior rules (e.g., "Remind me 10 min before deadlines," "Use sarcastic tone," "Always schedule a 15-min buffer after meetings").
    *   It also stores personality quiz results/settings and long-term stable preferences (default schedules, lunch breaks, work hour boundaries, communication style tweaks).
    *   The system regularly ingests this file. New instructions are merged; the system attempts to auto-resolve conflicting instructions or flags them for user review.
*   **Other `Life Folder` files** (`User_Info.gsheet`, `Long-Term Goals/`, etc.) provide further context for the AI.

## 6. Accessing Information: The Life Folder (Reiteration)

*   Users can browse their "Life Folder" which includes:
    *   `Memory/Instructions.md`: Personality, explicit instructions, preferences, master rules.
    *   `Memory/User_Info.gsheet`: Structured user data (Projects, Opinions, Key Relationships, etc.).
    *   `Inbox/`: For quickly captured, unstructured notes.
    *   `Long-Term Goals/`: For goal setting and review.
    *   Project-specific folders/documents.

## Overall Feeling

The user should feel like they have an intelligent, adaptive partner that understands their unique way of working and communicating. The AI's ability to "get them" is paramount, making task management and scheduling feel less like a chore and more like a supportive, evolving conversation. The experience is designed to reduce mental load, enhance focus, and provide a sense of control and motivation through a dynamic, back-and-forth planning process. 