# Thesis Jury Audit - Second Pass

Date: 2026-06-09
Scope: current bound thesis assembled by `thesis.tex` after the SI appendices
and figure restyle work. Reading stance: thesis-jury member reading for flow,
proportion, evidence discipline, figure/table quality, stale provenance,
over-explaining, and AI-like editorial signatures.

## Executive Assessment

The thesis is scientifically much stronger than a normal draft at this stage.
The central argument is clear: volatile polymer-electrolyte memristors are not
failed non-volatile memories; their fading memory can be chemically tuned and
used as a temporal-computing resource. The strongest feature is the explicit
evidence hierarchy: single-device proof of concept, campaign-scale
reproducibility diagnosis, replicated PEO/LiOTf composition spine, illustrative
chemistry/electrode landscape, and in-silico temporal-computing demonstration.

The previous big structural problem - SI asymmetry - has been addressed.
Appendices B/C/D now carry much of the methodological and per-cell machinery.
The remaining issues are not about the thesis being scientifically incoherent.
They are about presentation hygiene, stale source/provenance references, layout
defects, and prose that sometimes sounds too self-conscious about its own
caution.

The highest-priority fixes are:

1. Correct stale Chapter 4 caption provenance paths that still point to legacy
   `scripts/ch3_*` and `handouts/ch3_*` names, some of which no longer exist.
2. Align Chapter 6 limitations with the new Chapter 5 cross-corpus robustness
   result: the affective classification is WESAD-based, but the noise-robustness
   claim is no longer single-corpus.
3. Fix large overfull boxes in Chapter 5 tables.
4. Add Chapter 3 to the front-matter evidence hierarchy, or rewrite that
   hierarchy so it does not skip a whole contribution layer.
5. Run a targeted prose pass to reduce repetitive "not X but Y", "resource",
   "deliberately", "illustrative", and "sample-limited" framing.

## Current Build And Citation State

- `make thesis` reports the build is up to date.
- The build log shows no undefined references or undefined citations.
- The current exported PDF metadata reports 237 pages.
- The log does show large overfull hboxes in Chapter 5:
  - `chapters/chapter5_temporal.tex` lines 202-212 (`tab:ch5_sota`): about 110 pt too wide.
  - `chapters/chapter5_temporal.tex` lines 292-302 (`tab:ch5_wrist`): about 107 pt too wide.
  - `chapters/chapter5_temporal.tex` lines 320-332 (`tab:ch5_summary`): about 85 pt too wide.
- The newer Chapter 5 references added for the WESAD comparator/cross-corpus
  material resolve cleanly by DOI metadata:
  - `Bobade2020`: DOI `10.1109/ICIRCA48905.2020.9183244`, title matches.
  - `GilMartin2022`: DOI `10.1109/MAES.2021.3115198`, title matches.
  - `Birjandtalab2016`: DOI `10.1109/SiPS.2016.27`, title matches.

No new bibliography panic was found, but the bibliography audit log should be
updated if this check is meant to be durable.

## A. Objective Defects And Inconsistencies

### A1. Stale Chapter 4 provenance paths in main captions

Several Chapter 4 captions still cite legacy `ch3` script and CSV names:

- `chapters/chapter4_comparative.tex:117` cites
  `scripts/ch3_figures.py`.
- `chapters/chapter4_comparative.tex:159` cites
  `scripts/ch3_iratr.py` and `scripts/ch3_xrd.py`.
- `chapters/chapter4_comparative.tex:181` cites
  `scripts/ch3_uvvis.py`.
- `chapters/chapter4_comparative.tex:215` cites
  `scripts/ch3_eis.py` and `handouts/ch3_eis_by_cell.csv`.
- `chapters/chapter4_comparative.tex:238` cites
  `scripts/ch3_electrode.py` and `handouts/ch3_electrode_by_cell.csv`.

The repository now contains the corresponding Chapter 4 names:

