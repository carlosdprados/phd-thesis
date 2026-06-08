# Current Chapter Numbering

This repository follows the bound thesis order everywhere in active source,
analysis scripts, figure directories, and current machine-readable handout CSVs.

| Bound chapter | Role | Chapter source | Figures | Active scripts / data prefixes |
| --- | --- | --- | --- | --- |
| 1 | Introduction | `chapters/chapter1_introduction.tex` | `figures/chapter1/` | `ch1_*` figure assets |
| 2 | Proof of concept | `chapters/chapter2_proof_of_concept.tex` | `figures/chapter2/` | `scripts/ch2_figures.py` |
| 3 | Reproducibility bridge | `chapters/chapter3_bridge.tex` | `figures/chapter3/` | `scripts/bridge_*.py` |
| 4 | Comparative experimental study | `chapters/chapter4_comparative.tex` | `figures/chapter4/` | `scripts/ch4_*.py`, `handouts/ch4_*.csv` |
| 5 | Temporal-computing simulations | `chapters/chapter5_temporal.tex` | `figures/chapter5/` | `scripts/ch5_*.py`, `handouts/ch5_*.csv` |
| 6 | Conclusions | `chapters/chapter6_conclusions.tex` | n/a | n/a |

Historical planning handouts may still discuss the older five-chapter plan, in
which the comparative study was Chapter 3 and the temporal-computing work was
Chapter 4. Treat those as provenance only. For current work, trust `thesis.tex`,
this file, and the active filenames above.
