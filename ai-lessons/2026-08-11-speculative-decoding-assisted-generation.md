# Speculative Decoding & Assisted Generation: Speeding Up Inference Without Accuracy Loss

## The Quick Answer

**Speculative decoding = Use a small "draft" model to predict multiple tokens at once, then verify with the large model. Result: 2-5x faster inference with zero accuracy loss.**

LLM inference is slow because tokens are generated one at a time. Speculative decoding parallelizes this by having a small model draft 4-5 tokens ahead, then the large model verifies them all at once. If correct, move forward. If wrong, only re-do the incorrect ones.

**Core concept:** Let the small model guess ahead, the big model fact-checks.

**Biggest win:** 2-5x faster generation with zero accuracy compromise
**Easiest implementation:** Works with any LLM (no retraining needed)
**Most powerful:** Combine with other optimizations for 10x improvements

**Real example:** Llama 2 70B generating 1000 tokens. Without speculative decoding: 50 seconds. With speculative decoding: 12 seconds. Same output, 4x faster.

## Why Speculative Decoding Matters

### The Problem: Token-by-Token Generation Is Slow

```
Traditional autoregressive generation:

Token 1: Model processes all 1000 input tokens
         ↓ Predicts token 1 (50ms latency)
         
Token 2: Model processes input + token 1
         ↓ Predicts token 2 (50ms latency)
         
Token 3: Model processes input + tokens 1-2
         ↓ Predicts token 3 (50ms latency)
         
...repeat 997 more times

Total: 1000 tokens × 50ms = 50,000ms = 50 seconds

Throughput: 20 tokens/second
Latency: 50ms per token (feels slow for users)
```

### The Business Impact

```
AI Chat Service

Without speculative decoding:
- Average response: 50 seconds for 1000 tokens
- User experience: Feels slow (50ms latency)
- Throughput: 20 responses/second per GPU
- Hardware: 32 GPUs needed = $20K/month

With speculative decoding (4x speedup):
- Average response: 12.5 seconds for 1000 tokens
- User experience: Feels snappy (12ms latency)
- Throughput: 80 responses/second per GPU (4x)
- Hardware: 8 GPUs needed = $5K/month
- Cost savings: $15K/month

Impact:
- Monthly savings: $180K/year
- User experience: 4x improvement
- Scalability: Can handle 4x more users
- No accuracy loss (same model output)

ROI: Pays for implementation in days
```

## How Speculative Decoding Works

### The Concept

```
Traditional generation:
Large Model: [][][][][][][][][]... (slow, process entire model)
             ↓ 50ms per token
             Token 1 done
             ↓ 50ms per token
             Token 2 done

Speculative decoding:
Draft Model: [][][][] (fast, lightweight)
             ↓ 5ms
             Draft 4 tokens: "The quick brown fox"
             
Large Model: [][][][][][][][][]... (verify all 4 tokens at once)
             ↓ 20ms (verify 4 tokens in parallel)
             
Result: 4 tokens generated in 25ms (vs 200ms without)
        6.25ms per token average (vs 50ms)
        8x faster!

Key insight: Draft model speculates ahead, large model verifies in batch
```

### The Algorithm

```
Speculative Decoding Algorithm:

Input: Prompt tokens, large model, small model, K=4 (draft tokens)

Step 1: Draft phase (small model is fast)
- Small model generates K tokens quickly
- Tokens: [token_1, token_2, token_3, token_4]
- Time: 5ms (very fast)

Step 2: Verify phase (large model batch-processes)
- Large model processes: [prompt + token_1 + token_2 + token_3 + token_4]
- Gets probabilities for all positions at once
- Compares:
  - Position 1: small model said "the" → large model says "the" ✓ (correct)
  - Position 2: small model said "quick" → large model says "quick" ✓ (correct)
  - Position 3: small model said "brown" → large model says "brown" ✓ (correct)
  - Position 4: small model said "fox" → large model says "dog" ✗ (wrong)

Step 3: Accept/reject
- Accept tokens 1-3 (small model was right)
- Re-sample token 4 from large model (small model was wrong)
- Continue with next draft

Result: 3 tokens accepted (fast), 1 re-done (correct)
Average: 3.25 tokens per 20ms = 162 tokens/second (vs 20 without)
Speedup: 8x
Accuracy: 100% (large model always has final say)
```

