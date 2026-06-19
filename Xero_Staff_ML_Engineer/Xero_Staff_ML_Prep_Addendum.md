# Xero — Staff ML Engineer · Prep Addendum
### Self-Introduction · Gap-Handling · 20 ML-Reasoning Questions · Closing Questions

> Companion to the main prep package. This round targets the one real risk in your profile — looking *platform/infra-first* rather than *modelling-first* — and arms you to turn it into a strength honestly.

---

## 1. Self-Introduction (two versions)

**Audience:** Bryce Larson (Engineering Manager, ML) and Peter Hsu. Built to land with both engineering leadership and a technical peer. Personalise the closing line only if you genuinely know their focus.

### Version A — full (~75–90 sec)

> "I'm a Data & AI engineer with around ten years building ML systems that have to work in production, most recently as Senior Engineer for Data & AI at Bendigo and Adelaide Bank, where I built the company's ML platform from scratch in a heavily regulated environment.
>
> The thread through my career is making machine learning *reliable at scale* — not just training a model, but the harder problem of getting models to perform in production for real users: feature stores that kill train-serve skew, serving architectures with the latency and cost budgets to run for millions of calls, and the evaluation and monitoring to know when a model is quietly degrading. Lately a lot of that has been LLM and RAG systems, where I've learned that most 'the model is wrong' bugs are actually retrieval and grounding problems.
>
> What I care about most now is leverage beyond my own keyboard — setting the technical standards and paved paths that lift a whole team, and mentoring engineers into stronger ML practitioners. I led our AI enablement effort partly because I used to teach, and developing people compounds in a way shipping one more system doesn't.
>
> What drew me to this role is that Xero's AI Products group sits right at the research-meets-production seam I've spent my career on — and doing it for millions of small businesses, where the ML genuinely improves someone's day, is exactly the kind of problem I want to raise the bar on."

### Version B — concise (~40 sec, for when they say "briefly")

> "Ten years in Data & AI, most recently building Bendigo Bank's ML platform from scratch. My focus is production ML at scale — feature stores, real-time serving for millions, and lately LLM/RAG systems — and increasingly on the leverage side: setting technical standards and mentoring engineers, which is why I led our AI enablement work. Xero's AI Products group is exactly the research-meets-production problem I care about, at a scale and for a mission that matters."

**Delivery notes:** open with energy, slow down on the one ML insight (retrieval > generation), and let the mentoring line breathe — it's your strongest Staff signal. Don't list technologies like a résumé; name them only as evidence for a *capability*.

---

## 2. Handling the "this looks platform/infra, not ML" question

This is the question most likely to decide the loop. Here's how to win it — honestly.

### The mindset
Don't get defensive and don't fabricate model-building you haven't done. Instead: **(1) reframe the role**, **(2) claim the real ML work you *have* done**, and **(3) show ML reasoning live**. You have genuine ML in your history — productionised predictive/prescriptive models, MLlib work, 35% inference-time reduction through model optimisation, and end-to-end RAG/LLM systems. Lead with those plus the reasoning, and the "infra-only" frame dissolves on its own.

### Direct-answer script (use when asked outright)

> "It's a fair observation, and I'd actually frame it as a fit rather than a gap. This role, as written, is ML-infrastructure-and-services at scale — serving for millions, orchestration, LLM features, setting standards — and that's precisely the centre of my experience, not the edge of it.
>
> On the modelling side: I've productionised predictive and prescriptive models, cut model inference time 35% through optimisation, and built end-to-end RAG and multi-agent LLM systems where the hard calls are genuinely ML calls — chunking and retrieval strategy, faithfulness evaluation, calibration, handling drift. What I've deliberately specialised in is the part that's hardest and most often gets models *killed* in production: making them reliable, observable, and reproducible at scale.
>
> At Staff level I think that's the leverage point. Plenty of people can train a strong model in a notebook; far fewer can make a whole team's models trustworthy in production and bring the team's modelling practice up with them. That's the work I want to do here — and it's modelling-informed, not modelling-blind."

