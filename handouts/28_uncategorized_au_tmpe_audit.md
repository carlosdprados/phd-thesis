# Handout 28 — The Uncategorized Au/TMPE/(Li,Na,K)OTf Corpus: Provenance, Validation, Findings, and Thesis Integration

**Date:** 2026-06-11.
**Scripts:** `scripts/uncat_au_tmpe_audit.py` (parser/classifier/inventory) and
`scripts/uncat_au_tmpe_findings.py` (analyses F1–F7).
**Outputs:** `handouts/uncat_inventory.csv` (356 rows, one per raw file),
`handouts/uncat_reference_sweeps.csv` (90 catalogued same-generation sweeps),
`handouts/uncat_findings_{polarity,rate,vconst,pulse,relax}.csv`,
QA thumbnails + summary figures in `figures/uncat_qa/` (not thesis figures).

---

## 1. What the corpus is (provenance)

`DEVICES_LAB_DATA/uncategorized/` holds **eight dated campaign folders**
(2025-01-23-LiTr; 2025-02-04-NaTr; 2025-02-10-KTr; 2025-02-12-LiTr;
2025-02-12-NaTr; 2025-02-17-KTr; 2025-02-17-NaTr; 2025-02-21-NaTr) with
**356 .txt files**: 349 parseable Keithley TSB dumps (3 comma-separated rows =
current, voltage, time; occasional `TSP>` prefixes; NPLC 1/2/10 cadences =
20.3/41.7/202.4 ms; 1 mA compliance), 5 empty files, 1 single-line fragment,
and **one TSP measurement script** (`2025-02-17-NaTr/pulse, relaxation/pulses
python.txt`) that documents the relaxation protocol exactly.

**Device identity.**
- `2025-01-23-LiTr` **is NM_v316** (TMPE 0.3 / LiTr 0.09 / Au / 3000 rpm /
  90 °C 3 h / glovebox / filtered salt; fab-note: Au evaporated to ~150 nm of
  300 intended). Proof: the campaign-folder date equals v316's fabrication
  date and sampled files are **byte-identical (md5)** to files inside v316's
  catalogued device folder — the uncategorized copy is a reorganised duplicate
  holding ~18 extra files (R5 constant-voltage series, saturation-pulse runs)
  that the device folder lacks.
- The **February campaigns exist only here** (no duplicates in the archive; no
  library rows dated Feb 2025 — v317–v320 of 2/26 are electrode-free UV-Vis
  samples). File birth-times match the folder dates, so folder dates are
  **measurement dates**. By chemistry, recipe and timing they sit on the
  **2024-Q4 Au/TMPE generation** — most plausibly v304/v305 (TMPENaTr,
  2024-11-29), v306/v307 or v300/v301 (TMPEKTr), v308/v309 (TMPELiTr,
  2024-12-04) at device ages ~60–105 days, or unlogged substrates from the
  same recipe. **Exact NM numbers for February are unproven — confirm against
  the lab notebook.** Per the task instruction, salt (folder name), host TMPE
  0.3, salt 0.09, and Au electrode are taken as given; they are consistent
  with everything below.
- Spanish protocol notes and `REVISAR_RAMON_…` filenames indicate the
  campaigns were run with/by a collaborator (Ramón) on a Windows measuring PC
  ("New Text Document.txt" default names are unnamed data dumps, not notes).
- One session is explicitly flagged in-folder: `2025-02-04-NaTr/L5/pos Hyast
  (ojo que los electrodos estaban al reves)` — **electrodes physically
  reversed**; the analysis confirms exactly those measurements (and KTr
  "Pixel 1") invert the polarity asymmetry, so the note is real and respected.

**Why the pipeline never ingested it:** free-form folder/file naming (no
`Day<N>_<MeasType>/pixel/D1_all.txt` structure), which
`global_navigation.py` requires. The protocols themselves (sweep-rate series,
pulse-interval series, single-run potentiation+relaxation) also have no
feature-extraction module.

## 2. Validation — does it behave as Au + TMPE + triflate? **Yes.**

1. **Instrument/format**: cadences, compliance, buffer-print format all match
   the canonical Keithley TSB setup (and the recovered TSP script).
