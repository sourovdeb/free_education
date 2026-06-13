#!/usr/bin/env python3
"""
ELT365 batch WordPress publisher.
Usage: python3 wp_publisher_elt365.py
Posts Days 152-212 (Months 6 & 7) as drafts to sourovdeb.com.
Credential: X-Sourov-Key from .env or hardcoded for local use only.
"""
import json
import urllib.request
import urllib.error
import time
import os

WP_ENDPOINT = "https://sourovdeb.com/wp-json/sourov/v1/ai-post"
WP_KEY = os.environ.get("SOUROV_KEY", "")
DISCLAIMER = (
    "<hr><p><em>Independent project; not affiliated with, endorsed by, or accredited "
    "by Cambridge University Press &amp; Assessment. Confers no qualification.</em></p>"
)


def make_html(idea, example, try_task):
    return (
        f"<p><strong>Idea &mdash;</strong> {idea}</p>\n"
        f"<p><strong>Example &mdash;</strong> {example}</p>\n"
        f"<p><strong>Try &mdash;</strong> {try_task}</p>\n"
        f"{DISCLAIMER}"
    )


def wp_post(payload):
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
