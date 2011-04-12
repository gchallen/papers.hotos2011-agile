START = xxxnote
END = missing
CLASS = $(PYTEX)/cls/usenix.sty

all: paper ABSTRACT

figures:
	@cd figures ; make

ABSTRACT: $(PYTEX)/clean $(PYTEX)/lib.py introduction.tex
	@$(PYTEX)/clean introduction.tex ABSTRACT

# 16 Nov 2010 : GWA : Add other cleaning rules here.

clean: rulesclean
	@rm ABSTRACT

include $(PYTEX)/make/Makerules
