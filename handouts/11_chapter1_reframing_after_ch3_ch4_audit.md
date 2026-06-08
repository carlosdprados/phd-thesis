<!-- markdownlint-disable-file MD013 -->

# Chapter 1 Reframing Handout After the Chapter 3/4 Evidence Audit

**Date:** 2026-06-03  
**Scope:** Historical recommendation handout. Several high-priority items have since been implemented in `chapters/chapter1_introduction.tex` and the current Chapter-4 plan has moved to `handouts/12_chapter4_demonstration_plan_v4.md`. Use this file as provenance for why Chapter 1 was reframed, not as a current unchecked task list.

## Evidence Basis

This handout cross-checks `chapters/chapter1_introduction.tex` against the current planning and evidence documents:

- `handouts/08_chapter3_4_claims_audit.md`
- `handouts/10_chapter3_comparative_plan.md`
- `handouts/01_thesis_structure.md`
- `handouts/00_thesis_overview_memory.md`
- `handouts/04_chapter4_temporal_computing_plan.md`

The main evidence shift is clear:

- The replicated, quantitative Chapter 3 result is **composition control in the PEO/LiTr grid**.
- The universal **Li > Na > K cation-timescale law is not supported**. Cation identity should remain a chemical prior / limited illustrative comparison, not a primary thesis claim.
- Host, anion, and cation effects form a **sample-limited chemical-tuning landscape**, not a powered comparative axis.
- Drive/read protocol, especially potentiation amplitude, is a **major determinant and confound** of the apparent fading-memory timescale.
- Chapter 4 should be grounded primarily in composition-indexed fading-memory parameters, measured heterogeneity, pulse-update behavior, and delay-time kernels from the three common measurements.

## High-Priority Reframes

### 1. Polymer-electrolyte chemistry section overstates the cation law

**Location:** `chapters/chapter1_introduction.tex` lines 515-523, especially the paragraph ending before `fig:polymer_electrolyte_chemistry`.

**Current framing:** HSAB reasoning is presented as a cation-residence-time ordering that is expected to map directly onto device fading-memory timescales: `Li+ > Na+ > K+`.

**Problem:** The audit now says this is a useful microscopic prior but not a robust device-level law. The clean cation evidence is sparse, does not generalise across host/anion families, and is confounded by protocol and electrode.

**Suggested reframing:** Keep the HSAB chemistry, but explicitly separate:

- microscopic cation-oxygen coordination strength;
- device-level fading-memory timescale;
- experimental test of whether the former dominates the latter.

**Possible replacement message:** The HSAB series is a chemical hypothesis about coordination strength, not by itself a prediction that the complete device must obey `tau_Li > tau_Na > tau_K`. Device-level relaxation also depends on salt fraction, host morphology, anion, electrode, read/write protocol, and potentiation amplitude.

### 2. Figure 12 should be redrawn or at least panel (c) replaced

**Location:** `figures/chapter1/ch1_fig12_polymer_electrolyte_chemistry.png`; referenced at Chapter 1 lines 519-523.

**Current visual issue:** Panel (c) labels the HSAB ordering and directly maps it to an "expected fading-memory time constant" with `tau_Li > tau_Na > tau_K`.

**Why this needs more than a caption tweak:** The visual itself makes the unsupported cation law memorable. A caption caveat would fight the figure.

**Suggested new visual:** Keep panels (a) and (b), but replace panel (c) with a "chemical prior, not device law" panel:

- Top: cation-oxygen coordination strength `Li+ > Na+ > K+`.
- Middle: other device-level modifiers: host ratio, salt ratio, anion, morphology, electrode, write/read protocol.
- Bottom: "Measured fading-memory tau must be extracted at matched protocol and composition."

**If a lighter edit is preferred:** Retain the cation-size graphic but remove the `expected fading-memory time constant` axis and the `tau_Li > tau_Na > tau_K` line.

### 3. Composite rationale makes cation identity the slow-timescale setter

**Location:** Chapter 1 lines 555-569, especially lines 557-561.

**Current framing:** The salt/cation is described as the component that "sets the slow part of the device response", with composition introduced later as a "second level of control."

**Problem:** This reverses the current evidence hierarchy. Composition is the replicated quantitative knob. Cation is limited / illustrative and does not support a universal ranking.

**Suggested reframing:** Present three levels in this order:

1. Composition of the ion-transport phase as the primary experimental design space.
2. Broader electrolyte chemistry, including host/anion/cation, as mechanistic context and side evidence.
3. Drive/read protocol as an operational variable that can change the apparent timescale.

