# Pedagogical slide decks — the protocol

The deck is an **info deck**: a document a reader works through frame by frame and
*understands*, alone, without a speaker. It is not a presentation companion, and it
never restates source material — it teaches it. Every rule below was converged on by
iteration with the user; violations are the defects they corrected.

## 1. The per-frame contract

Apply to every frame, no exceptions:

1. **Every symbol is defined on the frame where it first appears** — or explicitly
   back-referenced to its defining frame ("R, the wave-frame energy of frame N").
   Displayed equations get a "where …" clause when new symbols enter.
2. **Every equation shows its provenance**: from which starting equation, by which
   operation (integrate once, average over the fast period, linearize about the orbit,
   eliminate a variable, take a limit) — with the key intermediate line *displayed*,
   not skipped. Derive, don't decree: even the opening definition is derived if it can
   be (e.g. the strength parameter from integrating the momentum kick, not stated).
3. **Every quantity gets its physical reading**: what it measures, what large/small
   means, its units, and *with respect to what* it is being compared. When a
   normalization has structure, use the "smart units" form that exposes it
   (dimensionless prefactors like (ω_P/kc)² × shape function, never raw 4πe²F/k²mc³).
4. **Concepts are named before they are used.** Any term of art (Floquet multiplier,
   Krein signature, hyperbolic vs elliptic, Lighthill criterion, ponderomotive force,
   dispersive shock, Landau–Zener crossing, Bragg gap, …) gets a 1–3 line
   **Definition box** at first use. Methods get their own "Tool:" frame before the
   frame that uses them.
5. **Look-alike concepts are explicitly separated** the moment confusion is possible
   (e.g. carrier steepening vs envelope steepening; the analogy object vs the physical
   object; particle motion vs field structure). If the reader could conflate two
   things, one sentence must say they are different and how.
6. **One named analogy per concept frame** (an **Analog box**): a concrete classical
   system the reader already owns (pendulum, Sagdeev well, Kapitza pendulum,
   Benjamin–Feir, undular bore, photonic crystal, driven oscillator below resonance).
   The analogy states the *mapping*, not just the name.
7. **Assertion titles**: every frame title is the claim of the frame ("Superluminal
   wells confine: smooth trains at every amplitude"), never a topic label
   ("Wavetrains").
8. **Honest scope**: what is proved, over what domain, with what controls, and what is
   open — stated on its own frame(s), with the open items named against the literature
   that lives there.

## 2. Zero meta text

No sentence about the document itself. Concretely banned (all appeared and were
removed): subtitles like "a self-contained tour", "Designed to be read: …",
"(reference card)", "Reading key for everything below:", "needed as vocabulary",
"(audited against the literature)". Cross-references to other frames and lectures are
content and are fine; commentary on the document's virtues, intent, or method of
construction is not. If a sentence would survive deletion with no loss of physics, it
is meta — delete it.

## 3. Visualization rules

1. **Every described phenomenon gets a visualization if one is constructible.**
   Especially: if a *dynamic* process is described in words, show it — as frames /
   time slices / space-time diagrams / snapshots at increasing parameter (a
   steepening sequence, multipliers walking off a circle, an envelope riding
   characteristics). Static figures that carry the dynamics as designed sequences;
   no animations.
2. **Figures come from verified code.** Reuse the project's verified computation
   modules; the figure script adds visual composition only, never new physics. If the
   exact theory cannot reach a regime the story needs (e.g. past a breaking
   threshold), illustrate the *mechanism* honestly and label it as an illustration
   (e.g. "ballistic continuation of the marginal profile").
3. **Every figure frame carries a reading guide**: what each panel and axis shows,
   the units, and what to look at ("t is time over one period; k = 0, nothing varies
   in space"). Big figures get a side-column caption; the caption is content, not
   decoration.
4. **One deck-wide color code**, stated once and kept everywhere (e.g. blue =
   branch A, red = branch B, grey sequence = time/amplitude progression, one accent
   color = instability/positive control). Anchor dots shared between panels reuse the
   same colors.
5. Figure script conventions: one function per figure, a `--only` CLI flag, outputs
   named `plot_<deck>_sN.pdf` beside the deck source; slide-sized fonts (labels ~11,
   ticks ~10, figures ~6.2 in wide for 16:9).

## 4. Structure of the deck

- **Opening frame: the problem**, with its central quantity *derived*.
- **Notation frame** early: the handful of symbols used everywhere, each with the
  why ("u not v because the Lorentz force is linear in u"), plus the fiducial
  numbers.
- **Vocabulary/taxonomy frame** before any classification is used (e.g. the wave
  families), ending with the reading key for which object each later frame means.
- **Parameter table** as a reference frame (symbol / meaning / fiducial size).
- Lectures/sections of ~10–14 frames, each closed by a one-line **recap frame**.
- **"Tool:" frames** introducing each method (what a Floquet problem is; what
  averaging means; what hyperbolic means) before the frames that apply it.
- Near the end: **what is new** (audited claims only) and **what is open** (the
  honest boundary), then a **crib-sheet frame**: the master results, one line each,
  with meaning and the lecture where each was derived.
- **Footline roadmap** (chain strip): the deck's spine with the current segment
  bolded, redefined per lecture.
- Length is not a constraint; understanding is. Split a dense frame rather than
  compress it. ~50 frames for a full paper is normal.

## 5. The build–inspect–iterate loop

1. Plan the frame list with the figure list before writing.
2. Build with latexmk after every batch of edits; **visually inspect every page** of
   the produced PDF (read it page by page). A page is defective if any text touches
   the footline or clips — fix by cutting words, never by cutting definitions,
   derivation steps, or physical readings.
3. Frames budget: ≤ ~14 rendered text lines at 10pt; drop to \small or \footnotesize
   before dropping content; if still over, split the frame.
4. **Reader questions are defects.** Every "what is X?", "where does this come
   from?", "what does this measure?", "in what units?" asked about the deck means the
   contract of §1 was violated on that frame: fix it *on the frame* (and check the
   same defect elsewhere), not only in conversation.
5. Physics discipline: every equation on a slide restates verified source content
   (paper + check scripts); added derivation steps are the source's own intermediate
   lines. New numbers require new verification before they appear.
