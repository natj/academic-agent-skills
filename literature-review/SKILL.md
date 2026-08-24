---
name: literature-review
description: Exhaustive, verified literature review for a manuscript — multi-modal ADS
  discovery (keywords, citation graphs, review reference-list mining, author/school
  tracking), fabrication-proof verification, source archiving to refs/, and categorized
  annotated citation lists written into the paper's introduction. Use when asked to do
  a literature review, survey prior work, or build a related-work/introduction citation
  list for a paper.
---

# Literature review protocol

Builds on the `ads-search` and `arxiv-fetch` skills — use their scripts, never
reimplement their functions:
- search/citations/bibtex/pdf: `python3 ~/.claude/skills/ads-search/ads_search.py`
- arXiv LaTeX source: `python3 ~/.claude/skills/arxiv-fetch/arxiv_fetch.py --id ID --outdir refs/`
- bulk verify + abstracts: `python3 ~/.claude/skills/literature-review/bulk_verify.py SELECTION OUTDIR`

## 0. Scope first
- Fix the taxonomy BEFORE searching: 4–8 topical categories per paper, each with seed
  authors and seed papers. For companion papers, split categories by paper (e.g.
  weak-wave topics vs strong-wave topics) — one categorized list per introduction.
- The search is ALWAYS exhaustive — do not ask the user for a target depth. Aim for
  100+ entries when the literature supports it; everything defensible goes in.
  Hidden/obscure papers (Soviet-era journals, conference papers, low-citation prior
  art) are the most valuable finds; landmarks are mandatory.
- Inventory existing refs.bib keys first (key/year/bibcode/title map) — reuse existing
  keys in the lists, never duplicate entries.

## 1. Discovery — run modalities in PARALLEL subagents (opus-class suffices)
One agent per topic shard, plus two special agents:
- **Topic agents**: several keyword variants per topic + `citations(bibcode:X)` on 2–3
  landmarks; year filters where useful; `--sort "citation_count desc"`.
- **Review-mining agent**: locate the modern reviews of the field, then mine each with
  `--search "references(bibcode:REVIEW)" --max-results 40 --sort "citation_count desc"`
  and a second pass with `--sort "date asc"` to surface the old layer; filter reference
  lists by title keyword rather than paging them.
- **School-tracking agent**: sweep named key authors AND their students/recurring
  co-authors (supervisor → student chains); constrain author sweeps with a topical
  `abs:` term to kill name collisions; try both transliterations of Soviet-era names.
- ANTI-FABRICATION RULE (put verbatim in every agent prompt): report ONLY rows copied
  from actual tool JSON output; NEVER write a bibcode from memory; note "expected but
  not found" honestly rather than inventing. Agents return a table:
  bibcode | first-author year | short title | arxiv_id | landmark-or-hidden | one-line
  gist (marked [T] if inferred from title only — the search tool returns no abstracts).
- ADS query lore (hard-won):
  - `&` inside bibcodes must stay literal — URL-encoding as `%26` silently returns 0.
  - The wrapper ANDs free-text terms: author-pair queries and `citations()`/`references()`
    beat multi-concept keyword strings.
  - Some authors are invisible to author search (ligatures like Skjæraasen, name-collision
    chemists, or unindexed initials — e.g. Decoster): reach them via `bibstem:` + `title:`
    or through citation graphs of their known papers.
  - Add `database:astronomy` to kill condensed-matter/Raman noise on plasma keywords.
  - Soviet papers often appear twice (Russian original + English translation bibcode):
    cite the translated record.

## 2. Select + verify + enrich (orchestrator, no agents)
- Merge candidate tables, dedup, map to existing keys, and build ONE master selection
  file, line format: `key | bibcode | arxiv_id(or -) | category | new/existing`.
  Keys follow the project convention (lowercase authoryear; suffix b/c on collisions).
- Run `bulk_verify.py` on the selection: it fetches bibtex for all new bibcodes via the
  ADS export API (THE FABRICATION GATE — fake bibcodes fail here), rewrites bibtex keys
  to project keys, and pulls all abstracts via the search API. Outputs: new_refs.bib,
  abstracts.json, keymap.json, plus a missing-bibtex/missing-abstract report.
- Append new_refs.bib to paper/refs.bib only after a programmatic key-collision check.

## 3. Archive sources to refs/ (fetch agents, sharded, RATE-LIMITED)
Per-paper priority: arXiv .tex via `arxiv_fetch.py --id ID --outdir refs/` → ADS PDF via
`ads_search.py --pdf BIBCODE --outdir refs/` → abstract-only (flag it; highly unwanted —
report the irreducible abstract-only list to the user). One retry max per paper.
Agents report: key | TEX/PDF/ABSTRACT-ONLY | filename.

Pacing discipline (arXiv throttles aggressive parallel source downloads and hanging
agents result; ADS has shown no such problem — its search/export/pdf calls need no
delay beyond the batching above):
- At most 2 fetch agents run concurrently, and each works through its shard as a
  SEQUENTIAL queue — never fire fetches in parallel within a shard.
- Sleep ~3 s between consecutive arXiv requests (arXiv API terms: ~1 request/3 s):
  `fetch; sleep 3; fetch; sleep 3; ...` within one shell call.
- Wrap every fetch in a hard timeout so a throttled download cannot hang the queue:
  `timeout 90 python3 .../arxiv_fetch.py --id ID --outdir refs/` (macOS without
  coreutils: `perl -e 'alarm 90; exec @ARGV' -- python3 ...`); on timeout, record
  FAILED-timeout and move to the next row — no immediate retry.
- Several timeouts in a row mean the endpoint is throttling: back off (sleep 60)
  before continuing the queue.

## 4. Write into the .tex (load analytic-derivations + latex-conventions skills first)
- Placement: the paper's Introduction. If none exists, create `\section{Introduction}`
  before the first content section: 2–3 content-first framing sentences, then the
  categorized list. Zero meta beyond that; one sentence per source line.
- Format: `\textbf{Topic.}` paragraph blocks; each entry is
  `\citep{key}: what was done---how it compares to us.`
  1–3 sentences; landmarks slightly longer (they are milestones); hidden finds get their
  discovery value noted; closely related keys may share one entry (`\citep{a, b}`).
  Comparison clauses point at specific parts of our work (`Sect.~\ref{}`, `Eq.~\eqref{}`).
- Summaries are written FROM THE FETCHED ABSTRACTS (abstracts.json), never from the [T]
  title-only guesses of the discovery stage.
- When rewriting an existing introduction into this format, preserve load-bearing prose
  (e.g. "(hereafter Paper~I)" definitions) and convert existing citation prose into
  entries without losing its physics content.

## 5. Verify end-to-end + bookkeeping
- Both PDFs rebuild (latexmk + bibtex) with 0 undefined citations/references and no new
  overfulls; render-check the intro pages.
- Spot-check ~10 random entries against their abstracts.
- Report to the user: entry counts, new-key count, TEX/PDF/abstract-only tally, and the
  seed corrections discovered (wrong titles/years/authors in the original leads are
  common and worth listing explicitly).
- Add a LIT row to the project's coverage ledger; update project memory with the key
  discoveries and any new search lore.