**Possible replacement message:** The cation is one chemically motivated variable, but the thesis ultimately treats it as one member of a wider set of coupled variables. The composition grid is the controlled quantitative test; cation substitution tests the HSAB prior only within strict evidence limits.

### 4. Figure 14 should be replaced, not just recaptioned

**Location:** `figures/chapter1/ch1_fig14_composite_architecture_timescale_ladder.png`; referenced at Chapter 1 lines 571-575.

**Current visual issue:** Panel (b) says "Cation identity (primary knob)" and "Composition knobs (secondary tuners)." The caption calls the cation/composition ordering the "central hypothesis" tested in Chapter 3.

**Problem:** This is the strongest visual overclaim in Chapter 1. It conflicts directly with the revised old-Chapter-3/current-Chapter-4 plan, where composition is the quantitative spine and cation is sample-limited.

**Suggested new figure:** Replace Figure 14 with a thesis-specific "evidence-disciplined tuning map":

- Panel (a): retain the two-terminal composite stack, possibly unchanged.
- Panel (b): show the **PEO/LiTr composition grid** as the primary design map, with `PEO ratio` and `salt ratio` axes and a qualitative `tau` / fading-memory color scale.
- Panel (c): show **chemical landscape side cards** for host, anion, and cation, each marked "illustrative / n-limited".
- Panel (d): show the **protocol lever**: write/read amplitude changes the written state depth and apparent `tau`.

The key label should be "composition-indexed fading-memory bank" rather than "cation timescale ladder."

### 5. Scope questions still ask for a cation-timescale result as if it is supported

**Location:** Chapter 1 lines 584-592.

**Current framing:** Question 2 asks how fixed-composition cation substitution shifts fading-memory timescale. Question 3 asks whether composition and cation identity provide timescale matching.

**Problem:** This is acceptable as a question only if it is framed as a test that may fail. Right now it reads like the later chapters will deliver composition and cation control symmetrically.

**Suggested reframing:** Revise the questions so they ask:

- Which variables actually survive the evidence filter as quantitative timescale controls?
- How does composition tune switching, potentiation, and fading-memory in the replicated PEO/LiTr grid?
- What can host/anion/cation comparisons show honestly given sample size and protocol limits?
- How strongly does protocol amplitude set the apparent relaxation time?

### 6. Objectives 4-6 need claim discipline

**Location:** Chapter 1 lines 598-607.

**Former framing now addressed in `chapters/chapter1_introduction.tex`:** Objective 4 said the thesis would quantify cation dependence; Objective 6 said the simulations used composition- and cation-driven timescale spread.

**Problem:** This overstates what the data can carry. It also omits the new methodological result that protocol amplitude affects apparent `tau`.

**Suggested objective rewrite, conceptually:**

- Quantify composition dependence in the replicated PEO/LiTr grid.
- Survey host, anion, and cation effects with explicit sample-size limits.
- Test the `Li > Na > K` HSAB-derived hypothesis rather than assuming it.
- Quantify protocol amplitude as a state-writing variable and comparison confound.
- Build Chapter 4 models primarily from the composition-indexed fading-memory bank, with cation only where the fitted data justify it.

### 7. Thesis outline still gives cation too much status

**Location:** Chapter 1 lines 617-619.

**Former framing now addressed in `chapters/chapter1_introduction.tex`:** Chapter 3 was described as a composition and ion-identity-dependence chapter, and Chapter 4 models were said to be extracted per composition and per cation.

**Problem:** The current Chapter 4 plan says composition is quantitative; host/anion/cation are illustrative. Chapter 5 should not look like it depends on a robust cation axis.

**Suggested reframing:** Update the old Chapter-3/current Chapter-4 outline to match `handouts/10_chapter3_comparative_plan.md`:

- "Compositional and Chemical Control of Volatile Polymer-Electrolyte Memristive Dynamics"
- quantitative spine: PEO/LiTr composition grid;
- chemical-tuning landscape: host/anion/cation, n-explicit and illustrative;
- methodological result: protocol amplitude controls apparent `tau`.

Update the Chapter 4 outline so the model inputs are "fitted composition cells and validated measured devices" rather than a guaranteed per-cation parameter set.

## Medium-Priority Reframes

### 8. Opening paragraph could state the evidence discipline earlier

**Location:** Chapter 1 line 30.

**Suggested addition:** Add one sentence to the introductory paragraph saying that the thesis treats chemical arguments as experimentally tested hypotheses and distinguishes the fully characterised Chapter 2 exemplar from the reduced, replicated measurement basis of Chapters 3 and 4.

