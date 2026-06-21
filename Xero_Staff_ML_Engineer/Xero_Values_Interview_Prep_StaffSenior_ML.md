# Xero Values Interview – Prep Guide
### Staff / Senior Machine Learning Engineer · AI Products (Data & Science)
**Interviewers:** Bryce Larson & Peter Hsu (Engineering Managers – Machine Learning)

---

## How to use this guide

This is a **behavioural / values interview**, not a coding round. The two Engineering Managers are assessing culture fit, leadership scope, judgement, and how you've lived Xero's values — *not* algorithms.

Xero's four current values (from Xero's careers site) are:

| Value | What it means |
|---|---|
| **We make it beautiful** | Creating experiences that customers love — quality, craft, simplicity |
| **We make it happen** | Moving fast on the *right* things to deliver value — decisiveness, ownership, prioritisation |
| **We make it human** | Caring personally and challenging respectfully — empathy, feedback, inclusion, wellbeing |
| **We make it together** | Collaborating to create a positive impact — cross-functional work, influence, knowledge sharing |

**Important:** the answers below are *model templates* built around realistic Staff/Senior ML scenarios drawn from the job descriptions (ML infra on Python/MLflow/TensorFlow/PyTorch, Airflow/Prefect orchestration, Spark/Dask, AWS EMR, real-time serving, LLM features, mentoring, cross-team standards). **Do not memorise them verbatim.** Swap in your *real* stories — interviewers can tell fabricated examples instantly, and Xero specifically values authenticity ("willing to be vulnerable, sharing our fears, failures and learnings"). Use these as a structure and a quality bar.

**STAR reminder:** **S**ituation (context, brief) → **T**ask (your responsibility) → **A**ction (what *you* did — most of the answer) → **R**esult (outcome, ideally quantified + what you learned).

A few tips specific to Staff/Senior level: lead with **scope** (cross-team, not just your own squad), show you can **influence without authority**, and always close with **measurable impact** and a **learning**.

---

# VALUE 1 — WE MAKE IT BEAUTIFUL
*Creating experiences customers love; quality, craft, and simplicity*

### Q1. Tell me about a time you raised the quality bar on a piece of work, even when "good enough" would have shipped.

**Situation:** Our team was about to ship a churn-prediction model behind a customer-facing insights panel. It hit the accuracy target, so most of the squad considered it done.
**Task:** As the senior engineer reviewing the release, I was responsible for whether it genuinely deserved to reach millions of users.
**Action:** I spent a day probing the edge cases and found the model performed well on average but badly on newly-onboarded small businesses — exactly the users who most needed early guidance. Rather than block the release outright, I quantified the gap, showed the segment-level error rates to the team and PM, and proposed a two-day fix: a fallback heuristic for low-data accounts plus a clear "still learning about your business" UI state. I paired with a junior engineer to implement it so they'd learn the technique.
**Result:** We shipped two days later with no embarrassing predictions for vulnerable users, and the "still learning" pattern was adopted as a team standard for cold-start cases. The lesson I carry: "beautiful" isn't average accuracy — it's the experience of the worst-served user.

### Q2. Describe a time you simplified something complex for the end customer.

**Situation:** We were surfacing cash-flow forecasts to small business owners, but early feedback showed people found the output confusing — too many numbers, confidence intervals they didn't understand.
**Task:** I owned the model-to-product interface and wanted the insight to feel effortless, not intimidating.
**Action:** I sat in on three customer research sessions instead of relying on second-hand feedback. I realised the model's statistical richness was the problem, not a feature. I worked with design and the applied scientist to collapse the output into a single plain-language statement ("You're likely to be short on cash in early March") with an optional drill-down. Technically, I had to add calibration so the confidence threshold for showing a warning was trustworthy, because a simple message with a wrong call would erode trust fast.
**Result:** Comprehension in follow-up testing improved markedly and engagement with the insight roughly doubled. It reinforced for me that craft in ML is often *removing* sophistication from what the user sees while keeping rigour underneath.

### Q3. Tell me about a time you cared about a detail that others thought was unimportant.

