SRC = src/phenopackets/schema/phenopackets.yaml
RUN = poetry run
CORE_MODS = timestamp any base measurement medical_action genome phenotypic_feature biosample disease interpretation individual meta_data pedigree vrs vrsatile phenopackets

all:
	$(RUN) gen-project -d project $(SRC)

# https://github.com/linkml/linkml/issues/907
gendocs:
#	$(RUN) gen-doc -d docs/  $(SRC)
#	$(RUN) gen-doc -d docs/ --include-top-level-diagram --diagram-type er_diagram --template-directory docgen-templates $(SRC)
	$(RUN) gen-doc -d docs/ --include-top-level-diagram --diagram-type er_diagram $(SRC)

py:
	cp project/phenopackets.py src/phenopackets/datamodel/


src/phenopackets/pydantic/model.py: $(SRC)
	$(RUN) gen-pydantic --pydantic-version 2 $< > $@

#src/phenopackets/datamodel/%.py: src/phenopackets/schema/%.yaml
#	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@

test:
	$(RUN) python -m unittest

sync-examples:
	cp tests/output/examples/* examples/

serve:
	$(RUN) mkdocs serve

gh-deploy:
	$(RUN) mkdocs gh-deploy

# Deploy gh docs
deploy-gh-doc: gendocs
	$(RUN) mkdocs gh-deploy

clean-site:
	rm site/*

sheets/phenopackets.tsv: $(SRC)
	$(RUN) linkml2sheets sheets/phenopackets-spec.tsv -s $< -o $@

nb:
	$(RUN) poetry run jupyter notebook

## --------------------
## TEST/VALIDATIONS
## --------------------

EXAMPLES = \
acute-myeloid-leukemia\
bethleham-myopathy\
covid\
marfan\
retinoblastoma\
squamous-cell-esophageal-carcinoma\
thrombocytopenia2\
urothelial-cancer

all-validate: $(patsubst %, validate-%, $(EXAMPLES))

validate-%: examples/%.json
	$(RUN) linkml-validate -s $(SRC) $<

examples/%.ttl: examples/%.json
	$(RUN) linkml-convert -s $(SRC) $< -o $@

## --------------------
## AUTO-CONVERSION FROM CONSTANTS
## --------------------
PXF_TOOLS = ../phenopacket-tools
src/schema/constants.yaml: $(PXF_TOOLS)/constants
	$(RUN) ingest-constants $(PXF_TOOLS)/constants/*.tsv > $@.tmp && mv $@.tmp $@

## --------------------
## AUTO-CONVERSION FROM PROTOBUF
## --------------------

# The schema is generated from a pinned release of phenopacket-schema, so that
# `make auto deploy` always gives the same result. To move to another release,
# change PXF_VERSION together with the two pins that follow it.
PXF_VERSION = 2.0.0
PXF_GITHUB = phenopackets/phenopacket-schema
# commit of the src/vrs-protobuf submodule in the $(PXF_VERSION) tag;
# src/main/proto/ga4gh/vrs/v1/vrs.proto is a symbolic link into that submodule
VRS_PROTOBUF_COMMIT = d045bb0c65152a0cb32177dfc21148cc13d40fbe
# protobuf.version in the pom.xml of the $(PXF_VERSION) tag (google/protobuf/*.proto)
PROTOBUF_VERSION = 3.14.0

GITHUB_RAW = https://raw.githubusercontent.com
FETCH = curl --fail --silent --show-error --location --create-dirs --output

# a recipe that fails must not leave a file that looks up to date
.DELETE_ON_ERROR:

# Everything that is downloaded or generated for these pins goes into a directory
# that is named after them, so that files made for other pins are never used
PXF_BUILD = tmp/phenopacket-schema-$(PXF_VERSION)_vrs-protobuf-$(VRS_PROTOBUF_COMMIT)_protobuf-$(PROTOBUF_VERSION)
# a copy of src/main/proto of the release
PXF = $(PXF_BUILD)/src/main/proto
PXF_CORE = $(PXF)/phenopackets/schema/v2/core
PXF_GOOGLE = $(PXF)/google/protobuf
PXF_GA4GH = $(PXF)/ga4gh
PXF_VRSA = $(PXF_GA4GH)/vrsatile/v1
VRS = $(PXF_GA4GH)/vrs/v1/vrs.proto
# the modules that are generated from them
PXF_LINKML = $(PXF_BUILD)/linkml

GOOGLE_MODS = timestamp any
# the modules of phenopackets/schema/v2/core
PXF_CORE_MODS = $(filter-out $(GOOGLE_MODS) vrs vrsatile phenopackets, $(CORE_MODS))

GOOGLE_PROTOS = $(patsubst %, $(PXF_GOOGLE)/%.proto, $(GOOGLE_MODS))
PXF_PROTOS = $(patsubst %, $(PXF_CORE)/%.proto, $(PXF_CORE_MODS)) $(PXF)/phenopackets/schema/v2/phenopackets.proto $(PXF_VRSA)/vrsatile.proto

$(GOOGLE_PROTOS): $(PXF_GOOGLE)/%.proto:
	$(FETCH) $@ $(GITHUB_RAW)/protocolbuffers/protobuf/v$(PROTOBUF_VERSION)/src/google/protobuf/$*.proto

$(VRS):
	$(FETCH) $@ $(GITHUB_RAW)/ga4gh/vrs-protobuf/$(VRS_PROTOBUF_COMMIT)/schema/vrs.proto

$(PXF_PROTOS): $(PXF)/%.proto:
	$(FETCH) $@ $(GITHUB_RAW)/$(PXF_GITHUB)/$(PXF_VERSION)/src/main/proto/$*.proto

auto: $(patsubst %, $(PXF_LINKML)/%.yaml, $(CORE_MODS))

deploy: auto
	cp $(PXF_LINKML)/*.yaml src/phenopackets/schema/

HACK = ./util/proto2linkml.pl

$(patsubst %, $(PXF_LINKML)/%.yaml, $(PXF_CORE_MODS)): $(PXF_LINKML)/%.yaml: $(PXF_CORE)/%.proto $(HACK)
	mkdir -p $(@D)
	$(HACK) $< > $@

# The root module is the only one that states where the schema comes from: its
# `source` is the file of the release that it was generated from
$(PXF_LINKML)/phenopackets.yaml: $(PXF)/phenopackets/schema/v2/phenopackets.proto $(HACK)
	mkdir -p $(@D)
	$(HACK) --source https://github.com/$(PXF_GITHUB)/blob/$(PXF_VERSION)/src/main/proto/phenopackets/schema/v2/phenopackets.proto $< > $@

$(PXF_LINKML)/vrsatile.yaml: $(PXF_VRSA)/vrsatile.proto $(HACK)
	mkdir -p $(@D)
	$(HACK) $< > $@

$(PXF_LINKML)/vrs.yaml: $(VRS) $(HACK)
	mkdir -p $(@D)
	$(HACK) $< > $@

$(patsubst %, $(PXF_LINKML)/%.yaml, $(GOOGLE_MODS)): $(PXF_LINKML)/%.yaml: $(PXF_GOOGLE)/%.proto $(HACK)
	mkdir -p $(@D)
	$(HACK) $< > $@