- `scripts/ch4_comparative_figures.py`
- `scripts/ch4_iratr.py`
- `scripts/ch4_xrd.py`
- `scripts/ch4_uvvis.py`
- `scripts/ch4_eis.py`
- `scripts/ch4_electrode.py`
- `handouts/ch4_eis_by_cell.csv`
- `handouts/ch4_electrode_by_cell.csv`

This is a real jury-facing defect because the captions claim traceability to
artifacts that are absent under those names. It also undermines the careful
provenance narrative of Chapters 3 and 4.

Recommendation: fix the names immediately. Better still, remove most script and
CSV paths from main captions and put them in Appendix C, keeping main captions
reader-facing.

### A2. Chapter 6 limitation conflicts with Chapter 5 cross-corpus claim

`chapters/chapter6_conclusions.tex:98` says:

> The affective results rest on a single corpus (WESAD)

That is no longer strictly true after `chapters/chapter5_temporal.tex:259-264`,
which adds a PhysioNet Non-EEG cross-corpus replication for the noise-robustness
claim.

Recommendation: revise Chapter 6 to distinguish:

- final-label affective classification and physiological-context reconstruction
  are principally WESAD-based;
- the deployment-critical noise-robustness result is replicated on PhysioNet
  Non-EEG;
- broader multi-corpus affective validation remains future work.

### A3. Front-matter evidence hierarchy skips Chapter 3

The front matter states an evidence hierarchy in three bullets:

- Chapter 2 exemplar;
- Chapter 4 composition/chemistry;
- Chapter 5 in-silico computing.

Chapter 3 is not included in that hierarchy, even though Chapter 6 later presents
four contribution layers and treats the reproducibility/provenance diagnosis as
a major contribution. See:

- `chapters/frontmatter_motivation.tex:33-39`
- `chapters/chapter6_conclusions.tex:49-57`

Recommendation: add a Chapter 3 evidence-hierarchy bullet, or recast the front
matter as "three scientific axes plus one methodological bridge." The simplest
solution is a fourth bullet:

- a campaign-scale reproducibility/provenance layer that explains why the
  platform changed from Hybrane to PEO and why later archive-wide comparisons
  are trustworthy.

### A4. Chapter 5 tables are visibly at risk

The build log reports severe table overflows in:

- `tab:ch5_sota`
- `tab:ch5_wrist`
- `tab:ch5_summary`

The likely causes are plain `tabular` environments with long labels and
multi-word column headers:

- `chapters/chapter5_temporal.tex:202-212`
- `chapters/chapter5_temporal.tex:292-302`
- `chapters/chapter5_temporal.tex:320-332`

Recommendation: convert these to `tabularx` with ragged `X` columns, shorten
headers, and use compact task labels. Avoid `resizebox` unless necessary,
because it can make already small tables hard to read.

### A5. Main captions still carry too much lab-internal provenance

Even when the paths are corrected, the main text has many captions ending with
"analysis in scripts/..." and "per-cell values in handouts/...". This is useful
for reproducibility but reads like a lab notebook in the main thesis.

Highest-impact examples:

- `chapters/chapter4_comparative.tex:70`
- `chapters/chapter4_comparative.tex:117`
- `chapters/chapter4_comparative.tex:137`
- `chapters/chapter4_comparative.tex:159`
- `chapters/chapter4_comparative.tex:181`
- `chapters/chapter4_comparative.tex:215`
- `chapters/chapter4_comparative.tex:238`

Recommendation: keep `n`, protocol, sample status, and key caveats in captions.
Move reproducibility paths to Appendix C/D provenance tables unless a path is
essential to interpret the figure.

## B. Scientific Claim Calibration

### B1. Chapter 4 cation "decisive evidence" is too strong for n=1/2

`chapters/chapter4_comparative.tex:174` calls the TMPE cation comparison
"decisive evidence" even while the paragraph correctly states that each cation
cell has one or two screened devices. The conclusion is defensible, but the word
"decisive" invites the examiner to attack the sample size.

