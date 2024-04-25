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

PXF = ../phenopacket-schema/src/main/proto
VRS = ../phenopacket-schema/src/vrs-protobuf/schema/vrs.proto
PXF_CORE = $(PXF)/phenopackets/schema/v2/core
PXF_GOOGLE = $(PXF)/google/protobuf
PXF_GA4GH = $(PXF)/ga4gh
PXF_VRSA = $(PXF_GA4GH)/vrsatile/v1


auto: $(patsubst %, tmp/%.yaml, $(CORE_MODS))

deploy: auto
	cp tmp/*yaml src/phenopackets/schema/

tmp/%.proto: $(PXF_CORE)/%.proto
	cp $< $@
.PRECIOUS: tmp/%.proto

tmp/timestamp.proto: $(PXF_GOOGLE)/timestamp.proto
	cp $< $@

tmp/any.proto: $(PXF_GOOGLE)/any.proto
	cp $< $@

tmp/vrsatile.proto: $(PXF_VRSA)/vrsatile.proto
	cp $< $@

tmp/vrs.proto: $(VRS)
	cp $< $@

tmp/phenopackets.proto: $(PXF)/phenopackets/schema/v2/phenopackets.proto
	cp $< $@

HACK = ./util/proto2linkml.pl
tmp/%.yaml: tmp/%.proto $(HACK)
	$(HACK) $< > $@