**Situation:** During an LLM-powered feature that drafted text for small business owners, the team was focused on response quality, but I noticed latency spikes producing 6–8 second waits perhaps 5% of the time.
**Task:** No one had flagged it because average latency looked fine, but I felt the occasional long wait would quietly damage trust.
**Action:** I instrumented p95/p99 latency rather than averages, traced the spikes to cold model-server instances and an un-batched retrieval call, and proposed warm pools plus request batching. I made the case with a short demo showing how an 8-second wait *feels* versus a 1-second one, which landed far better than a metrics table.
**Result:** p99 dropped under 2 seconds. More importantly, "measure tail latency, not averages" became part of how the team evaluated every serving change. Small, invisible details are exactly where customer-loved experiences are won or lost.

### Q4. Give an example of when you pushed back on a feature or shortcut because it would hurt the customer experience.

**Situation:** Under deadline pressure, there was a proposal to ship a recommendation model that re-used a feature pipeline known to have stale data refreshed only weekly.
**Task:** I needed to weigh delivery speed against the experience of users getting outdated recommendations.
**Action:** Rather than just say no, I quantified the harm — roughly what fraction of recommendations would be visibly wrong for active users — and offered an alternative: ship to a low-risk segment first with daily refresh, and fast-follow the pipeline fix. I framed it around the customer, not engineering purity, which kept the PM on side.
**Result:** We shipped on time to the safe segment, fixed the pipeline within the sprint, then rolled out fully. We avoided a launch that would have generated support tickets and trust erosion. I learned that "pushing back" lands best when you arrive with a costed alternative, not just an objection.

### Q5. Tell me about a time you improved the craft or engineering quality of something behind the scenes that customers never directly saw.

**Situation:** Our model evaluation was ad hoc — scientists ran notebooks, results lived in chat threads, and reproducing a past result was painful.
**Task:** As a senior engineer I felt this invisibly threatened quality, even if no customer saw it.
**Action:** I introduced standardised evaluation harnesses logged through MLflow, with versioned datasets and a shared metrics dashboard. I didn't mandate it; I built it for one project, showed how it caught a silent regression, then offered to help others adopt it.
**Result:** Within a quarter, three teams used it; reproducing any past evaluation went from hours to minutes, and we caught two regressions before release. The customer never saw the harness, but they felt it in fewer bad predictions. Beautiful systems underneath produce beautiful experiences on top.

### Q6. Describe a situation where you balanced technical elegance against shipping something usable.

**Situation:** I was designing a feature store and was tempted by an elegant, fully generic abstraction that would handle every future use case.
**Task:** I had to deliver something the team could use *this quarter*, not a perfect framework.
**Action:** I deliberately scoped down to the three feature types we actually used, built those cleanly, and documented clear extension points for later. I resisted my own instinct to over-engineer by writing down the YAGNI cases explicitly and reviewing them with a peer.
**Result:** We shipped in six weeks instead of a projected three months; two of the "future" cases I'd have built were never needed. The discipline of choosing usable-and-clean over elegant-and-theoretical is something I now actively coach juniors on, because over-engineering is a common trap for strong engineers.

### Q7. Tell me about feedback you received on quality or craft that changed how you work.

**Situation:** Early in a senior role, a manager told me my code was excellent but my documentation assumed too much context, making my work hard for others to build on.
**Task:** I had to accept that "beautiful" work that only I can maintain isn't beautiful — it's a bottleneck.
**Action:** I started writing design docs *before* implementation, added "why" comments (not just "what"), and asked a junior to review my docs specifically for clarity. I treated their confusion as a signal about my writing, not their ability.
**Result:** Code review cycles on my work got noticeably faster, and two engineers later told me my design docs were what helped them ramp. I genuinely changed my definition of quality to include "legible to others." That feedback reshaped my whole approach to senior work.

### Q8. How have you ensured an ML system was reliable and trustworthy in production, not just accurate in a notebook?

**Situation:** A model that performed beautifully offline degraded within weeks in production due to data drift no one was monitoring.
**Task:** I owned making our serving reliable, not just our training accurate.
**Action:** I built drift and data-quality monitoring into the serving path, set up automated alerts on input distribution shifts and prediction-distribution changes, and added a shadow-deployment step so new models were validated on live traffic before taking real load. I also wrote a lightweight runbook so on-call engineers could roll back confidently.
**Result:** We caught the next drift event within a day instead of weeks, and rollbacks went from a scary manual process to a routine one. The experience cemented my view that an ML system's "quality" is measured in production over time, not by a single offline metric.

