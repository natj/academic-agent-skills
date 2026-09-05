---
name: analytic-derivations
description: Protocol for analytic equations, physics derivations, and physics write-ups — point-of-entry assumption ledger, step-by-step derivation from the governing equations, precise naming of every approximation, symbolic verification, validation of a reduced set (reduction to known limits, conservation identities, dissipation structure, numerical tests, audit table), and a content-only document style. TRIGGER — read BEFORE writing any equation or any manuscript prose, whenever the task involves: deriving, reducing, re-casting, or checking an analytic result; expanding in a small parameter or taking a limit; dropping, neglecting, or truncating a term; stating a closure, ansatz, ordering, or scaling; claiming one result reduces to another; verifying, auditing, or validating a model or reduced equation set; checking an energy identity, conservation law, or dispersion relation; comparing equations with a reference paper; or drafting/editing a manuscript, primer, note, or write-up containing physics or mathematics. Applies on every project.
---

# Analytic equations & physics — protocol

Every assumption visible; no hidden or implicit step.

# A. Deriving

## 1. Assumption ledger, declared at point of entry
A result rests only on assumptions already declared. Declare each where it first enters, classify it there, and cite it wherever it is invoked later. No up-front block, no summary block. Categories, never conflated:
- **Foundations** — governing equations, constitutive/EOS laws, boundary conditions, domain, what is neglected, parameter ranges that matter. Cite the provenance of each; separate textbook equations from postulated model inputs (a free energy, a balance taken from a reference) — the reduction is only as trusted as those.
- **Structural closures** — modelling ansätze that define the reduced system (well-mixed column, self-similar profile). Not expansions.
- **Expansions** — small parameters, each expanded in turn to a stated order. One parameter per step; note where two couple.
- **Sources / forcing** — added physics (heating). Not a parameter.

State what is *not* assumed (no incompressibility, no posited field geometry) where a reader would otherwise supply it. If a step needs something undeclared, stop: declare it there as a new entry, or fix the derivation.

## 2. Derive step by step
Full equations → ordering → drop terms to the stated order → result. Every displayed equation is one step and names the ledger items it invokes. Lead through the chain; do not jump to the answer.

## 3. One correct form
One derived result, not a hedge among forms. Truncations (what the code solves, named limits) come after it, each labelled as a reduction. No solver chatter, comparison numbers, or alternatives inside the derivation.

## 4. Name every approximation
- A term is dropped by a named assumption with its error order and exact validity condition. Do not call a truncation a small-parameter limit if it is not one.
- Distinguish exact, controlled, and inconsistent truncation. Valid only in a special case (κ=1): say so, not "in the limit".
- Errors hide in the uncontrolled ingredient — the step that is not a small-parameter expansion (interpolation, phase-field switch, prescribed profile). Test where it is active, not only where it is constant.
- Limits are shown to reduce, not asserted (§7).

## 5. Verify, don't assert
- Every re-cast or new identity is checked symbolically (sympy) before it stands: concrete fields, random rational points, high precision, plus a negative control. A displayed equation is a passing check.
- The derived equations are the source of truth; a disagreeing source is flagged, not silently matched.
- A challenged claim is answered by deriving and showing the equations, never by "it's messy". If it is irreducible, exhibit the irreducible terms and the condition under which they vanish.
- A user's mistake or overclaim exposed by the derivation is corrected openly and at once.

## 6. Notation
One symbol per quantity, consistent throughout. Coefficient factors (κ, ½, signs) are verified, not carried by habit. Cross-references are confirmed to hold.

# B. Validating a reduced set

A reduced set is verified only after §7–10.

## 7. Reduce to known equations
- Each limit is a set of switch settings (coefficients → 0, 1, ∞), with nothing else dropped.
- Transcribe the reference equations in their notation with equation numbers; a table maps every symbol, sign convention, and normalization to ours.
- One script per limit prints PASS or the residual. A residual is a finding: name its cause (different regime, different assumption, error on one side).
- Do not conflate regimes (compressible vs anelastic, decoupled vs locked). State the correspondence at the level where it holds, no higher.
- An unshown "reduces to X" is a listed debt, not a statement in the paper.

## 8. Structural and conservation properties
Catches what step checks miss: sign errors, missing terms, inconsistent closures.
- **Energy identity.** Prove pointwise on concrete fields ∂ₜE + ∇·Φ = −𝒬, with 𝒬 a sum of sign-definite terms each tied to a coefficient. All channels together; coefficients spatially varying wherever the model has fronts.
- **Other exact balances** — particle number, momentum (stress-tensor form and where it fails), angular momentum, helicity — each a local identity ∂ₜ(density) + ∇·(flux) = source, verified the same way.
- **Dissipation.** Classify each non-ideal term reversible or dissipative by time-reversal parity or the Onsager structure of the flux–force matrix: antisymmetric parts (Hall, Magnus) do no work, symmetric parts are non-negative over the whole coefficient range.
- **Ideal invariants and Casimirs.** Which the ideal part conserves, and the rate at which each non-ideal term erodes them.
- **Blind re-derivation** of the highest-risk steps by an independent agent from the starting equations alone, without the answer, under a word cap with a checkpoint file. Disagreement is settled by derivation, not by vote.

## 9. Numerical solutions
- **Linear.** One mode per wave branch; frequency and damping against the analytic dispersion relation.
- **Known solutions** in each sub-limit: a 1D steady state, a static equilibrium, relaxation to a known end state.
- **Discrete conservation.** Energy budget against 𝒬, helicity, particle number; drift beyond truncation error is a bug.
- **Fronts.** A front moved through the domain; energy source term against the analytic prediction.
- **Convergence.** Three resolutions per test; report the order.

## 10. Bookkeeping
- One audit table per equation: assumptions invoked (§1–6), reference reproduced (§7), structural checks (§8), numerical test (§9). Blank cells are the open debts.
- Scripts, audit table, and blind reports live in a verification directory whose README maps each script to the equations it establishes. The paper carries only derived content (§11).
- Every check has a negative control — a wrong sign or missing term must fail — so a pass is known to be sensitive.
- When a check finds an error: fix the equation, propagate to every place it appears (dimensionless form, energy theorem, invariants, text), and add the check that would have caught it.
- Run the full suite on every change; "verified" means what the suite currently passes.

# C. Writing the document

## 11. Content only
- **Zero meta.** No companion-document references, no mention of scripts, tooling, or routine names, no "this section does X" framing, no style declarations. Verification (§1–10) is never mentioned in the document.
- **Start at the content.** The first sentence is substance (a definition, an equation, a physical statement), not preamble.
- **Assumptions inline**, as in §1: each stated where it first enters, as a numbered `Assumption` environment (amsthm, counter shared with definitions and propositions), cited by number wherever invoked. No front ledger section.
- **Cut anything that carries no mathematical or physical content.**