This prevents the reader from assuming that every synaptic metric and every chemical axis is available across the whole thesis.

### 9. Hardware-synapse specification should not imply all metrics propagate to Chapter 3

**Location:** Chapter 1 lines 170-184.

**Current framing:** The hardware synapse requirements are broad: analogue, reversible, multi-state, bidirectional, low-energy, matched dynamics.

**Problem:** Chapter 2 is the only chapter with the full synaptic suite. Chapters 3 and 4 use three common dynamical measurements.

**Suggested addition:** Add a short bridge after line 182:

- Chapter 2 tests the broad synaptic specification in one exemplar.
- Chapters 3 and 4 deliberately narrow the evidence basis to I-V hysteresis, variable-N potentiation, and variable-delay depotentiation because those are the measurements available across the comparative corpus.

### 10. Variability language should distinguish heterogeneity from uncontrolled noise

**Location:** Chapter 1 lines 278-296 and lines 300-310.

**Current framing:** The table says cycle-to-cycle variability should be minimized in fading-memory mode, while device-to-device heterogeneity is useful. Later text says heterogeneity is useful.

**Evidence alignment:** The audit supports large measured spread as a Chapter 4 resource, but only if it is quantified and separated into useful device-to-device heterogeneity versus harmful/readout-limiting instability.

**Suggested reframing:** Add one paragraph after line 296:

- The thesis treats variability as a measured distribution, not as automatically good or bad.
- Device-to-device spread in fitted time constants is a reservoir resource.
- Cycle-to-cycle spread can be tolerated or modelled only within a bounded envelope.

### 11. Dynamic-computing paradigms should not overpromise ion substitution

**Location:** Chapter 1 lines 300-310, especially line 306.

**Current framing:** Ionic memristors are attractive because relaxation time can be shifted by host composition or mobile ions.

**Suggested tweak:** Keep this sentence but qualify it: "in principle," and add that the thesis tests which of those knobs dominates in the actual archive. The answer is composition, while cation remains limited.

### 12. Inorganic comparison figure and discussion should mark the soft-ionic row as a target/design space

**Location:** Chapter 1 lines 364-388; `fig:inorganic_comparison_matrix`.

**Current framing:** Soft ionic devices are shown as highly chemically tunable and reservoir-ready.

**Risk:** The figure can be read as an achieved performance comparison rather than a design-space argument.

**Suggested tweak:** Add wording in the caption or surrounding text: "The soft-ionic row is a design-space position pursued in this thesis; the experimental chapters then determine which chemical axes are actually supported quantitatively."

### 13. Organic advantages section should foreground composition and protocol

**Location:** Chapter 1 lines 397-407.

**Current framing:** Organic materials allow independent variables including host, ion, and composition, and relaxation timescales can be engineered chemically.

**Suggested addition:** Add a sentence saying that in a real device these variables are coupled, so the thesis treats independence as an experimental question. The evidence later supports composition as the replicated knob and protocol as a major operational lever.

### 14. PEO anchor paragraph overstates variable attribution

**Location:** Chapter 1 lines 526-530.

**Current framing:** Anchoring in PEO lets observed differences across compositions and cations be attributed to the variable of interest rather than uncharacterised host effects.

**Problem:** This is too clean. The audit shows protocol, electrode, and sample coverage matter strongly.

**Suggested reframing:** PEO constrains the host background and makes controlled comparisons more plausible, but attribution still requires matching protocol, electrode, composition, and fit quality.

### 15. Figure 5 target-band language may need caveating

**Location:** Chapter 1 lines 163-164; `fig:synaptic_energy_density`.

**Risk:** The "organic / soft-ionic target band" may be read as achieved energy-density performance across the comparative corpus. Chapter 4 currently treats energy estimates as Chapter 2 sanity-check values, not robust corpus-wide benchmarks.

**Suggested tweak:** Reword as "target/design envelope" rather than achieved class envelope, or add a note that numerical performance is device- and protocol-specific.

## Dedicated Theoretical Framing to Add

The handout above already flags host, anion, and composition, but Chapter 1 would benefit from a more explicit theoretical bridge. The aim is not to promote host/anion/cation to powered claims. It is to make the physical-chemistry logic broad enough that the later evidence hierarchy makes sense: composition is the replicated quantitative knob; host and anion shifts are chemically interpretable but sample-limited; cation ordering is a tested prior, not a law.

### Host architecture: PEO versus TMPE

