# Model Quantization Techniques: Running AI Models Efficiently

## The Quick Answer

**Quantization = Reducing model precision to use less memory and run faster.**

AI models store weights as 32-bit floats (4 bytes each). A 70B model needs 280GB RAM. Quantization converts to 8-bit integers (1 byte): same 70B model needs 70GB RAM. Result: 4x memory reduction, 4x faster inference, minimal accuracy loss.

**Core concept:** Trade a tiny bit of accuracy for massive speed and efficiency gains.

**Biggest win:** Running large models on consumer GPUs (A100 → RTX 4090)
**Easiest implementation:** One-line library like bitsandbytes or AutoGPTQ
**Most powerful:** 4-bit quantization with LoRA fine-tuning on your laptop

**Real example:** Llama 2 70B model. Without quantization: needs 140GB VRAM. With 4-bit quantization: runs on 24GB GPU with 85% original accuracy.

## Why Quantization Matters

### The Problem: Large Models Require Huge Hardware

```
Llama 2 70B Model (original precision: float32)

Memory calculation:
- 70 billion parameters
- 4 bytes per parameter (float32)
- 70B × 4 bytes = 280 GB just for model weights
- + optimizer states, activations, etc.
- Total: ~560 GB needed

Hardware required:
- 1x H100 (80GB) = Not enough!
- 8x H100 (640GB total) = Finally works
- Cost: $2M+ investment

Result: Only massive enterprises can run the model
```

### The Business Impact

```
Content Generation Company - Deploy Llama 2 70B

Without quantization:
- Hardware cost: $2M for GPU cluster (8x H100)
- Monthly cost: $15K/month
- Inference cost: $0.50 per 1000 tokens
- Users served: 100/day

With 4-bit quantization:
- Hardware cost: $50K for powerful GPUs (2x RTX 6000)
- Monthly cost: $1K/month
- Inference cost: $0.05 per 1000 tokens (10x cheaper)
- Users served: 10,000/day

Impact:
- Cost savings: $14K/month
- Throughput: 100x more users
- Annual savings: $168,000
- Capital savings: $1.95M

ROI: Infinite (enables the product at all)
```

## How Quantization Works

### Precision Levels Explained

```
Float32 (baseline):
- Bits per value: 32
- Range: ±3.4×10^38
- Precision: Very high
- Model size: 280 GB (70B params × 4 bytes)
- Accuracy: 100% (baseline)

Float16 (half precision):
- Bits per value: 16
- Range: ±65,500
- Precision: Still good
- Model size: 140 GB (50% reduction)
- Accuracy: 98-99%

Int8 (8-bit integer):
- Bits per value: 8
- Range: -128 to 127
- Precision: Lower
- Model size: 70 GB (75% reduction)
- Accuracy: 95-98%

Int4 (4-bit integer):
- Bits per value: 4
- Range: -8 to 7
- Precision: Very low
- Model size: 35 GB (87.5% reduction)
- Accuracy: 90-95%

Comparison:
┌─────────────┬──────────────┬──────────┬───────────┐
│ Precision   │ Model Size   │ Accuracy │ Speed     │
├─────────────┼──────────────┼──────────┼───────────┤
│ Float32     │ 280 GB       │ 100%     │ Baseline  │
│ Float16     │ 140 GB       │ 98-99%   │ 1.3x      │
│ Int8        │ 70 GB        │ 95-98%   │ 2x        │
│ Int4        │ 35 GB        │ 90-95%   │ 3x        │
└─────────────┴──────────────┴──────────┴───────────┘
```

### Quantization Methods