---

# VALUE 2 — WE MAKE IT HAPPEN
*Moving fast on the right things; decisiveness, ownership, prioritisation, accountability*

### Q9. Tell me about a time you had to prioritise ruthlessly under constraints. How did you decide what *not* to do?

**Situation:** Going into a quarter, my squad had a backlog of fifteen "important" ML infrastructure improvements but capacity for maybe four.
**Task:** As the senior engineer I was expected to drive prioritisation, not just contribute to it.
**Action:** I mapped each item against two axes: customer/business impact and risk-of-not-doing-it. I made the trade-offs explicit in a one-page doc and reviewed it with the EM and PM so the *cuts* were visible and agreed, not silent. I deliberately deprioritised an elegant refactor I personally wanted to do because its impact was low.
**Result:** We delivered the four highest-leverage items, including a serving-cost reduction that paid for itself. Just as importantly, the team understood *why* the other eleven waited, which reduced the usual anxiety about dropped work. Prioritisation is mostly about making the "no" list legible and defensible.

### Q10. Describe a time you made a decisive call with incomplete information.

**Situation:** A production model started returning degraded predictions during peak hours, and we couldn't immediately tell whether it was a data issue, a serving issue, or a genuine model problem.
**Task:** I was the most senior engineer online and had to act before a full diagnosis.
**Action:** Rather than wait for certainty, I made a reversible decision: roll back to the previous model version to stop customer impact immediately, *then* investigate. I communicated the call clearly in the incident channel with my reasoning so no one was confused. We later traced it to a corrupted feature batch.
**Result:** Customer impact was contained within about twenty minutes. The investigation that followed was calmer because the bleeding had stopped. My principle: when impact is live, prefer a fast reversible decision over a slow perfect one — and make the reasoning visible.

### Q11. Tell me about a time you took ownership of something that wasn't strictly your responsibility.

**Situation:** A data pipeline owned by an adjacent team kept failing overnight, and our models silently trained on incomplete data as a result.
**Task:** It wasn't my pipeline, but it was my models' quality on the line.
**Action:** Instead of just filing a ticket and waiting, I dug into their Airflow DAG, identified the flaky upstream dependency, and brought a proposed fix to the owning team rather than a complaint. I offered to pair with them on it. I also added a data-completeness check on our side so we'd fail loudly instead of silently.
**Result:** The pipeline stabilised, and the two teams set up a shared on-call understanding for cross-boundary failures. Ownership at senior level means owning the *outcome* (good models) even when the cause sits outside your formal remit — while respecting the other team's ownership of their system.

### Q12. Give an example of managing technical debt. How did you decide when to pay it down versus live with it?

**Situation:** Our model-deployment tooling had grown into a tangle of bespoke scripts that slowed every release and was a frequent source of errors.
**Task:** I had to decide whether to invest in a rebuild or keep shipping features.
**Action:** I didn't argue for a big-bang rewrite. I quantified the debt — engineer-hours lost per release and error rates — to make it concrete for stakeholders. Then I proposed incremental "boy-scout" improvements alongside feature work, plus one focused refactor of the riskiest component. I tracked the debt explicitly in our backlog so it stayed visible.
**Result:** Release time dropped roughly by half over two quarters without ever stopping feature delivery. The lesson: debt decisions need data and incrementalism, not heroics. I now coach the team to *measure* debt so the conversation is about evidence, not opinion.

### Q13. Tell me about a time you delivered something faster by cutting the right scope (not the wrong corners).

**Situation:** Leadership wanted an LLM-based feature for a major customer event, on a tight timeline.
**Task:** I had to deliver something genuinely valuable without compromising safety or quality.
**Action:** I separated "must-have" from "nice-to-have." The must-have was reliable, safe, well-evaluated output for the top three use cases. The cuts were the long tail of edge cases and a custom fine-tune we didn't need yet — I used a well-prompted base model with retrieval instead. I made the scope cuts explicit and got sign-off so no one was surprised.
**Result:** We shipped on time with a feature that worked well on the cases that mattered, and the "deferred" items were prioritised properly afterward based on real usage. Speed came from cutting scope deliberately, never from skipping evaluation or safety.

