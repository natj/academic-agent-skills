# Scientific project on radio-pulsar pair cascades


## Comprehensive Paper Writing Guide

This guide synthesizes advice from various sources on writing effective academic papers.

### The Narrative: Foundation of a Great Paper

A paper should present a narrative of one to three specific concrete claims that you believe to be true, building to useful takeaways. Everything else exists to support this narrative. The second pillar is rigorous evidence for why these claims are true.

**What makes a good narrative:**
- Motivate why someone should care about these claims
- Contextualize them in existing literature
- Communicate them precisely with all relevant technical detail
- Provide sufficient evidence to support them

**Crafting claims:**
- One important claim with sufficiently strong evidence can be enough for a great paper
- If you have multiple claims, choose ones that fit together in a cohesive theme
- Adjust confidence based on evidence strength: existence-proof claims, systematic claims, hedged claims, narrow claims, or guarantees
- Stronger statements make for more interesting papers but require higher standards of evidence

**Key questions for finding your narrative:**
- Which results would be most exciting to show someone?
- What seems particularly important? Why should anyone care?
- What was hard about what you did that perhaps no one else has done?

**On novelty:**
- Be extremely clear about what is and is not novel, especially in the introduction and related work
- Liberally cite relevant papers and explain how your work differs
- Depending on how novelty is framed, the same paper could seem arrogant or making a modest contribution


### Paper Structure

**Abstract (TL;DR of the entire paper):**
- First sentence: Something uncontroversially true that situates the reader in the right sub-field
- Second sentence: Something that makes clear there is a need, something unknown, or a problem to solve (conveys motivation)
- Next sentences: State the crucial contribution and why it is exciting; include key definitions for necessary jargon
- Include a concrete metric or result that shows your results are real and substantial
- Final 1-2 sentences: Remind readers why the paper matters, its implications, and how it fits the broader context

**Introduction (Extended abstract):**
Introduction should roughly follow this structure:

- Paragraph 1: Context—what topic are we studying, what is the key motivating question, why does it matter?
- Paragraph 2: Technical background—what do we know about this problem, what established techniques does the paper rest on?
- Paragraph 3: Key contribution—what exactly is our main claim with key nuance, detail, and context?
- Paragraph 3.5: Our case—summarize the most critical evidence supporting the main claim
- Paragraph 4: Impact—what should you take away, what are the implications, why is this a big deal?
- End with a bullet-point list of contributions (concise descriptions of key claims with brief references to supporting evidence)

