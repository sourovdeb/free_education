# Claude Code Workflow: free_education

## Overview
This repository contains free educational content that syncs to sourovdeb.com.

## Content Sync to WordPress

### How it works
- **Script**: `sync_verification.py` (pairs with my_professional_documents)
- **Auth**: WordPress REST API with `X-Sourov-Key` header
- **Endpoint**: `https://sourovdeb.com/wp-json/sourov/v1/ai-post`
- **Output**: Draft posts on WordPress (never auto-published)
- **Dedup**: Checks title against existing posts
- **Categories**: Mental Health, ELT Masterclass, English Teaching, Philosophy, Photography, Software, DXO, Learn AI in Mistral Studio

### API contract
```python
POST /wp-json/sourov/v1/ai-post
Authorization: X-Sourov-Key: [key]
{
    "title": "string",
    "content": "string",
    "status": "draft",
    "category": "string",
    "tags": ["array"]  # MUST be JSON array, not string
}
```

**Critical bug fixed (2026-07-19)**: Tags must be JSON array, not string.

### Content included
- `elt365_lessons/` — 365 daily English lessons
- `routines/` — educational routines and frameworks
  - `01_elt365_lessons_routine/` — ELT lesson lessons
  - `02_python_toolkit_routine/` — Python learning materials
  - `03_human_nature_routine/` — Psychology/behavior primer
- Open PRs with lesson batches and audit routines

### Known issues
1. **Many ELT lessons already published** — lesson files carry explicit WordPress post IDs in frontmatter. Don't re-push.
2. **Shallow dedup**: Recommend WordPress post audit.
3. **No delete endpoint**: Manual WP admin cleanup required.

### Session history
- **2026-07-19 09:40 UTC**: First aggressive sync, pushed 9 mental-health audits
- **2026-07-19 ongoing**: Pushing additional lesson content