**Best location:** End of `subsec:ion_conducting_polymers`, after the current PEO/Hybrane discussion around lines 526-530, or in `subsec:composite_rationale` before composition is introduced.

**Theoretical point to add:** PEO and TMPE should be framed as different ion-transport host architectures, not just interchangeable oxygen-rich matrices.

- **PEO:** linear polyether; regular ether-oxygen spacing; well-known tendency toward crystallinity; ion motion strongly coupled to amorphous-phase segmental motion and salt-dependent disruption of crystallites.
- **TMPE / hyperbranched polyether:** branched, more frustrated packing; different free-volume distribution and local oxygen-donor topology; likely different ion residence, ion-pairing, and segmental-relaxation landscape.
- **Device implication:** host identity can shift the distribution of activation barriers and therefore the observed stretched-exponential decay shape, but the current dataset supports this as an illustrative chemical effect rather than a replicated quantitative axis.

**Suggested message:** Host architecture controls the mechanical and coordination landscape in which ions move. PEO provides the controlled, literature-rich baseline for the replicated composition grid; TMPE provides a chemically meaningful side comparison that tests how changing topology and segmental mobility can shift fading-memory dynamics.

### Salt/anion chemistry: triflate versus TFSI

**Best location:** After line 501, where the current text says triflate and TFSI are weakly coordinated, charge-delocalised anions.

**Theoretical point to add:** Triflate and TFSI are not merely two labels for weakly coordinating anions. They differ in size, charge delocalisation, ion-pairing tendency, host plasticisation, and possible interfacial/electrode interactions.

- **Triflate:** smaller than TFSI; still charge-delocalised, but comparatively more compact; can support a different balance of dissociation, cation association, and local packing in polyether hosts.
- **TFSI:** larger and more charge-delocalised; often improves salt dissociation in polymer electrolytes, but can also change morphology, plasticisation, and the effective depth of ionic states.
- **Device implication:** anion choice can alter both the number of mobile carriers and the relaxation pathway. The audit suggests anion effects may be large, but the evidence is not replicated enough for a powered law.

**Suggested message:** The anion should be framed as a modifier of ion pairing, carrier availability, morphology, and interfacial stability, not as a passive counter-charge. This helps explain why triflate/TFSI comparisons belong in the chemical landscape even when cation ordering fails.

### Composition: host fraction and salt fraction as coupled axes

**Best location:** Expand the current composition paragraph at lines 526 and 563.

**Theoretical point to add:** Composition is now the main experimental pillar and deserves more theory than "host ratio" and "salt ratio" as knobs.

- **Host-to-semiconductor ratio:** controls the volume fraction and connectivity of the ion-transport phase, the dilution/continuity of the electronic SY network, film morphology, free volume, crystallinity, and the spatial separation between ionic and electronic pathways.
- **Salt fraction:** controls nominal carrier density, but also ion pairing, screening, local coordination-site occupation, plasticisation, and possible over-driving/degradation at high pulse number.
- **Coupling:** these axes are not independent in the measured device. Increasing PEO can increase ion-host volume but dilute electronic pathways or change morphology; increasing salt can add carriers but also increase ion pairing and screening. That coupling is exactly why the composition grid is an experiment rather than a simple monotonic prediction.

**Suggested message:** The composition grid should be introduced as a controlled way to test how ionic mobility, carrier density, morphology, and electronic percolation combine to set switching window, pulse potentiation, and fading-memory decay.

### Protocol as part of the theory, not only a methods caveat

**Best location:** `subsec:composite_rationale`, near lines 563-567.

**Theoretical point to add:** In a volatile ionic device, the relaxation time measured after a pulse train is conditional on the state that the pulse train writes.

- Stronger write pulses can displace more ionic charge, access deeper or more spatially extended states, or trigger additional interfacial processes.
- The apparent `tau` is therefore a property of the material-plus-protocol pair.
- This explains why Chapter 3 must compare devices under matched write/read amplitude, pulse number, timing, electrode, and composition.

**Suggested message:** The material supplies the dynamical landscape; the protocol selects how deeply that landscape is explored.

### How this should change the Chapter 1 narrative

Chapter 1 should move from a single-axis cation ladder to a four-factor physical picture:

1. **Host architecture** sets segmental mobility, crystallinity/free volume, and coordination-site topology.
2. **Anion/salt chemistry** sets dissociation, ion pairing, carrier density, and interfacial stability.
3. **Composition** sets the balance between ionic pathway, electronic pathway, morphology, and mobile-charge density.
4. **Protocol** sets the depth of the written state and therefore the apparent decay timescale.