### Three tactics to *demonstrate* ML reasoning (so it never gets asked)
1. **Volunteer the "why" in every answer.** When you describe a system, add the model reasoning: "we used a gradient-boosted ranker over a neural model because the data was tabular and we needed sub-100ms serving and explainability for a regulated decision." That one sentence proves modelling judgement.
2. **Talk about failure modes and debugging.** Saying "most LLM errors are retrieval, not generation," or "I suspect leakage before I celebrate an offline metric" signals depth no résumé can.
3. **Bring metrics back to decisions.** "We didn't optimise accuracy under 0.1% fraud; we tuned recall-at-fixed-precision to the analyst review budget." Connecting metrics to business cost is exactly the reasoning they're checking for.

### What NOT to do
- Don't claim deep research/DL-architecture experience you don't have — a Staff ML EM will go three follow-ups deep and the floor disappears.
- Don't disparage infra work to sound more "ML." It's the role.
- Don't over-apologise. State the framing once, confidently, then redirect to evidence.

---

## 3. Twenty ML-Reasoning Questions (the gap area)

> These are the *"why"* questions that separate someone who reasons about models from someone who only runs them. Distinct from Part One's ML questions — these probe judgement and debugging. Each answer ~150 words.

**G1. Why use cross-entropy loss for classification instead of mean squared error?**
Cross-entropy is the right loss because it matches what a classifier is actually doing — estimating probabilities — and it penalises confident-but-wrong predictions far more steeply than MSE. With a sigmoid/softmax output, cross-entropy yields well-behaved gradients that stay large when the model is badly wrong, so learning doesn't stall; MSE paired with a sigmoid produces small gradients in exactly those high-error regions (the saturation problem), making training slow and prone to getting stuck. Cross-entropy is also the maximum-likelihood objective for categorical outcomes, so minimising it is principled, not arbitrary. MSE treats classification as regression onto 0/1 targets, which both mis-specifies the problem and distorts probability calibration. The practical tell I'd give a junior engineer: if you're outputting probabilities, use cross-entropy; reach for MSE only when you're genuinely predicting a continuous quantity. Choosing the loss that matches the output distribution is foundational modelling judgement.

**G2. Your model's offline accuracy went up but the business metric dropped after launch. How do you reason about that?**
This is the classic offline-online divergence, and accuracy going the "right" way while the business metric falls is a strong signal the offline metric is the wrong proxy. I'd reason through several causes. First, metric mismatch: accuracy may not reflect the decision's value — if errors are asymmetric or the action depends on a ranking or threshold, aggregate accuracy can rise while the *useful* predictions get worse. Second, distribution shift: the offline test set isn't the live population. Third, a feedback loop: the model changed user behaviour, so the metric it's judged on moved for reasons unrelated to quality. Fourth, calibration: better accuracy with worse probability calibration hurts threshold-based decisions. The lesson I'd draw and share: never trust a single offline metric — pair it with the online business metric and guardrails, and validate the *proxy* itself, because optimising a bad proxy reliably makes the product worse.

**G3. A model that performed well regressed after a routine retrain. Walk me through debugging it.**
I treat retraining regressions as a change-isolation problem: something in the inputs changed, since the code path is "the same." I'd diff the new training run against the prior one across the obvious axes. Data: did the new window include a distribution shift, a data-quality break upstream, or a label-generation change? Features: did a feature definition or upstream source silently change, introducing skew or nulls? Labels: late-arriving or noisier labels in the fresh window? Pipeline: a leakage source that inflated the *previous* model's offline score, now corrected, exposing the real performance? Randomness: high run-to-run variance from seeds/initialisation masquerading as regression. I'd compare feature distributions and evaluation slices between versions, not just the headline metric, because the regression usually hides in a subgroup. The durable fix is data and feature validation gates in the retrain pipeline so the next regression is caught before it ships.

