# Document style — manuscripts & write-ups, all projects

Documents are **content only and to the point**. Apply this to every manuscript, primer,
note, or write-up on any project:

- **Zero meta.** No references to companion papers or other documents, no mentions of verification/check scripts, tooling, or routine names, no "this paper/section does X" framing, no style declarations ("we work in the style of ..."). Everything is always verified (per DERIVATION_PROTOCOL.md) — but the verification is *never mentioned* in the document itself.
- **Start at the content.** The first sentence is substance (a definition, an equation, a physical statement), not preamble about what the document will do.
- **Assumptions inline, not in a front ledger.** In the *document*, do not collect assumptions into a separate up-front ledger section. State each assumption at the exact point where it first enters, highlighted as a numbered `Assumption` environment (amsthm, shared counter with definitions/propositions), and cross-reference those numbers wherever the assumptions are invoked. This is the same point-of-entry discipline as §1 of DERIVATION_PROTOCOL.md, formalized with the numbered `Assumption` environment; the set of declarations is still complete and closed.
- **Cut anything that carries no mathematical or physical content.**
