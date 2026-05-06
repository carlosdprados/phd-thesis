<!-- markdownlint-disable-file MD013 -->

# Chapter 1 — Figure Plan

**Author:** Carlos David Prado-Socorro
**Date:** 2026-04-15
**Status:** Planning only. No floats are inserted in `chapters/chapter1_introduction.tex` yet. No filenames are assigned.

---

## Selection criteria applied

A figure was retained only if it met all three of the following:

1. The surrounding prose has become dense or explicitly comparative.
2. The reader has already accumulated enough context to parse the figure at first sight.
3. The figure measurably reduces the verbal explanation load elsewhere in the chapter, or encodes a load-bearing framing that the thesis-wide argument relies on.

Figures that would merely duplicate the paragraph immediately above them, or that would arrive before the underlying concept had been introduced, were rejected. In all cases the figure is placed **after** the paragraph that creates the need for it, not before.

Ten insertion points met the criteria. They are listed in reading order.

---

## Figure 1 — The von Neumann bottleneck and the memory/energy walls

- **Proposed label.** `fig:vonneumann_bottleneck`
- **Section placement.** §1.1, `subsec:vonneumann`.
- **Position relative to prose.** After the paragraph that introduces the von Neumann bottleneck and the memory wall (the fourth paragraph of `subsec:vonneumann`). The figure arrives once the reader has been told that the CPU–memory bus is the limiting resource, and then reinforces that the bandwidth problem is compounded by an energy cost per data movement.
- **Figure type.** Composite schematic: a block diagram on the left (CPU, memory, shared bus, arrows indicating the mandatory round trip for every operation) and a small energy-cost bar on the right (arithmetic vs. on-chip SRAM vs. off-chip DRAM access, qualitative only, no invented numbers).
- **One-sentence message.** In a classical processor, every operation pays both a bandwidth and an energy toll to move data across the CPU–memory boundary, and the ratio of those tolls has grown with scaling rather than shrunk.
- **Caption draft.**
  > Schematic of the von Neumann architecture and the associated bandwidth and energy costs of data movement. (a) In the stored-program paradigm, the central processing unit and the memory unit are physically separated and communicate through a shared bus, so that every instruction fetch and every operand access must traverse that bus. (b) The energy cost of moving a word across this boundary exceeds, by orders of magnitude, the energy cost of the arithmetic operation performed on it, and this asymmetry has increased as technology has scaled. Together, the bandwidth ceiling of the bus (the von Neumann bottleneck) and the associated energy ceiling (the memory and energy walls) set the context in which non-von-Neumann and neuromorphic alternatives are evaluated.

---

## Figure 2 — Architectural responses to the von Neumann bottleneck: in-memory and event-driven paradigms

