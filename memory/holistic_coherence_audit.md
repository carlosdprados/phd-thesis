---
name: holistic-coherence-audit
description: 2026-06-12 whole-thesis coherence/Frankenstein audit; decision NOT to expand the lock-in/frequency findings or build a new Ch5 sim; keep illustrative corpora from rivalling the replicated spine
metadata:
  type: project
---

Holistic coherence audit of the thesis, 2026-06-12 (after the lock-in corpus integration, handout 29). User worried it read like a "Frankenstein" of accreted findings.

**Verdict: the spine is sound, not a Frankenstein.** Frontmatter's four evidence levels (exemplar → reproducibility/method → composition+chemistry control → temporal computing), the Ch6 four-layer close, and the chapter bridges all align. Backbone left untouched.

**The actual risk was concentrated in two places, both fixed:**
1. Ch4 §4.8 had swollen — three separately-mined *illustrative-tier* corpora (silver/gold electrode, gold negative-polarity, lock-in frequency sweeps), all at the lead composition, all generation-confounded, collectively rivalling the *replicated* composition core (§4.4) in length. Fix (commit 349bd7c): compressed the lock-in mega-paragraph to its two load-bearing claims (AC counterpart of the rate-gated window; bias-activated sub-10 Hz gain), pushed detail to SI C.8, collapsed the per-corpus caveat pile into one tiered statement, de-duplicated the gold cation-null restatement.
2. LLM-tics reintroduced by the post-audit additions. Fixed prose `provenance`→origin/source; softened Ch6 "replicated three times" enumeration; cut defensive **honesty-narration** ("deliberately unflattering and clarifying", "must be asked honestly", "the honest reading", "reported … rather than omitted", "equally disciplined") in Ch5/Ch6 (commit bd705c8) — scope statements and error bars kept, only the self-commentary dropped.

**Two decisions to NOT re-open (user asked directly):**
- The frequency-sweep / lock-in findings do **not** merit *more* main-body space. Illustrative tier (one batch, substrate-confounded cations), and the bias-programmed amplifier is an orthogonal *analog front-end* role, off the fading-memory→temporal-computing spine. Correct move was consolidate/compress, not expand. Its home is the compressed §4.8 block + the one Ch6 outlook line.
- Do **not** build a new Ch5 affective simulation from them. Would rest on a substrate-confounded single batch, and the "amplifier" maps onto a front-end, not a reservoir *node* — it would manufacture exactly the directionless accretion to avoid.

**Standing principle:** any future corpus added to Ch4 §4.8 (or similar) must stay compressed and clearly sub-tiered so it does not rival the replicated composition spine. Build stayed 268→267 pp, 0 undefined refs. See [[lockin_au_tmpe_corpus]], [[uncategorized_au_tmpe_corpus]], [[claim_tier_preference]].

**CORRECTION (user, same day): stop calling it a "cation null" — it is NOT a null.** The cation *does* shift the dynamics: silver \TMPE{}/triflate retention runs Li 3.8 → Na 5.0 → K 6.7 s (a real ~1.8× monotone ordering), and the lock-in junction capacitance runs K>Na>Li ~1.4×. What actually fails is the *specific hypothesised* \ce{Li+}>\ce{Na+}>\ce{K+} coordination law: the triflate retention runs the REVERSE (K longest), it re-orders with the anion (TFSI flips it), and at n=1–2 no host/anion-independent ordering can be fixed. The genuinely flat probes — ATR ion-association, UV-Vis optical gap — are *different observables* (ion pairing, electronic structure) that are *expected* to be flat under the thesis premise; they were wrongly enlisted as "the cation null confirmed three ways." Correct framing everywhere: "the cation shifts the dynamics but not in the predicted direction and not as a transferable law; what is missing is power, not effect." Reframed Ch4 §4.5/§4.8/§4.9/limitations, Ch6 summary/Q2/outlook, SI C cation paragraph (commit after build). The "cation null" wording in earlier memory notes ([[chapter3_electrode_au]], [[uncategorized_au_tmpe_corpus]], [[lockin_au_tmpe_corpus]]) is this same mis-frame — read those as "predicted ordering not established," not "no effect."