The evidence hierarchy then follows naturally: composition is the factor with enough replicated data for a quantitative Chapter 3 claim; host/anion/cation remain mechanistically useful but n-limited; protocol becomes a methodological result and a guardrail for all comparisons.

## New Paragraphs Worth Adding Later

### A. Hypothesis-versus-evidence discipline paragraph

**Best location:** After line 517 or after line 530.

**Purpose:** Prevent HSAB chemistry from becoming an implicit cation law.

**Draft intent:** HSAB gives a mechanistic prior for ion coordination. It does not by itself determine the device relaxation time, because the measured state includes ion redistribution, injection, morphology, electrode interactions, and the depth of the state written by the pulse protocol. Chapter 3 therefore treats cation ordering as a testable hypothesis, not an assumption.

### B. Common-measurement boundary paragraph

**Best location:** After line 182 or at the start of `Scope and Objectives`.

**Purpose:** Keep Chapter 2, Chapter 3, and Chapter 4 evidence levels separate.

**Draft intent:** The full synaptic suite belongs to the Chapter 2 proof-of-concept device. The comparative and computational chapters use the three measurements available broadly enough to support a corpus-level analysis: I-V hysteresis, variable-N potentiation, and variable-delay depotentiation.

### C. Protocol-as-state-writing paragraph

**Best location:** After line 563 or before line 567.

**Purpose:** Introduce the protocol result before Chapter 3.

**Draft intent:** In a volatile memristive device, the measured relaxation time is not only a materials constant; it also depends on how deeply the prior pulse train drives the internal state. Therefore, comparisons of `tau` require matched write/read amplitude, timing, electrode, and composition.

### D. Evidence-spine paragraph before objectives

**Best location:** Before line 584.

**Purpose:** Set reader expectations for the objectives.

**Draft intent:** The thesis distinguishes quantitative pillars from illustrative chemical evidence. Composition in PEO/LiTr is the replicated pillar; host/anion/cation comparisons are used to interpret the chemical landscape and motivate future work; Chapter 4 uses fitted, evidence-supported time constants rather than assumed cation labels.

## New or Replacement Pictures

### Required replacement: Figure 14

**Recommendation:** Replace the whole figure or at least rebuild panel (b).

**New title:** "Composite device and evidence-supported tuning map."

**Message:** The device is a two-terminal soft-ionic composite. Its useful temporal diversity is established primarily through the PEO/LiTr composition grid, with chemistry side comparisons and protocol effects treated explicitly.

### Required replacement or panel edit: Figure 12

**Recommendation:** Replace panel (c).

**New title for panel (c):** "Coordination-strength prior and device-level modifiers."

**Message:** HSAB ranks cation-oxygen binding strength, but the measured device timescale is a protocol-conditioned output of the full composite.

### Optional new figure: Chapter claim/evidence map

**Suggested location:** Start of `Scope and Objectives`, before line 584.

**Structure:**

- Chapter 2: full synaptic exemplar - I-V, potentiation/depression, EPSC, STM/LTM, STDP, impedance.
- Chapter 3: common comparative measurements - I-V, N-pulse, delay-time.
- Chapter 4: model ingredients - read function, pulse update, decay kernel, heterogeneity envelope.

**Message:** The thesis evidence narrows deliberately from full proof-of-concept functionality to replicated corpus-level dynamics.

### Optional update: Figure 5

**Recommendation:** Keep only if recast as design target / literature envelope, not achieved performance. Consider adding a small label: "target/design space; Chapter 2 energy is exemplar-level."

## Sections That Mostly Already Align

- `sec:crisis` and `subsec:paradigms` already set up in-memory versus event-driven computing clearly.
- `fig:paradigms_responses` and `fig:static_vs_fading` already match the new volatile-temporal-computing narrative.
- The organic history section already frames the need for a two-terminal ion-mediated platform and does not depend heavily on the old cation law.
- The distinction between trained-weight mode and fading-memory mode is strong and should be preserved.

## Suggested Revision Order

1. Fix Figure 14 and its surrounding prose.
2. Fix the HSAB/cation-ordering text and Figure 12.
3. Rewrite `Scope and Objectives` to match `handouts/10_chapter3_comparative_plan.md`.
4. Add the common-measurement boundary paragraph.
5. Add the protocol-as-state-writing caveat.
6. Lightly caveat Figures 5 and 9 so they read as design-space figures rather than achieved corpus-wide claims.