2. **Cross-check against catalogued same-generation sweeps** (v296–v316
   Hyst/NegaHyst/DualHyst, parsed with the same code): the negative-over-
   positive response asymmetry replicates (catalogued medians, on–off
   NEG vs POS: Li 1.44 vs 1.22 n=40/20; Na 2.02 vs 1.55; K 1.22 vs 1.01;
   peak-current ratios ≈4–70×), and uncategorized on–off at *matched fast
   rate* (~0.06–0.16 V/s: 0.8–2.1) agrees with the catalogued values; the
   large windows appear only at slow rate (finding F2), which the catalogued
   protocol never probed.
3. **Current scale**: µA at −3 V, consistent with catalogued NegaHyst peaks.
4. **Positive-polarity behaviour** reproduces the Ch4 picture exactly
   (on–off ≈0.8–1.5, weak): the catalogued "gold is feeble" numbers are
   recovered when (and only when) the drive is positive.
5. **Chemistry sanity**: all three salts show strong ionic dynamics
   (catalogued salt-free/host-free Au controls show none), thresholds and
   stretched-exponential relaxation are electrolyte-like throughout.
6. Documented anomalies (reversed-electrode session, Pixel-1 wiring) are
   the *only* polarity-inverted measurements — internal consistency.

**Verdict: the corpus is genuine, internally consistent, and consistent with
the catalogued Au/TMPE generation. Usable at the illustrative tier.**

## 3. Findings (F1–F7)

- **F1 — Au/TMPE devices are strongly polarity-asymmetric (unipolar-negative).**
  v316 Day-1 threshold: at ±1.6 V the negative branch carries ~20× the
  current (8.4e-7 vs 3.6e-8 A) and opens a window (on–off 1.27 vs 0.91).
  Within-pixel bipolar sweeps: |I(−A)|/|I(+A)| ≈ 2.5–42 (8/10 files; the two
  exceptions are the documented reversed-wiring sessions). The catalogued
  positive-drive corpus (Ch4 §4.8: on–off 1.3–1.5, "weaker potentiation") is
  the *positive-polarity face* of a device whose active face is negative.
- **F2 — The switching window is sweep-rate-gated.** Step-count series
  (10→2000 steps, i.e. ~0.003→0.4 V/s): on–off rises monotonically as the
  sweep slows (ρ(on–off, rate) < 0 in 7/10 series; strongest −0.99, p<0.001
  and −0.87, p=0.001); at −3 V slow sweeps reach **on–off 20–31** (Li and Na
  campaigns), vs ≈1 at ≳0.1 V/s. A textbook slow-ion memristive fingerprint,
  never measured anywhere in the canonical archive (the 2026-06-10 mining
  audit found no real rate variation to exploit).
- **F3 — Sharp constant-bias activation threshold.** During 2–10-min holds,
  |I| decays below ≈−1.2 V, is mixed at −1.5/−2 V, and grows 10–3000×
  at −2.5/−3 V (t63 ≈ 15–500 s) in every campaign; one −3 V hold rises
  3.5 decades then overshoots and partially relaxes under sustained bias
  (the "efecto látigo" the TSP script tries to minimise).
- **F4 — Strong bidirectional plasticity at negative read.** At the matched
  protocol (−5 V pulses, −2.25 V read, unsaturated): potentiation ratio
  medians **Li ≈233 (n=6), Na ≈48 (n=12), K ≈40 (n=15)** — orders of
  magnitude above the ×1.9 catalogued for Au/TMPE under positive drive.
  Positive pulses depress deeply and quickly (final/peak 0.002–0.05 at ±4–5 V).
  Spreads are huge and substrate-confounded → **no robust cation ordering**
  (the cation null replicates in dynamics, on a second electrode).
- **F5 — Fading memory measured for Au/TMPE for the first time** (the
  catalogued corpus has zero clean Au/TMPE decays). Sparse-read tails
  (TSP protocol: single-point −2.25 V reads after 0.075→30 s delays, device
  floating between reads): Kohlrausch β ≈ 0.33–0.5, model-free **t50 0.4–21 s**
  (per-salt medians: K 0.7, Li 2.2, Na 2.4 s; n=12/5/11). Same seconds scale
  as Ag/TMPE (3.7–5.2 s) — the host ordering (PEO ≫ TMPE retention) gains a
  real Au/TMPE data point (PEO/Au: 87 s). K's fastest tails follow
  compliance-saturated trains (protocol caveat); no cation claim.