**Theory/Background section:**
- Explain all concepts and prior work required for understanding the topic
- Define key terms and techniques--—readers have less context than you think
- If something is widespread knowledge (e.g., general relativity, no need to cover it, but err toward defining things

**Methods and Results:**
- Communicate information at several layers of abstraction
- Explain what your results are and how to interpret them
- Explain what you actually did for experiments in full detail
- Explain why your approach was reasonable and relevant to your claims
- Specify technical choices and their implications

**Related Work:**
- Compare and contrast—describing what another paper does is not enough
- Explain how their approach differs in assumptions or method
- If their method applies to your problem setting, include a comparison in experiments; if not, clearly state why not
- Can come after main content rather than as the second section

**Discussion/Conclusion:**
- Explain limitations of your work (crucial for scientific good practice)
- Discuss broader implications, general takeaways, and future work
- Put everything you wanted in the intro but couldn't because readers needed more context first


### Rigorous Supporting Evidence

**Reproducibility:**
- Explain all numerical simulation parameters, algorithms, and list all codes used
- Share your code and configuration to enable others to build on your work

**Statistical rigor:**
- Consider: How noisy is my experiment? What is the sample size and standard deviation? Are results clearly distinguishable from noise?

**Red-teaming your narrative:**
- When done with the first pass, perform a red-teaming exercise:
    - Assume you've made a mistake—what is it? Assume there's a hole in your case—where is it?
    - Then, re-iterate on the text and fix the shortcomings.
- Extensively discuss limitations; if you notice issues, design new experiments to test for them


### Figures and Tables

**Captions:**
- Give context on what the figure shows, the nuance and intended interpretation, and key technical detail
- Ideally, the reader understands everything from just the figure and caption
- Keep captions short and concise — typically 2–4 sentences. Long discursive captions belong in the prose, not the caption.
- Follow this structure:
  1. **First sentence** = the topic, as a short noun phrase ending in a period. E.g. *"Relativistic E×B drift error for different particle pushers."* The reader should know exactly what they are looking at after one sentence.
  2. **Setup sentence** = the configuration and what is being plotted. Quote axes, units, and field/parameter values briefly.
  3. **Curves sentence** = list the curves shown, with styling details in parentheses. E.g. *"Boris pusher (solid blue), Vay (dashed red), HC (dashed orange), unsplit Cayley (solid light green), and the synthesis pusher (thick dark green)."*
  4. **Optional one-sentence takeaway** = the headline finding, if not obvious from the figure (e.g. "Only the synthesis pusher clears the next-best scheme by a full order of magnitude.").
- Styling shorthand: place line/marker descriptors in parentheses after each label, not in a separate legend-prose sentence. Use compact phrases like "(solid blue)", "(dashed orange)", "(thick dark green)" rather than "is shown as a solid blue line".
- Do **not** dump end-of-run numerical values into the caption; that level of detail belongs in a comparison paragraph or a small inline table in the text.
- **Avoid meta-narrative about the act of plotting.** Phrases like "we plot X", "we show a plot of X", "the plot shows X" treat the visual representation as the action — "plotting" is conversational English, and in a caption the plot is the object, not an action. Use **show**, **depict**, **visualise**, or just state the quantity directly:
  - ✗ *"We plot the velocity error as a function of time."*
  - ✓ *"The velocity error is shown as a function of time."*
  - ✓ *"Velocity error versus time for the four pushers (curves as labelled)."*
  - ✓ *"The figure depicts/visualises the secular drift over 20 cyclotron periods."*
  This rule applies to body prose too: prefer "Figure~X shows Y" over "we plot Y in Figure~X".

**Figure placement:**
- Put an eye-catching figure on the first page—most readers decide whether to read based on that
- Explanatory diagrams can be very effective as Figure 1


### Writing Style and Clarity

**Core principles:**
- Be precise: Choose words carefully so you say what you mean; replace vague terms like "performance" with "accuracy" or "speed"
- Be concise: Most of us write in an overly wordy style; after writing initial text, try to delete around one-third of the words
- Avoid complex sentence structure: Research is already difficult; don't make it harder with run-on sentences
- Use consistent phrasing: Avoid synonyms for work-specific terminology at all costs
- Use simple language: Avoid rare words or sounding "fancy"; English is not the first language for many scientists

**Active voice:**
- Passive voice is overused, clunky, and obscures who did what—avoid it
- Never use passive tense; always specify the actor ("We find...")

**Sentence structure:**
- Put the verb as early in the sentence as possible (early verbs make sentences easier to parse)
- If a sentence gets too long, split it into two: one sentence, one idea
- Don't use long sentences with a lot of actual content; split them
- Long sentences are fine if they have simple, easy-to-understand words

**Paragraphs:**
- Lead and end paragraphs with strong, clear sentences; middle sentences are for elaboration
- Make sure every sentence adds information
- Ask about every word/sentence: "Is this necessary?" and "Can I phrase this more simply?"

**Words and phrases to remove or replace:**
- Remove: actually, a bit, fortunately, most connectives (e.g., "however"), "to our knowledge," "note that," "observe that," "try to," very/really/extremely
- Replace: want, hope, contractions ("it's" → "it is")
- Avoid words in quotation marks (a way to sneak imprecise or "dodgy" words in)
- Unfold apostrophes (X's Y → The Y of X)
- Limit hedging ("may" or "can")—hedge words should almost always be dropped

**Other style points:**
- Minimize pronouns; if you must use "this," "those," etc., use them as adjectives (e.g., "this result")
- Don't repeat similar-sounding words within a paragraph or sentence
- Don't start every sentence with "We"—add just a bit of variation
- "On the other hand" shouldn't come without "On the one hand"
- Don't use comparatives without explicitly specifying what two things are being compared
- Cite any claim not supported by your experiments; avoid grandiose language or overly broad claims
- Avoid subjective claims--—adjectives are usually red flags

**Equations:**
- Display equations can take up space if overused; too many inline equations hurt readability
- Think carefully about which equations are worth displaying
- If you leave a blank line after `\end{equation}` or `$`, you create an extra line break. Check that this is not unintentionally done.
- Mathematical equations follow standard punctuation rules—don't forget periods and commas after equations

**Cross-references (LaTeX):**
- Always use the abbreviated form with a non-breaking space (tilde) between the abbreviation and the reference command:
  - `Eq.~\eqref{eq:xx}` — equations (note `\eqref` adds parentheses automatically)
  - `Sect.~\ref{sect:xx}` — sections
  - `Fig.~\ref{fig:xx}` — figures
  - `Table~\ref{tab:xx}` — tables (no period; "Table" is not normally abbreviated)
  - `App.~\ref{app:xx}` — appendices
- Never use the `\S` symbol (`\S\ref{...}`) to denote a section reference; always spell it as `Sect.~\ref{...}`.
- The tilde `~` is essential: it produces a non-breaking space so the abbreviation and the number don't get split across a line break.
- At the start of a sentence, spell out the word in full: "Equation~\eqref{eq:xx} shows…" / "Section~\ref{sect:xx} discusses…".


### Common Pitfalls

**Illusion of transparency:**
- Address misconceptions and possible misunderstandings, even though they feel obvious to you
- Provide context before introducing new concepts
- You have spent months steeped in context; your reader has not

**Overclaiming:**
- The temptation to make work sound maximally exciting is dangerous; competent researchers see through this
- Clearly acknowledging limitations increases respect for your work

**Cherry-picking and post-hoc analysis:**
- Clearly track which results were obtained before vs. after formulating your claim

**Unnecessary complexity:**
- If readers don't understand your paper, they ignore it or assume it's not credible
- Use precise language, but within that constraint be as simple and accessible as possible
- You get points for quality technical insights, not for sounding fancy
