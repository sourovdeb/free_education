#!/usr/bin/env python3
"""Bite-Size English Lessons — Generator for sourovdeb.com WordPress

Personal note:
  Lessons draw from 18 years of hospitality management in Sydney,
  CELTA teacher training in Landerneau (2026), and life in La Reunion.

Usage:
  export WP_KEY=your_key_here
  python3 bite_size_lessons_generator.py

Disclaimer:
  Independent project; not affiliated with, endorsed by, or accredited
  by Cambridge University Press & Assessment. Confers no qualification.
"""
import os, requests, json, time

API_URL = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
KEY = os.environ.get("WP_KEY", "")  # Set via environment — never hardcode

DISCLAIMER = (
    '<p style="font-size:11px;color:#777;border-top:1px solid #e0e0e0;'
    'padding-top:8px;margin-top:20px;">Independent project — not affiliated with,'
    ' endorsed by, or accredited by Cambridge University Press &amp; Assessment.'
    ' Confers no qualification.</p>'
)

COLORS = {
    "A1": "#43A047", "A2": "#1E88E5",
    "B1": "#FB8C00", "B2": "#8E24AA",
    "C1": "#E53935", "TT": "#546E7A"
}

LABELS = {"TT": "Teacher Training"}


def build_html(l):
    c = COLORS.get(l["level"], "#546E7A")
    lv = LABELS.get(l["level"], l["level"])
    return f"""<section style="font-family:'Segoe UI',Arial,sans-serif;max-width:700px;margin:0 auto;border:1px solid #e0e0e0;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08);">
<div style="background:{c};color:#fff;padding:20px 24px;">
<div style="font-size:12px;opacity:.85;letter-spacing:.5px;">⏱ 5 MINUTES &nbsp;|&nbsp; 📊 {lv} &nbsp;|&nbsp; 📚 {l["focus"].upper()}</div>
<h2 style="margin:8px 0 0;font-size:22px;line-height:1.3;">{l["title"]}</h2>
</div>
<div style="background:#fffde7;border-left:5px solid {c};padding:14px 20px;">
<p style="margin:0;font-size:14px;">🎤 <strong>From the classroom:</strong> {l["note"]}</p>
</div>
<div style="padding:20px 24px;background:#fff;">
<h3 style="color:{c};margin-top:0;font-size:16px;">💡 The Idea</h3>
<p style="line-height:1.7;">{l["concept"]}</p>
<h3 style="color:{c};font-size:16px;">🗣 Example</h3>
<blockquote style="background:#f8f9fa;border-left:4px solid {c};margin:0;padding:12px 16px;border-radius:0 8px 8px 0;font-size:14px;line-height:1.7;">{l["example"]}</blockquote>
<h3 style="color:{c};margin-top:20px;font-size:16px;">🎯 Try It Now!</h3>
<div style="background:#f3f4f6;border-radius:8px;padding:16px 20px;">{l["activity"]}</div>
<details style="margin-top:16px;">
<summary style="cursor:pointer;font-weight:700;color:{c};font-size:14px;">✅ Check Your Answers</summary>
<div style="background:#e8f5e9;border-radius:6px;padding:12px 16px;margin-top:8px;font-size:14px;">{l["answers"]}</div>
</details>
</div>
{DISCLAIMER}
</section>"""


def post_lesson(l):
    if not KEY:
        print("ERROR: Set WP_KEY environment variable first.")
        return None
    payload = {
        "title": l["title"],
        "content": build_html(l),
        "status": "draft",
        "category": l.get("cat", "English Teaching"),
        "tags": l.get("tags", []),
        "meta_description": l.get("meta", l["title"][:155]),
        "seo_title": l.get("seo", l["title"][:60])
    }
    try:
        r = requests.post(API_URL, json=payload,
                          headers={"X-Sourov-Key": KEY,
                                   "Content-Type": "application/json"}, timeout=30)
        d = r.json()
        pid = d.get("id", d.get("post_id", "?"))
        print(f"  ✓ [{l['level']}] ID:{pid} — {l['title'][:60]}")
        return pid
    except Exception as e:
        print(f"  ✗ FAILED: {l['title'][:60]} — {e}")
        return None


# Add your lessons here in the same format as the originals.
# See LESSON_INDEX.md for the full list of 34 lessons already posted.
LESSONS = [
    # Example structure:
    # {
    #     "title": "Lesson Title",
    #     "level": "B1",  # A1, A2, B1, B2, C1, TT
    #     "focus": "Grammar",
    #     "cat": "English Teaching",
    #     "tags": ["grammar", "B1", "ELT365"],
    #     "note": "Personal anecdote...",
    #     "concept": "The teaching concept...",
    #     "example": "HTML example content...",
    #     "activity": "HTML activity content...",
    #     "answers": "Answer key content...",
    #     "meta": "SEO meta description (max 155 chars)",
    #     "seo": "SEO title (max 60 chars)"
    # },
]


def main():
    print(f"Posting {len(LESSONS)} lessons to WordPress as drafts...\n")
    success = 0
    fail = 0
    for i, lesson in enumerate(LESSONS, 1):
        print(f"[{i:02d}/{len(LESSONS)}] {lesson['title'][:55]}...")
        pid = post_lesson(lesson)
        if pid and pid != "?":
            success += 1
        else:
            fail += 1
        time.sleep(0.5)
    print(f"\n{'='*50}")
    print(f"Success: {success} | Failed: {fail}")


if __name__ == "__main__":
    main()