- **F6 — Pulse-interval (frequency) dependence of potentiation.** In three
  independent matched series (9–11 points each): ρ(pot-ratio, interval) =
  **−0.94 to −0.99 (p<0.001)** — shorter intervals potentiate more
  (frequency facilitation). Input *timing* demonstrably matters.
- **F7 — Drive history sets the forgetting time on Au too.** Across 28
  potentiation+relaxation runs: Spearman(pot-ratio, t50) = **+0.46
  (p=0.015)** — deeper potentiation decays slower, replicating the Ch4
  "drive co-sets the timescale" lever on a second electrode/host/polarity.

## 4. Candidate claims and their honest tier

Supportable (illustrative tier — single composition 0.3/0.09, 1–2 substrates
per salt, no human curation, exploratory protocols, February device identity
inferred):

1. *Polarity, not the electrode alone, gates the inert-electrode response*:
   with the active Ag pathway removed, switching concentrates in the negative
   branch; under negative drive the Au/TMPE system recovers wide windows
   (×20–30), strong bidirectional plasticity (×40–230 / ÷20–500) and
   seconds-scale fading memory. This **refines** (not contradicts) Ch4 §4.8:
   "weaker on gold" → "weaker under the canonical positive drive; the active
   face is negative".
2. *The window is rate-gated* (F2) — first direct sweep-rate evidence of the
   slow-ion mechanism in the entire archive.
3. *Integration and forgetting interact and were measured together* (F6+F7):
   the matched-amplitude pulse train sweeping count and interval, with decay
   in the same run — the experiment Ch5 §model/§limitations and Ch6 outlook
   name as "the single most valuable bench experiment" — exists here in Au/
   TMPE negative-polarity form. It empirically confirms the *direction* of
   Ch5's stated suspicion (the composition assumption "under-estimates the
   coupling between drive and retention") while not supplying lead-cell
   (PEO/Ag) parameters.
4. *Cation null replicates in dynamics on Au* (F4/F5) — strengthens the
   Ch4 chemistry-landscape and Ch6 "null as outcome" stance.

Not supportable: any cation ordering; any composition statement; quantitative
transfer of the Au negative-drive parameters into the Ch5 measured banks
(different host/electrode/polarity/read); "tonic gap closed" (decays here are
seconds, not minutes).

## 5. Chapter-placement decision

**Recommendation: fold into Chapter 4 — no new chapter.** Rationale:

- The corpus is **single-composition** (0.3/0.09 throughout): it cannot stand
  parallel to Ch4's composition spine, which is the thesis's quantitative
  axis. It is a chemistry/electrode/protocol corpus — exactly the material
  Ch4 already hosts at the illustrative tier (§4.5 chemistry, §4.7 protocol,
  §4.8 electrode).
- By the thesis's own evidence-tier rules (replication + curation for the
  comparative tier), an uncurated, 1–2-substrate, protocol-exploratory corpus
  with inferred February identities is illustrative; a standalone chapter
  built on it between two quantitative chapters would be the weakest chapter
  in the book and a natural jury target. The bridge chapter precedent (Ch3)
  was justified by methodology payload, not data volume.
- The findings *strengthen existing Ch4/Ch5 narratives* (polarity refinement,
  rate gating, drive→τ replication, cation null, the named bench experiment)
  rather than open an independent question that needs its own arc.
- Practical: thesis is jury-polished at ~246 pp; Ch4 main text ~31 pp of a
  ≤35 budget. The fold costs ~2 pp; a chapter costs weeks and a renumber.

What *would* justify revisiting: lab-notebook confirmation of the February
device identities + a curation pass + fresh matched-generation replication
(the Ag/Au split batch already named in future work).

## 6. Holistic accommodation audit (edit list)

**Chapter 4 (`chapters/chapter4_comparative.tex`):**
1. §4.8 *Electrode Dependence* → retitle "Electrode and Polarity Dependence";
   add ~1–1.5 pp: polarity asymmetry (F1), negative-drive windows/plasticity
   (F2/F4 headline numbers), Au/TMPE fading memory (F5), explicit statement
   that the existing Ag-vs-Au contrast is positive-polarity-conditional; keep
   the active/inert mechanism reading, now sharpened (without Ag⁺ the
   response is carried by field-driven ion redistribution whose active
   interface/polarity is the ITO side — state as working hypothesis).
2. §4.8 existing text: qualify "narrows the window… weakens potentiation"
   and the TMPE/Li "(on–off 3.8→1.3; peak 54×→1.9×)" with "under the
   canonical positive drive".