- **Proposed label.** `fig:paradigms_responses`
- **Section placement.** §1.1, `subsec:paradigms`.
- **Position relative to prose.** After the opening paragraph of `subsec:paradigms` that names the two responses (in-memory / near-memory / processing-in-memory, and event-driven / temporal). The figure operates as a roadmap: the reader sees both architectures side-by-side before the prose describes each one in turn, so the deep-dive paragraphs that follow can be parsed against an already-loaded visual.
- **Figure type.** Three-panel architectural schematic that builds on Figure 1 and is deliberately disjoint from Figure 7. Panel (a) recapitulates the classical von Neumann data path (CPU ↔ shared bus ↔ memory) with the bus highlighted as the bottleneck inherited from Figure 1, drawn small enough to act as a visual anchor rather than a repeat. Panel (b) shows the *in-memory* response: a resistive crossbar with input voltages on rows, programmed conductances encoding a matrix, column currents emerging as the matrix–vector product, and an explicit annotation that no datum crosses a CPU–memory boundary during the operation. Panel (c) shows the *event-driven* response: a sparse, time-resolved input event train enters a dynamical substrate whose intrinsic relaxation is itself the computation, with only a trained linear readout downstream; a small inset trace contrasts a clocked dense waveform with the asynchronous event stream. Throughout, the emphasis is on **data flow relative to the bottleneck**, not on device figures of merit.
- **Distinction from Figure 7 (`fig:static_vs_fading`).** Figure 2 lives at the *architecture* level — it answers "where does data move during a computation, relative to the bottleneck of Figure 1." Figure 7 lives at the *device* level — it answers "what figures of merit must a single memristive cell satisfy to play either role." The two figures are deliberately complementary: Figure 2 motivates *why* two architectures are pursued; Figure 7 specifies *what the device must do* in each. Figure 2 has three panels (vN baseline + the two responses) and no figures-of-merit table; Figure 7 has two panels (one per device mode) plus the figures-of-merit inset. Figure 2 shows information flow with arrows; Figure 7 shows static device-mode contrasts. The crossbar appears in both but plays different rhetorical roles — in Figure 2 as a system that bypasses the bus, in Figure 7 as a programmable-weight cell whose retention/endurance/linearity are the metrics of interest.
- **One-sentence message.** The in-memory and event-driven paradigms attack the von Neumann bottleneck from two different directions — the first by collapsing the storage/compute boundary in space, the second by replacing clocked dense data movement with sparse temporal events flowing through a dynamical substrate whose own physics performs the computation.
- **Caption draft.**
  > Two architectural responses to the von Neumann bottleneck. (a) In the classical stored-program architecture (recapitulated from \cref{fig:vonneumann_bottleneck}), every operation traverses a CPU–memory bus that fixes the bandwidth and energy ceilings of the system. (b) In the in-memory paradigm, computation is performed inside the memory array: a resistive crossbar with programmed conductances executes an analogue matrix–vector multiplication by Ohm's and Kirchhoff's laws, so the dot product no longer crosses the CPU–memory boundary. (c) In the event-driven paradigm, dense clocked data are replaced by a sparse stream of asynchronous events that drive a dynamical substrate whose intrinsic relaxation is itself the computation; only a linear readout layer downstream is trained. The figure is intended as an architectural roadmap for \cref{subsec:paradigms} and is complementary to \cref{fig:static_vs_fading}, which addresses the device-level requirements that each paradigm places on a single memristive cell.

---

## Figure 3 — Neuron anatomy and the action-potential waveform

- **Proposed label.** `fig:neuron_action_potential`
- **Section placement.** §1.2, `subsec:neural_signal`.
- **Position relative to prose.** After the second paragraph of `subsec:neural_signal` (the paragraph that introduces the action potential, the \ce{Na+}/\ce{K+} channel sequence, the all-or-nothing character, and the explicit callback to event-driven computing in `subsec:paradigms`). The figure earns its place there because both of its panels' contents have just been described in prose: neuron anatomy in the preceding paragraph and the action-potential waveform in the paragraph it follows. It also lands before the synapse-level discussion picks up in the next paragraph and before \cref{fig:synapse_plasticity}, so the chapter's biology coverage progresses cleanly from neuron level to synapse level.
- **Figure type.** Two-panel didactic schematic. Panel (a): a labelled neuron cartoon — dendrites collecting inputs, soma, axon hillock as the firing threshold region, axon (myelinated segments optional), and axon terminals contacting a downstream cell; small arrows indicate dendritic input integration, threshold crossing at the hillock, and unidirectional propagation along the axon to the terminals. Panel (b): the action-potential waveform on a membrane-potential vs. time axis, showing resting potential, threshold, the \ce{Na+}-driven depolarisation, the peak, the \ce{K+}-driven repolarisation, the after-hyperpolarisation, and the return to rest, with the threshold and the stereotyped all-or-nothing character marked. The two panels are connected visually by indicating that the waveform of (b) is what travels along the axon of (a).
- **Distinction from Figure 4 (`fig:synapse_plasticity`).** Figure 3 is at the *cellular* level — a whole neuron and the electrical event that travels along its axon. Figure 4 is at the *sub-cellular synapse* level — the presynaptic terminal, the cleft, the postsynaptic membrane, and the plasticity-timescale ladder. Figure 3 provides the orientation that lets the reader parse Figure 4's zoom-in: the axon terminal in Figure 4 (a) is the structure at the right-hand end of Figure 3 (a), and the calcium-triggered release event in Figure 4 (a) is initiated by the action potential of Figure 3 (b) arriving at that terminal. The two figures are sequential zooms, not parallel views.
- **One-sentence message.** A neuron is a polarised cell that integrates dendritic inputs at the soma, fires a stereotyped all-or-nothing action potential at the axon hillock when the membrane potential crosses a threshold, and propagates that waveform to its synaptic terminals — a single physical sequence that anchors every later use of "spike", "spike train", "threshold", and "event-driven" in the chapter.
- **Caption draft.**
  > Anatomy of a neuron and the action-potential waveform. (a) A neuron collects synaptic inputs through its dendrites, integrates them at the soma, and fires an outgoing electrical event when the membrane potential at the axon hillock crosses a threshold; the resulting waveform propagates unidirectionally along the axon to the synaptic terminals, where it triggers chemical transmission onto downstream cells (the zoom shown in \cref{fig:synapse_plasticity}). (b) The action potential is a stereotyped millisecond-scale depolarisation produced by the opening of voltage-gated \ce{Na+} channels, followed by a \ce{K+}-mediated repolarisation and a brief after-hyperpolarisation before the return to the resting potential; its all-or-nothing character means that information about the input is carried by the timing and rate of these events rather than by their amplitude, which is the cellular basis of the event-driven view of neural computation introduced in \cref{subsec:paradigms}.

