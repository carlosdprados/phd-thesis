## ============================================================
##  Makefile — PhD thesis LaTeX build targets
##
##  Per-chapter targets run latexmk from ./chapters/ so that the
##  relative paths used inside each chapter (../figures,
##  ../bibliography) resolve correctly.
##
##  The thesis target runs from the repo root and uses TEXINPUTS
##  to make chapters/thesis-format.sty findable.
## ============================================================

CHAPTER_DIR    := chapters
BUILD_CHAPTERS := build/chapters
BUILD_THESIS   := build
EXPORTS        := exports

CHAPTER1_SRC := chapter1_introduction.tex
CHAPTER2_SRC := chapter2_proof_of_concept.tex
THESIS_SRC   := thesis.tex

LATEXMK       := latexmk -pdf
THESIS_TEXINPUTS := TEXINPUTS=./$(CHAPTER_DIR):

.PHONY: all thesis chapter1 chapter2 \
        thesis-clean chapter1-clean chapter2-clean clean \
        export exports chapter1-text chapter2-text texts

all: chapter1 chapter2 thesis

chapter1:
	cd $(CHAPTER_DIR) && $(LATEXMK) -outdir=../$(BUILD_CHAPTERS) $(CHAPTER1_SRC)

chapter2:
	cd $(CHAPTER_DIR) && $(LATEXMK) -outdir=../$(BUILD_CHAPTERS) $(CHAPTER2_SRC)

thesis:
	$(THESIS_TEXINPUTS) $(LATEXMK) -outdir=$(BUILD_THESIS) $(THESIS_SRC)

chapter1-clean:
	cd $(CHAPTER_DIR) && latexmk -C -outdir=../$(BUILD_CHAPTERS) $(CHAPTER1_SRC)

chapter2-clean:
	cd $(CHAPTER_DIR) && latexmk -C -outdir=../$(BUILD_CHAPTERS) $(CHAPTER2_SRC)

thesis-clean:
	$(THESIS_TEXINPUTS) latexmk -C -outdir=$(BUILD_THESIS) $(THESIS_SRC)

clean: chapter1-clean chapter2-clean thesis-clean

## Snapshot the current PDFs into exports/ (tracked in git).
exports: all
	@mkdir -p $(EXPORTS)
	cp $(BUILD_CHAPTERS)/chapter1_introduction.pdf $(EXPORTS)/
	cp $(BUILD_CHAPTERS)/chapter2_proof_of_concept.pdf $(EXPORTS)/
	cp $(BUILD_THESIS)/thesis.pdf $(EXPORTS)/

export: exports

## Plain-text exports for AI-detection tools (one paragraph per line, no
## figures, tables, citations, or LaTeX markup). Safe to copy-paste into
## GPTZero and similar.
chapter1-text:
	@mkdir -p $(EXPORTS)
	python3 scripts/export_plaintext.py $(CHAPTER_DIR)/$(CHAPTER1_SRC) $(EXPORTS)/chapter1_introduction.txt

chapter2-text:
	@mkdir -p $(EXPORTS)
	python3 scripts/export_plaintext.py $(CHAPTER_DIR)/$(CHAPTER2_SRC) $(EXPORTS)/chapter2_proof_of_concept.txt

texts: chapter1-text chapter2-text
