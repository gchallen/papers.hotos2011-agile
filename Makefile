START = noxxxnote nodraft blue
END = missing
PYTEX = $(shell pwd)/pytex/
CLASS = $(PYTEX)/cls/usenix.sty

all: paper ABSTRACT

figures:
	@cd figures ; make

ABSTRACT: $(PYTEX)/bin/clean $(PYTEX)/bin/lib.py introduction.tex
	@$(PYTEX)/bin/clean introduction.tex ABSTRACT

# 16 Nov 2010 : GWA : Add other cleaning rules here.

clean: rulesclean
	@rm ABSTRACT

include $(PYTEX)/make/Makerules
