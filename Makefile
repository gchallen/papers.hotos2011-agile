START = xxxnote
END = missing

all: paper

figures:
	@cd figures ; make

# 16 Nov 2010 : GWA : Add other cleaning rules here.

clean: rulesclean

include Makerules