Recommendation: replace with "most controlled evidence" or "most informative
evidence." Preserve the conclusion: no host- and anion-independent Li/Na/K law
is demonstrated.

### B2. Chapter 3 hydrolysis language sometimes outruns the evidence

The Chapter 3 hydrolysis section is careful overall, but a few phrases still
sound stronger than the available FTIR/GPC-free evidence:

- `chapters/chapter3_bridge.tex:152`: "this single process accounts for all of
  the measured signatures"
- `chapters/chapter3_bridge.tex:159`: "textbook signature"

Recommendation: revise to "could account for the measured signatures" and
"consistent with". The data still support the hypothesis; the tone should match
the admitted lack of direct stock chemistry.

### B3. Chapter 5 SOTA comparison should stay contextual, not competitive

`chapters/chapter5_temporal.tex:194-209` is careful about accuracy versus
macro-F1 and validation mismatch, but a jury may still see the table and ask
whether the comparison is fair. Because the device result is in silico and uses
macro-F1 while the comparators report accuracy, this table is a soft spot.

Recommendation: either move `tab:ch5_sota` to Appendix D or keep it in the main
text but shorten it and make the first sentence explicitly say "not a ranking."
The body text should emphasize "same order of magnitude/range under constrained
readout", not "competitive with deep models."

### B4. "For free" in the operating budget needs precision

`chapters/chapter5_temporal.tex:304` says temporal feature extraction "happens
for free as the signal drives the material." This is rhetorically effective but
physically imprecise because the write events have an energy budget.

Recommendation: replace with a precise claim: the reservoir state update is
performed by the device dynamics, reducing digital feature-extraction compute;
it is not literally energy-free.

### B5. Chapter 2 biological language is mostly acceptable but should be checked

The proof-of-concept chapter uses "biologically realistic" for the STDP time
constant at `chapters/chapter2_proof_of_concept.tex:281`. This is supported by
the cited timescale, but the waveform and device mechanism are artificial.

Recommendation: no major change needed. If polishing, "biologically relevant
time range" is slightly less vulnerable.

## C. Flow, Proportion, And Signposting

The thesis now has strong structure, but it still over-signposts. The front
matter gives objectives and structure; each chapter then opens with a role
statement; several chapters close with bridge sections; Chapter 6 restates the
whole hierarchy. Some of this is useful in a long thesis, but the repeated
roadmap prose slows the read.

Candidate trims:

- `chapters/chapter2_proof_of_concept.tex:61-65`: compress the named-set
  explanation and remove the section-by-section roadmap.
- `chapters/chapter3_bridge.tex:48`: trim the "(i) ... (v)" roadmap; the section
  headings already show the flow.
- `chapters/chapter4_comparative.tex:53-55`: keep the evidence-tier statement
  but make it shorter; it repeats front matter and Chapter 6.
- `chapters/chapter5_temporal.tex:52-54`: the four-stage introduction is useful
  but too dense for the first page of the chapter; turn it into a shorter
  paragraph or split it into one scope paragraph plus one evidence-base
  paragraph.
- `chapters/chapter6_conclusions.tex:43`: remove the meta-list of what the
  chapter will do. The section headings do that work.

Recommendation: do not remove all roadmaps. Keep the front-matter roadmap and
end-of-chapter bridges. Cut most in-chapter "the chapter proceeds..." lists.

## D. Repetition And AI-Like Prose Signatures

The draft no longer has obvious generic LLM filler such as "delve" or
"tapestry". The issue is subtler: repeated rhetorical scaffolds.

Counts across chapter sources:

- `rather than`: 94
- `not ... but`: 38
- `resource`: 30
- `deliberately`: 22
- `illustrative`: 25
- `sample-limited`: 13
- `design rule`: 10

These words are often technically justified. The problem is accumulated texture:
the thesis repeatedly tells the reader how disciplined, bounded, and reframed it
is. That can sound defensive, and it has the signature of prose that has been
polished by an assistant.

High-value phrase targets:

- "resource, not a defect"
- "not X but Y"
- "deliberately constrained"
- "claim discipline"
- "sober placement"
- "raw material"
- "the right reference class"
- "decisive"
- "candidly"

Recommendation: run a light style pass that preserves the scientific caution
but removes meta-commentary. The evidence can carry the caution; the prose does
not need to announce it as often.

## E. What Belongs In SI

The big SI repackaging has been done. Remaining SI candidates are smaller:

1. Main-caption provenance paths should move to Appendix C/D.
2. `tab:ch5_sota` could move to Appendix D because it is contextual and
   vulnerable to metric mismatch.
3. Some Chapter 5 deployment details could be left in Appendix D, with only the
   headline budget in main text. The current main text and Appendix D duplicate
   the operating-budget logic.
4. Appendix C already has per-cell tables; do not move the main Chapter 4
   heatmaps or design-space figures. They are central to the result.

## F. Figures And Tables

Figure count is high but justified by the thesis form:

- Chapter 1: 12 figures, 1 table
- Chapter 2: 5 figures
- Chapter 3: 4 figures, 2 tables
- Chapter 4: 12 figures, 1 table
- Chapter 5: 8 figures, 7 tables

Chapter 1's sideways figures using `width=0.95\textheight` are intentional
inside `sidewaysfigure`; no action needed unless visual QA shows clipping.

The main figure issue is caption density, not asset availability. Chapter 4
captions in particular are doing three jobs at once: explaining the result,
stating caveats, and recording provenance. Split those roles:

- Main caption: what the panel shows, sample status, key caveat.
- SI: exact script, CSV, curation/provenance path.
- Text: interpretation.

The main table issue is Chapter 5 table width. Fix before final export.

## Proposed Implementation Plan

Each phase is a sensible commit boundary.

### Commit 1 - Fix objective inconsistencies and build-visible defects

- Correct stale Chapter 4 `scripts/ch3_*` and `handouts/ch3_*` references.
- Update Chapter 6 limitation text to acknowledge PhysioNet Non-EEG robustness
  replication while preserving WESAD as the main affective corpus.
- Add Chapter 3 to the front-matter evidence hierarchy.
- Fix the three large Chapter 5 table overflows.
- Build `make thesis`.

Suggested commit message:

`Fix thesis consistency and table layout issues`

### Commit 2 - Move lab-internal provenance out of main captions

- Shorten Chapter 4 captions by removing script/handout path tails.
- Add or strengthen Appendix C/D provenance statements so traceability is not
  lost.
- Keep sample size, protocol, and caveats in the main captions.
- Build `make thesis`.

Suggested commit message:

`Move figure provenance details to supporting information`

### Commit 3 - Claim calibration pass

- Rephrase "decisive evidence" in the cation section.
- Soften Chapter 3 hydrolysis overstatements.
- Tighten Chapter 5 SOTA/budget language.
- Optionally move `tab:ch5_sota` to Appendix D if the user agrees.
- Build `make thesis`.

Suggested commit message:

`Calibrate claims in bridge, comparative, and temporal chapters`

### Commit 4 - Flow and prose-signature pass

- Trim duplicated chapter roadmaps.
- Reduce repeated "not X but Y", "resource", "deliberately", "claim
  discipline", and similar meta-prose.
- Preserve the evidence hierarchy and limitations.
- Build `make thesis`.

Suggested commit message:

`Polish thesis flow and reduce repetitive signposting`

### Commit 5 - Refresh exports

- Run `make exports` after the text/layout changes.
- Commit changed PDFs only after the source build is clean.

Suggested commit message:

`Refresh thesis exports after jury-polish pass`

## Approval Needed

The recommended first edits are objective and low risk: stale path fixes, Chapter
6 consistency, front-matter hierarchy alignment, and table layout. The later
prose and SI moves are editorial choices. Before editing the thesis sources, ask
the author to approve either:

- the full plan above; or
- only Commit 1 first, then review the diff before proceeding.

