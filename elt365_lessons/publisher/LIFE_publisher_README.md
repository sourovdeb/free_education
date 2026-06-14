# LIFE Series Publisher

Three Python scripts posted all 30 LIFE lessons to WordPress as drafts.

## Scripts

| Script | Lessons | Levels | WP IDs |
|--------|---------|--------|--------|
| `LIFE_batch1_A1_A2.py` | LIFE001–010 | A1–A2 | ~1172–1181 |
| `LIFE_batch2_B1_B2.py` | LIFE011–020 | B1–B2 | 1183–1192 |
| `LIFE_batch3_C1_C2.py` | LIFE021–030 | C1–C2 | 1193–1202 |

## Re-run instructions

If you need to re-post any lesson (e.g. after deletion), run:

```bash
python3 LIFE_batch2_B1_B2.py
```

Each script uses the `X-Sourov-Key` header. The key is stored in the script.
Change `status: draft` to `status: publish` before re-running to publish directly.

## Endpoint

```
POST https://www.sourovdeb.com/wp-json/sourov/v1/ai-post
Headers: X-Sourov-Key: [see script]
Body: {title, content, status, category, tags, meta_description, seo_title}
```
