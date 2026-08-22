# Batch Processing & Async Inference: Scaling AI Workloads Efficiently

## The Quick Answer

**Batch processing = Process many requests together instead of one at a time.**

Instead of processing 1,000 customer emails individually (1,000 API calls), batch them into groups of 100 and process all 100 at once. Result: 10x faster, 50% cheaper.

**Core concept:** Batching trades latency for throughput. Perfect for background jobs, not real-time requests.

**Biggest win:** Email/document processing (1,000 items: 1 hour → 6 minutes)
**Easiest implementation:** Collect requests in queue, process every 10 seconds
**Most powerful:** Combine with async processing for fully non-blocking systems

**Real example:** Support ticket classification. Processing 10,000 tickets: without batching 2 hours, with batching 12 minutes (10x faster).

## Why Batch Processing Matters

### The Problem: Processing One at a Time Is Slow

```
Real-time processing (one request at a time):
Request 1: 1 second
Request 2: 1 second
Request 3: 1 second
...
Request 1000: 1 second
Total: 1000 seconds (16.7 minutes) for all

Batch processing (100 at a time):
Batch 1 (100 requests): 2 seconds (parallel)
Batch 2 (100 requests): 2 seconds
...
Batch 10 (100 requests): 2 seconds
Total: 20 seconds for all (50x faster)

Why? GPU parallelism:
- Processing 1 request = 1% GPU utilization
- Processing 100 requests = 95% GPU utilization
- Same hardware, 95x more efficient
```

### The Business Impact

```
Email Campaign Analysis System

Without batching:
- 50,000 emails to process
- 1 second per email (API call)
- Total time: 50,000 seconds = 13.9 hours
- Cost: 50,000 × $0.01 per API call = $500

With batching (100 at a time):
- Process in batches of 100
- 500 batches × 2 seconds = 1000 seconds = 16.7 minutes
- Cost: 500 × $0.01 per batch = $5 (10x cheaper due to efficiency)
- Time saved: 13+ hours per campaign
- Cost saved: $495 per campaign

Impact:
- Daily campaigns: $5 per day vs $500 per day = $495 saved/day
- Monthly: $14,850 saved
- Annual: $178,200 saved

ROI: Pays for engineering time in 1 week
```

## How Batch Processing Works

### Architecture

```
Synchronous (One at a Time):
Request 1 → Process → Return immediately → Client waits
Request 2 → Process → Return immediately → Client waits
Request 3 → Process → Return immediately → Client waits

Time: 3 seconds
Latency: 1 second per request
GPU efficiency: 10%

Batch Processing:
Request 1 ┐
Request 2 ├─ Queue ──→ Batch (100 items) ──→ Process ──→ Return all → Clients get results
Request 3 ┤                                    (2s)
...       ┘

Time: 2 seconds for all
Latency: 2 seconds (wait in queue)
GPU efficiency: 95%
```

### The Queue System

```
Timeline for batch system:

T=0s: Request 1 arrives → Queued (waiting for batch)
T=1s: Request 2 arrives → Queued
T=2s: Request 3 arrives → Queued
T=3s: Request 4 arrives → Queued
...
T=9s: Request 100 arrives → Queued
T=10s: BATCH READY (100 items) → Start processing
       Requests 1-100 processing...
       GPU utilization: 95%
T=12s: Batch complete → Return all 100 results
       Latency for Request 1: 12 seconds (queue 10s + process 2s)
       But throughput: 100 requests in 2 seconds = 50 requests/second

Compare to real-time:
- Real-time latency: 1 second (immediate)
- Real-time throughput: 1 request/second
- Batch latency: 12 seconds (including wait)
- Batch throughput: 50 requests/second
```

### Async Processing Pattern

```
Traditional approach (blocking):
1. Request arrives
2. Process request
3. Wait for result
4. Return to client
(Client blocked during processing)

Async approach (non-blocking):
1. Request arrives
2. Add to queue (immediate, no waiting)
3. Return job ID to client
4. Client can do other work
5. Process request in background
6. Store result in cache
7. Client polls for result or gets webhook callback

Example:
Client: "Process my 50K documents"
Server: "Job ID: job_12345. Check status at /status/12345"
Client: Does other work
1 minute later...
Client: GET /status/job_12345
Server: Results ready! Here's your analysis

No blocking = happier users
```

