# Prompt Caching & Context Window Optimization: Maximizing AI Efficiency

## The Quick Answer

**Prompt caching = Storing and reusing input tokens to avoid re-processing the same text.**

Every time you send a prompt to an AI model, it processes all tokens. With prompt caching, frequently reused text (system prompts, documents, codebases) is cached, cutting costs by 90% and latency by 50%.

**Biggest win:** System prompt caching (used in every request)
**Easiest implementation:** Add cache control headers to API calls
**Most powerful:** Caching large codebases or documentation sets

**Real example:** Customer support system with 10K-token knowledge base. Without caching: $0.50/request. With caching: $0.05/request. 20x cheaper.

## Why Prompt Caching Matters

### The Problem: Context Is Expensive

```
Standard API call:
Input: 100K tokens (document + prompt)
Cost: 100K × $0.003 per 1K = $0.30 per request
Latency: 2 seconds (process all 100K tokens)

With 1000 requests/day:
- Cost: $300/day or $9,000/month
- Latency: 2 seconds/request adds up for users

This is wasteful because:
- 90% of tokens are the same (system prompt, documentation)
- Only 10% change (user query)
- We're re-processing 90K identical tokens every request
```

### The Business Impact

```
Legal Document Analysis System

Without caching:
- 50K-token contract template + prompt
- 100 daily analysis requests
- Cost: (50K × $0.003) × 100 = $15/day = $450/month
- Latency: 2.5 seconds per request

With prompt caching:
- Cache 50K contract template (one-time: $0.15)
- Each request only processes 500 new tokens: 500 × $0.0003 = $0.15
- 100 requests: $0.15 × 100 = $15/day ≈ $15/month
- Latency: 1.2 seconds per request (skip cached token processing)

Savings:
- Monthly cost: $450 → $15 (97% reduction)
- Latency: -50% (2.5s → 1.2s)
- Annual savings: $5,220

ROI: Free - costs the same to implement
```

## How Prompt Caching Works

### Architecture

```
Request 1 (No cache):
┌─────────────────────────────────────────┐
│ System Prompt (1K tokens)               │ ← Process all
├─────────────────────────────────────────┤
│ Knowledge Base (5K tokens)              │ ← Process all
├─────────────────────────────────────────┤
│ User Query (100 tokens)                 │ ← Process all
└─────────────────────────────────────────┘
Total: 6,100 tokens processed
Cost: $0.0183, Latency: 1.5s

Request 2 (With prompt caching):
┌─────────────────────────────────────────┐
│ System Prompt (1K tokens)               │ ← CACHED
├─────────────────────────────────────────┤
│ Knowledge Base (5K tokens)              │ ← CACHED
├─────────────────────────────────────────┤
│ User Query (100 tokens)                 │ ← Process
└─────────────────────────────────────────┘
Total: 100 tokens processed
Cost: $0.0003, Latency: 0.5s (skip processing cached part)

Savings per request:
- Cost: 98% reduction
- Latency: 67% reduction
```

### Cache Mechanics

```
How caching works:

1. CREATE cache:
   - Send request with cache_control header
   - Model processes all tokens
   - Result is cached

2. USE cache:
   - Send another request with same prefix
   - Model detects matching cache
   - Skips processing cached portion
   - Only processes new tokens

3. EXPIRE cache:
   - Default: 5 minutes (no requests)
   - Maximum: 24 hours
   - Manual expiry: Delete or set new cache key

Cache hit example:
Request 1:
"You are an expert lawyer.
Here is a contract: [5000 tokens of contract]
Question: Is this legal?"
→ Cache created (5000 tokens stored)

Request 2:
"You are an expert lawyer.
Here is a contract: [5000 tokens of contract - IDENTICAL]
Question: Is this compliant?"
→ Cache HIT! Only new question processed
```

### Implementation (Claude API)

```python
import anthropic
from anthropic.types.cache_control_ephemeral_param import CacheControlEphemeralParam

client = anthropic.Anthropic()

# Large static content (cached)
knowledge_base = """
[5000 tokens of company knowledge base]
Product features, pricing, policies, FAQ...
"""

system_prompt = """
You are a helpful customer support assistant.
Answer questions based on the knowledge base provided.
"""

# Request 1: Create cache
response1 = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=100,
    system=[
        {
            "type": "text",
            "text": system_prompt,
        },
        {
            "type": "text",
            "text": f"Knowledge base:\n{knowledge_base}",
            "cache_control": {"type": "ephemeral"}  # ← Enable caching
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "What's your refund policy?"
        }
    ]
)

# First request costs: process full prompt
# usage: 5,100 input tokens, 50 output tokens

# Request 2: Reuse cache
response2 = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=100,
    system=[
        {
            "type": "text",
            "text": system_prompt,
        },
        {
            "type": "text",
            "text": f"Knowledge base:\n{knowledge_base}",
            "cache_control": {"type": "ephemeral"}  # ← Same cache
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "Do you offer free shipping?"
        }
    ]
)

# Second request costs: ONLY new query (let's say 10 tokens)
# usage: 10 input tokens, 45 output tokens
# → 98% cost reduction vs first request
```

