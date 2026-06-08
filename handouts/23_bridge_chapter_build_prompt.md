<!-- markdownlint-disable-file MD013 -->

# Build Prompt — Bridge Chapter figures + draft (for a fresh session)

Paste everything below the line into a new Claude Code session started from the
`phd-thesis` repo root.

---

You are continuing a PhD thesis. Historical note: this prompt was used to draft the bridge chapter that is now Chapter 3. It is retained as provenance, not as a current task.

## Read these first (do not skip)

- `handouts/22_bridge_chapter_plan.md` — the authoritative plan (rev 5+). Follow it. Pay special attention to §1A–1E (controls, verified results, mechanistic hypothesis), §2 (notes/quotes), §3 (methods legacy), §4 (chapter structure), §5 (figures), §6 (Ch2 reconciliation).
- `scripts/bridge_hybrane_peo_reproducibility.py` and `handouts/bridge_hybrane_peo_summary.csv` — the reproducible evidence. **Re-run the script first** (`python3 scripts/bridge_hybrane_peo_reproducibility.py`) and cite only numbers it prints, in case the DATABASE changed.
- `chapters/chapter2_proof_of_concept.tex` and `chapters/chapter4_comparative.tex` — for tone, LaTeX macros (`\SY`, `\Hybrane`, `\PEO`, `\LiTf`, `\twoterminal`, etc.), the `\ifdefined\thesismode` standalone guard, figure/caption style, and `\cref`/label conventions. `chapters/thesis-format.sty` holds shared formatting.
- Project memory `bridge_chapter_decision.md` (loaded via MEMORY.md) — the condensed decisions.

Data lives in the sibling folder; scripts use `DB = "../Nanomem_Devices_Library/DATABASE"` from repo root. The author's interactive tool is `../Nanomem_Devices_Library/project_feature_explorer` (for reference; the audit script already reproduces its slicing).

## Hard constraints (claim discipline — the chapter's credibility depends on these)

- **Read each feature at its expressing amplitude:** window features (on-off ratio, normalized area) at the **~3 V** stratum; conductivity features at the matched **~1.2 V** stratum. Never read window features at 1.2 V.
- **Always per-device weighting** (pixels/device fell 16→2 over the campaign, ρ=−0.80 vs date — pixel-pooled stats are invalid). Use the **standard-protocol corpus** (SY/Hy/LiTr/Ag, 75 °C anneal, no 2nd stage, Hy 0.3, LiTr 0.09; n≈69). Test the collapse as a **step at the NM_v026 inflection** (early ≤Apr 2021 vs later, Mann-Whitney), not a whole-campaign correlation.
- **Headline degradation** = switching-window + potentiation collapse at 3 V: on-off **2.44→1.21** (p=0.002), normalized area **0.235→0.027** (p=0.0005), %Δ max-V current **+18%→−2%** (p=0.013). **Mechanism** = ohmic drift at matched 1.2 V (current/raw-area/on-off-current-difference rise, ρ≈+0.45–0.69, p<10⁻³, strengthens when the ≥2022-03 recovery tail is dropped).
- **Do NOT claim** (these were tested and dropped as confounded): a "~90× conductivity rise"; a whole-campaign monotonic on-off decline; PEO being "more reproducible" in a *within-batch CV* sense.
- **`broken %` is NOT a degradation metric** — it *decreases* over time (handling/contacts improved); the health metric that rises is `is_saturated` (fails-to-potentiate). Carry the deliberate-stress caveat for any health metric.
- **Resolution (PEO):** two wins — better features (wider window at matched 3 V: area 0.26→0.42, p=0.018; on-off 2.45→4.91) **and** *temporal* reproducibility (PEO/Ag on-off @3 V sustained ~2.6 across 2022–2024, no collapse, vs Hybrane stuck ~1.35). State "reproducible" precisely = temporal/batch, not within-batch CV.
- **Attribution = the Hybrane stock** (old/new SY made no difference; SY eliminated).
- **Mechanistic hypothesis** (moisture-driven hydrolytic aging of the polyester-amide stock) must be **labelled a hypothesis**, supported by the annealing-recovery test (late 150 °C on-off 1.95 vs 75 °C 1.22, p=0.024, n=6 — suggestive), the electrical signature, and the material class; confirming experiments (FTIR/GPC/Karl-Fischer/EIS on retained aged-vs-fresh stock) listed as future work. Do not over-claim.
- **v061/v064 multi-day stability** is a Hybrane *positive* → belongs in **Ch2 SI**, not here; in the bridge timeline use only their fresh-day points.