```
Method 1: Post-Training Quantization (PTQ)
- Apply AFTER model is trained
- No retraining needed
- Speed: Fast (minutes)
- Accuracy loss: 2-5%
- Use case: Quick deployment

Method 2: Quantization-Aware Training (QAT)
- Apply DURING training
- Model learns to handle lower precision
- Speed: Slow (requires retraining)
- Accuracy loss: 1-2%
- Use case: Production quality

Method 3: Dynamic Quantization
- Compute quantization parameters per input
- Slower but better accuracy
- Use for real-time, high-accuracy requirements

Method 4: Static Quantization
- Pre-compute quantization parameters
- Faster inference
- Use for batch/offline processing
```

### The Mathematics

```
Quantization formula:
quantized_value = round((original_value - min_value) / scale) × scale

Example: Convert float32 to int8
Original weights: [-2.5, -1.2, 0.3, 1.8]
Min value: -2.5
Max value: 1.8
Range: 4.3

Scale factor: 4.3 / 255 = 0.0168

Quantization (store as int8):
-2.5 → -128 (minimum int8)
-1.2 → ((-1.2 - (-2.5)) / 0.0168) = 77
0.3 → ((0.3 - (-2.5)) / 0.0168) = 167
1.8 → 127 (maximum int8)

Result: [-128, 77, 167, 127] (8-bit integers)

Dequantization (reconstruct):
-128 × 0.0168 = -2.55 (≈ -2.5, tiny error)
77 × 0.0168 = 1.29 (vs original -1.2, acceptable error)
```

## Quantization Strategies

### Strategy 1: Symmetric Quantization

```
How it works:
- Find min and max values in weights
- Map to symmetric range [-127, 127] for int8
- Preserve zero exactly

Example:
Weights: [-3.0, -1.5, 0.0, 1.5, 3.0]
Min: -3.0, Max: 3.0
Map to [-127, 127] ← Symmetric

Pros:
- Simple to implement
- Faster computation
- Preserves zero-point

Cons:
- Can't use negative and positive ranges asymmetrically
- Wastes range if distribution is skewed

Use case: General purpose quantization
```

### Strategy 2: Asymmetric Quantization

```
How it works:
- Don't require symmetry
- Map to full range [-128, 127]
- Optimal for skewed distributions

Example:
Weights: [-3.0, -2.8, -2.5, ..., 0.2, 0.3] (mostly negative)
Min: -3.0, Max: 0.3
Map full [-128, 127] range (asymmetric)
Better precision on negative side

Pros:
- Optimal range usage
- Better accuracy for skewed data
- Smaller quantization error

Cons:
- More complex computation
- Needs zero-point offset
- Slower inference

Use case: When data distribution is skewed
```

### Strategy 3: Per-Channel Quantization

```
How it works:
- Quantize each channel/neuron separately
- Different scale factors per output neuron

Example: Linear layer output (1000 neurons)
Traditional: 1 scale factor for all 1000 outputs
Per-channel: 1000 different scale factors (one per neuron)

Benefits:
- Better accuracy (handles variation across channels)
- Minimal speed cost

Trade-off:
- Slightly larger model (store scale factors)
- Marginally slower than per-layer

Typical improvement: 1-3% accuracy gain
```

### Strategy 4: Mixed-Precision Quantization

```
How it works:
- Different layers use different precision
- Keep important layers at higher precision
- Quantize less-important layers aggressively

Example: Language model quantization
- Attention layers: Float16 (high precision)
- FFN input: Int8
- FFN output: Int4 (most quantized)
- Embeddings: Int8

Result:
- Critical layers preserved
- Overall model still compressed
- Better accuracy than uniform quantization

Use case: Production models where accuracy is critical
```

## Real-World Quantization Examples

### Example 1: Running Llama 2 70B Locally