### Q14. Describe a time a project of yours failed or didn't deliver what you hoped. What did you do?

**Situation:** I led an effort to replace a rules-based system with an ML model, confident it would outperform. In production it barely matched the baseline and added latency.
**Task:** I had to own the outcome honestly and decide what to do.
**Action:** I didn't bury it. I ran an honest retro, presented the data showing the model wasn't worth its complexity, and recommended we revert and keep the simpler system. I documented *why* it failed — the signal wasn't as learnable as I'd assumed — so the team wouldn't repeat it. I took accountability rather than blaming data or timelines.
**Result:** We avoided maintaining a complex system for no gain, and the write-up later stopped another team going down the same path. Xero values sharing failures and learnings, and this is one I share openly — being wrong cheaply and visibly is far better than being wrong expensively and quietly.

### Q15. Tell me about a time you had to balance research flexibility with production reliability.

**Situation:** Applied scientists needed freedom to experiment, but their experimental code kept leaking into production paths and causing instability.
**Task:** As the ML engineer bridging research and production, I had to enable both.
**Action:** I designed a clear boundary: a flexible experimentation environment with loose constraints, and a hardened production path with strict interfaces, testing, and review. I built harnesses that let scientists hand models over without rewriting everything, so the boundary helped rather than hindered them.
**Result:** Experiment velocity stayed high while production incidents from research code essentially stopped. The scientists actually preferred it because they no longer feared breaking production. Making it happen at scale means designing the system so the fast path and the safe path don't fight each other.

### Q16. Give an example of when you had to say no to a stakeholder or push back on a deadline.

**Situation:** A senior stakeholder wanted a model in production within two weeks, but we hadn't validated it for fairness across customer segments.
**Task:** I had to protect quality without being obstructive.
**Action:** I acknowledged the urgency genuinely, then laid out the specific risk — untested segment performance reaching real businesses — and offered a concrete alternative: a two-week limited rollout to validate, full launch a fortnight later. I framed it as protecting *their* goal (a successful launch) rather than blocking it.
**Result:** They agreed; the staged rollout surfaced a real issue with one segment that we fixed before broad release, avoiding a public misstep. I've learned that "no" lands far better as "yes, and here's the safer path to what you actually want."

### Q17. Tell me about a time you drove a decision that was technically unpopular but right.

**Situation:** The team favoured adopting a trendy new ML framework. I believed it would add operational risk for marginal benefit on our workloads.
**Task:** As a senior voice I had to advocate for the less exciting choice without dismissing people's enthusiasm.
**Action:** I ran a small, time-boxed bake-off comparing it against our existing stack on our actual data and serving constraints, and shared the results transparently — including where the new tool *was* better. The data showed the operational cost outweighed the gains for us right now.
**Result:** The team agreed to defer adoption and revisit when our needs changed. Because the decision was evidence-based and I'd genuinely engaged with the appeal of the new tool, no one felt overruled. Decisiveness backed by a fair, transparent experiment beats decisiveness by seniority.

### Q18. How do you decide what to build versus buy versus reuse?

**Situation:** We needed vector search for an LLM retrieval feature and the team's instinct was to build it ourselves.
**Task:** I had to make a principled build/buy call.
**Action:** I framed it around our differentiation: vector search wasn't where we added customer value, so building it would be undifferentiated heavy lifting. I evaluated managed options against our scale, cost, and data-governance requirements, documented the trade-offs, and recommended a managed service with an abstraction layer so we could swap later.
**Result:** We shipped the feature months sooner and kept engineering focus on the model and product experience that actually differentiated us. My rule of thumb: build where you're differentiated, buy or reuse where you're not — and always keep an exit ramp.

### Q19. Tell me about a time you improved velocity for the whole team, not just yourself.

**Situation:** Every engineer was setting up training environments differently, causing "works on my machine" failures and slow onboarding.
**Task:** I wanted to remove friction for everyone, not optimise my own setup.
**Action:** I built a standardised, containerised development and training environment with sensible defaults, documented it, and ran a short session walking the team through it. I made adoption easy by ensuring it solved real pains people already complained about.
**Result:** New-engineer onboarding to a first training run dropped from days to hours, and environment-related failures largely disappeared. The multiplier effect of fixing a shared bottleneck is exactly the kind of leverage I think a Staff engineer should be hunting for.