## Batching Strategies

### Strategy 1: Time-Based Batching

```
How it works:
- Collect requests for N seconds
- Process all accumulated requests together
- Return results to all clients

Example: 10-second batch window

T=0s:  Request 1 arrives → Queue (size: 1)
T=2s:  Request 2 arrives → Queue (size: 2)
T=5s:  Request 3 arrives → Queue (size: 3)
T=7s:  Request 4 arrives → Queue (size: 4)
T=10s: BATCH! Process 4 items → Return all results
T=12s: Results ready

Pros:
- Predictable latency (max: batch_window + processing_time)
- Simple to implement
- Good for background jobs

Cons:
- Small requests wait longer
- Batch might be small if traffic is light

Best for: Email, document processing, daily reports
```

### Strategy 2: Size-Based Batching

```
How it works:
- Process when batch reaches target size
- No waiting if batch fills up quickly
- Still process after timeout if batch not full

Example: Process when 100 items accumulated OR 30 seconds elapsed

T=0s:  Item 1 → Queue (1/100)
T=2s:  Item 2 → Queue (2/100)
...
T=15s: Item 50 → Queue (50/100)
...
T=28s: Item 99 → Queue (99/100)
T=29s: Item 100 → Queue (100/100) ← BATCH FULL!
T=30s: Start processing (batch took 30 seconds to fill)
T=32s: Complete → Return all 100 results

Pros:
- Most efficient batch size
- Maximize GPU utilization
- Reduced latency for high-volume requests

Cons:
- Low traffic = long waits
- Requires size prediction

Best for: Real-time services with variable load
```

### Strategy 3: Adaptive Batching

```
How it works:
- Monitor incoming request rate
- Adjust batch size and timeout dynamically
- High traffic = smaller batches (process faster)
- Low traffic = larger batches or longer timeout

Pseudo-code:
if requests_per_second > 100:
    batch_size = 50
    timeout = 5s
elif requests_per_second > 10:
    batch_size = 100
    timeout = 10s
else:
    batch_size = 500
    timeout = 30s

Benefits:
- Adapts to traffic patterns
- Keeps latency consistent
- Maximizes efficiency

Example: E-commerce site during Black Friday
- Normal: 10 requests/sec → batch_size=100, latency=10s
- Black Friday: 1000 requests/sec → batch_size=50, latency=5s
- Auto-adjusted for best performance
```

### Strategy 4: Micro-Batching

```
How it works:
- Process batches very frequently (every 100ms)
- Minimize latency while still batching
- Accumulate 10-50 items per batch

Timeline:
T=0ms:    Request 1 → Queue
T=10ms:   Request 2 → Queue
T=50ms:   Request 3 → Queue
T=100ms:  BATCH! (3 items) → Process → Complete T=102ms
T=105ms:  Request 4 → Queue
T=150ms:  BATCH! (1 item) → Process → Complete T=151ms

Latency: ~100ms max (good for real-time)
Throughput: Good batching efficiency
Trade-off: Smaller batches = less efficiency per batch

Best for: Real-time requests with low latency requirements
```

## Real-World Batching Examples

### Example 1: Document Processing Pipeline

```
Scenario: Legal firm processes 10,000 contracts/day

Real-time processing:
- 1 contract: 5 seconds
- 10,000 contracts: 50,000 seconds = 13.9 hours
- Cost: $500 (1 API call per contract)

Batch processing (500 per batch):
- Batch 1 (500): 8 seconds
- Batch 2 (500): 8 seconds
- ...
- Batch 20 (500): 8 seconds
- Total: 20 × 8 = 160 seconds = 2.7 minutes
- Cost: $5 (20 batch API calls)

Improvement:
- Time: 13.9 hours → 2.7 minutes (308x faster)
- Cost: $500 → $5 (100x cheaper)
- Same-day delivery vs 2-day processing
```

### Example 2: Email Classification System