**G4. When does adding more training data NOT help, and what do you do instead?**
More data helps a high-variance (overfitting) model, but does little for a high-bias one — if training and validation error are both high and close, the model is too simple or lacks the right features, and ten times the data won't move it. Data also won't help when it's more of the same distribution but the failures live in an underrepresented slice; you need *targeted* data there, not bulk. It won't help if labels are noisy — you'd be adding noise — or if the ceiling is set by irreducible aleatoric uncertainty in the problem itself. Instead of reflexively gathering data I'd diagnose via learning curves: flat, converged curves say invest in features, model capacity, or better labels, not volume. This reasoning matters at scale because data collection and labelling are expensive — knowing when *not* to spend on data is as valuable as knowing when to.

**G5. How do you choose precision versus recall, concretely, for a real feature?**
I anchor entirely on the cost of each error type in context. Recall matters when missing a positive is expensive: in fraud or a compliance alert, a false negative (missed fraud) can cost far more than a false positive (an extra review), so I'd favour recall and accept more reviews. Precision matters when acting on a false positive is costly or erodes trust: an auto-applied action shown to a user — say auto-categorising a transaction or pushing an alert — should be high-precision, because wrong actions destroy confidence faster than missed ones build it. I make this explicit with stakeholders, often fixing one and optimising the other ("maximise recall at 95% precision"), and tune the *threshold* to that operating point rather than defaulting to 0.5. The reasoning I'd model for the team: precision/recall isn't a math choice, it's a product and cost decision wearing a math costume.

**G6. Your model is overfitting despite heavy regularisation. What's going on?**
If regularisation isn't fixing overfitting, I question whether it's truly overfitting or actually *leakage* dressed as great training performance. First suspect: a feature that encodes the target (or a proxy available only at train time), which no amount of regularisation cures — it'll happily "learn" the leak. Second: the train/validation split is wrong (random split on temporal or grouped data), so the validation set isn't really held out and the gap is illusory or the generalisation estimate is broken. Third: data leakage through preprocessing fit on the full dataset before splitting. Fourth: the validation set is too small or unrepresentative, giving a noisy gap. Only after ruling those out would I keep pushing regularisation, simplify the model, or get more data. The instinct I'd teach: when a standard fix doesn't work, stop turning the same knob harder and question the assumption — here, "is it overfitting at all, or is it leakage?"

**G7. How do you decide whether a feature is genuinely useful or just noise?**
Importance scores alone aren't enough — a feature can look important by overfitting noise, especially high-cardinality ones. I triangulate. Permutation importance on a held-out set (shuffle the feature, measure the metric drop) is more honest than impurity-based importance. Stability: does the feature's importance hold across folds and over time, or does it flicker? Leakage check: is it suspiciously powerful? That's often a red flag, not a win. Ablation: does removing it actually hurt validation performance, or does the model just route around it? And a domain sanity check: does a human expert find it plausible? A feature that's predictive but inexplicable in a regulated finance context is a liability even if it helps. The reasoning I'd model: a feature earns its place by improving *generalisation* stably and surviving a leakage and plausibility check — not by topping an importance chart once.

**G8. Why might a deep neural network underperform gradient boosting on your data?**
Most enterprise data — transactions, customer attributes — is tabular, heterogeneous, modest in volume per task, and full of feature interactions, which is exactly gradient boosting's home turf. Trees handle mixed scales, missingness, and non-linear interactions natively and need little tuning to perform; neural nets shine on high-dimensional unstructured data (images, text, audio) where representation learning pays off, and they're data-hungry and tuning-sensitive. On a few hundred thousand tabular rows, a deep net often overfits or underperforms while costing more compute and engineering. So underperformance usually isn't a bug — it's the wrong tool for the data's structure. I'd still run a neural baseline to be sure, and reach for DL when inputs are genuinely unstructured or when I need learned embeddings of high-cardinality fields. The judgement: match model class to data structure first; don't reach for deep learning because it's fashionable.

