#!/usr/bin/env python3
"""
ELT365 + Mixed Lessons — batch draft publisher for sourovdeb.com
Posts 50 bite-size (5-min) lessons as draft to the custom WP endpoint.
Disclaimer required on every post per SKILL_elt365_micro_lesson_writer §1.3
"""

import urllib.request
import urllib.error
import json
import time
import sys

WP_ENDPOINT = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
WP_KEY = "0767044896thevenet_"

DISCLAIMER = (
    "<p><em>Independent project; not affiliated with, endorsed by, or accredited by "
    "Cambridge University Press &amp; Assessment. Confers no qualification.</em></p>"
)

def wrap(idea, example, try_task, disclaimer=True):
    body = (
        f"<p><strong>Idea —</strong> {idea}</p>\n"
        f"<p><strong>Example —</strong> {example}</p>\n"
        f"<p><strong>Try —</strong> {try_task}</p>"
    )
    if disclaimer:
        body += "\n<hr>\n" + DISCLAIMER
    return body

def wrap_pro(idea, practice, action):
    return (
        f"<p><strong>The idea —</strong> {idea}</p>\n"
        f"<p><strong>In practice —</strong> {practice}</p>\n"
        f"<p><strong>One-minute task —</strong> {action}</p>"
    )

# See elt365_lessons/ELT365_M06_Receptive_Skills_D152-181.md for lesson content
# Lessons are defined inline in the published script; see that file for markdown source.

def post_lesson(lesson, idx, total):
    payload = {
        "title": lesson["title"],
        "content": lesson["content"],
        "status": "draft",
        "category": lesson["category"],
        "tags": lesson["tags"],
        "meta_description": lesson["meta_description"],
        "seo_title": lesson["seo_title"],
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        WP_ENDPOINT,
        data=data,
        headers={
            "X-Sourov-Key": WP_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            print(f"[{idx:02d}/{total}] OK  — {lesson['title'][:70]}")
            try:
                parsed = json.loads(body)
                post_id = parsed.get("id") or parsed.get("post_id") or "?"
                print(f"          post_id={post_id}")
                return {"ok": True, "id": post_id, "title": lesson["title"]}
            except Exception:
                print(f"          response: {body[:120]}")
                return {"ok": True, "id": "?", "title": lesson["title"]}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:200]
        print(f"[{idx:02d}/{total}] ERR — {lesson['title'][:70]}")
        print(f"          HTTP {e.code}: {body}")
        return {"ok": False, "error": f"HTTP {e.code}: {body}", "title": lesson["title"]}
    except Exception as exc:
        print(f"[{idx:02d}/{total}] ERR — {lesson['title'][:70]}: {exc}")
        return {"ok": False, "error": str(exc), "title": lesson["title"]}


def main(lessons):
    total = len(lessons)
    print(f"Publishing {total} lessons as draft to {WP_ENDPOINT}\n")
    results = []
    for i, lesson in enumerate(lessons, start=1):
        result = post_lesson(lesson, i, total)
        results.append(result)
        time.sleep(0.8)

    ok  = [r for r in results if r["ok"]]
    err = [r for r in results if not r["ok"]]
    print(f"\n--- Done: {len(ok)} posted, {len(err)} failed ---")
    if err:
        print("Failures:")
        for r in err:
            print(f"  {r['title'][:60]} — {r['error'][:100]}")
    return 0 if not err else 1
