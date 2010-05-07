LATEX_COMMAND=latex
BIBTEX_COMMAND=bibtex

latex: bibtex dbtech-project-part2.tex
	$(LATEX_COMMAND) dbtech-project-part3

bibtex: mybib.bib
	$(LATEX_COMMAND) dbtech-project-part3
	$(BIBTEX_COMMAND) dbtech-project-part3

clean:
	rm -rf *~ *.log *.aux *.toc *.out *.pdf *.bbl *.blg