### Why It Works

```
Key assumptions:

1. Small model agrees with large model most of the time
   - Both are trained on similar data
   - Small model captured main distributions
   - Disagreement: typically <20%

2. Batch processing is much faster than sequential
   - 4 tokens in parallel: ~20ms
   - 4 tokens sequential: ~200ms (10x slower)
   - Speculative decoding exploits this

3. Rejection sampling is fast
   - If small model wrong: just re-sample from large model
   - No repeated computation (already have probabilities)

Typical agreement rate: 80-95%
If agreement > 50%: Speculative decoding is worth it
```

## Speculative Decoding Strategies

### Strategy 1: Simple Draft Model Approach

```
Setup:
- Large model: Llama 2 70B
- Draft model: Llama 2 7B (smaller version)
- Draft tokens: K=4

Characteristics:
- Draft model: Similar architecture, just smaller
- Agreement rate: 85-90% (very high)
- Speedup: 3-4x

Implementation:
1. Load both models
2. Generate draft tokens with 7B (fast)
3. Verify with 70B (batch)
4. Accept correct ones, re-sample wrong ones
5. Repeat

Pros:
- Simple to implement
- High agreement rate (same architecture)
- Well-tested approach

Cons:
- Requires loading two models (memory overhead)
- Best results with similar model families
```

### Strategy 2: Distilled Speculative Model

```
Setup:
- Large model: Llama 2 70B
- Draft model: Distilled from 70B (1-2B parameters)
- Draft tokens: K=3-4

Distillation process:
1. Train small model to match large model outputs
2. Use large model as teacher (knowledge distillation)
3. Small model learns to predict what 70B would predict
4. Result: Tiny model that thinks like the big one

Benefits:
- Better agreement (trained to match large model)
- Smaller memory footprint than 7B version
- Can load on CPU while large model on GPU

Typical performance:
- Agreement: 90-95% (even better than 7B)
- Speedup: 3-5x
- Model size: Only 1-2B parameters
```

### Strategy 3: Multi-Draft Speculative Decoding

```
Setup:
- Large model: Llama 2 70B
- Multiple draft models: 
  - Draft 1: 1B params (very fast)
  - Draft 2: 3B params (fast)
- Strategy: Use fastest model for high-agreement cases

How it works:
Iteration 1:
- Try 1B model (ultra-fast) for 4 tokens
- Agreement rate: 70%
- Result: Mostly correct, 1 wrong

Iteration 2:
- For the wrong token, use 3B model (more accurate)
- Agreement rate: 90%
- Result: Correct

Benefit:
- Average uses fastest model possible
- Fallback to more accurate model if needed
- Maximizes speedup while maintaining correctness

Typical speedup: 4-6x
```

### Strategy 4: Lookahead Caching + Speculative Decoding

```
Setup:
- Combine speculative decoding with KV-cache optimization
- Draft model generates tokens
- Large model reuses cached keys/values

Optimization:
Without optimization:
- Draft 4 tokens: 5ms
- Large model processes all 4: 20ms
- Total: 25ms per batch

With KV-cache reuse:
- Draft 4 tokens: 5ms (same)
- Large model processes with cached attention: 10ms (2x faster)
- Total: 15ms per batch (50% faster!)

Result:
- Base speedup: 8x from speculative decoding
- Additional speedup: 1.5x from KV-cache optimization
- Combined: 12x speedup
```

## Real-World Speculative Decoding Examples

### Example 1: Chat API Speed Improvement

