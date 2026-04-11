CHAPTER2_SRC := handouts/chapter2_proof_of_concept.tex
CHAPTER2_DIR := handouts
CHAPTER2_OUT := build/handouts

.PHONY: chapter2 chapter2-clean

chapter2:
	cd $(CHAPTER2_DIR) && latexmk -pdf -outdir=../$(CHAPTER2_OUT) $(notdir $(CHAPTER2_SRC))

chapter2-clean:
	cd $(CHAPTER2_DIR) && latexmk -C -outdir=../$(CHAPTER2_OUT) $(notdir $(CHAPTER2_SRC))