```
Scenario: Email provider classifies 100 million emails/day

Single-request processing:
- 1 email: 200ms
- 100M emails: 200M seconds = 2,314 days (6+ years!)
- Cost: $1M (at $0.01 per email)
- Latency: 200ms average

Batch processing (10K per batch):
- Batch size: 10,000 emails
- Process time: 2 seconds (GPU parallel)
- Batches: 100M / 10K = 10,000 batches
- Total time: 10,000 × 2 = 20,000 seconds = 5.6 hours
- Cost: $100 (10K batch API calls at $0.01)
- Latency: 10 seconds average (wait + process)

Improvement:
- Time: 6+ years → 5.6 hours (millions of times faster)
- Cost: $1M → $100 (10,000x cheaper)
- Infrastructure: 1 GPU vs 100,000 servers
```

### Example 3: Image Processing at Scale

```
Scenario: Image hosting platform processes 50M images/month

Real-time CDN processing:
- Process immediately on upload
- Response time: 2 seconds per image
- Cost: $500K/month (at $0.01 per image)
- Server utilization: 10%

Nightly batch processing:
- Collect during day
- Process during off-peak (11pm-2am)
- Batch size: 1M images
- 50 batches total
- Process time: 15 seconds per batch
- Total: 50 × 15 = 750 seconds = 12.5 minutes
- Cost: $50/month (at $0.01 per image - same price, better time)
- Server utilization: 95%

Trade-offs:
- Latency: Immediate → 12-24 hours (acceptable for thumbnails)
- Cost: Stays same but uses infrastructure better
- Throughput: 25,000 images/second vs 1 image/second
```

### Example 4: ML Model Inference Server

```
Scenario: Fraud detection model serving a payment processor

Real-time inference (current):
- Request arrives
- Model processes 1 transaction
- Latency: 50ms
- Throughput: 20 transactions/second
- 1 GPU server: $5K/month

Batch inference (optimized):
- Collect transactions for 50ms
- Process batch of 1000
- Total latency: 50ms (collection) + 100ms (processing) = 150ms
- Throughput: 10,000 transactions/second
- 1 GPU server: $5K/month (same cost, 500x throughput)

Better approach: Adaptive micro-batching
- Batch accumulation: 10ms
- Batch size: 200 transactions
- Process time: 30ms
- Latency: 40ms (collection) + 30ms (process) = 70ms (still < 100ms SLA)
- Throughput: 5,000 transactions/second
- Hardware: 1 GPU can handle 5000x more volume
```

## Async Inference Pattern

### The Event-Driven Model

```
Synchronous (blocking):
User Request → API → Model → Wait for result → Return

Asynchronous (non-blocking):
User Request → API → Queue → Return job_id
              ↓
         Background Worker
              ↓
         Process in batch
              ↓
         Store result
              ↓
User polls or gets webhook → Result delivered
```

### Implementation Pattern

```python
import asyncio
from queue import Queue
import time

class BatchProcessor:
    def __init__(self, batch_size=100, timeout=10):
        self.queue = Queue()
        self.batch_size = batch_size
        self.timeout = timeout
        self.results = {}
        
    async def submit_request(self, request_id, data):
        # Add to queue, return immediately
        self.queue.put({"id": request_id, "data": data})
        return {"job_id": request_id, "status": "queued"}
    
    async def get_result(self, request_id):
        # Client polls for result
        if request_id in self.results:
            return self.results[request_id]
        return {"status": "processing"}
    
    async def process_batches(self):
        # Background worker
        while True:
            batch = []
            start_time = time.time()
            
            # Collect requests
            while len(batch) < self.batch_size:
                if time.time() - start_time > self.timeout:
                    break
                try:
                    item = self.queue.get(timeout=0.1)
                    batch.append(item)
                except:
                    pass
            
            if batch:
                # Process batch
                results = await self.process_batch(batch)
                
                # Store results
                for item, result in zip(batch, results):
                    self.results[item["id"]] = {
                        "status": "completed",
                        "result": result
                    }
    
    async def process_batch(self, batch):
        # Your model inference here
        # Process all items in batch in parallel
        return [{"prediction": "result"} for _ in batch]

# Usage
processor = BatchProcessor()

# Client submits request
response = await processor.submit_request("req_1", data)
# Immediately returns: {"job_id": "req_1", "status": "queued"}

# Client polls later
result = await processor.get_result("req_1")
# Eventually returns: {"status": "completed", "result": {...}}
```

## Batching Best Practices

### Best Practice 1: Monitor Queue Depth