**G9. What is probability calibration, and when does it matter more than accuracy?**
A model is calibrated when its predicted probabilities match observed frequencies — among cases it calls 0.7, about 70% are actually positive. Calibration matters more than raw accuracy whenever you *act on the probability itself* rather than just the top class: threshold-based decisions, expected-value calculations, risk scoring, or ranking where the score feeds a downstream cost trade-off. A model can have great AUC (good ranking) yet be badly calibrated, so its 0.9 means nothing reliable — fatal if you set a policy threshold on it. Causes include class rebalancing/resampling, which distorts probabilities, and some model families (e.g. boosted trees, SVMs) being inherently miscalibrated. Fixes: Platt scaling or isotonic regression on a held-out set. In finance, where probabilities often drive money decisions and need to be defensible, I treat calibration as a first-class check, not an afterthought. The reasoning: if a number drives a decision, the number has to be trustworthy.

**G10. A model's errors are high — how do you reason about whether it's a data, feature, or model problem?**
I localise systematically rather than guessing. Start with learning curves: if train and validation error are both high and close, it's bias — likely features or model capacity, not data volume. A large train-validation gap points to variance — overfitting, more data or regularisation. Then slice the errors: are they concentrated in a subgroup (a data-coverage or feature problem for that segment) or uniform (a global model/feature issue)? Inspect the worst errors by hand — patterns there often scream "missing feature" or "label noise." Check data quality and leakage before blaming the model, since both masquerade as model problems. Try a stronger and a simpler model: if a much bigger model barely helps, the ceiling is data/features, not capacity. The principle I'd teach: don't reflexively reach for a fancier model — diagnose where the error *comes from* first, because the cheapest fix is usually better data or features.

**G11. Explain how learning rate affects training and how you'd tune it.**
Learning rate sets how big a step the optimiser takes down the gradient. Too high and training oscillates, diverges, or skips good minima — loss spikes or plateaus high. Too low and training crawls, wastes compute, and can get stuck in poor local regions. It's usually the single most impactful hyperparameter. I tune it first and coarsely: a learning-rate range test (ramp it up and watch where loss starts decreasing fastest then blows up) gives a strong starting band quickly. I pair it with a schedule — warmup then decay (cosine or step) — so it's large early for fast progress and small late for fine convergence; for transformers/LLM fine-tuning, warmup is near-essential to avoid early instability. I'd also note interactions with batch size and optimiser. The reasoning I'd share: spend your first tuning budget here, because no amount of tuning elsewhere rescues a badly-set learning rate.

**G12. How do you detect and handle label noise?**
Label noise quietly caps your performance and corrupts evaluation, so I treat it as a real risk, not an edge case. Detection: train a model and inspect its highest-confidence *disagreements* with the labels — those are prime suspects for mislabels; cross-validated out-of-fold predictions that confidently contradict the label flag likely errors. Inter-annotator agreement (if multiple labellers) quantifies it. Suspiciously easy-to-fit noise or a performance ceiling well below expectations are signals. Handling: clean or re-label the highest-impact suspects (especially in the *evaluation* set — noisy test labels are worse than noisy train labels because they corrupt your judgement of everything), use robust losses less sensitive to outliers, or down-weight low-confidence labels. For weak/auto-generated labels I'd model the noise explicitly. The reasoning I'd emphasise: your model can't be more correct than your labels, so I always sanity-check label quality before trusting any metric or chasing the last few points of accuracy.

**G13. Concept drift versus data drift — how does your modelling response differ?**
Data drift is the input distribution changing while the input-to-output relationship holds; concept drift is that *relationship* itself changing (the same inputs now map to different outcomes). The distinction drives the response. For pure data drift, the model may still be valid in the regions it knows — sometimes I just need to extend coverage with data from the new region, or recalibrate. For concept drift, the learned mapping is now wrong, so retraining on recent data is essential and I may need to *forget* stale data via time-weighting or a shorter training window, since old patterns mislead. Detection differs too: data drift shows in input-distribution monitors (PSI, KS), while concept drift shows as performance decay even when inputs look stable, so I need ground-truth feedback to catch it. The reasoning: diagnosing *which* drift you have prevents the wrong fix — retraining won't help if the real issue is just coverage, and recalibration won't help if the world genuinely changed.

