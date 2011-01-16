START = xxxnote
END = missing

all: paper ABSTRACT

figures:
	@cd figures ; make

ABSTRACT: ./bin/clean introduction.tex
	./$< introduction.tex ABSTRACT

# 16 Nov 2010 : GWA : Add other cleaning rules here.

clean: rulesclean
	@rm ABSTRACT

include Makerules
