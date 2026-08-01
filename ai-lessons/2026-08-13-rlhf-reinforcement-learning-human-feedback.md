# RLHF: Reinforcement Learning from Human Feedback - Making AI Listen to You

## The Quick Answer

**RLHF = Train AI models to follow human preferences by having humans rate responses, then optimize the model to match those preferences using reinforcement learning.**

Traditional LLMs are trained on next-token prediction (predict the next word). This creates models that are good at generating text but not necessarily good at following instructions or producing helpful responses. RLHF fixes this by adding a preference layer: collect human feedback on model outputs, then use that feedback as a reward signal to fine-tune the model.

**Core concept:** Humans rate AI responses, AI learns to generate more responses like the ones humans prefer.

**Biggest win:** Models aligned with human values (ChatGPT, Claude, Llama 2)
**Easiest implementation:** Hire raters, collect data, train reward model, run PPO
**Most powerful:** Foundation for safe, helpful, honest AI systems

**Real example:** GPT-3 (base model, 72% factually wrong) → RLHF training → ChatGPT (95% accurate, follows instructions, polite).

## Why RLHF Matters

### The Problem: Base Models Don't Follow Instructions

```
Base LLM (GPT-3 before RLHF):

User: "Write a haiku about cats"
Model: "ChatGPT write haiku, but no, write poem instead, users like prose"
(Ignores instruction, outputs nonsense)

User: "Explain quantum computing"
Model: "Quantum computing is... and then the cat sat on the keyboard. Most people think cats are good at computing. Actually dogs are better. Here's the quantum..."
(Starts hallucinating, goes off-topic)

User: "What's 2+2?"
Model: "2+2 could be 4, or 5, or 22, or the sound of silence. Mathematicians debate this."
(Doesn't commit to correct answer)

Problem: Base models optimize for next-token prediction, not helpfulness
```

### The Business Impact

```
AI Customer Support System

Without RLHF (base model):
- Accuracy: 60% (often gives wrong answers)
- Customer satisfaction: 20% (frustrated, unhelpful responses)
- Refund rate: 15% (customers get bad advice)
- Cost per interaction: $5 (many need human review)
- Training cost: $50K for fine-tuning
- Time to deployment: 3 months

With RLHF:
- Accuracy: 95% (aligns with correct answers)
- Customer satisfaction: 85% (helpful, accurate responses)
- Refund rate: 2% (mostly satisfactory)
- Cost per interaction: $0.50 (minimal human review)
- Training cost: $150K (RLHF pipeline + raters)
- Time to deployment: 2 months

Impact:
- Quality: 60% → 95% accuracy (+35%)
- Satisfaction: 20% → 85% (+65%)
- Cost: $5 → $0.50 per interaction (90% reduction)
- Customer refunds: 15% → 2% (13% reduction)
- Annual savings: 1M interactions × $4.50 = $4.5M

ROI: Pays for itself in 1 month
```

## How RLHF Works

### The Process (4 Steps)

```
Step 1: Collect Human Feedback
Goal: Rate model responses

Process:
- Raters generate diverse prompts
- Run base model on each prompt (multiple outputs per prompt)
- Raters rank outputs: best → second best → worst
- Example: "Write a poem about love"
  Output A: "Love is a chemical reaction in your brain..." (rated #1 - scientific)
  Output B: "Love makes my heart sing..." (rated #2 - poetic)
  Output C: "Love is good I think maybe yes" (rated #3 - incoherent)

Scale: Collect millions of preference pairs (expensive, ~$0.01-0.05 per rating)
```

### Step 2: Train Reward Model

```
Goal: Learn to predict human preferences

Input: Two model outputs A and B
Output: Probability that A is better than B

Training data:
Prompt: "Explain photosynthesis"
Output A: "Plants take light and turn it into energy using chlorophyll..."
Output B: "Photosynthesis is when plants... uh... do stuff with sun"
Label: A > B (human rated A as better)

Repeat: 10M-100M preference pairs

Result: Reward model that can score any output on human preference scale
- Good response: high reward (+10)
- Bad response: low reward (-10)
- Mediocre response: medium reward (0)
```

### Step 3: Use Reward Model to Score Base Model Outputs