```
Scenario: OpenAI-like chat API serving millions of users

Current setup (without speculative decoding):
- Model: GPT-4 equivalent (large, accurate)
- Latency: 50ms per token
- User request: "Write a story" (500 tokens)
- Response time: 25 seconds
- User experience: Feels slow

With speculative decoding:
- Large model: GPT-4 equivalent
- Draft model: Distilled 2B model
- Speedup: 4x
- New latency: 12.5ms per token
- Response time: 6.25 seconds
- User experience: Feels responsive (real-time)

Cost impact:
- Latency improvement: 4x faster response
- Throughput: 4x more users per GPU
- Hardware: 4x fewer GPUs needed
- Annual savings: $100M+ for large-scale API
```

### Example 2: Mobile On-Device Inference

```
Scenario: Smartphone running AI locally

Without speculative decoding:
- Mobile CPU only
- Model: Llama 2 7B (requires good CPU)
- Latency: 100ms per token
- Generating 50 tokens: 5 seconds (feels slow)
- Battery: Heavy drain (15% per generation)

With speculative decoding:
- Large model: Llama 2 7B
- Draft model: 500M parameters (ultra-lightweight)
- Combined latency: 30ms per token (3.3x faster)
- Generating 50 tokens: 1.5 seconds (feels responsive)
- Battery: 5% per generation (3x better)

Benefit:
- 3x faster = better UX
- 3x better battery = more sessions per charge
- Same accuracy (7B model output)
```

### Example 3: Long-Context Processing

```
Scenario: Analyzing 50K tokens of legal documents

Traditional (slow):
- Input: 50K token document
- Generate: 500 token summary
- Latency: 50ms per token × 500 = 25 seconds
- Cost: Process all 50K tokens for each generated token

With speculative decoding:
- Draft model: Fast summarization (generates 4 tokens)
- Large model: Batch-verifies all 4 at once
- Latency: 50ms per batch × 125 batches = 6.25 seconds (4x faster)
- Cost: Same (large model still processes all context)

Benefit for long-context:
- Speed: 4x improvement
- Accuracy: No loss (large model validates)
- Context handling: No change (still processes full context)

Use case: Document analysis, summarization, Q&A on large texts
```

### Example 4: Enterprise Code Generation

```
Scenario: GitHub Copilot-like code generation

Setup:
- Large model: Code-specific LLM (70B)
- Draft model: 7B code model
- Scenario: Generate 200 lines of code (2000 tokens)

Performance comparison:
Traditional:
- Latency: 50ms × 2000 = 100 seconds
- User wait: 100 seconds (unacceptable)

With speculative decoding:
- Speculative speedup: 4x
- Latency: 25 seconds
- User wait: 25 seconds (acceptable for code)

Additional optimization (with caching):
- First request: 25 seconds
- Subsequent edits: 10 seconds (cached prefix)
- Typical workflow: Edit in 5-10 seconds

Benefit:
- Real-time development experience
- No accuracy loss (same model output)
- 4x more concurrency on hardware
```

## Speculative Decoding Best Practices

### Best Practice 1: Choosing Draft Model Size

```
Decision matrix:

Large model: 70B parameters

Draft model options:
- 1B (ultra-lightweight): 8x speedup, 70% agreement
- 3B (lightweight): 5x speedup, 85% agreement  
- 7B (balanced): 4x speedup, 90% agreement
- 13B (aggressive): 2x speedup, 95% agreement

Selection based on target:
- Max speed (edge/mobile): Use 1B, accept 30% re-sampling
- Balanced (typical): Use 3B-7B, 85-90% agreement
- Max accuracy: Use 13B, 95% agreement

Rule of thumb:
draft_size ≈ large_size / 10

Example: 70B large → 7B draft
         100B large → 10B draft
```

### Best Practice 2: Agreement Rate Monitoring