---

## Figure 4 — The chemical synapse and the plasticity timescales

- **Proposed label.** `fig:synapse_plasticity`
- **Section placement.** §1.2. The figure opens at the end of `subsec:neural_signal` and is referenced again in `subsec:plasticity`.
- **Position relative to prose.** After the paragraph that completes the description of neurotransmitter release and postsynaptic current generation in `subsec:neural_signal`. Placing the figure there lets the subsequent plasticity subsection refer back to an image the reader has already parsed.
- **Figure type.** Two-panel schematic / taxonomy. Left panel: anatomical cartoon of a chemical synapse (presynaptic terminal with vesicles, synaptic cleft, postsynaptic membrane with receptors, Ca²⁺-triggered release). Right panel: a timescale ladder summarising short-term plasticity (ms), STDP window (tens of ms), and LTP/LTD (minutes to hours), labelled by mechanism rather than by numerical value.
- **One-sentence message.** A biological synapse is a single physical element that supports a hierarchy of plasticity regimes spanning six orders of magnitude in time, and this hierarchy is the engineering target against which candidate synaptic hardware is judged.
- **Caption draft.**
  > Anatomy and plasticity regimes of the chemical synapse. (a) A presynaptic terminal releases neurotransmitter vesicles into the synaptic cleft in response to a calcium-triggered action potential, and postsynaptic receptors convert the released signal into an excitatory postsynaptic current. (b) The same synapse supports a graded hierarchy of plasticity regimes — short-term facilitation and depression on millisecond timescales, spike-timing-dependent plasticity on tens of milliseconds, and long-term potentiation and depression on timescales from minutes to hours — each associated with distinct microscopic mechanisms. This hierarchy, spanning several orders of magnitude in time in a single physical element, is the engineering target against which candidate synaptic hardware is judged in the remainder of the chapter.

---

## Figure 5 — Energy and density of synaptic-equivalent operations across biology, digital CMOS, and memristive devices