## Deliverable 1 — figures

Create `scripts/bridge_figures.py` (matplotlib; reuse the loading/corpus logic from `bridge_hybrane_peo_reproducibility.py`) that writes PDFs into a new `figures/chapter3_bridge/`:

- **F1 — window collapse (headline):** on-off ratio and normalized area at ~3 V, per-device, **early (≤Apr 2021) vs later** (box + strip/jitter; annotate the medians and MWU p). Optionally a small %Δ-max-V-current panel showing the +18%→−2% flip.
- **F2 — mechanism + methodology:** (a) ohmic drift at matched 1.2 V — current at max V (and/or raw area) vs fabrication date, per-device, log y, with the recovery tail marked; (b) a small inset/panel making the confounds legible: `number_pixels_measured` vs date (ρ=−0.80) and the sweep-amplitude×date overlap.
- **F3 — resolution:** (a) Hybrane vs PEO normalized-area & on-off at matched 3 V (box/strip, p=0.018); (b) PEO temporal stability — on-off @3 V per device vs year (2022–2024) showing the sustained window vs Hybrane's collapsed level.
- Optional **F4** — annealing-recovery (late 150 °C vs 75 °C on-off @3 V).

Match the visual style of existing `scripts/ch4_comparative_figures.py` / `ch5_figures.py` if present. Commit after the figures render.

## Deliverable 2 — chapter draft

Create `chapters/chapter3_bridge.tex` with `\chapter{...}\label{ch:bridge}`, mirroring the standalone `\ifdefined\thesismode` guard and preamble of `chapter4_comparative.tex` so it compiles standalone. Target **12–18 pp**, methods + negative-result + positive-legacy — **not** a lab diary. Follow the §4 structure:

1. The reproducibility problem (anchor on the v026 inflection; scientific question, not confession).
2. Was it us or the materials? — a controlled elimination (compact methods-of-elimination *table* from §2; the Lorenzo cross-person corroboration; this motivates the provenance library).
3. The quantitative degradation signal — open with the four controls (§1A) as the methodological backbone; headline window/potentiation collapse (§1B); mechanism = ohmic drift; chemical **hypothesis** (§1E) with the annealing-recovery support.
4. The resolution: why PEO — better features + temporal reproducibility (§1C).
5. The methodological legacy carried forward (§3) — provenance standard, normalized characterization procedure, feature pipeline, trend-discovery tooling = the apparatus powering Ch3/Ch4. Positive going-forward beat.
6. Reconciliation with Chapter 2 + bridge to the comparative chapter (§6): partition Ch2's shelf-stability claim (device stable ~2 weeks — keep) from the supply/batch collapse (new finding); add the v061/v064 stability figure to Ch2 SI; forward-point to the comparative chapter.

Also: add 1–2 sentences to Ch2 §2.7 / summary (`chapters/chapter2_proof_of_concept.tex`, the Hybrane-stability passage ~line 437) flagging that batch reproducibility is revisited in the new chapter, so the reader meets the tension on the author's terms.

## Conventions

- **Do NOT** renumber/rename the other chapter files or edit `thesis.tex`/`Makefile` this session — the rename to a 6-chapter scheme is a separate step. Write the bridge chapter to slot in as the new Chapter 3; rely on `\cref{ch:bridge}` labels so numbers resolve later.
- Any **new external citations** (e.g. polyester-amide hydrolysis, hygroscopicity) must be verified against CrossRef before use — no hallucinated DOIs/titles (see memory `bibliography_audit_chapter1`). The chapter is mostly internal-data-driven, so keep external cites minimal and verified.
- Build the chapter standalone to confirm it compiles (latexmk via the repo Makefile or `TEXINPUTS=./chapters: latexmk -pdf -outdir=build chapters/chapter3_bridge.tex`).
- **Commit after each meaningful milestone** (figures; chapter skeleton; each major section; Ch2 reconciliation). **Do NOT add a Claude co-author trailer** (repo convention).
- Use the TodoWrite tool to track the multi-step work.

When done, report: figures produced, chapter section status, standalone-build result, and any claim where the data came out weaker/stronger than the plan stated (flag it; do not paper over it).
