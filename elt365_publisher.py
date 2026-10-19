#!/usr/bin/env python3
"""ELT365 Months 6 & 7 publisher — posts lessons as drafts to sourovdeb.com.

Usage: python3 elt365_publisher.py
Endpoint: POST https://sourovdeb.com/wp-json/sourov/v1/ai-post
Auth header: X-Sourov-Key

Note: API key is stored as an environment variable or GAS Script Property.
Do not hardcode the key in files committed to a public repository.

Duplicate guard (added 2026-10-19, after the months 6-7 re-import incident
that put up to 11 copies of the same lesson day on the live site):
- Before publishing, the script fetches existing post titles: published
  posts via the public REST API, drafts via the authenticated /scheduled
  endpoint.
- A lesson is skipped if its exact title already exists, or if any existing
  ELT365 post already uses the same day number. Re-imports used different
  wording for the same day, so the day-number check is the real protection.
- The guard FAILS CLOSED: if the existing-post check cannot be completed,
  the run aborts and nothing is published.
"""

import urllib.request
import urllib.error
import json
import re
import time
import os

ENDPOINT = "https://sourovdeb.com/wp-json/sourov/v1/ai-post"
SCHEDULED_ENDPOINT = "https://sourovdeb.com/wp-json/sourov/v1/scheduled"
REST_POSTS = "https://sourovdeb.com/wp-json/wp/v2/posts"
API_KEY = os.environ.get("SOUROV_WP_KEY", "")
DISCLAIMER = (
    "<p><em>Independent project; not affiliated with, endorsed by, or accredited by "
    "Cambridge University Press &amp; Assessment. Confers no qualification.</em></p>"
)


def build_html(idea, example, try_task):
    return (
        f"<p><strong>Idea &#8212;</strong> {idea}</p>"
        f"<p><strong>Example &#8212;</strong> {example}</p>"
        f"<p><strong>Try &#8212;</strong> {try_task}</p>"
        f"{DISCLAIMER}"
    )


def _http_get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def _elt365_day(title):
    """Return the ELT365 day number of a title, or None."""
    if not title or "elt365" not in title.lower():
        return None
    m = re.search(r"\bDay\s?(\d{1,3})\b", title, re.IGNORECASE)
    return int(m.group(1)) if m else None


def existing_posts():
    """Return (titles, days, check_ok). check_ok=False means ABORT the run."""
    titles, days = set(), set()
    # 1) Published posts — public REST API, paginate everything.
    try:
        page = 1
        while page <= 20:
            body = _http_get(f"{REST_POSTS}?per_page=100&page={page}&_fields=id,title")
            batch = json.loads(body)
            if not batch:
                break
            for post in batch:
                rendered = (post.get("title") or {}).get("rendered", "")
                titles.add(rendered.strip().lower())
                day = _elt365_day(rendered)
                if day is not None:
                    days.add(day)
            if len(batch) < 100:
                break
            page += 1
    except Exception as e:
        print(f"  X Duplicate check failed (published posts): {e}")
        return set(), set(), False
    # 2) Drafts — authenticated scheduled endpoint.
    if API_KEY:
        try:
            body = _http_get(SCHEDULED_ENDPOINT, headers={"X-Sourov-Key": API_KEY})
            for post in json.loads(body):
                rendered = post.get("title") if isinstance(post, dict) else str(post)
                rendered = rendered if isinstance(rendered, str) else ""
                titles.add(rendered.strip().lower())
                day = _elt365_day(rendered)
                if day is not None:
                    days.add(day)
        except Exception as e:
            print(f"  X Duplicate check failed (drafts): {e}")
            return set(), set(), False
    return titles, days, True


def post_lesson(title, content, tags, meta, seo_title):
    payload = {
        "title": title,
        "content": content,
        "status": "draft",
        "category": "English Teaching",
        "tags": tags,
        "meta_description": meta,
        "seo_title": seo_title,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"X-Sourov-Key": API_KEY, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except Exception as e:
        return 0, str(e)


# Lesson data: (day, title, idea, example, try_task, tags, meta, seo_title)
# See ELT365_M06_*.md and ELT365_M07_*.md for full lesson text.
ALL_LESSONS = []
# Add lessons here in the same tuple format before running.


def main():
    if not API_KEY:
        print("Set SOUROV_WP_KEY environment variable before running.")
        return
    titles, used_days, check_ok = existing_posts()
    if not check_ok:
        print("ABORT: could not verify existing posts. Nothing was published.")
        print("Fix duplicate-check connectivity, then re-run.")
        return
    print(f"Duplicate check: {len(titles)} existing titles, "
          f"{len(used_days)} ELT365 day numbers already used.")
    print(f"Publishing {len(ALL_LESSONS)} ELT365 lessons as drafts...\n")
    ok_count = 0
    skip_count = 0
    for i, lesson in enumerate(ALL_LESSONS):
        day, title, idea, example, try_task, tags, meta, seo = lesson
        full_title = f"ELT365 · Day {day:03d} — {title}"
        if full_title.strip().lower() in titles:
            print(f"  SKIP D{day:03d}: exact title already exists")
            skip_count += 1
            continue
        if day in used_days:
            print(f"  SKIP D{day:03d}: day number already imported (different wording)")
            skip_count += 1
            continue
        content = build_html(idea, example, try_task)
        status, body = post_lesson(full_title, content, tags, meta, seo)
        posted = status in (200, 201)
        ok_count += posted
        print(f"  {'OK' if posted else 'FAIL'} D{day:03d} (HTTP {status}): {title[:60]}")
        if not posted:
            print(f"    {body[:120]}")
        if i < len(ALL_LESSONS) - 1:
            time.sleep(0.4)
    print(f"\nDone: {ok_count}/{len(ALL_LESSONS)} published, {skip_count} skipped by duplicate guard.")


if __name__ == "__main__":
    main()
