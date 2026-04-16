# PhD Thesis Repository

Working repository for the PhD thesis on ion-mediated polymeric memristive devices.

## Structure

- `thesis.tex`: top-level entrypoint that assembles all chapters into a single bound thesis.
- `handouts/`: planning documents, chapter outlines, and working notes.
- `chapters/`: LaTeX chapter source files under active thesis development.
- `bibliography/`: shared BibLaTeX database files.
- `figures/`: thesis figures and exported graphics.
- `exports/`: committed PDF snapshots of chapters and the full thesis (tracked in git).
- `build/`: generated LaTeX outputs. Ignored by git.
- `.vscode/`: workspace settings for LaTeX Workshop and editor behavior.

## Current Working Files

- `thesis.tex`: top-level build, \include's every chapter.
- `chapters/chapter1_introduction.tex`: current Chapter 1 draft (also compiles standalone).
- `chapters/chapter2_proof_of_concept.tex`: current Chapter 2 draft (also compiles standalone).
- `bibliography/references.bib`: bibliography database used by the LaTeX sources.
- `handouts/00_...` to `05_...`: thesis planning and structure handouts.

## LaTeX Workflow

Chapter files are designed to compile both standalone and as part of the full
thesis. Each chapter wraps its standalone preamble in an
`\ifdefined\thesismode\else ... \fi` guard that `thesis.tex` neutralises by
defining `\thesismode` before `\include`-ing the chapters. The full-thesis
build prints a single unified bibliography from `thesis.tex`; standalone
chapter builds keep their own `\printbibliography` inside the guard.

Repo-level build targets:

```sh
make chapter1       # build/chapters/chapter1_introduction.pdf
make chapter2       # build/chapters/chapter2_proof_of_concept.pdf
make thesis         # build/thesis.pdf
make all            # chapter1 + chapter2 + thesis
make exports        # refresh exports/*.pdf snapshots
make clean          # remove all generated artefacts
```

Direct terminal equivalents (run from the repo root):

```sh
# Chapter 1 / Chapter 2 (standalone)
cd chapters && latexmk -pdf -outdir=../build/chapters chapter1_introduction.tex
cd chapters && latexmk -pdf -outdir=../build/chapters chapter2_proof_of_concept.tex

# Full thesis
TEXINPUTS=./chapters: latexmk -pdf -outdir=build thesis.tex
```

## Conventions

- Keep planning material in `handouts/` and formal thesis source in `chapters/`.
- Keep bibliography files in `bibliography/` and graphical assets in `figures/`.
- Keep generated LaTeX artefacts out of version control.
- Keep local editor and agent metadata out of version control.
- Prefer relative LaTeX builds from the source directory because the repo path contains spaces and accented characters.