- **Proposed label.** `fig:synaptic_energy_density`
- **Section placement.** §1.2, `subsec:why_hw`.
- **Position relative to prose.** After the opening paragraph of `subsec:why_hw` that quotes \(\sim 10^{14}\)–\(10^{15}\) synapses operating at \(\sim 20\,\mathrm{W}\) in biology and contrasts that envelope with the per-operation cost of a von-Neumann CMOS implementation. The figure earns its place there because the prose has just committed to the comparison numerically; the chart fixes the comparison visually before §1.3 introduces the device alternative. It also breaks up the long stretch of unillustrated text between `fig:synapse_plasticity` (end of §1.2.2) and `fig:memristor_theory_fingerprint` (in §1.3.1), which currently spans the entirety of §1.2.3 and the §1.3 / §1.3.1 introductions.
- **Figure type.** Single-panel log–log scatter / bubble plot. Axes: energy per synaptic-equivalent event (x) versus areal synaptic density (y). Marker classes:
  - **Biology** anchor: cortical synaptic region placed from the per-event energy estimate of Attwell & Laughlin and the cortical synaptic-density estimate of Herculano-Houzel, drawn as a labelled bounded region rather than a point to acknowledge the spread.
  - **Digital CMOS neuromorphic** envelope: representative ranges drawn from the published large-scale platforms cited via Indiveri & Liu (e.g., TrueNorth-class, Loihi-class, SpiNNaker-class order-of-magnitude regions), with the per-event energy dominated by SRAM-cell access plus arithmetic and the density limited by the cell + multiplier footprint.
  - **Inorganic memristive** families: metal-oxide filamentary, PCM, and STT-MTJ, drawn from the same review sources as the inorganic comparison matrix (Sun 2019; Ielmini & Wong 2018; Kuzum 2013) so that the two figures stay quantitatively consistent.
  - **Organic / soft-ionic target band**: forward-referenced to §1.5–§1.6, drawn as a target arrow / shaded band rather than as a published cluster — this is the design space the thesis proposes to occupy, not a survey of existing demonstrations.
- A diagonal **iso-power reference line** corresponding to the \(\sim 20\,\mathrm{W}\) brain-scale envelope (energy per event × density × characteristic event rate) is overlaid to anchor the plot to the power budget quoted in the prose.
- All numerical envelopes are conservative orders of magnitude drawn from the indicated reviews; individual devices may sit outside the bands shown. No invented numbers.
- **Distinction from Figure 1 (`fig:vonneumann_bottleneck`) and from the inorganic comparison matrix (now Figure 8).** Figure 1 expresses the *system-level* energy asymmetry between arithmetic and data movement, qualitatively, with no density axis; this figure expresses the *element-level* energy of one synaptic-equivalent event and pairs it with a density axis. The inorganic comparison matrix compares memristor families on qualitative axes (retention, tunability, substrate compatibility, reservoir-readiness); this figure compares the same families plus biology and digital CMOS on two quantitative physical axes. The three figures answer different questions, and the chapter's energy-and-density argument benefits from carrying all three.
- **One-sentence message.** Biological synapses, digital CMOS neuromorphic implementations, and present-day inorganic memristive families occupy distinct, largely non-overlapping regions of the energy-per-event / density plane, and the soft-ionic two-terminal route developed in the rest of the chapter is the only one positioned to approach the biological region on both axes simultaneously.
- **Caption draft.**
  > Approximate energy and density envelopes of synaptic-equivalent operations across implementation regimes. Each cluster represents a class of physical realisation: biological cortical synapses, digital CMOS neuromorphic implementations in which a synapse occupies an SRAM cell plus an arithmetic unit, the inorganic memristor families surveyed in §\ref{sec:inorganic_memristors}, and the soft-ionic composite target region forward-referenced to §\ref{sec:polymer_electrolyte_composites}. The diagonal reference line marks the brain-scale iso-power envelope (\(\sim 20\,\mathrm{W}\) for \(\sim 10^{14}\)–\(10^{15}\) synapses) introduced at the start of §\ref{subsec:why_hw}. Numerical bounds are conservative orders of magnitude drawn from the reviews cited in the surrounding text (Attwell & Laughlin 2001; Herculano-Houzel 2009; Kuzum 2013; Indiveri & Liu 2015; Ielmini & Wong 2018; Sun 2019); individual devices may sit outside the envelopes shown. The figure complements \cref{fig:vonneumann_bottleneck}, which makes the same energy-asymmetry argument at the system level, and \cref{fig:inorganic_comparison_matrix}, which compares the inorganic families on qualitative rather than quantitative axes.

