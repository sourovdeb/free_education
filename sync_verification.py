#!/usr/bin/env python3
"""
Content sync verification & deduplication script.
Runs hourly to push categorized content to sourovdeb.com without duplicates.
"""

import json
import os
import requests
from pathlib import Path
from collections import defaultdict
from datetime import datetime

API_KEY = "0767044896thevenet_"
WP_URL = "https://sourovdeb.com"
WP_ENDPOINT = f"{WP_URL}/wp-json/sourov/v1"

CATEGORIES = {
    "Mental Health": ["therapy", "wellbeing", "trauma", "mental health", "psychology"],
    "ELT Masterclass": ["elt365", "masterclass", "teaching", "english language"],
    "English Teaching": ["celta", "teaching", "english", "grammar", "phonology"],
    "Philosophy": ["philosophy", "stoic", "ethics", "metaphysics"],
    "Photography": ["photography", "photo", "visual", "image", "dxo"],
    "Software": ["code", "programming", "software", "automation", "script"],
    "DXO": ["dxo", "image", "photo", "editing"],
    "Learn AI in Mistral Studio": ["ai", "mistral", "llm", "learning"],
}

def get_existing_titles():
    """Fetch titles of all draft/scheduled posts on WordPress."""
    try:
        resp = requests.get(
            f"{WP_ENDPOINT}/scheduled",
            headers={"X-Sourov-Key": API_KEY},
            timeout=10
        )
        if resp.status_code == 200:
            posts = resp.json()
            return {post['title'] for post in posts}
    except Exception as e:
        print(f"⚠ Could not fetch existing posts: {e}")
    return set()

def categorize_content(filepath, content):
    """Infer category from file path and content."""
    path_str = str(filepath).lower()
    content_str = content[:500].lower()

    for category, keywords in CATEGORIES.items():
        if any(kw in path_str or kw in content_str for kw in keywords):
            return category
    return "Software"  # default fallback

def scan_repositories():
    """Scan documented content directories in my_professional_documents and free_education
    for publishable content. Only the directories CLAUDE.md lists as sync sources are
    scanned — repo docs (READMEs, guides, CLAUDE.md) and personal files (cover letters,
    job lists, credentials) are never candidates."""
    items = []

    # Skip sensitive/archive directories
    skip_patterns = {
        "archives", "_archive", "extracted", "chat-history",
        "Biography_and_Medical", "Legal_Documents", "therapy_and_wellbeing",
        "Story_of_Sourov", ".git", "__pycache__", "node_modules"
    }

    repo_include_dirs = {
        Path("/home/user/my_professional_documents"): [
            "blog_and_essays", "daily_essays", "posts", "guides",
            "AI_Lessons", "AI_Term_Lessons", "CELTA_Teaching_Materials",
            "presentations", "Presentations", "Growth_Hub", "initiatives",
            "weekly-briefings",
        ],
        Path("/home/user/free_education"): [
            "elt365_lessons", "routines",
        ],
    }

    for repo_path, include_dirs in repo_include_dirs.items():
        if not repo_path.exists():
            continue

        candidate_files = []
        for include_dir in include_dirs:
            candidate_files.extend((repo_path / include_dir).glob("**/*.md"))

        for filepath in candidate_files:
            # Skip if in skip patterns
            if any(skip in str(filepath) for skip in skip_patterns):
                continue

            # Skip reusable templates - not publishable content
            if "template" in filepath.stem.lower():
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Skip files already published/synced (carry explicit WP post IDs)
                if "wp id" in content[:1000].lower() or "wp status" in content[:1000].lower():
                    continue

                # Use filename as title if frontmatter not present
                title = filepath.stem.replace('_', ' ').replace('-', ' ').title()
                category = categorize_content(filepath, content)

                items.append({
                    "title": title,
                    "content": content[:2000],  # excerpt
                    "filepath": str(filepath),
                    "category": category,
                    "word_count": len(content.split()),
                })
            except Exception as e:
                print(f"⚠ Error reading {filepath}: {e}")

    return items

def push_draft(title, content, category):
    """Create a draft post on WordPress."""
    try:
        resp = requests.post(
            f"{WP_ENDPOINT}/ai-post",
            json={
                "title": title,
                "content": content,
                "status": "draft",
                "category": category,
                "tags": [category.lower().replace(" ", "_")],
            },
            headers={"X-Sourov-Key": API_KEY},
            timeout=15
        )
        if resp.status_code in [200, 201]:
            data = resp.json()
            return data.get('id')
    except Exception as e:
        print(f"⚠ Could not push '{title}': {e}")
    return None

def main():
    print(f"\n=== CONTENT SYNC VERIFICATION {datetime.now().isoformat()} ===\n")

    # Get existing titles to avoid duplicates
    existing = get_existing_titles()
    print(f"📊 Found {len(existing)} existing posts on WordPress")

    # Scan repos for content
    all_items = scan_repositories()
    print(f"📂 Scanned repos: found {len(all_items)} candidate items")

    # Filter out duplicates and categorize
    new_items = [item for item in all_items if item['title'] not in existing]
    print(f"✓ After dedup: {len(new_items)} new items to push")

    # Group by category
    by_category = defaultdict(list)
    for item in new_items:
        by_category[item['category']].append(item)

    print(f"\n📋 Items by category:")
    for cat in sorted(by_category.keys()):
        print(f"   {cat}: {len(by_category[cat])}")

    # Push drafts (max 5 per run to avoid overwhelming the queue)
    pushed = 0
    for item in new_items[:5]:
        post_id = push_draft(item['title'], item['content'], item['category'])
        if post_id:
            print(f"✓ Pushed: {item['title']} → ID {post_id}")
            pushed += 1

    if pushed < len(new_items):
        print(f"\n⏳ Queued {len(new_items) - pushed} more items for next run")

    print(f"\n=== SYNC COMPLETE ===\n")

if __name__ == '__main__':
    main()