```
Scenario: Developer wants to run Llama 2 70B on their workstation

Without quantization:
- Requirements: RTX 6000 Ada (48GB) - not enough!
- Need: 2-4x RTX 6000 or H100
- Cost: $50K+ for GPU setup
- Inference speed: 50 tokens/second

With 4-bit quantization (bitsandbytes):
- Requirements: RTX 4090 (24GB) - fits!
- Cost: $4K for single GPU
- Inference speed: 40 tokens/second (only 20% slower)
- Memory used: 20GB (comfortable)

Trade-off summary:
- Memory: 280GB → 20GB (14x reduction)
- Cost: $50K → $4K (12.5x reduction)
- Speed: 50 → 40 tokens/sec (minor impact)
- Accuracy: <1% loss

Result: Democratizes access to state-of-the-art models
```

### Example 2: Mobile Deployment

```
Scenario: Mobile app needs to run image captioning model

Float32 model:
- Model size: 500 MB
- Inference time: 2 seconds
- Memory peak: 1.2 GB
- Battery: Heavy drain (5% per inference)
- Can't fit on most phones

Int8 quantized:
- Model size: 125 MB (4x smaller)
- Inference time: 800ms (2.5x faster)
- Memory peak: 300 MB (4x less)
- Battery: Normal drain
- Fits on all phones

Trade-off:
- Size reduction: 500MB → 125MB
- Speed improvement: 2000ms → 800ms
- Accuracy: <2% loss acceptable for captions
- Battery: 1 hour more usage per charge

Impact: 10M+ app downloads possible (was impossible before)
```

### Example 3: Edge Deployment (IoT)

```
Scenario: Garbage collection company deploys waste sorter on edge devices

Original model (float32):
- Model: ResNet-152 for image classification
- Size: 230 MB
- Speed: 500ms per image
- Device: Needs 2GB RAM, 128GB storage
- Cost: $500 per edge device

Quantized (int4 + pruning):
- Model: 28 MB (8x smaller)
- Speed: 100ms per image (5x faster)
- Device: Needs 512MB RAM, 32GB storage (cheaper)
- Cost: $150 per edge device

Deployment scale:
- Without quantization: 1000 devices = $500K
- With quantization: 1000 devices = $150K + $350K savings
- Annual savings: Maintains efficiency with 65% cost reduction

Result: Makes edge AI economically viable
```

### Example 4: High-Throughput Inference Server

```
Scenario: Cloud API serving 10,000 concurrent requests

Float32 approach:
- Batch size: 4 (memory limited)
- Throughput: 100 requests/second
- Latency: 200ms
- Cost: 32 A100 GPUs = $50K/month

Int8 quantization:
- Batch size: 16 (4x more due to 4x memory savings)
- Throughput: 400 requests/second
- Latency: 50ms (less queueing)
- Cost: 8 A100 GPUs = $12.5K/month

Impact:
- Throughput: 4x improvement
- Latency: 4x improvement
- Cost: 75% reduction
- Can serve 10M customers/month instead of 2.5M

Annual savings: $450,000
```

## Quantization Best Practices

### Best Practice 1: Choose the Right Precision

```
Decision tree:

Is accuracy-critical (medical, finance)?
├─ Yes → Use float16 or 8-bit
└─ No  → Try int8 or int4

Is inference speed critical?
├─ Yes → Use int4 or int8
└─ No  → Float16 acceptable

Device memory limited?
├─ <8GB → int4 essential
├─ 8-16GB → int8 good, int4 works
└─ >16GB → float16 acceptable

Target accuracy ≥95%?
├─ Yes → int8 or float16
└─ <95% → int4 acceptable (5% loss ok)

Recommended:
- General: int8 (20% memory reduction, 1-2% accuracy loss)
- Aggressive: int4 (87% reduction, 5-10% loss)
- Production: float16 + selective int8 (hybrid)
```

### Best Practice 2: Calibration Strategy

```
Calibration = Finding optimal quantization parameters

Data selection (minimize representative error):

1. Random calibration:
   - Use random subset of data
   - Fast but potentially suboptimal
   - Use when data access is limited

2. Entropy-based:
   - Pick samples that maximize information
   - Better accuracy but slower
   - Recommended for most cases

3. Percentile-based:
   - Use distribution's extreme values
   - Good for outlier handling
   - Robust for edge cases

Example:
# Random calibration
calibration_data = random.sample(dataset, 1000)

# Entropy-based (recommended)
calibration_data = select_high_entropy_samples(dataset, 1000)

# Result: Same model, better accuracy from better calibration
```

