SRC_DIR = src
SCHEMA_DIR = $(SRC_DIR)/schema
SOURCE_FILES := $(shell find $(SCHEMA_DIR) -name '*.yaml')
SCHEMA_NAMES = $(patsubst $(SCHEMA_DIR)/%.yaml, %, $(SOURCE_FILES))

SCHEMA_NAME = phenopackets
SCHEMA_SRC = $(SCHEMA_DIR)/$(SCHEMA_NAME).yaml
TGTS = graphql jsonschema docs shex owl csv graphql python jsonld sqlddl

#GEN_OPTS = --no-mergeimports
GEN_OPTS = 

all: gen stage test
gen: $(patsubst %,gen-%,$(TGTS))
clean:
	rm -rf target/
	rm -rf docs/

t:
	echo $(SCHEMA_NAMES)

echo:
	echo $(patsubst %,gen-%,$(TGTS))

test: pytest

pytest:
	pytest -s tests/test_*py

install:
	. environment.sh
	pip install -r requirements.txt

tdir-%:
	mkdir -p target/$*
docs:
	mkdir $@

stage: $(patsubst %,stage-%,$(TGTS))
stage-%: gen-%
	cp -pr target/$* .
stage-python: gen-python
	cp target/phenopackets/*.py target/sqlddl/*.py phenopackets/

stage-examples:
	cp tests/target/* examples/

###  -- MARKDOWN DOCS --
# Generate documentation ready for mkdocs
# TODO: modularize imports
gen-docs: target/docs/index.md copy-src-docs
.PHONY: gen-docs
copy-src-docs:
	cp $(SRC_DIR)/docs/*md target/docs/
target/docs/%.md: $(SCHEMA_SRC) tdir-docs
	gen-markdown $(GEN_OPTS) --dir target/docs $<
stage-docs: gen-docs
	cp -pr target/docs .

###  -- MARKDOWN DOCS --
# TODO: modularize imports
gen-python: $(patsubst %, target/phenopackets/%.py, $(SCHEMA_NAMES))
.PHONY: gen-python
target/phenopackets/%.py: $(SCHEMA_DIR)/%.yaml
	gen-python --no-mergeimports $(GEN_OPTS) $< > $@

###  -- MARKDOWN DOCS --
# TODO: modularize imports. For now imports are merged.
gen-graphql:target/graphql/$(SCHEMA_NAME).graphql 
target/graphql/%.graphql: $(SCHEMA_DIR)/%.yaml tdir-graphql
	gen-graphql $(GEN_OPTS) $< > $@

###  -- SQL DDL --
# TODO: modularize imports. For now imports are merged.
gen-sqlddl: target/sqlddl/$(SCHEMA_NAME).sql
target/sqlddl/%.sql: $(SCHEMA_DIR)/%.yaml tdir-sqlddl
	gen-sqlddl $(GEN_OPTS) --python-import 'phenopackets.phenopackets' --sqla-file target/sqlddl/$*_db_mappings.py $< > $@

####  -- JSON schema --
# TODO: modularize imports. For now imports are merged.
gen-jsonschema: target/jsonschema/$(SCHEMA_NAME).schema.json
target/jsonschema/%.schema.json: $(SCHEMA_DIR)/%.yaml tdir-jsonschema
	gen-json-schema $(GEN_OPTS) -t transaction $< > $@

###  -- JSON-LD context --
gen-jsonld: target/jsonld/$(SCHEMA_NAME).context.jsonld
target/jsonld/%.context.jsonld: $(SCHEMA_DIR)/%.yaml tdir-jsonld
	gen-jsonld-context $(GEN_OPTS)  $< > $@

###  -- Shex --
# one file per module
gen-shex: $(patsubst %, target/shex/%.shex, $(SCHEMA_NAMES))
target/shex/%.shex: $(SCHEMA_DIR)/%.yaml tdir-shex
	gen-shex --no-mergeimports $(GEN_OPTS) $< > $@

###  -- CSV --
# one file per module
gen-csv: $(patsubst %, target/csv/%.csv, $(SCHEMA_NAMES))
target/csv/%.csv: $(SCHEMA_DIR)/%.yaml tdir-csv
	gen-csv $(GEN_OPTS) $< > $@

###  -- OWL --
# TODO: modularize imports. For now imports are merged.
gen-owl: target/owl/$(SCHEMA_NAME).owl.ttl
.PHONY: gen-owl
target/owl/%.owl.ttl: $(SCHEMA_DIR)/%.yaml tdir-owl
	gen-owl $(GEN_OPTS) $< > $@

###  -- RDF (direct mapping) --
# TODO: modularize imports. For now imports are merged.
gen-rdf: target/rdf/$(SCHEMA_NAME).ttl
target/rdf/%.ttl: $(SCHEMA_DIR)/%.yaml tdir-rdf
	gen-rdf $(GEN_OPTS) $< > $@

###  -- LinkML --
# linkml (copy)
# one file per module
gen-linkml: target/linkml/$(SCHEMA_NAME).yaml
target/linkml/%.yaml: $(SCHEMA_DIR)/%.yaml tdir-limkml
	cp $< > $@

# test docs locally.
docserve:
	mkdocs serve

gh-deploy:
	mkdocs gh-deploy