## Caching Strategies

### Strategy 1: System Prompt Caching

```
Best for: Every API call uses same system prompt

Example: Translation API
- System prompt: 500 tokens (always same)
- User input: 100 tokens (varies)

Without caching:
- Every request: 600 tokens processed

With caching:
- First request: 600 tokens
- Subsequent requests: 100 tokens only
- Savings: 83% per request

Implementation:
system_prompt = "You are a translator..."
cache_control = {"type": "ephemeral"}  # Cache it

Estimated monthly impact:
- 10K requests/day
- System prompt tokens: 5K × $0.003 = $15
- Without cache: 10K × $15 = $150K/month
- With cache: $15/month (one-time) + 10K × queries
- Savings: $149,500+/month
```

### Strategy 2: Knowledge Base Caching

```
Best for: Large static documents (contracts, codebases, manuals)

Example: Legal Contract Analysis
- Contract template: 50K tokens (same for all customers)
- Analysis prompt: 200 tokens (varies)

Without caching:
- Cost per analysis: 50K × $0.003 = $0.15
- 1000 analyses: $150

With caching:
- First analysis: $0.15 (cache created)
- Subsequent analyses: 200 × $0.0003 = $0.06
- 1000 analyses: $0.15 + ($0.06 × 999) = $60

Savings: 60% cost reduction
```

### Strategy 3: Session-Based Caching

```
Best for: Multi-turn conversations where context is reused

Example: Code Review Tool
Turn 1: "Here's my codebase (10K tokens)"
Turn 2: "Review this function"
Turn 3: "Optimize this other function"

Without caching:
- Turn 1: 10K tokens
- Turn 2: 10K tokens + new query
- Turn 3: 10K tokens + new query
- Total: 30K+ tokens

With caching:
- Turn 1: 10K tokens (cache created)
- Turn 2: 10K tokens CACHED + new query = only new query
- Turn 3: 10K tokens CACHED + new query = only new query
- Total: 10K + small overhead

Savings: 66% cost reduction over conversation
```

### Strategy 4: Multi-Tenant Caching

```
Best for: Shared resources across many users

Example: Customer Support with Shared Knowledge Base

All customers share:
- Company FAQ: 5K tokens
- Product knowledge: 10K tokens
- Company policies: 3K tokens
- Total: 18K shared tokens

Customer A: 100 support requests/day
Customer B: 150 support requests/day
Customer C: 80 support requests/day
Total: 330 requests/day

Without caching:
- Cost per request: 18K × $0.003 = $0.054
- Daily: 330 × $0.054 = $17.82
- Monthly: $534.60

With caching (shared):
- First request: 18K tokens (one-time cache)
- Each request: only customer-specific query
- Cost per request: ~$0.0003 (just query)
- Daily: 330 × $0.0003 = $0.099
- Monthly: ~$3

Savings: 99% reduction! $531.60/month
```

## Real-World Caching Examples

### Example 1: Customer Support Platform

```
System: Multi-language customer support with 8000-token knowledge base

Request volume: 5,000/day
Average prompt: 8000 KB + 150 new tokens

WITHOUT prompt caching:
- Cost: 5000 × (8000 × $0.003 + 150 × $0.003)
- Cost: 5000 × $24.45 = $122,250/day = $3.67M/month

WITH prompt caching:
- Cache the 8000 tokens (one-time cost)
- Each request: only 150 tokens × $0.0003 = $0.045
- Cost: 5000 × $0.045 = $225/day = $6,750/month
- Plus cache refreshes: ~$50/month

Monthly savings: $3.6M+
Implementation time: 2 hours
ROI: Infinite
```

### Example 2: Code Analysis Tool

```
Scenario: GitHub Copilot-like tool analyzing a 50K codebase

Per developer:
- Codebase size: 50K tokens
- Analysis prompts: 500 tokens each
- Daily queries: 20

WITHOUT caching:
- Per analysis: 50,500 tokens × $0.003 = $0.1515
- Per developer per day: 20 × $0.1515 = $3.03
- 100 developers per day: $303
- Monthly: $9,090

WITH caching:
- Cache codebase: 50K tokens (one-time)
- Per analysis: 500 tokens × $0.0003 = $0.00015
- Per developer per day: 20 × $0.00015 = $0.003
- 100 developers per day: $0.30
- Monthly: $9

Savings: $9,081/month (99.9% reduction)
Latency improvement: 2.5s → 1.2s per query
```

### Example 3: Content Generation Platform

```
Scenario: Blog post generation using templates + guidelines

Template + Guidelines: 15K tokens (always same)
User input (topic): 100 tokens (varies)

10,000 blog posts/month

WITHOUT caching:
- Cost per post: 15,100 tokens × $0.003 = $0.0453
- Monthly: 10,000 × $0.0453 = $453

WITH caching:
- Cache template (one-time): $0.045
- Per post: 100 tokens × $0.0003 = $0.00003
- Monthly: 10,000 × $0.00003 = $0.30

Monthly savings: $452.70
Annual savings: $5,432
```

