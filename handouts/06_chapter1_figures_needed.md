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

Seven insertion points met the criteria. They are listed in reading order.

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

## Figure 2 — The chemical synapse and the plasticity timescales

- **Proposed label.** `fig:synapse_plasticity`
- **Section placement.** §1.2. The figure opens at the end of `subsec:neural_signal` and is referenced again in `subsec:plasticity`.
- **Position relative to prose.** After the paragraph that completes the description of neurotransmitter release and postsynaptic current generation in `subsec:neural_signal`. Placing the figure there lets the subsequent plasticity subsection refer back to an image the reader has already parsed.
- **Figure type.** Two-panel schematic / taxonomy. Left panel: anatomical cartoon of a chemical synapse (presynaptic terminal with vesicles, synaptic cleft, postsynaptic membrane with receptors, Ca²⁺-triggered release). Right panel: a timescale ladder summarising short-term plasticity (ms), STDP window (tens of ms), and LTP/LTD (minutes to hours), labelled by mechanism rather than by numerical value.
- **One-sentence message.** A biological synapse is a single physical element that supports a hierarchy of plasticity regimes spanning six orders of magnitude in time, and this hierarchy is the engineering target against which candidate synaptic hardware is judged.
- **Caption draft.**
  > Anatomy and plasticity regimes of the chemical synapse. (a) A presynaptic terminal releases neurotransmitter vesicles into the synaptic cleft in response to a calcium-triggered action potential, and postsynaptic receptors convert the released signal into an excitatory postsynaptic current. (b) The same synapse supports a graded hierarchy of plasticity regimes — short-term facilitation and depression on millisecond timescales, spike-timing-dependent plasticity on tens of milliseconds, and long-term potentiation and depression on timescales from minutes to hours — each associated with distinct microscopic mechanisms. This hierarchy, spanning several orders of magnitude in time in a single physical element, is the engineering target against which candidate synaptic hardware is judged in the remainder of the chapter.

---

## Figure 3 — The memristor as the fourth circuit element and its pinched-hysteresis fingerprint

- **Proposed label.** `fig:memristor_theory_fingerprint`
- **Section placement.** §1.3. The figure is positioned at the end of `subsec:tio2_memristor`, once the TiO₂ demonstration has been discussed.
- **Position relative to prose.** After the paragraph that identifies oxygen-vacancy drift in TiO₂ as the microscopic origin of the measured pinched hysteresis. At that point the reader has been given the Chua quadrant argument and a concrete physical realisation, so the figure ties the symbolic and experimental views together.
- **Figure type.** Two-panel didactic schematic. Left panel: the constitutive-relations diagram of the four fundamental circuit elements — resistor (v–i), capacitor (v–q), inductor (i–φ), memristor (q–φ) — with the fourth element highlighted. Right panel: an idealised pinched-hysteresis current–voltage loop at two driving frequencies, showing the characteristic narrowing of the loop with increasing frequency.
- **One-sentence message.** The memristor is defined by a charge–flux constitutive relation that the other three passive elements do not express, and its macroscopic fingerprint is a frequency-dependent pinched hysteresis in the current–voltage plane.
- **Caption draft.**
  > The memristor as a constitutive element and its experimental fingerprint. (a) The four fundamental two-terminal passive circuit elements, arranged by the pair of constitutive variables they relate: the resistor (v–i), the capacitor (v–q), the inductor (i–φ), and the memristor (q–φ), which completes the quadrant. (b) A memristive device driven by a periodic voltage exhibits a pinched current–voltage hysteresis loop that narrows with increasing driving frequency and that passes through the origin at each zero-crossing; this loop is the unique experimental signature of memristive operation and is observed in all of the device families surveyed in the remainder of the chapter.

---

## Figure 4 — Static programmable weights versus volatile fading-memory elements