### Q20. Describe a time you had to recover from a production incident. What was your role?

**Situation:** A model-serving deployment caused elevated error rates affecting a customer-facing feature during business hours.
**Task:** I was incident lead and had to coordinate the response while keeping people calm.
**Action:** I focused first on mitigation (rolled back to restore service), kept a clear timeline in the incident channel, and assigned roles so we weren't all debugging the same thing. After service was restored, I ran a blameless post-mortem focused on the system gaps — missing pre-deploy validation — not individuals.
**Result:** Service was restored quickly, and the post-mortem produced concrete safeguards (a mandatory shadow-test gate) that prevented recurrence. I'm a strong believer that how you handle an incident — calm, blameless, systemic — sets the team's whole engineering culture.

---

# VALUE 3 — WE MAKE IT HUMAN
*Caring personally and challenging respectfully; empathy, feedback, inclusion, wellbeing*

### Q21. Tell me about a time you mentored a junior engineer. How did you adapt to them?

**Situation:** A junior ML engineer joined my squad strong on modelling but anxious and quiet in technical discussions.
**Task:** I wanted to grow their capability *and* their confidence, not just delegate tasks.
**Action:** I paired with them weekly, but rather than giving answers I asked questions that let them reach conclusions themselves. I deliberately created low-stakes opportunities for them to present work, and gave specific, kind feedback privately first. I also shared my own past mistakes so failure felt normal, not shameful.
**Result:** Within a few months they were leading a workstream and speaking up confidently in reviews; one of their suggestions improved our retraining cadence. Caring personally meant meeting them where they were emotionally, not just technically. Watching someone grow like that is, honestly, the part of senior work I value most.

### Q22. Describe a time you gave someone difficult feedback. How did you do it?

**Situation:** A talented peer was producing great individual work but dominating design discussions, which was shutting down quieter voices.
**Task:** I needed to raise it directly without damaging the relationship — "specific, direct and kind."
**Action:** I spoke to them privately, led with genuine appreciation for their contributions, then described the specific behaviour and its effect ("in yesterday's review, two people's ideas didn't get aired") rather than labelling them. I asked how they saw it and offered a concrete suggestion: actively inviting others in. I checked my own perception wasn't unfair before raising it.
**Result:** They were initially surprised but grateful, and consciously started drawing others out — meetings became noticeably more inclusive. The relationship stayed strong precisely because the feedback was caring *and* candid. Xero's "care personally and challenge directly" framing is exactly how I try to operate.

### Q23. Tell me about a time you received difficult feedback. How did you respond?

**Situation:** A peer told me in a retro that my pace in meetings sometimes steamrolled people who needed more time to think.
**Task:** My instinct was to defend myself, but I wanted to actually grow.
**Action:** I sat with it instead of reacting, asked for a specific example, and recognised they were right. I started consciously pausing, asking quieter colleagues for their view directly, and sometimes circulating proposals in writing beforehand so async thinkers could contribute.
**Result:** Several teammates later said discussions felt more open, and I genuinely make better decisions now because I hear more views. I try to model receiving feedback gracefully, because juniors watch how seniors take criticism — if I get defensive, they learn to hide their feedback.

### Q24. Give an example of when you supported a teammate who was struggling or burning out.

**Situation:** A teammate was visibly overloaded heading into a release, working late and making uncharacteristic errors.
**Task:** I cared about both the release and the person — and the person came first.
**Action:** I checked in privately and non-judgementally, asked how they were doing rather than about the work, and listened. It turned out they'd taken on too much and felt unable to say no. I helped them re-prioritise, took two items off their plate myself, and flagged the capacity issue to our EM without throwing them under the bus.
**Result:** They got breathing room, the quality of their work recovered, and the release still landed. They later said it mattered that someone noticed. Wellbeing isn't separate from delivery — a burnt-out engineer ships worse code. Looking out for each other is part of the job.

### Q25. Tell me about a time you worked to make a discussion or team more inclusive.

