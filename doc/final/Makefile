LATEX_COMMAND=latex
BIBTEX_COMMAND=bibtex

latex: bibtex dbtech-project-final.tex
	$(LATEX_COMMAND) dbtech-project-final

bibtex: mybib.bib
	$(LATEX_COMMAND) dbtech-project-final
	$(BIBTEX_COMMAND) dbtech-project-final

clean:
	rm -rf *~ *.log *.aux *.toc *.out *.pdf *.bbl *.blg
