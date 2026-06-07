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
CHAPTER3_SRC := chapter3_bridge.tex
CHAPTER4_SRC := chapter4_comparative.tex
CHAPTER5_SRC := chapter5_temporal.tex
CHAPTER6_SRC := chapter6_conclusions.tex
THESIS_SRC   := thesis.tex

LATEXMK       := latexmk -pdf
THESIS_TEXINPUTS := TEXINPUTS=./$(CHAPTER_DIR):

.PHONY: all thesis chapter1 chapter2 chapter3 chapter4 chapter5 chapter6 \
        thesis-clean chapter1-clean chapter2-clean chapter3-clean chapter4-clean chapter5-clean chapter6-clean clean \
        export exports

all: chapter1 chapter2 chapter3 chapter4 chapter5 chapter6 thesis

chapter1:
	cd $(CHAPTER_DIR) && $(LATEXMK) -outdir=../$(BUILD_CHAPTERS) $(CHAPTER1_SRC)

chapter2:
	cd $(CHAPTER_DIR) && $(LATEXMK) -outdir=../$(BUILD_CHAPTERS) $(CHAPTER2_SRC)

chapter3:
	cd $(CHAPTER_DIR) && $(LATEXMK) -outdir=../$(BUILD_CHAPTERS) $(CHAPTER3_SRC)

chapter4:
	cd $(CHAPTER_DIR) && $(LATEXMK) -outdir=../$(BUILD_CHAPTERS) $(CHAPTER4_SRC)

chapter5:
	cd $(CHAPTER_DIR) && $(LATEXMK) -outdir=../$(BUILD_CHAPTERS) $(CHAPTER5_SRC)

chapter6:
	cd $(CHAPTER_DIR) && $(LATEXMK) -outdir=../$(BUILD_CHAPTERS) $(CHAPTER6_SRC)

thesis:
	$(THESIS_TEXINPUTS) $(LATEXMK) -outdir=$(BUILD_THESIS) $(THESIS_SRC)

chapter1-clean:
	cd $(CHAPTER_DIR) && latexmk -C -outdir=../$(BUILD_CHAPTERS) $(CHAPTER1_SRC)

chapter2-clean:
	cd $(CHAPTER_DIR) && latexmk -C -outdir=../$(BUILD_CHAPTERS) $(CHAPTER2_SRC)

chapter3-clean:
	cd $(CHAPTER_DIR) && latexmk -C -outdir=../$(BUILD_CHAPTERS) $(CHAPTER3_SRC)

chapter4-clean:
	cd $(CHAPTER_DIR) && latexmk -C -outdir=../$(BUILD_CHAPTERS) $(CHAPTER4_SRC)

chapter5-clean:
	cd $(CHAPTER_DIR) && latexmk -C -outdir=../$(BUILD_CHAPTERS) $(CHAPTER5_SRC)

chapter6-clean:
	cd $(CHAPTER_DIR) && latexmk -C -outdir=../$(BUILD_CHAPTERS) $(CHAPTER6_SRC)

thesis-clean:
	$(THESIS_TEXINPUTS) latexmk -C -outdir=$(BUILD_THESIS) $(THESIS_SRC)

clean: chapter1-clean chapter2-clean chapter3-clean chapter4-clean chapter5-clean chapter6-clean thesis-clean

## Snapshot cleanly rebuilt PDFs into exports/ (tracked in git).
## Separate recursive invocations enforce ordering, including under make -j.
exports:
	$(MAKE) clean
	$(MAKE) all
	@mkdir -p $(EXPORTS)
	cp $(BUILD_CHAPTERS)/chapter1_introduction.pdf $(EXPORTS)/
	cp $(BUILD_CHAPTERS)/chapter2_proof_of_concept.pdf $(EXPORTS)/
	cp $(BUILD_CHAPTERS)/chapter3_bridge.pdf $(EXPORTS)/
	cp $(BUILD_CHAPTERS)/chapter4_comparative.pdf $(EXPORTS)/
	cp $(BUILD_CHAPTERS)/chapter5_temporal.pdf $(EXPORTS)/
	cp $(BUILD_CHAPTERS)/chapter6_conclusions.pdf $(EXPORTS)/
	cp $(BUILD_THESIS)/thesis.pdf $(EXPORTS)/

export: exports