**Situation:** In a globally distributed team, our design discussions happened in synchronous meetings that disadvantaged colleagues in distant time zones and non-native English speakers.
**Task:** I wanted everyone's perspective in decisions, not just the loudest voices in the dominant time zone.
**Action:** I shifted important design decisions to an async-first model — written proposals with a comment window — so people could contribute thoughtfully in their own time and language at their own pace. I also rotated meeting times and made sure to explicitly solicit views from quieter members.
**Result:** We started getting substantive input from colleagues who'd previously been silent, and several decisions improved as a result. Inclusion isn't only the right thing — diverse perspectives demonstrably produced better engineering decisions. In a global team like Xero's, this is essential rather than optional.

### Q26. Describe a time you assumed good intent in a tense situation.

**Situation:** Another team made a change that broke our model pipeline without warning, and my first reaction was frustration.
**Task:** I had to resolve it without poisoning the relationship.
**Action:** Instead of firing off an angry message, I assumed they hadn't realised the downstream impact — which was almost certainly true. I reached out calmly, explained the impact, and asked if we could set up a heads-up mechanism for changes affecting consumers of their data. I focused on the system gap, not blame.
**Result:** They were apologetic and we jointly set up a change-notification process. Had I attacked, we'd have spent energy on defensiveness instead of fixing the actual problem. Assuming good intent ("be kind and assume the best") almost always de-escalates and gets to the solution faster.

### Q27. Tell me about a time you disagreed with someone but maintained a strong relationship.

**Situation:** I disagreed with an applied scientist about whether a complex model was worth the production cost.
**Task:** I had to challenge the approach without making it personal or dismissive of their expertise.
**Action:** I separated the person from the position — I acknowledged the modelling work was genuinely strong, and framed my concern as a shared problem ("how do we get this value at a cost we can run?"). We agreed to test a simpler variant head-to-head rather than argue in the abstract.
**Result:** The simpler model captured most of the value at a fraction of the cost, and we shipped it; the scientist and I came out of it with more mutual respect, not less. Challenging respectfully means attacking the problem together, never each other.

### Q28. Give an example of when empathy for the end user changed a technical decision.