3. §4.7 *Drive Protocol Sets the Timescale*: one paragraph — F6 (interval)
   + F7 (drive-history→t50, ρ=+0.46) replicate the lever on Au/TMPE.
4. §4.9 Discussion, electrode sentence ("weakens the switching and
   potentiation but lengthens retention"): add the polarity qualifier.
5. §4.10 Limitations: **item 4 is now factually stale** ("the archive
   contains no experiment that varies the input timing") — rewrite: the
   experiment exists on the Au/TMPE corpus (negative polarity, illustrative
   tier); the gap that remains is *on the lead PEO/Ag composition at matched
   read*. Same correction in the future-work paragraph ("the clean test…
   is named as future work" → "was realised on the gold corpus; the
   lead-composition version remains future work").
6. Caveat sentence somewhere in §4.8: February device identities inferred
   from chemistry+generation (notebook confirmation pending), device ages
   ~2–3 months, no curation, one collaborator-run session with reversed
   wiring excluded.
7. `fig:ch4_electrode` caption: mark panels as positive-drive.

**Appendix C (`appendix_chapter4_comparative_SI.tex`):** new section
"The uncategorized gold-electrode dynamics corpus" — provenance (§1 above),
per-salt tables from `uncat_findings_*.csv`, the rate-dependence and
relaxation figures (restyled via `figstyle.py`), protocol decode from the
TSP script, and the validation cross-check table; fill the empty Au/TMPE
decay cells of `app:ch4_electrode_table` with the negative-read values,
clearly footnoted as a different (negative, supra-threshold) read protocol.

**Chapter 5 (`chapters/chapter5_temporal.tex`):**
8. §model (≈line 75 "Two constraints…"): after "not a measured fact… most
   likely under-estimates the true coupling", add: a first direct
   measurement of that coupling now exists (Au/TMPE negative-drive corpus,
   Ch4 §4.8: interval facilitation ρ≈−0.95, drive-history→t50 ρ=+0.46),
   confirming the direction of the under-estimate; parameters are not
   transferable to the PEO/Ag bank, so the modelling assumption stands but
   is no longer untested in kind. Mirror one sentence in §5.x limitations
   (≈line 359) and keep the κ-sweep control as the bound.
9. **No change to simulations/parameter cards**: banks remain measured-Ag;
   tonic-node extension stays labelled extrapolation (the new decays are
   seconds-scale and do not close the tonic gap). Optionally cite the Au
   σ(ln t50) spread as a second-electrode echo of heterogeneity in
   `app:ch5_scatter` (one sentence).

**Chapter 6 (`chapter6_conclusions.tex`):**
10. §limitations bullet ("electrode contrast … illustrative"): add "and
    polarity-resolved only on gold (negative-drive corpus, Ch4 §4.8)".
11. §outlook "Close the composition assumption" (≈line 109): acknowledge the
    Au/TMPE realisation of the experiment and re-scope the ask to the lead
    composition/electrode/read. "Power the chemistry landscape" (≈line 111):
    can now also cite that the cation null replicated in gold dynamics.

**Repo/docs:** `docs/experimental_archive_and_pipeline.md` — document the
uncategorized folder (this handout §1–§2). `README.md` — add the two new
scripts. Memory updated.

**Untouched:** Ch1, Ch2, Ch3 bridge, front matter, all Ch5 result numbers,
bibliography (no new citations strictly required; optional: a PPF/frequency-
facilitation citation if F6 enters the main text — CrossRef-verify first).

## 7. Caveats register (for whoever writes the text)

- February device identity inferred (chemistry+generation+dates), not logged.
- Device age at measurement: v316 days 1–6; February campaigns ~60–105 days
  post-fabrication if the v30x mapping holds (glovebox-stored).
- No human curation; saturated trains flagged (17 files touch 1 mA
  compliance — mostly KTr 02-17); reversed-wiring session excluded from
  asymmetry claims; pixel labels missing in four February campaigns ("unk").
- Decay observable differs from the Ag delaytime protocol (negative
  supra-threshold sparse read vs +2 V read) — compare orders of magnitude,
  not values; t50 is model-free, Kohlrausch β floor-checked (0,1].
- The L5/L4 "0,±1.6 V" threshold comparison spans two pixels (within one
  substrate); the within-pixel asymmetry evidence is the dual sweeps.