```
Goal: Generate reward signal for RL training

Process:
1. Base model generates response
2. Reward model scores it: 0.8 (pretty good) or -0.3 (pretty bad)
3. Keep score for later

Example:
Base model: "The capital of France is Paris."
Reward model: +0.95 (accurate, helpful) → High reward
Base model: "The capital of France is... probably... London?"
Reward model: -0.85 (wrong) → Low reward
```

### Step 4: Optimize Model with Reinforcement Learning (PPO)

```
Goal: Update model to maximize reward

Algorithm: Proximal Policy Optimization (PPO)

Process:
1. Base model generates response to prompt
2. Reward model scores response
3. If reward is high (+0.9): Encourage model to generate similar responses
4. If reward is low (-0.8): Discourage model from generating similar responses
5. Update model weights using gradient descent

Update rule (simplified):
if reward > threshold:
    loss = -log(probability of generated tokens)  # Encourage
else:
    loss = log(probability of generated tokens)   # Discourage

Repeat: 1-3 epochs on ~50K prompts

Result: Model learns to generate responses that maximize reward (= human preference)
```

### The Full Pipeline

```
Base LLM (trained on next-token prediction)
         ↓
    (Human feedback collection)
         ↓
Preference pairs (A preferred over B)
         ↓
  (Train reward model on preferences)
         ↓
  Reward Model (predicts human preference)
         ↓
  (Use reward model to score base model outputs)
         ↓
   Reward signals (this response scored 0.8)
         ↓
(Optimize base model using PPO on reward signal)
         ↓
RLHF-tuned LLM (aligned with human preferences)
         ↓
    ChatGPT / Claude / Llama 2
```

## RLHF Strategies

### Strategy 1: Basic RLHF Pipeline

```
Setup:
- Base model: GPT-3 (175B parameters)
- Raters: 100 humans
- Prompts: 50K diverse prompts
- Reward model: Same size as base model

Timeline:
1. Collect feedback: 2 weeks (50K prompts × 3 raters each = 150K ratings)
2. Train reward model: 1 week (on 50K preference pairs)
3. Generate outputs: 2 weeks (base model generates responses)
4. RLHF optimization: 2 weeks (PPO training)
5. Evaluation: 1 week
Total: 2 months

Cost breakdown:
- Rater labor: 150K ratings × $0.05 = $7.5K
- Compute (training reward model): $20K
- Compute (RLHF/PPO): $50K
- Infrastructure: $10K
- Total: ~$87.5K

Result: Aligned model (ChatGPT-like)
```

### Strategy 2: Iterative RLHF (Continuous Improvement)

```
Process:
Cycle 1: Collect feedback, train reward model, RLHF optimize
         ↓
Evaluate performance, identify failures
         ↓
Cycle 2: Collect more feedback on failures, update reward model
         ↓
RLHF optimize again with better reward signal
         ↓
Repeat: 3-5 cycles for continuous improvement

Benefit:
- Early cycles cheap (small datasets)
- Later cycles target specific failure modes
- Result: Better aligned model with lower total cost
- Typical improvement per cycle: 5-10% accuracy gain
```

### Strategy 3: Constitutional AI (CAI)

```
Alternative to RLHF (less human feedback needed):

Process:
1. Define constitution (set of principles)
   Example: "Be helpful. Be honest. Be harmless."
2. Model critiques own outputs against constitution
3. Model revises outputs to follow constitution better
4. Light human feedback (10x less than RLHF)

Benefit:
- 90% less rater labor
- More scalable
- Aligns with explicit principles

Trade-off:
- Slightly lower quality than full RLHF
- Requires good constitution definition
```

### Strategy 4: Mixture of Reward Models

```
Setup: Multiple reward models for different dimensions

Example (support chatbot):
- Reward Model 1: Accuracy (technical correctness)
- Reward Model 2: Helpfulness (addresses user need)
- Reward Model 3: Tone (polite, professional)
- Reward Model 4: Safety (no harmful content)

Weighted combination:
Total reward = 0.4 × Accuracy + 0.3 × Helpfulness + 0.2 × Tone + 0.1 × Safety

Benefit:
- Optimize for multiple dimensions simultaneously
- Trade-off explicit (weights) rather than implicit
- Better control over model behavior
```

