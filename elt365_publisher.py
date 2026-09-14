#!/usr/bin/env python3
"""ELT365 Months 6 & 7 publisher — posts lessons as drafts to sourovdeb.com.

Usage: python3 elt365_publisher.py
Endpoint: POST https://sourovdeb.com/wp-json/sourov/v1/ai-post
Auth header: X-Sourov-Key

Note: API key is stored as an environment variable or GAS Script Property.
Do not hardcode the key in files committed to a public repository.
"""

import urllib.request
import json
import time
import os

ENDPOINT = "https://sourovdeb.com/wp-json/sourov/v1/ai-post"
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
    print(f"Publishing {len(ALL_LESSONS)} ELT365 lessons as drafts...\n")
    ok_count = 0
    for i, lesson in enumerate(ALL_LESSONS):
        day, title, idea, example, try_task, tags, meta, seo = lesson
        full_title = f"ELT365 · Day {day:03d} — {title}"
        content = build_html(idea, example, try_task)
        status, body = post_lesson(full_title, content, tags, meta, seo)
        ok = status in (200, 201)
        ok_count += ok
        print(f"  {'✓' if ok else '✗'} D{day:03d} (HTTP {status}): {title[:60]}")
        if not ok:
            print(f"    {body[:120]}")
        if i < len(ALL_LESSONS) - 1:
            time.sleep(0.4)
    print(f"\nDone: {ok_count}/{len(ALL_LESSONS)} published.")


if __name__ == "__main__":
    main()