---

## Figure 6 — The memristor as the fourth circuit element and its pinched-hysteresis fingerprint

- **Proposed label.** `fig:memristor_theory_fingerprint`
- **Section placement.** §1.3. The figure is positioned at the end of `subsec:tio2_memristor`, once the TiO₂ demonstration has been discussed.
- **Position relative to prose.** After the paragraph that identifies oxygen-vacancy drift in TiO₂ as the microscopic origin of the measured pinched hysteresis. At that point the reader has been given the Chua quadrant argument and a concrete physical realisation, so the figure ties the symbolic and experimental views together.
- **Figure type.** Two-panel didactic schematic. Left panel: the constitutive-relations diagram of the four fundamental circuit elements — resistor (v–i), capacitor (v–q), inductor (i–φ), memristor (q–φ) — with the fourth element highlighted. Right panel: an idealised pinched-hysteresis current–voltage loop at two driving frequencies, showing the characteristic narrowing of the loop with increasing frequency.
- **One-sentence message.** The memristor is defined by a charge–flux constitutive relation that the other three passive elements do not express, and its macroscopic fingerprint is a frequency-dependent pinched hysteresis in the current–voltage plane.
- **Caption draft.**
  > The memristor as a constitutive element and its experimental fingerprint. (a) The four fundamental two-terminal passive circuit elements, arranged by the pair of constitutive variables they relate: the resistor (v–i), the capacitor (v–q), the inductor (i–φ), and the memristor (q–φ), which completes the quadrant. (b) A memristive device driven by a periodic voltage exhibits a pinched current–voltage hysteresis loop that narrows with increasing driving frequency and that passes through the origin at each zero-crossing; this loop is the unique experimental signature of memristive operation and is observed in all of the device families surveyed in the remainder of the chapter.

---

## Figure 7 — Static programmable weights versus volatile fading-memory elements

- **Proposed label.** `fig:static_vs_fading`
- **Section placement.** §1.3. End of `subsec:volatile_paradigms`.
- **Position relative to prose.** After the paragraph that states explicitly that retention time is a design variable, not a figure of merit to be maximised, and that device-to-device heterogeneity can be a resource in a reservoir. The figure earns its place by making the two complementary computational modes visually comparable in a single frame.
- **Figure type.** Two-panel conceptual schematic. Left panel: a trained crossbar array performing a matrix–vector multiplication, with each cell holding a programmed conductance (static weight). Right panel: a reservoir of volatile nodes driven by a time-varying input, each with a different decay time constant, followed by a trained linear readout layer. A small inset table lists the figures of merit appropriate to each mode (retention, endurance, ON/OFF for the crossbar; memory capacity, class separability, timescale spread for the reservoir).
- **One-sentence message.** Memristive hardware supports at least two complementary computational modes — static programmable weights for trained networks, and volatile fading-memory elements for temporal processing — and each mode has its own set of relevant figures of merit.
- **Caption draft.**
  > Two complementary computational roles for memristive devices. (a) A trained crossbar holds programmed conductances as non-volatile weights and performs matrix–vector multiplication by Ohm's and Kirchhoff's laws; here retention, endurance, linearity and symmetry are the relevant figures of merit. (b) A reservoir of volatile fading-memory nodes, driven by a time-varying input, projects temporal signals into a high-dimensional dynamical state; only a linear readout layer is trained, and the relevant figures of merit become memory capacity, class separability, and the spread of available time constants. The thesis treats these two modes as complementary targets for memristive hardware rather than as a hierarchy, and develops the second of them as the primary application of the polymer-electrolyte composite family.

---

## Figure 8 — Inorganic memristor families: comparison matrix