## Cache Management Best Practices

### Best Practice 1: Cache Stability

```
Good:
- Cache large, static content (system prompts, documentation)
- Cache stays consistent across requests
- High hit rate → maximum savings

Bad:
- Caching content that changes frequently
- Cache invalidation overhead
- Low hit rate → minimal savings

Example:
✓ GOOD: "Here is our company handbook (stable)"
✗ BAD: "Here is today's stock prices (changes constantly)"
```

### Best Practice 2: Cache TTL (Time To Live)

```
Ephemeral cache (default):
- TTL: 5 minutes
- Good for: Support sessions, analysis tools, chatbots
- Use case: User has multiple requests within 5 min window

Persistent cache:
- TTL: 24 hours
- Good for: Scheduled batch jobs, nightly analysis
- Use case: System processes same data daily

Selection:
if request_frequency > 10_per_minute:
    use_ephemeral_cache()  # 5 min TTL
elif request_frequency > 1_per_hour:
    use_persistent_cache()  # 24 hour TTL
else:
    no_caching_benefit()  # Too infrequent
```

### Best Practice 3: Monitor Cache Performance

```
Metrics to track:

1. Cache hit rate
   - Formula: cache_hits / total_requests
   - Target: > 80%
   - Tool: Log cache_hit header in responses

2. Cost per request
   - Before: Total cost / requests
   - After: Total cost / requests
   - Track savings month-over-month

3. Latency improvement
   - Before: Avg response time
   - After: Avg response time
   - Goal: 50%+ reduction

4. Cache efficiency
   - Tokens cached / total tokens
   - Larger static portion = better savings
```

### Best Practice 4: Cache Invalidation

```
When to invalidate cache:

1. Content changes
   - System prompt updated → Invalidate
   - Knowledge base refreshed → Invalidate
   - Policy documents changed → Invalidate

2. Version updates
   - New Claude version released → Re-cache
   - Model parameters changed → Invalidate

3. Time-based
   - Default: 5 minutes (ephemeral)
   - Option: 24 hours (persistent)

Implementation:
# Cache key includes version hash
cache_key = hash(system_prompt + knowledge_base + model_version)
if cache_key != previous_cache_key:
    invalidate_cache()
    create_new_cache()
```

## Cache Limitations & Considerations

### Limitation 1: Minimum Cache Size

```
Not all APIs support caching (minimum token thresholds vary)

Typical:
- Minimum cacheable block: 1,024 tokens
- Maximum cached tokens: Usually no limit
- Overhead: ~200 tokens for cache management

Example:
✓ GOOD: Caching 5K token knowledge base
✗ BAD: Trying to cache 100 token snippets (too small)
```

### Limitation 2: Cache Overhead for Small Requests

```
If your request is mostly new tokens:
- Cache benefit: Minimal
- Example: 50 cached tokens + 5000 new tokens
- Savings: 1% cost reduction (not worth complexity)

Rule of thumb:
Cached tokens / Total tokens > 50% for meaningful savings
```

### Limitation 3: Cache Invalidation Complexity

```
Challenges:
- Knowing when content changes
- Syncing cache across multiple instances
- Versioning mismatches

Solution:
- Use content hash as cache key
- Automatically invalidate on hash change
- Log all cache invalidations
- Monitor cache hit rates
```

## Common Mistakes

❌ **Caching frequently-changing content** — Invalidation overhead negates savings
❌ **Not monitoring cache hit rates** — Silent performance issues
❌ **Caching too-small prompts** — API overhead > savings
❌ **Ignoring TTL implications** — Stale cache causes wrong answers
❌ **No cache invalidation strategy** — Outdated content served
❌ **Over-optimizing latency** — Cache complexity isn't always worth it
❌ **Cache without versioning** — Model updates break cached prompts

## Pro Tips

**Tip 1:** Start with system prompt caching (easiest, highest ROI)
**Tip 2:** Cache only if cached tokens > 50% of total
**Tip 3:** Monitor cache hit rates daily
**Tip 4:** Invalidate cache on content changes automatically
**Tip 5:** Use persistent cache for batch jobs, ephemeral for interactive
**Tip 6:** Version your cached content (include version in cache key)
**Tip 7:** Test cache behavior before production deployment
**Tip 8:** Track cost savings month-over-month
**Tip 9:** Cache size recommendations: 1K-100K tokens optimal
**Tip 10:** Combine with other optimizations: batching, quantization, etc.

## The Bottom Line

- **Prompt caching cuts costs by 90%+ for static content**
- **Latency drops by 50%+ for cached requests**
- **Implement with API headers (2-line code change)**
- **Best for: System prompts, documentation, knowledge bases**
- **ROI: Highest in multi-user, high-volume systems**
- **Monitor: Track cache hit rates and cost savings**

---

**Series:** AI Concepts Explained Simply | **Concept #29:** Prompt Caching & Context Window Optimization
**Previous:** Monitoring & Observability in Production AI | **Mistral Studio:** https://console.mistral.ai
