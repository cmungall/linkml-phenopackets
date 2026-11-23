# -*- coding: utf-8 -*-
import json

from linkml.validator import Validator
from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, rdflib_dumper, yaml_dumper
from linkml_runtime.loaders import json_loader
from rdflib import Literal

from phenopackets.datamodel import MAIN_SCHEMA_PATH
from phenopackets.datamodel.phenopackets import Family, Phenopacket
from tests import INPUT_EXAMPLES_PATH, INPUT_PATH, OUTPUT_EXAMPLES_PATH

"""Test the module can be imported."""

import unittest

# The phenopackets that release 2.0.0 of phenopacket-schema tests its own Python
# bindings with (src/test/python in https://github.com/phenopackets/phenopacket-schema)
RELEASE_EXAMPLES_PATH = INPUT_PATH / "phenopacket-schema-2.0.0" / "examples"
RELEASE_EXAMPLES = [
    "covid19",
    "mcahs1",
]

PHENOPACKET_EXAMPLES = [
    "AVED",
    "nemalineMyopathy",
    "statin-myopathy",
    "warburg-micro-syndrome",
    "thrombocytopenia2",
    "pseudoexfoliation",
    "holoprosencephaly5",
    "duchenne",
    "acute-myeloid-leukemia",
    "bethleham-myopathy",
    "covid",
    "marfan-simple",
    "marfan",
    "retinoblastoma",
    "squamous-cell-esophageal-carcinoma",
    "urothelial-cancer",
]

FAMILY_EXAMPLES = [
    "family",
]

DEFAULT_PREFIX_MAP = {
    "HP": "http://purl.obolibrary.org/obo/HP_",
    "ex": "https://example.org/",
    "MONDO": "http://purl.obolibrary.org/obo/MONDO_",
    "UBERON": "http://purl.obolibrary.org/obo/UBERON_",
    "NCBITaxon": "http://purl.obolibrary.org/obo/NCBITaxon_",
    "NCIT": "http://purl.obolibrary.org/obo/NCIT_",
    "EFO": "http://www.ebi.ac.uk/efo/EFO_",
    "PMID": "https://www.ncbi.nlm.nih.gov/pubmed/",
    "OMIM": "http://omim.org/entry/",
    "GENO": "http://purl.obolibrary.org/obo/GENO_",
    "ECO": "http://purl.obolibrary.org/obo/ECO_",
    "DOI": "https://doi.org/",
    "DrugCentral": "http://identifiers.org/drugcentral/",
    "LOINC": "https://loinc.org/",
    "UCUM": "http://unitsofmeasure.org/",
    "PATO": "http://purl.obolibrary.org/obo/PATO_",
    "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
    "SCTID": "http://snomed.info/id/",
    "SNOMEDCT": "http://snomed.info/id/",
    "UO": "http://purl.obolibrary.org/obo/UO_",
    "xsd": "http://www.w3.org/2001/XMLSchema#",  # TODO - should not be required
    "__base": "https://example.org/base/",
}


class TestExamples(unittest.TestCase):
    """Tests examples folder.

    Note: this test will soon become redundant with the new
    linkml-run-examples framework
    """

    def setUp(self) -> None:
        self.sv = SchemaView(str(MAIN_SCHEMA_PATH))
        self.sv.namespaces()._base = "https://example.org/base/"
        self.validator = Validator(
            str(MAIN_SCHEMA_PATH),
            validation_plugins=[JsonschemaValidationPlugin(closed=True)],
        )
        OUTPUT_EXAMPLES_PATH.mkdir(parents=True, exist_ok=True)

    def validation_messages(self, instance: dict, target_class: str):
        report = self.validator.validate(instance, target_class)
        return [result.message for result in report.results]

    def test_schemaview(self):
        slot = self.sv.induced_slot("reference", "ExternalReference")
        print(f"{slot.name} {slot.range} {slot.domain}")
        self.assertEqual(slot.range, "string")

    def test_examples(self):
        examples = [(Phenopacket, ex) for ex in PHENOPACKET_EXAMPLES] + [
            (Family, ex) for ex in FAMILY_EXAMPLES
        ]
        for typ, ex in examples:
            # print(f"EXAMPLE={ex} // {typ}")
            phenopacket = json_loader.load(
                f"{INPUT_EXAMPLES_PATH / ex}.json", target_class=typ
            )

            # What the datamodel writes has to be valid against the schema. (The
            # input is not validated directly: in protobuf JSON 64 bit integers such
            # as VcfRecord.pos are strings, which the datamodel converts.)
            normalized = json.loads(json_dumper.dumps(phenopacket, inject_type=False))
            self.assertEqual([], self.validation_messages(normalized, typ.class_name), ex)

            base = f"{typ.class_name}-{ex}"
            json_dumper.dump(phenopacket, OUTPUT_EXAMPLES_PATH / f"{base}.json")
            yaml_dumper.dump(phenopacket, OUTPUT_EXAMPLES_PATH / f"{base}.yaml")
            rdflib_dumper.dump(
                phenopacket,
                schemaview=self.sv,
                prefix_map=DEFAULT_PREFIX_MAP,
                to_file=OUTPUT_EXAMPLES_PATH / f"{base}.ttl",
            )

    def test_release_examples(self):
        """The phenopackets of the release are valid as they are."""
        for ex in RELEASE_EXAMPLES:
            path = RELEASE_EXAMPLES_PATH / f"{ex}.json"
            with open(path) as stream:
                self.assertEqual([], self.validation_messages(json.load(stream), "Phenopacket"), ex)
            phenopacket = json_loader.load(str(path), target_class=Phenopacket)
            self.assertEqual("2.0", phenopacket.metaData.phenopacketSchemaVersion)

    def test_maps(self):
        """The entries of protobuf map fields are kept, in JSON and in RDF."""
        path = f"{INPUT_EXAMPLES_PATH / 'family'}.json"
        with open(path) as stream:
            # the compact {key: value} form of the protobuf JSON mapping is valid
            self.assertEqual([], self.validation_messages(json.load(stream), "Family"))
        family = json_loader.load(path, target_class=Family)
        file = family.files[0]
        self.assertEqual(
            {"genomeAssembly": "GRCh38", "fileFormat": "VCF", "description": "multi-sample VCF file for family.1"},
            {key: entry.value for key, entry in file.fileAttributes.items()},
        )
        self.assertEqual(5, len(file.individualToFileIdentifiers))
        self.assertEqual("sample.3", file.individualToFileIdentifiers["daughter.1"].value)

        reloaded = json_loader.loads(json_dumper.dumps(family), target_class=Family)
        self.assertEqual(file.fileAttributes, reloaded.files[0].fileAttributes)
        self.assertEqual(file.individualToFileIdentifiers, reloaded.files[0].individualToFileIdentifiers)

        graph = rdflib_dumper.as_rdf_graph(family, schemaview=self.sv, prefix_map=DEFAULT_PREFIX_MAP)
        literals = set(graph.objects())
        # keys and values that occur nowhere else in the family
        for expected in ["genomeAssembly", "multi-sample VCF file for family.1", "sample.3"]:
            self.assertIn(Literal(expected), literals)
