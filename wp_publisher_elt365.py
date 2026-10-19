#!/usr/bin/env python3
"""
ELT365 batch WordPress publisher.
Usage: python3 wp_publisher_elt365.py
Posts Days 152-212 (Months 6 & 7) as drafts to sourovdeb.com.
Credential: X-Sourov-Key from .env or hardcoded for local use only.

Duplicate guard (added 2026-10-19, after the months 6-7 re-import incident):
wp_post() refuses to create a post if the exact title already exists or if
any existing ELT365 post already uses the same day number. The check FAILS
CLOSED: if the existing-post lookup cannot run, nothing is posted.
"""
import json
import re
import urllib.request
import urllib.error
import time
import os

WP_ENDPOINT = "https://sourovdeb.com/wp-json/sourov/v1/ai-post"
SCHEDULED_ENDPOINT = "https://sourovdeb.com/wp-json/sourov/v1/scheduled"
REST_POSTS = "https://sourovdeb.com/wp-json/wp/v2/posts"
WP_KEY = os.environ.get("SOUROV_KEY", "")
DISCLAIMER = (
    "<hr><p><em>Independent project; not affiliated with, endorsed by, or accredited "
    "by Cambridge University Press &amp; Assessment. Confers no qualification.</em></p>"
)

_existing_cache = None


def _http_get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode("utf-8")


def _elt365_day(title):
    if not title or "elt365" not in title.lower():
        return None
    m = re.search(r"\bDay\s?(\d{1,3})\b", title, re.IGNORECASE)
    return int(m.group(1)) if m else None


def _existing_titles_and_days():
    """Fetch (titles, days, ok) once per run. ok=False means ABORT."""
    global _existing_cache
    if _existing_cache is not None:
        return _existing_cache
    titles, days = set(), set()
    ok = True
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
    except Exception as exc:
        print(f"Duplicate check failed (published posts): {exc}")
        ok = False
    if ok and WP_KEY:
        try:
            body = _http_get(SCHEDULED_ENDPOINT, headers={"X-Sourov-Key": WP_KEY})
            for post in json.loads(body):
                rendered = post.get("title") if isinstance(post, dict) else str(post)
                rendered = rendered if isinstance(rendered, str) else ""
                titles.add(rendered.strip().lower())
                day = _elt365_day(rendered)
                if day is not None:
                    days.add(day)
        except Exception as exc:
            print(f"Duplicate check failed (drafts): {exc}")
            ok = False
    _existing_cache = (titles, days, ok)
    return _existing_cache


def make_html(idea, example, try_task):
    return (
        f"<p><strong>Idea &mdash;</strong> {idea}</p>\n"
        f"<p><strong>Example &mdash;</strong> {example}</p>\n"
        f"<p><strong>Try &mdash;</strong> {try_task}</p>\n"
        f"{DISCLAIMER}"
    )


def wp_post(payload):
    # Fail-closed duplicate guard: refuse to publish if we cannot verify.
    titles, days, ok = _existing_titles_and_days()
    if not ok:
        return {"error": "ABORT: duplicate check unavailable; refusing to publish (fail-closed)"}
    title = payload.get("title", "")
    key = title.strip().lower()
    if key in titles:
        return {"skipped": f"exact title already exists: {title}"}
    day = _elt365_day(title)
    if day is not None and day in days:
        return {"skipped": f"day {day} already imported: {title}"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        WP_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json", "X-Sourov-Key": WP_KEY},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}", "body": body}
    except Exception as exc:
        return {"error": str(exc)}


def build_payload(day, title_text, idea, example, try_task, tag):
    full_title = f"ELT365 · Day {day} — {title_text}"
    content = make_html(idea, example, try_task)
    meta = f"ELT365 Day {day}: {title_text} — a 5-minute teacher-training micro-lesson on {tag}."[:155]
    seo_title = f"ELT365 Day {day} — {title_text} | Sourov Deb"[:60]
    return {
        "title": full_title,
        "content": content,
        "status": "draft",
        "category": "English Teaching",
        "tags": f"ELT365, teacher training, ELT, {tag}",
        "meta_description": meta,
        "seo_title": seo_title,
    }


if __name__ == "__main__":
    if not WP_KEY:
        print("Set SOUROV_KEY environment variable before running.")
        exit(1)
    print("Run publish_elt365.py (which includes lesson data) instead.")