```
Metrics to track:
- Queue size (items waiting)
- Average wait time
- Batch processing time
- GPU utilization

Alerts:
- Queue size > 1000 items → Too slow, add processing capacity
- Wait time > 30 seconds → Users frustrated
- GPU utilization < 50% → Not batching efficiently
- GPU utilization > 95% → Close to bottleneck

Example dashboard:
Queue depth:     234 items (good, under 1000)
Avg wait time:   8 seconds (good, under 30s)
GPU utilization: 75% (good, not idle or maxed)
Latency:         10 seconds (queue 8s + process 2s)
Throughput:      500 items/minute
```

### Best Practice 2: Graceful Degradation

```
High traffic scenario:
- Batch timeout: normally 10 seconds
- During spike: reduce to 5 seconds (smaller batches)
- Still maintain SLA while handling surge

Implementation:
if queue_depth > 500:
    batch_timeout = 5s  # Process faster
    batch_size = 50     # Smaller batches
elif queue_depth > 1000:
    batch_timeout = 2s  # Very fast
    batch_size = 25     # Even smaller

Result:
- Normal: 10s latency, 500/min throughput
- Light spike: 7s latency, 600/min throughput (adapt)
- Heavy spike: 3s latency, 800/min throughput (adapt further)
```

### Best Practice 3: Request Prioritization

```
Normal queue:
Request 1 ┐
Request 2 ├─ FIFO (first in, first out)
Request 3 ┤
Request 4 ┘

Priority queue:
High Priority   ┐ Process first
Medium Priority ├─ In order
Low Priority    ┘ Process last

Example: E-commerce
- Premium customer request: High priority
- Regular customer request: Medium priority
- Analytics request: Low priority

Result:
- Premium customers see 5s latency
- Regular customers see 15s latency
- Analytics jobs see 60s latency
- All get value, premium users happier
```

### Best Practice 4: Batch Size Optimization

```
Finding optimal batch size:

Batch Size 10:
- Per-item latency: 10 items × 50ms = 500ms base + 100ms queue = 600ms
- Throughput: 10 items per 100ms = 100 items/second
- Efficiency: Low (many batches, overhead)

Batch Size 100:
- Per-item latency: 100 items × 5ms = 500ms base + 1s queue = 1.5s
- Throughput: 100 items per 1.5s = 66 items/second
- Efficiency: Better

Batch Size 1000:
- Per-item latency: 1000 items × 0.5ms = 500ms base + 10s queue = 10.5s
- Throughput: 1000 items per 10.5s = 95 items/second
- Efficiency: Best throughput but long wait

Sweet spot depends on:
- Latency SLA (how long users can wait)
- GPU memory (can it fit larger batches)
- Traffic pattern (steady vs bursty)

Usually: batch_size = 100-500 for most applications
```

## Common Mistakes

❌ **Batching without monitoring** — Silent queue buildup, users get angry
❌ **Fixed batch size** — Can't adapt to traffic spikes
❌ **No timeout** — Waits forever for full batch, leaves requests hanging
❌ **Ignoring GPU memory** — Batch too large, out of memory crash
❌ **Not prioritizing** — All requests equal, premium users suffer
❌ **Syncing instead of async** — Defeats purpose, blocks application
❌ **No fallback** — Single batch processor = single point of failure

## Pro Tips

**Tip 1:** Start with time-based batching (simplest to implement)
**Tip 2:** Size-based batching for high-volume scenarios
**Tip 3:** Always have a timeout (process partial batches)
**Tip 4:** Monitor queue depth like you'd monitor stock prices
**Tip 5:** Use async patterns to avoid blocking client threads
**Tip 6:** Implement request prioritization for fairness
**Tip 7:** Test batch size experimentally (100, 500, 1000)
**Tip 8:** Log all batch processing metrics
**Tip 9:** Combine batching with caching (cached + batched = best)
**Tip 10:** Use adaptive batching for variable traffic

## The Bottom Line

- **Batch processing trades latency for throughput**
- **10-1000x speed improvement for background jobs**
- **Requires async processing pattern (fire and forget)**
- **Best for: email, documents, images, reports**
- **Monitor: queue depth, wait time, GPU utilization**
- **Sweet spot: 100-500 items per batch**

---

**Series:** AI Concepts Explained Simply | **Concept #30:** Batch Processing & Async Inference
**Previous:** Prompt Caching & Context Window Optimization | **Mistral Studio:** https://console.mistral.ai
