# Front-End Details: Planner-Manager App

This document describes the visual layout, feel, and key UI components of the Planner-Manager App, complementing the existing Front-End UI section in the README.md.

## 1. Overall Aesthetic & Feel

*   **Clean, Modern, and Uncluttered:** The UI should prioritize clarity and ease of use, avoiding visual noise. Think minimalist but not stark.
*   **Personalized Vibe:** While the core structure is consistent, subtle cues (e.g., color accents, avatar styles for the AI, perhaps even minor layout adjustments based on information density preference) could adapt slightly based on the user's chosen personality/tone for the AI and preferences stored in the `user_llm_instructions` and `user_personality_profile` tables in Supabase.
*   **Responsive & Fast:** The application must feel snappy and responsive across devices (desktop, tablet, mobile web) as a PWA.
*   **Focus on Readability:** Clear typography and good contrast are essential for comfortable long-term use.

## 2. Core Navigation & Layout (Reiteration and Expansion)

*   **Three Swipeable Panels (as per README):**
    *   **To-Do List View:** Displays tasks, filterable by status, project, priority. Clear visual cues for deadlines and progress. Ability to quick-add tasks.
    *   **Calendar / Daily Schedule View:** This is a key interactive view.
        *   Integrates with Google Calendar (events are distinctly styled).
        *   Primarily displays the AI-generated and user-confirmed time-blocked schedule for the day, with clear project labels on each block.
        *   Shows persistent preference blocks (e.g., "Lunch," "No Meetings Before 10 AM" if set in user preferences) visually distinct or as reserved space.
        *   Offers day and week views. Month view might be a simpler overview.
        *   Supports direct manipulation (drag-and-drop to reschedule, drag to adjust duration) for time blocks, with changes confirmed via AI chat or a simple modal.
    *   **Life Folder View:** A simple file-explorer-like interface to navigate the Google Drive "Life Folder" (Inbox, Long-Term Goals, Projects, etc.). Allows for quick viewing and potentially basic editing of notes and documents. Note: Core user preferences and personality settings are now stored in Supabase tables rather than files.
*   **Bottom Navigation Bar (as per README):**
    *   Three clear icons for switching between To-Do, Calendar/Schedule, and Life Folder views.
    *   Active view is clearly indicated.
*   **Persistent Chat Input Area:**
    *   Located at the bottom of the screen, always accessible (styled as "Ask me stuff…" input field).
    *   Tapping/clicking it expands into a GPT-style chat bubble overlay for interacting with the AI (task input, queries, schedule adjustments, feedback on AI tone, etc.).
    *   The overlay can be swiped down or dismissed to return to the previous panel view.

## 3. Key UI Components & Interactions

*   **Chat Interface (Overlay):**
    *   Clean, conversational bubbles.
    *   Supports text input; voice input icon (mic) for speech-to-text.
    *   AI responses are clearly differentiated from user inputs, perhaps with a subtle AI avatar reflecting the chosen personality.
    *   May include interactive elements within the chat (e.g., buttons for "Accept Schedule Change," "Snooze Reminder," quick replies like "Yes/No/Later").
*   **Personality On-Ramp Quiz / Settings:**
    *   Quiz: A series of engaging, visually clean multiple-choice questions with a progress indicator.
    *   Results page introduces their "AI assistant persona" and explains how personality settings affect AI behavior.
    *   Quiz results are stored in the `user_personality_profile` table in Supabase for AI personalization.
    *   Direct settings for users who skip the quiz or want to manually override personality archetype, motivation style, and communication tone.
*   **Task Items (in To-Do List View & potentially within Calendar Blocks):**
    *   Clear display of task name, due date/time, priority (e.g., color-coded dots/tags), project association.
    *   Checkboxes for marking tasks complete (syncs with Supabase tasks table).
    *   Expandable area for task description, subtasks, and dependencies.
*   **Daily Plan / Visual Schedule Interface (Calendar View):**
    *   Visual representation of time blocks for tasks and calendar events, color-coded by project or type (work, personal - user configurable preference stored in Supabase).
    *   Clear labels on blocks.
    *   Drag-and-drop rescheduling and duration adjustments.
    *   Visual indication of conflicts if a proposed change leads to one, with AI suggesting resolutions in chat.
*   **Settings Menu (Top Right):**
    *   Access to:
        *   Profile/Personality Quiz Retake or Manual Adjustment.
        *   Management style overrides (updates `user_llm_instructions` table in Supabase).
        *   Notification preferences (cadence, type).
        *   Google Account connection status.
        *   User preference editor for common settings like lunch time, work hours, check-in frequency.
        *   Future Add-On toggles.
*   **Notifications/Nudges:**
    *   Delivered as system notifications (if PWA permissions granted) and/or subtle in-app banners/badges.
    *   Content, tone, and frequency are driven by the AI's personality profile and user instructions stored in Supabase.

## 4. Visual Language Considerations

*   **Icons:** Consistent and intuitive icon set.
*   **Color Palette:** A primary palette that is calming and focus-oriented. Accent colors used meaningfully for priorities, project tags, AI persona highlights, and calendar event types. The orange/blue/lavender project color-coding system (as detailed in `UI_Style_Guide.md`) allows for user-configurable themes based on personality settings.
*   **Typography:** A readable sans-serif font family (Inter) with clear hierarchy as specified in `UI_Style_Guide.md`.
*   **Micro-interactions:** Subtle animations for feedback (e.g., task completion, schedule adjustment confirmation), state changes, and enhancing the feeling of a responsive system.

## 5. "Feels Like" Adjectives

Intelligent, adaptive, personal, organized, calm, supportive, efficient, understanding, intuitive, **anticipatory, conversational.**
The app should feel less like a rigid tool and more like a responsive, understanding assistant that learns and adapts through a continuous back-and-forth dialogue. 