- **Proposed label.** `fig:static_vs_fading`
- **Section placement.** §1.3. End of `subsec:volatile_paradigms`.
- **Position relative to prose.** After the paragraph that states explicitly that retention time is a design variable, not a figure of merit to be maximised, and that device-to-device heterogeneity can be a resource in a reservoir. The figure earns its place by making the two complementary computational modes visually comparable in a single frame.
- **Figure type.** Two-panel conceptual schematic. Left panel: a trained crossbar array performing a matrix–vector multiplication, with each cell holding a programmed conductance (static weight). Right panel: a reservoir of volatile nodes driven by a time-varying input, each with a different decay time constant, followed by a trained linear readout layer. A small inset table lists the figures of merit appropriate to each mode (retention, endurance, ON/OFF for the crossbar; memory capacity, class separability, timescale spread for the reservoir).
- **One-sentence message.** Memristive hardware supports at least two complementary computational modes — static programmable weights for trained networks, and volatile fading-memory elements for temporal processing — and each mode has its own set of relevant figures of merit.
- **Caption draft.**
  > Two complementary computational roles for memristive devices. (a) A trained crossbar holds programmed conductances as non-volatile weights and performs matrix–vector multiplication by Ohm's and Kirchhoff's laws; here retention, endurance, linearity and symmetry are the relevant figures of merit. (b) A reservoir of volatile fading-memory nodes, driven by a time-varying input, projects temporal signals into a high-dimensional dynamical state; only a linear readout layer is trained, and the relevant figures of merit become memory capacity, class separability, and the spread of available time constants. The thesis treats these two modes as complementary targets for memristive hardware rather than as a hierarchy, and develops the second of them as the primary application of the polymer-electrolyte composite family.

---

## Figure 5 — Inorganic memristor families: comparison matrix

- **Proposed label.** `fig:inorganic_comparison_matrix`
- **Section placement.** §1.4. End of `subsec:inorganic_limits`. Replaces the existing `% TODO:` comment at the end of §1.4 and supersedes the original intention to defer it until after the organic section; the organic section is now drafted, so the comparison can be made symmetric with a final "soft ionic" column for the polymer-electrolyte route developed in §1.5 and §1.6.
- **Position relative to prose.** After the closing paragraph of `subsec:inorganic_limits` that articulates the four shared constraints of the inorganic families. The figure consolidates the section's comparative argument and prepares the reader for the organic landscape that follows.
- **Figure type.** Comparison matrix. Rows: metal-oxide memristors, phase-change memory, STT-MTJ, soft ionic (polymer electrolyte composite, forward-referenced). Columns: retention (volatile ↔ non-volatile range), analogue tunability / number of reliable states, chemical tunability, substrate compatibility (vacuum / high-T vs. solution / mild-T), reservoir-readiness. Entries qualitative (symbols or shaded bands), not numerical.
- **One-sentence message.** The inorganic memristor families cover complementary regions of the memristive design space, but the combination of analogue, chemically tunable, timescale-rich operation on solution-processable substrates is not where any of them is most naturally located.
- **Caption draft.**
  > Comparison of inorganic memristor families with the soft-ionic composite route pursued in this thesis. For each family, qualitative assessments are shown along five axes: retention (the range of fading-memory to non-volatile behaviour that has been demonstrated), analogue tunability (the number of reliably programmable intermediate states), chemical tunability (the extent to which composition acts as an independent design handle on the switching physics), substrate compatibility (vacuum/high-temperature workflows versus solution-processable and mild-temperature workflows), and reservoir-readiness (suitability as a fading-memory node in a temporal-computing scheme). The comparison is intended to locate each family in the design space rather than to rank them; the soft-ionic row is forward-referenced and is developed in §\ref{sec:organic_memristors} and §\ref{sec:polymer_electrolyte_composites}.

---

## Figure 6 — Organic memristor historical landscape

- **Proposed label.** `fig:organic_timeline`
- **Section placement.** §1.5. End of `subsec:organic_history`. Replaces the existing `% TODO:` comment at the end of that subsection.
- **Position relative to prose.** After the concluding paragraph of `subsec:organic_history` that states what the field had and had not consolidated by the early 2020s. The figure condenses the preceding narrative survey into a visual form the reader can refer back to during §1.6 and §1.7.
- **Figure type.** Timeline / taxonomy hybrid. Horizontal axis: year (approximate, from the late 2000s to the early 2020s). Rows, grouped by mechanism family: early ionic/electrochemical cells (Zakhidov/Malliaras), simple polymer-film devices (Lei), two-terminal redox biomimetics (Liu), three-terminal OECT synaptic devices (Gkoupidenis, Xu, van de Burgt/ENODe, Fuller), flexible/nervetronic synaptic devices (Kim, Park), molecular memristors (Goswami), organic reservoir-computing demonstrations (Cucchi). Each entry is a small labelled marker on the axis rather than a paragraph block.
- **One-sentence message.** The organic memristor field is not a single lineage but a set of parallel mechanism-driven streams whose individually demonstrated features had not yet been combined, by the early 2020s, into a two-terminal ion-mediated platform with both reversibility and analogue control.
- **Caption draft.**
  > Historical landscape of organic memristive and organic synaptic devices, arranged by mechanism family and by year of representative publication. Early ionic and electrochemical demonstrations, simple polymer-film bistable devices, two-terminal redox biomimetics, three-terminal electrochemical-transistor synaptic devices, flexible and nervetronic synaptic devices, molecular memristors, and organic reservoir-computing demonstrations are shown as parallel streams rather than as steps of a single lineage. The view supports the observation that, by the early 2020s, several of the individually demanding features of a neuromorphic organic device had each been demonstrated, but that no single two-terminal platform combined reversibility, multi-state analogue behaviour, and a clearly interpretable ion-mediated mechanism.

