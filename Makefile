.PHONY: test-examples run-all-examples

EXAMPLES = examples/hello_network.py \
           examples/using_udg.py \
           examples/boundary_estimation.py \
           examples/using_gg.py

run-all-examples:
	@echo "Running all GeoNet examples..."
	@for example in $(EXAMPLES); do \
		echo "\nRunning $$example..."; \
		python3 $$example; \
	done

test-examples:
	@echo "Running individual examples..."
	@for example in $(EXAMPLES); do \
		echo "\nRunning $$example..."; \
		python3 $$example; \
	done

# Default target
all: run-all-examples 