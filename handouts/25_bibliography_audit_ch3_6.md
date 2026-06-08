# Bibliography Audit — Chapters 3–6 (CrossRef verification)

Date: 2026-06-08
Scope: every `\cite` key used in Ch3 (bridge), Ch4 (comparative), Ch5 (temporal),
Ch6 (conclusions) that is **not** already in the previously-verified Ch1/Ch2 set.
Method: each DOI-bearing entry queried against the live CrossRef API
(`api.crossref.org/works/<DOI>`); title, year, first author, and journal compared
against `bibliography/references.bib`.

## Result: all clean — no hallucinated DOIs or titles

11 keys are new to Ch3–6. 9 carry DOIs and were verified against CrossRef; 2 are
non-CrossRef source types (verified by type, not API).

| Key | DOI | CrossRef match |
|---|---|---|
| Appeltant2011 | 10.1038/ncomms1476 | ✅ title/year/author/journal exact |
| AtiyaParlos2000 | 10.1109/72.846741 | ✅ exact |
| Boucsein2012EDA | 10.1007/978-1-4614-1126-0 | ✅ exact (book, Springer US) |
| Munar2012 | 10.1002/adfm.201102687 | ✅ exact |
| Picard1997 | 10.7551/mitpress/1140.001.0001 | ✅ exact (book, MIT Press) |
| Schmidt2018WESAD | 10.1145/3242969.3242985 | ✅ exact (ICMI '18) |
| Sturman2003 | 10.1103/PhysRevLett.91.176602 | ✅ exact |
| TaskForce1996HRV | 10.1161/01.CIR.93.5.1043 | ✅ exact (Circulation) |
| Vallee1992 | 10.1016/0013-4686(92)80115-3 | ✅ exact |

Non-CrossRef (cited correctly by source type, no DOI expected):

| Key | Type | Note |
|---|---|---|
| Jaeger2002STM | techreport | GMD Report 152, German National Research Center for IT — canonical RC reference, not in CrossRef |
| ChourpiliadisBhardwaj2022 | online | StatPearls (NCBI Bookshelf), URL + urldate present |

## Action taken
- Hardened the Ch3 hydrolysis-lability claim: grounded it explicitly in the
  ester/amide bond chemistry and cited both Hybrane sources already in the bib
  (`Froehling2004`, `VoitLederer2009`) rather than a single review. No new bib
  entry was introduced, to avoid adding an unverified citation.

## Status of the thesis bibliography
- Ch1: previously fixed (hallucinated DOIs removed).
- Ch2: previously CrossRef-verified clean.
- **Ch3–Ch6 (this audit): CrossRef-verified clean.**

The full thesis citation base is now CrossRef-verified.