- **Proposed label.** `fig:inorganic_comparison_matrix`
- **Section placement.** §1.4. End of `subsec:inorganic_limits`. Replaces the existing `% TODO:` comment at the end of §1.4 and supersedes the original intention to defer it until after the organic section; the organic section is now drafted, so the comparison can be made symmetric with a final "soft ionic" column for the polymer-electrolyte route developed in §1.5 and §1.6.
- **Position relative to prose.** After the closing paragraph of `subsec:inorganic_limits` that articulates the four shared constraints of the inorganic families. The figure consolidates the section's comparative argument and prepares the reader for the organic landscape that follows.
- **Figure type.** Comparison matrix. Rows: metal-oxide memristors, phase-change memory, STT-MTJ, soft ionic (polymer electrolyte composite, forward-referenced). Columns: retention (volatile ↔ non-volatile range), analogue tunability / number of reliable states, chemical tunability, substrate compatibility (vacuum / high-T vs. solution / mild-T), reservoir-readiness. Entries qualitative (symbols or shaded bands), not numerical.
- **One-sentence message.** The inorganic memristor families cover complementary regions of the memristive design space, but the combination of analogue, chemically tunable, timescale-rich operation on solution-processable substrates is not where any of them is most naturally located.
- **Caption draft.**
  > Comparison of inorganic memristor families with the soft-ionic composite route pursued in this thesis. For each family, qualitative assessments are shown along five axes: retention (the range of fading-memory to non-volatile behaviour that has been demonstrated), analogue tunability (the number of reliably programmable intermediate states), chemical tunability (the extent to which composition acts as an independent design handle on the switching physics), substrate compatibility (vacuum/high-temperature workflows versus solution-processable and mild-temperature workflows), and reservoir-readiness (suitability as a fading-memory node in a temporal-computing scheme). The comparison is intended to locate each family in the design space rather than to rank them; the soft-ionic row is forward-referenced and is developed in §\ref{sec:organic_memristors} and §\ref{sec:polymer_electrolyte_composites}.

---

## Figure 9 — Organic memristor historical landscape

- **Proposed label.** `fig:organic_timeline`
- **Section placement.** §1.5. End of `subsec:organic_history`. Replaces the existing `% TODO:` comment at the end of that subsection.
- **Position relative to prose.** After the concluding paragraph of `subsec:organic_history` that states what the field had and had not consolidated by the early 2020s. The figure condenses the preceding narrative survey into a visual form the reader can refer back to during §1.6 and §1.7.
- **Figure type.** Timeline / taxonomy hybrid. Horizontal axis: year (approximate, from the late 2000s to the early 2020s). Rows, grouped by mechanism family: early ionic/electrochemical cells (Zakhidov/Malliaras), simple polymer-film devices (Lei), two-terminal redox biomimetics (Liu), three-terminal OECT synaptic devices (Gkoupidenis, Xu, van de Burgt/ENODe, Fuller), flexible/nervetronic synaptic devices (Kim, Park), molecular memristors (Goswami), organic reservoir-computing demonstrations (Cucchi). Each entry is a small labelled marker on the axis rather than a paragraph block.
- **One-sentence message.** The organic memristor field is not a single lineage but a set of parallel mechanism-driven streams whose individually demonstrated features had not yet been combined, by the early 2020s, into a two-terminal ion-mediated platform with both reversibility and analogue control.
- **Caption draft.**
  > Historical landscape of organic memristive and organic synaptic devices, arranged by mechanism family and by year of representative publication. Early ionic and electrochemical demonstrations, simple polymer-film bistable devices, two-terminal redox biomimetics, three-terminal electrochemical-transistor synaptic devices, flexible and nervetronic synaptic devices, molecular memristors, and organic reservoir-computing demonstrations are shown as parallel streams rather than as steps of a single lineage. The view supports the observation that, by the early 2020s, several of the individually demanding features of a neuromorphic organic device had each been demonstrated, but that no single two-terminal platform combined reversibility, multi-state analogue behaviour, and a clearly interpretable ion-mediated mechanism.

---

## Figure 10 — Two-terminal polymer-electrolyte composite architecture and the composition/cation timescale ladder

