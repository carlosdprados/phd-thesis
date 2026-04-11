# PhD Thesis Repository

Working repository for the PhD thesis on ion-mediated polymeric memristive devices.

## Structure

- `handouts/`: planning documents, chapter outlines, and working notes.
- `chapters/`: LaTeX chapter source files under active thesis development.
- `bibliography/`: shared BibLaTeX database files.
- `figures/`: thesis figures and exported graphics.
- `build/`: generated LaTeX outputs. Ignored by git.
- `.vscode/`: workspace settings for LaTeX Workshop and editor behavior.

## Current Working Files

- `chapters/chapter2_proof_of_concept.tex`: current Chapter 2 LaTeX draft.
- `bibliography/references.bib`: bibliography database used by the LaTeX sources.
- `handouts/00_...` to `05_...`: thesis planning and structure handouts.

## LaTeX Workflow

The repository is configured so LaTeX Workshop uses `latexmk` with filename-only arguments and writes generated files to `build/<relative-source-dir>/`.

For the current Chapter 2 draft, the default repo-level commands are:

```sh
make chapter2
make chapter2-clean
```

For the current Chapter 2 draft, the safe terminal workflow is:

```sh
cd chapters
latexmk -pdf -outdir=../build/chapters chapter2_proof_of_concept.tex
```

To clean generated files for that draft:

```sh
cd chapters
latexmk -C -outdir=../build/chapters chapter2_proof_of_concept.tex
```

## Conventions

- Keep planning material in `handouts/` and formal thesis source in `chapters/`.
- Keep bibliography files in `bibliography/` and graphical assets in `figures/`.
- Keep generated LaTeX artefacts out of version control.
- Keep local editor and agent metadata out of version control.
- Prefer relative LaTeX builds from the source directory because the repo path contains spaces and accented characters.