## Real-World RLHF Examples

### Example 1: ChatGPT Training

```
Timeline:
Jan 2022: GPT-3 released (next-token prediction only)
         - Accuracy: 72%
         - Follows instructions: 30% of time
         - Hallucination rate: 40%

Sep 2022: RLHF training starts
         - Hire 40-80 raters
         - Collect 10,000+ preference pairs
         - Train InstructGPT (RLHF version of GPT-3)
         - Cost: ~$500K (labor + compute)

Dec 2022: ChatGPT released (InstructGPT + RLHF + additional tuning)
         - Accuracy: 95%
         - Follows instructions: 90% of time
         - Hallucination rate: 5%
         - 1M users in 5 days

Impact:
- Quality: 72% → 95% accuracy (+23%)
- Instruction following: 30% → 90% (+60%)
- User experience: Went from research tool to consumer product
- Cost: $500K one-time training cost → worth billions in market value
```

### Example 2: Llama 2 Open Source RLHF

```
Meta's approach (open source alternative to ChatGPT):

Base model: Llama 2 (13B, 70B versions)

RLHF training:
- Collected 27.5K preference annotations manually
- Trained reward model
- Used PPO to optimize model

Performance improvement:
- Instruction following: 50% → 85%
- Accuracy: 65% → 92%
- Safety: Low → High
- Training cost: ~$300K (much cheaper than ChatGPT due to smaller model)

Result: Llama 2 Chat (open source, competitive with ChatGPT)
- Downloadable, fine-tunable
- Enabled by RLHF
```

### Example 3: Constitutional AI at Anthropic

```
Scenario: Build helpful, harmless, honest AI (Claude)

Approach:
1. Define constitution (12 principles)
   - Be helpful and informative
   - Be honest and avoid deception
   - Prioritize user safety
   - Be aware of limitations
   - etc.

2. Minimal human feedback (100x less than RLHF)
   - Critique-revision pairs: 10K
   - Direct preference pairs: 10K
   - Total: vs 100K+ for traditional RLHF

3. Model learns to critique and revise own outputs
   - "This response is not helpful because..."
   - "I should revise to be more accurate..."

Result: Claude model
- Efficient training (10x cheaper RLHF)
- High quality (competitive with ChatGPT)
- Aligned with constitution (transparency)
- Cost: ~$50-100K for RLHF + CAI
```

### Example 4: E-Commerce Product Recommendation RLHF

```
Scenario: Fine-tune LLM to recommend products

Base model: Llama 2 7B
Task: "Based on customer history, recommend products"

RLHF setup:
- Raters: Product specialists
- Feedback: Rate recommendations quality (1-5 stars)
- Reward signal: User satisfaction after purchase

Process:
1. Generate 5K products recommendations
2. Collect 5K ratings (cost: $5K at $1/rating)
3. Train reward model (accuracy: 90%)
4. RLHF optimize (1 week on 8x A100)
5. Deploy

Result:
- Recommendation quality: 60% → 88% (+28%)
- Revenue per user: $100 → $120 (+20%)
- Click-through rate: 5% → 8.5% (+70%)
- Customer satisfaction: 3.2/5 → 4.1/5

ROI:
- Training cost: $15K (raters + compute)
- Monthly additional revenue: $10K × 20% = $2K
- Payback period: 7.5 months
- Annual additional revenue: $24K
```

## RLHF Best Practices

### Best Practice 1: Rater Quality & Agreement

```
Critical factor: Inter-rater agreement

Definition: How often raters agree on preference

Measurement:
- If raters disagree on which output is better → low agreement
- If raters consistently prefer same outputs → high agreement

Target: >70% agreement (raters mostly aligned)

How to achieve:
1. Clear rating guidelines (detailed rubric)
2. Train raters on task (examples + feedback)
3. Regular calibration meetings
4. Remove raters with <60% agreement
5. Use rater expertise (domain specialists for domain tasks)

Example rating rubric:
5 stars: Accurate, helpful, well-explained
4 stars: Mostly accurate, somewhat helpful
3 stars: Partially accurate, ambiguous
2 stars: Mostly inaccurate, unhelpful
1 star: Completely wrong, harmful
```