- **Proposed label.** `fig:composite_architecture_timescale_ladder`
- **Section placement.** §1.6. End of `subsec:composite_rationale`. Replaces the existing `% TODO:` comment at the end of §1.6.
- **Position relative to prose.** After the paragraph that articulates composition and cation identity as computational design knobs and introduces the temporal-kernel-bank view. The figure is the thesis-central device figure and also bridges directly into Chapter 2; placing it at the end of §1.6 lets the reader carry a concrete mental image of the device across the chapter boundary.
- **Figure type.** Two-panel schematic. Panel (a): a cross-section of the vertical two-terminal composite device — bottom ITO electrode on glass, composite active layer containing a conjugated polymer network, a polyether host with coordinated cations, and a dissociated salt, topped by an evaporated silver electrode; arrows indicate ionic redistribution under bias. Panel (b): a qualitative timescale ladder along which the \ce{Li+}, \ce{Na+}, \ce{K+} cation substitution and the composition knobs of the host/salt ratios are expected to place the fading-memory time constant, with ordering but without numerical values, to be made quantitative by the Chapter 3 delay-time fits. A small side cartoon may optionally contrast this two-terminal composite with the three-terminal OECT architecture referenced throughout §1.5 and §1.6.
- **One-sentence message.** The thesis-specific device is a vertical two-terminal composite in which a conjugated semiconductor and a polyether-hosted alkali salt share a single active layer, and its fading-memory timescale is expected to be set by the cation and composition chemistry of that layer.
- **Caption draft.**
  > The thesis-specific polymer-electrolyte composite device and its chemically tunable dynamical timescale. (a) Vertical two-terminal stack: a solution-processed composite active layer, combining a conjugated semiconducting polymer network with a polyether host, coordinated alkali-metal cations, and a dissociated salt, is sandwiched between a patterned ITO bottom electrode and an evaporated silver top electrode; the internal state of the device is set by the residual ionic distribution that remains after a driving bias is removed. (b) Qualitative timescale ladder on which the cation identity (\ce{Li+} through \ce{Na+} to \ce{K+}, weakening the cation–oxygen coordination) and the composition knobs of the host/salt ratios are expected to place the fading-memory time constant of the device. The ordering is the central hypothesis developed from the physical-chemistry argument of §\ref{sec:polymer_electrolyte_composites}; its quantitative test is the object of Chapter 3.

---

## Not selected, with reason

The following candidates were considered but not retained in the current nine-figure plan:

- **HSAB periodic-table excerpt in §1.6.1.** The HSAB ordering is compact enough to carry in prose and is reused in Figure 9 (b) as a labelled axis; a dedicated periodic-table figure would duplicate material that the reader can already parse.
- **Taxonomy figure in `subsec:memristor_classes`.** The mechanism classification is already absorbed into Figure 7 (the inorganic comparison matrix) and Figure 8 (the organic timeline) from the opposite direction; a separate taxonomy figure in §1.3.3 would duplicate those without adding a new axis of comparison.
- **Dedicated LEC operating-principle schematic in `subsec:lec_precedent`.** The LEC argument is conceptual, not architectural, and the section is explicit that the thesis is not about light emission; a figure there would divert attention from the precedent argument to the LEC device itself.
- **Detailed behavioural-model block diagram for Chapter 4 in §1.7.** Chapter 4 has its own planning document (`handouts/04_chapter4_temporal_computing_plan.md`) and its own figure budget; the Chapter 1 outline should not preempt it.

---

## Next actions (for later passes, not now)

1. Commission or draft the ten figures as vector graphics.
2. Assign filenames under `figures/chapter1/` at that point.
3. Insert `\begin{figure} ... \end{figure}` floats carrying the labels and captions above, positioned as specified. Three of the ten (Figures 8, 9, 10) replace existing `% TODO:` comments at the ends of §1.4, §1.5, and §1.6; the remaining seven (Figures 1, 2, 3, 4, 5, 6, 7) are fresh insertions in subsections that do not currently carry a TODO marker.
4. Re-run `pdflatex → biber → pdflatex × 2` and verify that all cross-references to the new labels resolve.
