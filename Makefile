SHELL := /usr/bin/env bash
GO ?= go
YAML_FILES := $(shell find .github config -name '*.yml' -o -name '*.yaml')

.PHONY: fmt vet test generate manifests test-race verify test-e2e yaml-parse

fmt:
	$(GO) fmt ./...

vet:
	$(GO) vet ./...

test:
	$(GO) test ./...

generate:
	@echo "M0 scaffold has no generated Go objects yet; M1 will add Kubebuilder object generation."

manifests:
	python3 scripts/generate-manifests.py

test-race:
	$(GO) test -race ./...

yaml-parse:
	@ruby -e 'require "yaml"; ARGV.each { |path| YAML.load_file(path) }' $(YAML_FILES)

verify: fmt vet test manifests generate yaml-parse test-race
	git diff --exit-code

test-e2e:
	@echo "LOCAL_REQUIRED: make test-e2e requires Docker, kind, and a verified disposable Kubernetes context."
	@exit 2
