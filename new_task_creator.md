## New Task Creator Algorithm

* **User Intent Recognition**: Detect when the user expresses a need to add a task (e.g., “Bring paperwork to the office before 5:00”).
* **Project Tagging**: Automatically assign relevant project tags (e.g., `work`, `errand`).
* **Title & Description Generation**: Generate a concise title (e.g., “Deliver papers to office”) and a detailed description based on the user’s input.

## Information Extraction & Inference

* **Explicit vs. Inferred Data**:

  * **Use Provided Info**: If the user specifies duration, importance, or deadline hardness, use it directly.
  * **Historical Inference**: If missing, search past similar tasks to infer:

    * Duration
    * Dependencies
    * Priority level
    * Deadline hardness
* **No Historical Match**: Prompt user for any missing information when no similar task exists.

## Historical Task Analysis

* **Similarity Search**: Query the database for tasks with matching descriptions or tags.
* **Data Retrieval**: Extract metrics from past tasks:

  * How long they took
  * Dependencies
  * Priority evolution
  * Deadline strictness
* **Estimation**: Use historical metrics to estimate current task parameters.

## Task Breakdown & Dependencies

* **Decomposition Detection**: Identify tasks that logically split into sub-tasks (e.g., `grocery shopping`).
* **User Prompt on First Encounter**: Offer to split into subtasks (e.g., `Create shopping list` → `Do grocery shopping`).
* **Dependency Recording**: Store subtask dependencies for future auto-breakdown.
* **Auto-Subdivision**: On subsequent similar requests, auto-generate subtasks using stored dependencies without prompting.

## Confirmation UI

* **Review Screen**: Display the suggested task(s) with:

  * **Confirm** button (auto-press after 10–20 seconds)
  * **Edit** button for manual adjustments

## Scheduling Decision Engine

* **Immediate Scheduling Criteria**:

  * Hard deadlines
  * High-priority tasks
  * Insufficient dependencies (requires immediate slot)
* **Delay Criteria**:

  * Many dependencies indicating prolonged work
  * Lower urgency

## Scheduling Algorithm

* **Historical Scheduling Patterns**: Use time-of-day data from past occurrences.
* **Errand Grouping**: Slot errands at beginning/end of other errands when possible.
* **Conflict Resolution**:

  * Bump lower-priority tasks into adjacent slots
  * Respect hard deadlines over flexible tasks
* **User Prompt**: If no viable slot, explain conflict and suggest alternatives.
* **Scheduling Confirmation UI**: Auto-confirm after 15 seconds; Edit button offers up to three specific options.

### Morning Planning & Freestyle List

* **Unscheduled Tasks**: Surface during daily morning planning session.
* **Freestyle List**: Provide a catch-all list for on-the-fly task addition and review.


