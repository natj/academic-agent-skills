# Working with analytic equations & physics — protocol

Follow this whenever we derive, present, or manipulate analytic equations or physics, on **any project**. The goal is a derivation with **100% visible assumptions and no hidden or implicit steps, ever**.

## 1. Exhaustive assumption ledger, declared where each assumption enters
Every reduced result rests on a closed set of assumptions: at any stage it may rest only on assumptions already declared, and nothing enters silently. Declare each assumption at the exact point in the derivation where it first becomes relevant, classify it there, and cross-reference it wherever it is later invoked. There is no up-front block and no summary block — the ledger *is* the set of these point-of-entry declarations. Classify each; **never conflate the categories**:
- **Foundations** — the governing equations, constitutive/EOS laws, boundary conditions, domain, and what is neglected (e.g. dissipation). Include parameter *ranges* that matter (e.g. κ∈(0,1)).
- **Structural closures** — modelling ansätze that *define* the reduced system (e.g. well-mixed column; self-similar vertical profile). These are **not** expansions; declare them explicitly.
- **Expansions** — the small parameters, each expanded *in turn* to a stated order (e.g. ε, M_A, σ, λ). One parameter = one step. Note where two parameters couple.
- **Sources / forcing** — added physics (e.g. heating Q). A source is **not** a parameter.

Also state briefly **what is NOT assumed** (e.g. no geostrophy/QG, no incompressibility, flow amplitude free, no posited field geometry) at the point where a reader might otherwise supply it. If a step needs something not yet declared:
**STOP** — surface it, then either declare it there as a new ledger entry (saying explicitly that it is one) or fix the derivation.

## 2. Derive step by step from the governing equations
Start from the full/3D equations → apply the ordering → drop terms to the stated order → reach the result. 
Every displayed equation is a step; annotate which ledger item(s) it invokes. 
Show the relevant equations at each stage; lead the reader through the chain, don't jump to the answer.

## 3. One mathematically-correct form
Present the single correct result, **derived** — not a hedge among competing forms or truncations.
- Downstream truncations — "what e.g., the code solves", named limits — come **after** the correct derivation, each clearly labelled as a reduction. Never interleave code/solver chatter, comparison numbers, or alternative truncations into the derivation itself.

## 4. Name every approximation precisely
- Do **not** call a truncation small parameter limit or similar if it isn't. A term is dropped by a *named* assumption; identify it and its **error order** and **exact validity condition**.
- Distinguish "exact / controlled truncation / inconsistent truncation". If dropping a term is only valid in a special case (e.g. κ=1), say exactly that — don't imply it's a general limit.
- Reductions/limits (e.g. κ→1, B→0) must be **shown to reduce**, not asserted.

## 5. Verify, don't assert
- Every re-cast or new identity is checked **symbolically** (e.g. sympy) before it stands — by hand and/or a runnable script. Displayed equations correspond to passing checks.
- The **derived equations are the source of truth**. If other sources disagree, it is suspect — flag it, don't silently match it.
- When a claim is **challenged, DERIVE and SHOW the actual equations** — never hand-wave "it's messy/dirty". Seriously attempt the cast; if the result is genuinely irreducible, exhibit the irreducible terms and the exact condition under which they vanish.
- If a derivation exposes a mistake or an overclaim that the user made, **correct it openly** and immediately. Correctness before politeness.

## 6. Notation & bookkeeping discipline
Unify symbols (one symbol per quantity); keep variable choices consistent; watch coefficient factors (κ, ½, signs) — verify them rather than carrying them by habit. Confirm cross-references and limits actually hold.