```
Metric: How often small model agrees with large model

Measurement:
- Run speculative decoding on test data
- Count tokens where small model == large model
- Agreement rate = tokens_agreed / total_tokens

Typical ranges:
- Agreement rate > 80%: Very efficient (worth doing)
- Agreement rate 50-80%: Still worthwhile
- Agreement rate < 50%: Not worth overhead

How to improve agreement:
1. Distill small model (train on large model outputs)
2. Use similar architecture (both LLaMA, both GPT, etc)
3. Increase draft model size (7B > 3B > 1B)
4. Reduce number of draft tokens K (3 instead of 5)
```

### Best Practice 3: Draft Token Count Optimization

```
Parameter: K = number of tokens to draft per iteration

K=1: Minimum drafting
- Always correct (only 1 token rarely wrong)
- Speedup: 1.2x (minimal)
- Use when: Space constrained

K=3-4: Balanced (recommended)
- Agreement: 85-90%
- Speedup: 3-4x
- Use for: Most applications

K=5-6: Aggressive
- Agreement: 80-85%
- Speedup: 4-5x (more re-sampling overhead)
- Use for: High-latency tolerance

K>8: Very aggressive
- Agreement: 70-75%
- Speedup: Diminishing (high re-sampling cost)
- Use: Only for throughput optimization

Testing:
for k in [1, 2, 3, 4, 5]:
    speedup = measure_speedup(draft_model, large_model, k)
    agreement = measure_agreement(draft_model, large_model, k)
    latency = measure_latency(draft_model, large_model, k)

Pick K that maximizes speedup while maintaining agreement > 80%
```

### Best Practice 4: Integration with Other Optimizations

```
Speculative decoding works well with:

1. Quantization
   - 4-bit quantized large model
   - Speculative decoding speeds up inference
   - Combined: 2x (quantization) × 4x (speculative) = 8x faster

2. Batching
   - Batch verification in speculative decoding
   - Process multiple sequences simultaneously
   - Maximize GPU utilization

3. KV-cache optimization
   - Reuse attention cache for verified tokens
   - Reduce redundant computation
   - 1.5x additional speedup

4. Model sharding
   - Distribute large model across GPUs
   - Small model on CPU
   - Parallel computation

Combined optimization:
Quantization (2x) × Speculative (4x) × Batching (2x) × Cache (1.5x) = 24x speedup
```

## Common Mistakes

❌ **Using agreement rate < 50%** — Negative speedup (re-sampling costs more than benefit)
❌ **Drafting too many tokens** — Diminishing returns after K=5
❌ **Wrong draft model** — Different training data = low agreement
❌ **Not measuring actual latency** — Look good in theory, slow in practice
❌ **Forgetting memory overhead** — Two models require twice the memory
❌ **No fallback mechanism** — If draft model fails, system breaks
❌ **Ignoring batch processing benefits** — Not leveraging parallel verification

## Pro Tips

**Tip 1:** Start with draft_size = large_size / 10 (good heuristic)
**Tip 2:** Distill draft model from large model (better agreement)
**Tip 3:** Monitor agreement rate continuously (critical metric)
**Tip 4:** K=4 is sweet spot for most applications
**Tip 5:** Combine with KV-cache for additional 1.5x speedup
**Tip 6:** Test on your actual workload (agreement varies by domain)
**Tip 7:** Use quantized draft model (even faster)
**Tip 8:** Measure actual latency, not theoretical speedup
**Tip 9:** Consider memory overhead (two models vs one)
**Tip 10:** Integrate with batching for maximum throughput

## The Bottom Line

- **Speculative decoding: 2-5x faster with zero accuracy loss**
- **No retraining needed (works with any LLM)**
- **Agreement rate > 80% = worthwhile optimization**
- **Draft model = large_model / 10 is good starting point**
- **Combines well with quantization, batching, caching**
- **Production-ready: Already implemented in major APIs**

---

**Series:** AI Concepts Explained Simply | **Concept #33:** Speculative Decoding & Assisted Generation
**Previous:** Low-Rank Adaptation (LoRA) | **Mistral Studio:** https://console.mistral.ai