**G14. A model has excellent AUC but makes poor real-world decisions. Why?**
AUC measures ranking quality — the chance a random positive scores above a random negative — and a model can rank well yet decide badly for several reasons. First, the operating threshold: AUC is threshold-independent, but decisions aren't; a great ranker with a badly chosen cutoff makes poor calls. Second, calibration: AUC ignores whether 0.8 means 80%, so probability-driven decisions go wrong even with high AUC. Third, AUC under heavy imbalance is optimistic and can look strong while precision in the operating region is terrible — PR-AUC is more honest there. Fourth, the metric may not reflect the actual cost structure of decisions. Fifth, AUC is an aggregate that can hide poor performance in the subgroup that matters most. The reasoning I'd model: a single ranking metric is necessary but not sufficient — tie evaluation to the threshold, calibration, and cost of the real decision, not just to a number that looks good on a slide.

**G15. How do you reason about the right level of model complexity?**
Complexity should be the minimum that captures the real signal — no more — because every added parameter costs generalisation risk, compute, latency, and maintainability. I reason from the data and the requirements, not from what's exciting: how much labelled data do I have (more data supports more complexity), how non-linear is the true relationship, what's the latency/cost budget at serving, and how much explainability does the context (here, regulated finance) demand? I start simple — a strong baseline — and only add complexity if it buys validated, stable improvement that justifies its operational cost. Learning curves tell me whether complexity or data is the binding constraint. The "Beautiful"-value framing fits: elegance is the simplest model that solves the problem well, not the most sophisticated one I can build. The judgement I'd teach the team: complexity is a cost you pay forever in production, so make it earn its place every time.