### Best Practice 2: Reward Model Quality

```
Critical: Reward model must accurately predict human preferences

Evaluation:
- Measure reward model agreement with held-out human ratings
- Target: >80% accuracy on test set

How to improve:
1. Collect more preference data (10K+ pairs minimum)
2. Use stronger model for reward model (same size or larger than base)
3. Multiple raters per sample (3+ raters, take majority vote)
4. Separate models for different domains (support vs coding vs writing)
5. Continuously update with new feedback

Red flag: Reward model accuracy <70% → RLHF will optimize for bad signal
```

### Best Practice 3: PPO Hyperparameters

```
Key hyperparameters for RLHF optimization:

Learning rate: 5e-6 to 1e-5 (very small)
- Too high: Model forgets language ability
- Too low: Slow convergence

Batch size: 64-256 (depends on GPU memory)

Gradient accumulation steps: 4-8 (effective larger batch)

PPO clip ratio: 0.2 (constrains update size)
- Prevents model from deviating too much from base model
- Maintains language quality while improving reward

Number of epochs: 1-3 on same data
- Usually 1-2 epochs best
- Prevents overfitting to reward model

Entropy penalty: 0.01-0.1
- Encourages model diversity
- Prevents collapse to single best answer

Value function coefficient: 1.0
- Balances reward optimization vs value prediction
```

### Best Practice 4: Evaluation Metrics

```
How to measure RLHF success:

1. Reward model score:
   - Mean reward on test prompts
   - Should increase by 50-100% after RLHF

2. Human evaluation:
   - Sample 200-500 responses
   - Have raters compare RLHF vs base model
   - Target: 70%+ prefer RLHF

3. Task-specific metrics:
   - Accuracy: % correct answers
   - Instruction following: % responses follow instructions
   - Safety: % responses don't contain harmful content
   - Helpfulness: % responses are useful to user

4. Automatic benchmarks:
   - MMLU: General knowledge (target >70%)
   - HumanEval: Code generation (target >50%)
   - GSM8K: Math reasoning (target >70%)

5. Regression testing:
   - Ensure base capabilities not degraded
   - Example: Math accuracy shouldn't decrease
```

## Common RLHF Mistakes

❌ **Ignoring rater agreement** — Use low-quality preferences to train reward model (cascading failures)
❌ **Overfitting to reward model** — Model optimizes reward but loses language quality
❌ **Too few preference pairs** — <10K pairs = noisy reward model
❌ **Not tuning PPO hyperparameters** — Generic settings often fail
❌ **Single dimension reward** — Can't optimize for multiple goals (accuracy + safety)
❌ **Neglecting model drift** — RLHF model diverges too much from base model
❌ **Using cheap raters** — Untrained raters give inconsistent feedback
❌ **Not evaluating on diverse prompts** — Good on training distribution, bad on new prompts

## Pro Tips

**Tip 1:** Start with Constitutional AI (cheaper) before full RLHF
**Tip 2:** Use domain experts as raters (10x better agreement)
**Tip 3:** Collect 5-10K preference pairs minimum before training
**Tip 4:** Evaluate reward model on held-out test set
**Tip 5:** Use entropy penalty to maintain output diversity
**Tip 6:** Monitor for model drift (KL divergence from base model)
**Tip 7:** Iterate: RLHF → evaluate failures → collect more feedback → RLHF again
**Tip 8:** Combine multiple reward models for multidimensional optimization
**Tip 9:** Use smaller reward model (faster inference, easier to train)
**Tip 10:** Save model checkpoints during RLHF training (often earlier = better)

## The Bottom Line

- **RLHF = Alignment via human feedback and RL optimization**
- **Base model 72% → RLHF model 95% accuracy (+23%)**
- **Powers ChatGPT, Claude, Llama 2, and modern helpful AI**
- **Scalable: Constitutional AI reduces human labor 10x**
- **Challenges: Rater quality, reward model accuracy, PPO stability**
- **Future: Automated preference signals, self-improvement loops**

---

**Series:** AI Concepts Explained Simply | **Concept #35:** RLHF - Reinforcement Learning from Human Feedback
**Previous:** Vision Transformers & Image Understanding | **Mistral Studio:** https://console.mistral.ai