---

## Figure 7 — Two-terminal polymer-electrolyte composite architecture and the composition/cation timescale ladder

- **Proposed label.** `fig:composite_architecture_timescale_ladder`
- **Section placement.** §1.6. End of `subsec:composite_rationale`. Replaces the existing `% TODO:` comment at the end of §1.6.
- **Position relative to prose.** After the paragraph that articulates composition and cation identity as computational design knobs and introduces the temporal-kernel-bank view. The figure is the thesis-central device figure and also bridges directly into Chapter 2; placing it at the end of §1.6 lets the reader carry a concrete mental image of the device across the chapter boundary.
- **Figure type.** Two-panel schematic. Panel (a): a cross-section of the vertical two-terminal composite device — bottom ITO electrode on glass, composite active layer containing a conjugated polymer network, a polyether host with coordinated cations, and a dissociated salt, topped by an evaporated silver electrode; arrows indicate ionic redistribution under bias. Panel (b): a qualitative timescale ladder along which the \ce{Li+}, \ce{Na+}, \ce{K+} cation substitution and the composition knobs of the host/salt ratios are expected to place the fading-memory time constant, with ordering but without numerical values, to be made quantitative by the Chapter 3 delay-time fits. A small side cartoon may optionally contrast this two-terminal composite with the three-terminal OECT architecture referenced throughout §1.5 and §1.6.
- **One-sentence message.** The thesis-specific device is a vertical two-terminal composite in which a conjugated semiconductor and a polyether-hosted alkali salt share a single active layer, and its fading-memory timescale is expected to be set by the cation and composition chemistry of that layer.
- **Caption draft.**
  > The thesis-specific polymer-electrolyte composite device and its chemically tunable dynamical timescale. (a) Vertical two-terminal stack: a solution-processed composite active layer, combining a conjugated semiconducting polymer network with a polyether host, coordinated alkali-metal cations, and a dissociated salt, is sandwiched between a patterned ITO bottom electrode and an evaporated silver top electrode; the internal state of the device is set by the residual ionic distribution that remains after a driving bias is removed. (b) Qualitative timescale ladder on which the cation identity (\ce{Li+} through \ce{Na+} to \ce{K+}, weakening the cation–oxygen coordination) and the composition knobs of the host/salt ratios are expected to place the fading-memory time constant of the device. The ordering is the central hypothesis developed from the physical-chemistry argument of §\ref{sec:polymer_electrolyte_composites}; its quantitative test is the object of Chapter 3.

---

## Not selected, with reason

The following candidates were considered but not retained in the current seven-figure plan:

- **HSAB periodic-table excerpt in §1.6.1.** The HSAB ordering is compact enough to carry in prose and is reused in Figure 7 (b) as a labelled axis; a dedicated periodic-table figure would duplicate material that the reader can already parse.
- **Taxonomy figure in `subsec:memristor_classes`.** The mechanism classification is already absorbed into Figure 5 (the inorganic comparison matrix) and Figure 6 (the organic timeline) from the opposite direction; a separate taxonomy figure in §1.3.3 would duplicate those without adding a new axis of comparison.
- **Dedicated LEC operating-principle schematic in `subsec:lec_precedent`.** The LEC argument is conceptual, not architectural, and the section is explicit that the thesis is not about light emission; a figure there would divert attention from the precedent argument to the LEC device itself.
- **Detailed behavioural-model block diagram for Chapter 4 in §1.7.** Chapter 4 has its own planning document (`handouts/04_chapter4_temporal_computing_plan.md`) and its own figure budget; the Chapter 1 outline should not preempt it.

---

## Next actions (for later passes, not now)

1. Commission or draft the seven figures as vector graphics.
2. Assign filenames under `figures/chapter1/` at that point.
3. Replace the three outstanding `% TODO:` comments in the chapter source with `\begin{figure} ... \end{figure}` floats carrying the labels and captions above, positioned as specified.
4. Re-run `pdflatex → biber → pdflatex × 2` and verify that all cross-references to the new labels resolve.
