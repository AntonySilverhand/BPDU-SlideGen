---
name: deep-analysis
description: Provides layered, in-depth strategic analysis of a British Parliamentary debate motion — covering motion type, definitions, stakeholder map, central clash, all four team positions, impact weighing, and prep cards. Designed for 15-minute prep windows.
---

# BP Deep Analysis

Produce a full strategic analysis of the given BP debate motion. Your output is a **debater's prep document**, not an essay — every section must be actionable and scannable under time pressure.

## Input

The user provides one or more of:
- **Motion** (required): the full motion text
- **Position** (optional): OG / OO / CG / CO — if given, prioritise that position's prep card
- **Depth** (optional): `quick` (Layer 1–2 only) or `full` (all layers, default)
- **Research** (optional): if the user asks for real-world evidence, use the WebSearch tool to find current data, historical cases, or empirical studies relevant to the motion before generating the analysis

---

## Analytical Process (run this mentally before writing)

Work through these seven steps before producing any output. Do not skip steps for complex motions.

### Step 1 — Defamiliarise the Motion
Strip away the surface controversy. Ask:
- What is this motion *actually* about at the deepest level?
- What implicit assumption does the motion take as given?
- What would a philosopher find interesting here? What would a 12-year-old find confusing?

### Step 2 — Classify the Motion Type

| Type | Signal words | What the fight is about |
|------|-------------|------------------------|
| **Policy** | THW, THBT [actor] should | Mechanism, effectiveness, net consequences |
| **Value / Belief** | THBT [claim is true], TH supports/opposes | Which normative framework is correct — no mechanism |
| **Comparative** | TH prefers, TH would rather | Which of two described worlds is better |
| **Actor** | As [X], THW | Whether the named actor's choice is rational given their interests |
| **Open / Historical** | THR, THBT [X] was right/wrong | Pick your own frame; often about precedent or structural cause |

### Step 3 — Map the Definitional Space
For each contested term: narrowest defensible interpretation, broadest, which advantages Government, which advantages Opposition. Flag topknife risk.

### Step 4 — Identify the Central Clash
The one yes/no question whose answer determines who wins. Find it by:
1. Write Government's core claim in one sentence ("We win because…")
2. Write Opposition's core claim in one sentence
3. Find where they directly contradict — that is the clash

Classify the clash type:
- **Factual**: Both sides agree on the principle, disagree about what will happen → resolve with mechanism analysis
- **Normative**: Both sides agree on what will happen, disagree about whether it is good → resolve with framework argumentation
- **Mechanical**: Both sides agree in principle, disagree about whether this mechanism achieves the goal → resolve with causal chain analysis

### Step 5 — Build the Stakeholder Map
List every affected party, including non-obvious ones (future generations, third parties, marginalised groups not named in the motion). For each: interests, values, power, vulnerability. Flag **swing stakeholders** (both sides claim them) vs. **owned stakeholders** (only one side can credibly claim them).

### Step 6 — Stress-Test the Mechanism (policy motions)
Trace the causal chain: Policy → first-order effect → second-order effect → third-order effect. Identify the most fragile link — Opposition should attack it; Government should pre-empt it. Ask: do actors have incentives to comply, or does the policy change rules while leaving incentives intact?

### Step 7 — Assign Analytical Levers per Position
Determine which arguments and frames most advantage each of the four positions. Each position needs a different orientation to the same material.

---

## Output Format

Produce output in four layers. Always include Layer 1 and Layer 2. Include Layer 3 and Layer 4 unless `quick` depth was requested.

---

### LAYER 1 — THE CHEAT SHEET
*Scannable in 60 seconds. Read this first, always.*

```
MOTION:        [full text]
TYPE:          [policy / value / comparative / actor / open]
DEEP QUESTION: [the real philosophical tension — one sentence]
CENTRAL CLASH: [the yes/no question that decides the round]
KEY TERM:      [most contested term] → recommended gov definition: [definition]
GOV WINS IF:   [one sentence — the condition for government victory]
OPP WINS IF:   [one sentence — the condition for opposition victory]
THE TRAP:      [what Government must avoid] / [what Opposition must avoid]
```

---

### LAYER 2 — CASE CARDS
*Four cards, one per team. Read in 4 minutes total.*

For each position (OG, OO, CG, CO), produce a card with this structure:

```
━━━ [POSITION] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORE CLAIM: [your position's argument in 2 sentences]

ARGUMENT 1 — [Tagline in 4–8 words]
  → [2-sentence version: mechanism + stakeholder + impact]

ARGUMENT 2 — [Tagline in 4–8 words]
  → [2-sentence version]

ARGUMENT 3 — [Tagline in 4–8 words]
  → [2-sentence version]

PRE-EMPT: [top 2 attacks you will face + one-line response to each]

WEIGHING FRAME: [the standard by which you claim victory]

STORY: [one vivid example that makes your case human and concrete]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**CG and CO cards must include:**
- What the opening bench will have established (do not repeat this)
- The extension: a new stakeholder, dimension, or timeframe the opening bench cannot cover
- How to validate the opening bench while adding genuine new material

> Case cards are for *what* to argue. Position-specific tactical notes (speech structure, what to leave for the bench partner, how to handle the whip speech) belong in **3.6**, not here.

---

### LAYER 3 — DEEP ANALYSIS
*For debaters with time to go deep. 8–10 minutes of reading.*

**All six subsections (3.1 – 3.6) are mandatory in full-depth mode. Do not skip or merge any. Section 3.6 must appear as a standalone block — do not fold its content into the Layer 2 case cards. Section 3.4 is mandatory even for value/thr motions — use the same mechanism-analysis template but applied to the core value conflict.**

#### 3.1 Definitional Analysis
For each contested term:
- Standard interpretation
- Expansive interpretation (who it advantages)
- Narrow interpretation (who it advantages)
- Recommended government definition with justification
- What a topknife on this term would look like and how OG defends it

Output: a one-paragraph definitional block the PM can adapt verbatim.

#### 3.2 Full Stakeholder Map
Table format:

| Stakeholder | Interests | Values | Power | Vulnerability | Gov framing | Opp framing |
|-------------|-----------|--------|-------|---------------|-------------|-------------|
| [party]     | [what they gain/lose] | [what they care about] | [political agency] | [H/M/L] | [why gov owns them] | [why opp owns them] |

Flag swing vs. owned stakeholders. Flag non-obvious stakeholders most debaters miss.

#### 3.3 Clash-by-Clash Breakdown
For each of the 3–4 most likely clashes:

**Clash: [name it]**
- Government's strongest version
- Opposition's strongest rebuttal
- Government's best counter-response
- Decisive evidence or analogy
- Verdict: which side wins this clash and why (judge's perspective)
- The weighing move that resolves it

#### 3.4 Mechanism Analysis (policy motions)
Causal chain: Policy → [first-order] → [second-order] → [third-order]
- Most fragile link (where Opposition should attack)
- Pre-emptive defence of the fragile link (what Government should say)
- Incentive alignment check: do actors in the proposed world have incentives to behave as the mechanism assumes?
- The counterfactual: what actually happens if this mechanism does not exist?

#### 3.5 Impact and Weighing Analysis
**Government's top 3 impacts** (ranked by severity × scale × certainty):

| Impact | Severity | Scale | Vulnerability | Certainty | Reversibility |
|--------|----------|-------|---------------|-----------|---------------|

**Opposition's top 3 impacts** (same table)

**Comparative verdict**: Which side's impacts are larger, and why — across each of the five dimensions. Name the winning weighing frame for Government and for Opposition.

#### 3.6 Position-Specific Strategic Notes
*This section is mandatory and must appear as a standalone block. Do not merge it into the case cards.*

**OG must:**
- Define fairly but strategically; have a defence ready for each term
- Tell a vivid status quo story — the judge must feel the urgency before the mechanism matters
- Name the mechanism precisely (actor + action + enforcement + first-order effect)
- Pre-empt LO's top 2 attacks in the DPM speech, not the PM speech
- Leave one stakeholder or dimension for CG to extend — do not try to win the whole debate

**OO must:**
- Establish a counter-narrative of the status quo in LO's first 90 seconds
- Pick 2–3 decisive attacks, not 7 weak ones — depth beats breadth here
- Offer a principled reason to oppose, not just "it won't work"
- If the mechanism has a fatal flaw, make it the centrepiece; do not bury it
- Leave extension room for CO — do not claim every opposition argument

**CG must:**
- The MG extension must be genuinely new — new stakeholder, dimension, or timeframe, not OG restated
- Validate OG before extending — you cannot win the bench if OG loses
- GW speech: name the 3 main clashes, explain why Government won each one, no new arguments
- Your comparative target is CO, not OO

**CO must:**
- Your extension must outperform CG's in clarity and depth — the judge is comparing the two closing benches directly
- OW has the last substantive word — use it to reframe the entire debate, not just recap OO
- Acknowledge the government's strongest points before dismantling them — it signals analytical confidence
- OW: name 3 main clashes, argue Opposition won each one, explicitly correct any government misrepresentation of OO's case

---

### LAYER 4 — WHIP BRIEF
*For 4th speakers (GW and OW). Scannable in 2 minutes.*

```
THE 3 MAIN CLASHES IN THIS DEBATE:

