TARGETS = componentgraph.pdf transitiongraph.pdf

all: $(TARGETS)
	@echo > /dev/null

componentgraph.pdf: gencomponentgraph.py
	./$<

transitiongraph.pdf: gentransitiongraph.py transitiongraph.txt
	./$< transitiongraph.txt

clean:
	@rm -f $(TARGETS)

.PHONY: clean all
