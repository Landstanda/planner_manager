# Book‑Builder

A mobile‑first web app and workflow toolkit that turns your big, nested outline into a polished manuscript.
It combines **Next.js + Tailwind** for the UI, **n8n** for orchestration, **Supabase** for the data layer, and **Fly.io** for hosting. It leverages an advanced LLM like **GPT-4.1** (or similar models with large context windows, e.g., 1 million tokens) for its intelligence, offering a blend of power, cost-effectiveness, and smart content generation.

---

## What It Does

| Phase                        | Purpose                                                                                            | Key Workflow                 |
| ---------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------- |
| **1. World‑Building**        | Capture facts about characters, lore, timelines. Extract triples & store them for semantic recall. | `/webhook/world-builder`     |
| **2. Multi‑Level Outlining** | Nest writing‑formula steps (Hero's Journey, etc.) 3–4 layers deep.                                 | `/webhook/outline-generator` |
| **3. Draft Writing**         | Generate, iterate, and commit prose for each section.                                              | `/webhook/draft-generator`   |

Each phase is a standalone n8n workflow with its own webhook, so you can toggle between them in the mobile UI.

---

## 🖼️ High‑Level Architecture

```
Mobile PWA (Next.js)  <----->  Supabase Edge Functions  <----->  Supabase Postgres
                                       |                                |  (pgvector, ltree)
                                       |                                |
                             +---------------------+
                             |  n8n (Fly.io)       |
                             |  – World Builder    |
                             |  – Outliner         |
                             |  – Draft Writer     |
                             +---------------------+
                                       |
                                       |
                                 LLM (GPT-4.1)
```

### Front End

* **Next.js / React** – routes & API proxies.
* **Tailwind CSS** – utility‑first, mobile‑first.
* **Headless UI + react‑swipeable** – swipe drawers for TOC & settings.
* **React Query** – caching & realtime updates.

### Orchestration

* **n8n** – three modular workflows (one per phase) exposed via webhooks.

### Data Layer

* **Supabase Postgres** – single source‑of‑truth with pgvector + ltree.
* **Realtime** – push section updates to the UI.
* **Auth** – row‑level security.

### Hosting

* **Fly.io** – Dockerized deployments for both Next.js and n8n.

---

## Database Schema (Supabase)

### Core Tables

| Table        | Purpose                       | Highlight Columns                                                                                                                                                    |
| ------------ | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sections`   | Outline & manuscript tree     | `id`, `parent_id`, `position` (ltree), `title`, `is_title` (bool), `content_type` (`outline`\|`draft`\|`final`), `formula_layer`, `text`, `outline_notes`              |
| `formulas`   | Writing‑cycle templates       | `id`, `name`, `mood_id`, `template`, `default_length`, `default_temp`                                                                                                  |
| `moods`      | Voice & style snippets        | `id`, `label`, `prompt_snippet`                                                                                                                                      |
| `entities`   | Characters / objects / places | `id`, `type`, `name`, `attributes` (jsonb), `biography`                                                                                                              |
| `facts`      | RDF‑style triples             | `id`, `subject_id`, `predicate`, `object`, `started_at`, `ended_at`, `context_section`                                                                               |
| `embeddings` | Semantic search               | `id`, `section_id`, `vector` (pgvector)                                                                                                                              |

### Indexes & Extensions

* **`ltree`** on `sections.position` – fast subtree queries.
* **Full‑text index** on `sections.text`.
* **`pgvector`** on `embeddings.vector` for similarity search.
* **JSONB GIN** on `entities.attributes`.

---

## n8n Workflows

### 1. World‑Building (`/webhook/world-builder`)

1. **Webhook** → Function (normalize) → Airtable/Supabase upsert `entities`
2. **HTTP Request** to LLM → extract triples & attributes
3. **SplitInBatches** → insert into `facts`
4. **Respond** with JSON form for UI pre‑fill

### 2. Outline Generator (`/webhook/outline-generator`)

1. Fetch current context (parent section)
2. For each formula step: **HTTP → LLM** to get sub‑outline (requires very detailed prompts).
3. Merge & write into `sections` (content\_type=`outline`)
4. Return updated outline JSON

### 3. Draft Writer (`/webhook/draft-generator`)

1. Build prompt from `sections`, `moods`, `formulas` (requires very detailed prompts).
2. **HTTP → LLM** generate prose.
3. Engage in an iterative refinement process with the user, allowing for multiple rounds of feedback and LLM-driven revisions (individual revisions are not stored).
4. Commit final text (`content_type=final`) + Git mirror (optional).
5. Slack/email notification

---

## Getting Started

### Prerequisites

* Node  >=  18
* Docker  &  Fly  CLI
* Supabase account (free tier OK)
* n8n cloud or self‑host

### Environment Variables

```bash
# /.env
SUPABASE_URL=…
SUPABASE_ANON_KEY=…
N8N_WEBHOOK_URL=https://<flyapp>.fly.dev/webhook/
OPENAI_API_KEY=…
```

### Local Dev

```bash
yarn install
supabase start    # spin up local Postgres
npx supabase db push   # apply schema
npx supabase gen types typescript --local
yarn dev          # next dev on http://localhost:3000
```

### Deploy

```bash
fly launch        # generates fly.toml
fly deploy        # pushes Next.js
fly scale vm shared-cpu-1x
```

For n8n, either:

* Use n8n Cloud → set `N8N_WEBHOOK_URL` accordingly, or
* `fly launch` a second app with the n8n Docker image.

---

##  Development Tips

* **Cursor  AI**: prompt it to scaffold React components & API routes.
* **Detailed Prompts**: Crafting highly detailed and specific prompts for the LLM is crucial for achieving desired outputs in all phases.
* **Branch‑per‑chapter** workflow: use Supabase RLS + Git history to prevent merge pain.
* **Error Handling**: every AI call in n8n gets an error branch → Slack.
* **Testing**: Thoroughly test workflows, potentially using mock LLM responses for consistency and focusing on data integrity within Supabase.

---

## Roadmap / Nice‑To‑Haves

* [ ] Visual timeline Gantt chart for facts & events
* [ ] Embedding‑powered "similar scene" suggestions

---

## 📄 License

MIT ©  Jeff Steele
