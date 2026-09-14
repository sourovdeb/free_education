#!/usr/bin/env python3
"""
Psychology/Marketing Claim Audit — draft publisher for sourovdeb.com
Posts the ego-depletion audit micro-blog as a DRAFT via the custom WP endpoint,
following the same pattern as elt365_lessons_publisher.py.
"""

import urllib.request
import urllib.error
import json

WP_ENDPOINT = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
WP_KEY = "0767044896thevenet_"
MENTAL_HEALTH_CATEGORY_ID = 582

POST = {
    "title": "Audit: Is \"Ego Depletion\" (Willpower Fatigue) Actually Real?",
    "content": (
        "<p>For 15 years, \"ego depletion\" — the idea that willpower is a fuel tank "
        "that empties with use — was social psychology's most-cited finding on "
        "self-control. Baumeister, Bratslavsky, Muraven &amp; Tice's original 1998 study "
        "(<em>Journal of Personality and Social Psychology</em>, funded by two public NIH "
        "grants, not industry money) reported that resisting cookies in favor of radishes "
        "made people quit a puzzle faster. It spawned a \"muscle model\" of willpower, a "
        "glucose-depletion theory, and a cottage industry of productivity advice "
        "(\"do the hard task first, before you run out\").</p>\n"
        "<p>Then came the checks. A 2010 meta-analysis found a large pooled effect — but "
        "a 2016 <strong>Registered Replication Report</strong>, pre-registered across "
        "23–24 independent labs and 2,141 participants, found essentially nothing: "
        "d = 0.04, 95% CI [−0.07, 0.15], statistically indistinguishable from zero. A "
        "follow-up 36-lab replication (3,531 participants) found d = 0.06. A separate "
        "bias-corrected meta-analysis found the original literature was riddled with "
        "publication bias, shrinking the \"true\" effect toward zero once corrected.</p>\n"
        "<p>No pharma or marketing money is implicated — the original funding was public. "
        "This looks like ordinary academic incentives at work: small samples, flexible "
        "analysis choices, and a bias toward publishing positive results, not a "
        "funder-driven conclusion. <strong>Verdict:</strong> contested, likely far smaller "
        "than claimed, possibly zero. Treat \"protect your willpower\" advice as folklore, "
        "not science.</p>\n"
        "<p><strong>Sources:</strong></p>\n"
        "<ul>\n"
        "<li><a href=\"https://pubmed.ncbi.nlm.nih.gov/9599441/\">Original 1998 study — PubMed</a></li>\n"
        "<li><a href=\"https://journals.sagepub.com/doi/10.1177/1745691616652873\">2016 Registered Replication Report — Perspectives on Psychological Science</a></li>\n"
        "<li><a href=\"https://www.sciencedaily.com/releases/2016/07/160729143034.htm\">ScienceDaily coverage of the 2016 replication</a></li>\n"
        "<li><a href=\"https://replicationindex.com/2016/04/18/rr1egodepletion/\">Replicability-Index critique of the glucose mechanism</a></li>\n"
        "</ul>\n"
        "<hr>\n"
        "<p><em>Independent research-literacy note, not medical or clinical advice. "
        "Always consult a qualified professional for mental-health treatment decisions.</em></p>"
    ),
    "status": "draft",
    "category": MENTAL_HEALTH_CATEGORY_ID,
    "tags": ["psychology", "replication", "willpower", "research audit"],
    "meta_description": (
        "An evidence audit of 'ego depletion': what the original 1998 study found, who "
        "funded it, and why large registered replications found the effect close to zero."
    ),
    "seo_title": "Is Ego Depletion Real? A Replication Audit",
}


def post():
    data = json.dumps(POST).encode("utf-8")
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
            print(f"OK — {POST['title'][:70]}")
            try:
                parsed = json.loads(body)
                post_id = parsed.get("id") or parsed.get("post_id") or "?"
                print(f"post_id={post_id}")
                return {"ok": True, "id": post_id}
            except Exception:
                print(f"response: {body[:200]}")
                return {"ok": True, "id": "?"}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:300]
        print(f"ERR — HTTP {e.code}: {body}")
        return {"ok": False, "error": f"HTTP {e.code}: {body}"}
    except Exception as exc:
        print(f"ERR — {exc}")
        return {"ok": False, "error": str(exc)}


if __name__ == "__main__":
    post()