**G16. How would you explain a model's individual prediction to a non-technical stakeholder, or for a regulated decision?**
I'd separate global from local explanation and speak in the stakeholder's terms, not the model's. Globally: "the model weighs these few factors most." Locally, for one prediction, I'd use feature attributions (SHAP-style) translated into plain drivers: "this transaction was flagged mainly because the amount and merchant were unusual for this account at this time." For a regulated decision the bar is higher — the explanation must be faithful (not a post-hoc rationalisation that doesn't reflect the model), reproducible, and logged for audit, with the model version and inputs traceable. I'd favour inherently interpretable models where the decision is high-stakes, accepting a small accuracy trade for defensibility. The reasoning I'd model: in finance, "the model said so" is never an acceptable answer — explainability is a design requirement, so I choose models and tooling that can answer "why this decision" before I optimise the last point of accuracy.

**G17. Your validation score swings a lot between runs. How do you reason about and fix it?**
High run-to-run variance means my performance estimate is unstable, so I'd first quantify it before trusting any single result. Causes: a validation set too small to estimate the metric precisely; high variance from random seeds, initialisation, or data shuffling (common with small data or deep models); an unstable training process (learning rate too high); or non-deterministic data splits. Fixes: use cross-validation and report mean ± standard deviation rather than one number, so I'm comparing distributions not lucky draws; fix seeds for reproducibility while still measuring seed sensitivity; enlarge or stratify the validation set; and stabilise training. Critically, I wouldn't pick a model or hyperparameter based on a single noisy score — that's how teams chase noise and ship worse models. The reasoning I'd emphasise: if the measurement is noisy, every decision built on it is suspect, so I invest in a stable estimate before optimising against it.

**G18. How do you choose an evaluation metric for a ranking/recommendation problem, and what are its pitfalls?**
I match the metric to how results are consumed. If users see a ranked list and position matters, NDCG (rewards relevant items near the top, with graded relevance) fits; for binary relevance, MAP or precision/recall@k; for "did they find anything useful," recall@k. Pitfalls: offline ranking metrics assume your logged relevance labels reflect true preference, but they're biased by what the *old* system showed — you only have feedback on items users saw, so the metric flatters models that mimic the incumbent (presentation/position bias). They also ignore diversity and can reward redundant top results. And offline gains routinely fail to translate to the online objective (engagement, action-rate), partly due to feedback loops. So I'd validate offline with NDCG@k but treat the online A/B on a real business metric as the arbiter, and correct for position bias where I can. The reasoning: offline ranking metrics guide iteration but don't decide — the live behavioural metric does.

**G19. How would you reason about whether to retrain a model, and how often?**
Retraining cadence should follow the data and the cost of staleness, not a calendar habit. I'd reason from how fast the world changes (concept drift rate), how quickly labels arrive, the cost of retraining and redeploying, and the risk of a stale model. Static problems may need retraining rarely; fast-moving ones (fraud, anything seasonal or behaviour-driven) need frequent or drift-triggered retraining. I prefer *triggered* retraining — fire when monitoring detects performance decay or input drift past a business-tied threshold — over fixed schedules, because schedules either waste compute or react too late. Every retrain must pass the same quality, fairness, and guardrail gates and deploy progressively with rollback, since retraining is a top source of silent regressions. The reasoning I'd model: retraining isn't free or safe — it's a change like any other, so I'd automate it behind monitoring and gates rather than treat "retrain weekly" as inherently virtuous.

**G20. How do you reason about the trade-off between model performance and inference cost/latency at scale?**
At millions of calls, cost and latency are modelling constraints, not afterthoughts — a 1% accuracy gain that doubles latency or spend usually isn't worth it, and that judgement is part of the modelling decision. I reason about it explicitly: define the latency budget (e.g. p99) and cost ceiling up front, then treat accuracy as something to maximise *within* those bounds. Levers: a smaller or distilled model on the hot path, quantisation, caching frequent predictions/embeddings, precomputing heavy features offline so only light ones run online, and routing easy cases to a cheap model with escalation only for hard ones. For LLMs, use the smallest model that clears the quality bar and retrieve rather than stuff context. I'd validate that the cheaper architecture's quality is acceptable on the slices that matter, not just on average. The reasoning I'd teach: the best production model is the one that meets the quality bar at a latency and cost the business can actually sustain — I reduced inference time 35% precisely by treating this as a design goal, not a cleanup task.

---

## 4. Questions to ask THEM at the end (Staff-level signal)

> Ask 2–3. Each is chosen to signal that you operate at Staff altitude and have read the role deeply. Adapt wording to the conversation. Don't ask anything you could have Googled.

**Closing Q1 — the JD's core tension (shows you read it and think at platform level):**
> "The role description leans hard on supporting both research flexibility and production reliability. In practice, where does the team feel that tension most right now — and where do you think a Staff engineer could move the needle, versus where it's already working well?"

*Why it lands:* it's the literal heart of the role, it invites them to be candid about real pain, and it positions you as someone who'd come in to solve *that*, not just take tickets.

**Closing Q2 — defining the level (shows you understand Staff vs Senior):**
> "For a Staff engineer here, what does 'raising the bar across teams' actually look like day to day — and how do you and the team distinguish Staff-level impact from a really strong senior engineer's?"

*Why it lands:* it signals you're thinking about leverage and influence, not scope of code, and the answer tells you exactly how to be successful and how you'll be evaluated.

**Closing Q3 — domain depth on LLMs (shows you know the real failure modes):**
> "As you explore LLM-powered features for small businesses, what's been the hardest part so far — retrieval quality, faithfulness and trust, cost at scale, or evaluation — and where do you see the biggest open problems?"

*Why it lands:* it demonstrates you already know where LLM products actually break (not the hype), and it opens a genuinely technical conversation where your RAG experience can surface naturally.

**Bonus Q4 — team & growth (use if rapport is warm, especially with the EM):**
> "What does growth look like for strong engineers on this team — and what's something the team has gotten meaningfully better at in the last year?"

*Why it lands:* signals you care about team development (your mentoring strength) and surfaces the team's trajectory and self-awareness.

**One to avoid:** don't open with comp, logistics, or "what does a typical day look like" — save those for the recruiter. Closing questions are your last impression; spend them on substance.

---

### Final reminder
Your honest story is strong: a decade of making ML *work in production*, real LLM/RAG depth, and a genuine mentoring/enablement track record — for a role that is, by its own description, ML-infrastructure-at-scale. You don't need to hide anything. You need to *reframe confidently* and *show the reasoning*. Do both and the "infra not ML" worry never gets traction.