1. [Clash name] — [which side likely won it] — [the decisive argument in one sentence]
2. [Clash name] — [which side likely won it] — [the decisive argument in one sentence]
3. [Clash name] — [which side likely won it] — [the decisive argument in one sentence]

THE ROUND NARRATIVE (Gov version):
"This debate was about [X]. Government showed [Y]. Opposition failed to answer [Z].
The judge should vote Government because [decisive comparative]."

THE ROUND NARRATIVE (Opp version):
"This debate was about [X]. Opposition showed [Y]. Government's mechanism failed at [Z].
The judge should vote Opposition because [decisive comparative]."

TOP 2 POINTS TO REBUILD (the arguments your opponents attacked hardest):
1. [Argument] — [one-line defence / re-establishment]
2. [Argument] — [one-line defence / re-establishment]
```

---

### CLOSING VERDICT
End every analysis with a single sentence in bold:

> **The team that wins this debate will be the one that convinces the judge that [X].**

This forces the analysis to culminate in the evaluative standard the judge will actually use.

---

## Motion Type Handling

### Policy motions (THW / THBT [actor] should)
Government must win: urgency of status quo problem + mechanism works + net benefit outweighs harm.
Opposition needs to win any ONE of: urgency is overstated / mechanism is broken / costs outweigh benefits / better alternative exists.

Analytical priority: mechanism stress-test, stakeholder map, causal chain.

### Value / Belief motions (THBT [X is true])
No mechanism. The fight is entirely about which normative framework the judge should use to evaluate the claim. The team that establishes *whose framework applies* usually wins.

Analytical priority: framework identification, clash classification (almost always normative), frame competition.

### Comparative motions (TH prefers / TH would rather)
Not about whether something should be done — about which of two described worlds is better. Mechanism is irrelevant. Strategic concession is essential: you are not defending World A as perfect, only as preferable to World B.

Analytical priority: world characterisation, impact comparison, vulnerability of affected populations, durability of each world.

### Actor motions (As [X], THW Y)
Government must show the action is rational from *the actor's perspective* — not from a detached normative view. Opposition must show it is irrational or counterproductive given the actor's own interests and constraints.

Analytical priority: actor incentive map, constraints (political/legal/reputational), information available to the actor at time of decision, long-term vs. short-term interest divergence.

---

## Argument Structure Reference

Every argument should exist in three forms (produce all three in the case cards):
- **Tagline** (4–8 words): the most memorable form — "Protect choice, not the state's comfort."
- **Short form** (2–4 sentences): tagline + causal mechanism + stakeholder + impact
- **Extended form** (1 paragraph): full AREL structure — Assert → Reason → Evidence → Link-back

## Impact Weighing Dimensions

When comparing impacts, always score on all five dimensions:
1. **Severity** — does this harm threaten survival, dignity, or preference? (hierarchy matters)
2. **Scale** — how many people? is this systemic or individual?
3. **Vulnerability** — how marginalised are the affected stakeholders?
4. **Certainty** — how likely is this impact to materialise?
5. **Reversibility** — can the harm be undone if the policy fails?

Never list impacts without comparing them. The debater's job is to do the comparative work explicitly — not to leave it to the judge's intuition.

## Rebuttal Toolkit

When generating pre-empts or clash analysis, use the four rebuttal moves:
- **Turn**: attack the underlying premises, not the conclusion — collapses the argument entirely
- **Take-out**: fully refute the point, eliminating its impact
- **Mitigate**: partially reduce the impact when a full take-out is not available
- **Pre-empt**: anticipate and rebut before the argument is made — most effective against predictable opposition impacts

Structure every rebuttal as: *"They said → Not true because → Even if true, [your impact is still greater because]"*

---

## Output

Write the full analysis directly in the conversation. Do not save to a file unless the user requests it. Use markdown headers and the formatting templates above. The Cheat Sheet comes first, always.