**Situation:** We were tuning a model that flagged potential errors in a small business's accounts.
**Task:** I had to choose a precision/recall trade-off.
**Action:** I thought hard about the human on the other end — a stressed business owner, not a data point. A false positive meant needless worry and wasted time; a false negative meant a missed real error. I weighted toward higher precision for the *alerts we surfaced proactively* (don't cry wolf and erode trust) while keeping a less intrusive "things to review" surface for lower-confidence cases.
**Result:** Customer feedback on the alerts was markedly more positive, and trust in the feature held up. The technical choice flowed directly from imagining the actual person affected. Keeping the human in mind is what stops ML from being coldly optimised for a metric that doesn't match real life.

### Q29. Tell me about a time you helped someone grow who wasn't your direct report.

**Situation:** An engineer on an adjacent team kept asking me ML deployment questions and clearly wanted to move into ML engineering.
**Task:** They weren't mine to manage, but I cared about their growth and the wider org's capability.
**Action:** I offered to mentor them informally — reviewing their learning project, suggesting resources, and giving them a small real task on our team's tooling with my support. I made sure their own manager was aware and supportive so it was above board.
**Result:** They built real ML deployment skills and later moved into an ML engineering role. Lifting capability across teams, not just my own squad, is exactly the scope I think Staff/Senior engineers should operate at — and it makes the whole org stronger.

### Q30. Describe a time you had to be vulnerable or admit you didn't know something.

**Situation:** In a design review for a distributed training setup, a junior asked a question about a failure mode I genuinely didn't have a confident answer to.
**Task:** I could have bluffed, but I wanted to model honesty.
**Action:** I said plainly that I wasn't sure and that it was a good question worth investigating properly, then we worked through it together on the spot and I followed up afterward with what I'd learned. I made a point of crediting the junior for surfacing it.
**Result:** We caught a real gap in the design, and afterward a couple of people told me it made them more comfortable admitting uncertainty themselves. Seniority isn't knowing everything — it's making it safe not to. Pretending to have all the answers quietly kills a team's ability to learn.

---

# VALUE 4 — WE MAKE IT TOGETHER
*Collaborating to create positive impact; cross-functional work, influence, knowledge sharing*

### Q31. Tell me about a time you influenced a technical direction across multiple teams without formal authority.

**Situation:** Several ML teams were each building their own model-monitoring solutions, duplicating effort and creating inconsistency.
**Task:** I had no authority over the other teams but believed a shared approach would help everyone.
**Action:** I didn't try to mandate anything. I built a strong proof of concept, wrote a clear proposal showing the duplicated cost, and — crucially — went and listened to each team's specific needs first so the shared solution actually served them. I found allies on each team and let them co-own it rather than imposing my design.
**Result:** A shared monitoring approach was adopted across three teams, saving duplicated effort and giving leadership a consistent view of model health. Influence without authority comes from a compelling artifact plus genuine listening — people adopt what they helped shape.

### Q32. Describe how you've collaborated with applied scientists or researchers to get a model into production.

**Situation:** A scientist had a promising model in a notebook that needed to become a reliable production service.
**Task:** As the ML engineer, my job was to bridge research and production safely.
**Action:** I partnered with them early rather than waiting for a "handover." I built an interface and harness that let them keep iterating on the model while I hardened the serving, testing, and monitoring around it. I translated production constraints (latency, cost, reproducibility) into terms that helped them make better modelling choices, and I learned enough of their domain to be a real collaborator.
**Result:** The model reached production smoothly with good reliability, and the scientist became a repeat collaborator because the process respected their work. The JD describes exactly this partnership; I think the magic is engaging during research, not after it.

### Q33. Tell me about a time you communicated a complex technical idea to a non-technical audience.

**Situation:** I needed buy-in from product and business stakeholders to invest in an expensive ML infrastructure upgrade.
**Task:** They didn't care about distributed-systems internals; they cared about outcomes.
**Action:** I dropped the jargon and framed it in their terms: the current system limited how fast we could ship AI features and risked outages affecting customers. I used a simple analogy and one clear chart linking the investment to delivery speed and reliability, and I tied it explicitly to customer impact.
**Result:** I got the investment approved. The lesson I apply constantly: translate technical work into the audience's currency — for product it's customer value and speed, for finance it's cost and risk. The same idea needs a different language for each room.

### Q34. Give an example of when you shared knowledge to lift the wider team.

**Situation:** I'd developed effective practices for evaluating and deploying LLM features, but that knowledge lived in my head.
**Task:** I wanted to spread it so the team wasn't dependent on me.
**Action:** I ran a hands-on internal workshop, wrote a concise playbook covering evaluation, prompt management, and safety checks, and made it a living document others could extend. I deliberately encouraged people to improve it rather than treating it as mine.
**Result:** Other engineers started shipping LLM features confidently without me as a bottleneck, and the playbook became a team reference that newcomers used to ramp up. Knowledge hoarded is a single point of failure; knowledge shared is leverage. At senior level, making yourself non-essential to specific knowledge is a feature, not a threat.

### Q35. Tell me about a time cross-functional collaboration led to a better outcome than you'd have reached alone.

**Situation:** I was designing an ML feature and had a technically clean plan, but looped in design and a PM early.
**Task:** I wanted the best outcome, not just my outcome.
**Action:** In those conversations, design revealed that my "clean" output format would confuse users, and the PM surfaced a regulatory constraint I hadn't known about. Rather than defend my plan, I reworked the design with their input. It meant more engineering work but a genuinely better feature.
**Result:** We shipped something more usable and compliant than my original would have been, and avoided a costly rework later. It reinforced that the best engineering decisions are rarely made in an engineering vacuum — pulling other disciplines in early is how you "make it together."

### Q36. Describe a disagreement between teams that you helped resolve.

**Situation:** Our team and a platform team disagreed on who should own a shared data pipeline, and it was causing friction and dropped responsibilities.
**Task:** I wanted a resolution that served the customer, not a turf win.
**Action:** I brought both sides together and reframed the conversation away from "whose job is it" toward "what does the customer need and what's the cleanest ownership model to deliver it reliably?" I proposed a clear boundary with explicit interfaces and a shared on-call understanding for the seam.
**Result:** We agreed on ownership, the dropped-responsibility gaps closed, and the relationship between teams improved. Reframing turf disputes around shared customer outcomes almost always dissolves them — most conflict is about unclear interfaces, not genuinely opposed goals.

### Q37. Tell me about a time you built consensus on a contentious technical decision.

**Situation:** The team was split on whether to standardise on Airflow or Prefect for orchestration, and the debate was going in circles.
**Task:** As a senior voice I needed to get us to a decision without a winner-takes-all fight.
**Action:** I structured the decision: we agreed on the criteria that mattered (reliability, team familiarity, ecosystem fit) *before* arguing options, which depersonalised it. I ran a small spike on the contentious points and documented findings. Then I facilitated a decision against the agreed criteria.
**Result:** We reached a clear, well-understood decision that stuck, and people who'd preferred the other option still supported it because the process was fair. Agreeing on criteria before options is my go-to technique for turning a heated debate into a solvable problem.

### Q38. How do you keep a globally distributed team aligned?

**Situation:** Our AI Products team spanned several time zones, and alignment was slipping — people occasionally worked at cross purposes.
**Task:** I wanted shared context without forcing everyone into painful meeting times.
**Action:** I leaned into async-first practices: clear written design docs, decisions recorded in a single discoverable place, and concise written updates rather than relying on synchronous meetings. I made sure context wasn't trapped in any one time zone's conversations and used overlap hours only for genuine discussion.
**Result:** Alignment improved measurably and people felt less excluded by geography. Working effectively across time zones is a core skill for a team like Xero's; the key is treating written, discoverable communication as the default and synchronous time as a scarce resource for real collaboration.

---

# ROLE-SPECIFIC & CLOSING QUESTIONS
*Motivation, Staff/Senior scope, and culture fit*

### Q39. Why Xero, and why this role specifically?

**Situation:** I've spent my career building ML systems, and I've reached a point where I want my impact to be both technically deep and genuinely meaningful.
**Task:** I was looking for a role where I could set technical direction *and* believe in the mission.
**Action:** I was drawn to Xero because the AI Products group sits right at the intersection of research and production I find most rewarding — turning models into products that serve millions — and because the mission of making life better for small businesses is one I care about; small businesses are the backbone of the economy and they're underserved by good software. The Staff/Senior scope — raising the engineering bar, mentoring, setting standards across teams — matches where I want to grow, beyond just building things myself.
**Result:** What I'm looking for and what this role offers line up unusually well: hard technical problems (scale, reliability, LLMs) plus real human impact plus the chance to lift a whole team. That combination is genuinely rare, and it's why I'm here rather than applying broadly.

### Q40. As a Staff/Senior engineer, how do you create impact beyond your own code?

**Situation:** Earlier in my career, my impact was measured by what I personally built. At senior level I've deliberately shifted that.
**Task:** I see my job now as multiplying the team's effectiveness, not just maximising my own output.
**Action:** Concretely, I do this in a few ways: I set technical standards and patterns that make everyone's work better (shared evaluation harnesses, serving standards); I mentor so capability compounds over time; I make principled architecture decisions that ripple across teams; and I influence direction through clear proposals and listening, not authority. I consciously spend time on leverage — fixing shared bottlenecks, writing the doc that unblocks ten people — even when individual coding would feel more immediately satisfying.
**Result:** The teams I've worked on have shipped faster and more reliably, and several engineers have grown significantly under my mentorship. My measure of success at this level is the team's output and growth, not my personal commit count — and the JD's emphasis on "raising the bar" and "enabling others" is exactly how I think about the role.

---

## Final preparation checklist

- **Pick 8–10 of your *real* stories** that you can flex across multiple questions. Most of the 40 above map to a handful of strong experiences — you don't need 40 separate stories.
- **Quantify results** wherever you can (latency, cost, time saved, error reduction, people grown).
- **Lead with scope** at Staff/Senior level — cross-team impact, influence, mentoring.
- **Be authentic about failures** — Xero explicitly values vulnerability and learning. Have 2–3 genuine "what I got wrong" stories ready.
- **Mirror the language of the values** naturally ("challenge respectfully", "make it happen", "care personally") without sounding scripted.
- **Prepare 2–3 questions for Bryce and Peter** — e.g. about how the AI Products team balances research flexibility and production reliability, how they approach mentoring/growth, or what "raising the bar" looks like in practice on their team.
- **Keep answers ~2 minutes** — STAR, with most of the time on Action and a crisp Result.