### Best Practice 3: Layer-Wise Analysis

```
Monitor accuracy impact by layer:

Layer          │ Weight Range │ Quantization │ Accuracy Impact
───────────────┼──────────────┼──────────────┼─────────────────
Embedding      │ [-2, 2]      │ int8         │ <0.5% (safe)
Attention Q/K  │ [-10, 10]    │ int8         │ 1-2% (ok)
Attention V    │ [-20, 20]    │ int4         │ 2-3% (consider)
FFN input      │ [-5, 5]      │ int8         │ <1% (safe)
FFN output     │ [-50, 50]    │ int4         │ 3-5% (risky)
Prediction     │ [-100, 100]  │ float16      │ <0.1% (keep)

Strategy:
- Keep first/last layers at higher precision
- Quantize middle layers aggressively
- Test each layer's sensitivity

Result: Optimal compression with minimal accuracy loss
```

### Best Practice 4: Testing & Validation

```
Quantization validation workflow:

1. Quantize model
quantized_model = quantize(model, bits=8)

2. Test on benchmark
accuracy_quantized = evaluate(quantized_model, benchmark)
accuracy_original = evaluate(model, benchmark)
accuracy_loss = accuracy_original - accuracy_quantized

3. Check accuracy loss
if accuracy_loss < 2%:
    print("Acceptable quantization")
elif accuracy_loss < 5%:
    print("Try selective quantization")
else:
    print("Try higher precision or fine-tuning")

4. Benchmark speed/memory
memory_reduction = 1 - (size_quantized / size_original)
speed_improvement = latency_original / latency_quantized

5. Decision
if accuracy_loss < threshold AND speed > 2x:
    deploy_quantized()
else:
    try_different_precision()
```

## Common Mistakes

❌ **Quantizing without testing accuracy** — Silent degradation discovered by users
❌ **Uniform quantization for all layers** — Losing too much accuracy unnecessarily
❌ **Not using calibration data** — Suboptimal quantization parameters
❌ **Forgetting about outliers** — Few extreme values destroy quantization quality
❌ **Quantizing before validation** — Can't revert if accuracy too bad
❌ **Not measuring end-to-end** — Focused on model accuracy, ignore application impact
❌ **Over-aggressive quantization** — int4 for everything causes 10%+ accuracy loss

## Pro Tips

**Tip 1:** Start with int8 (good default, 75% memory reduction)
**Tip 2:** Use bitsandbytes or AutoGPTQ (easiest implementations)
**Tip 3:** Test on your actual data, not just benchmark
**Tip 4:** Keep first layer at float16 (embedding quality matters)
**Tip 5:** Quantize middle layers aggressively, last layer at float16
**Tip 6:** Use mixed precision for critical models
**Tip 7:** Combine quantization + pruning for 90%+ compression
**Tip 8:** Profile actual inference speed (sometimes faster on GPU, not CPU)
**Tip 9:** QLoRA for efficient fine-tuning of quantized models
**Tip 10:** Monitor production accuracy metrics after deployment

## The Bottom Line

- **Quantization trades minor accuracy for major efficiency**
- **4-8x memory reduction, 2-4x speed improvement typical**
- **Int8 is default (75% compression, 1-2% accuracy loss)**
- **Enables running billion-parameter models on consumer hardware**
- **Critical for edge deployment and cost reduction**
- **Requires careful calibration and layer-wise analysis**

---

**Series:** AI Concepts Explained Simply | **Concept #31:** Model Quantization Techniques
**Previous:** Batch Processing & Async Inference | **Mistral Studio:** https://console.mistral.ai
