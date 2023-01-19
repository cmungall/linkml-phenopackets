# -*- coding: utf-8 -*-
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, rdflib_dumper, yaml_dumper
from linkml_runtime.loaders import json_loader

from phenopackets.datamodel import MAIN_SCHEMA_PATH
from phenopackets.datamodel.phenopackets import Family, Phenopacket
from tests import INPUT_EXAMPLES_PATH, OUTPUT_EXAMPLES_PATH

"""Test the module can be imported."""

import unittest

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
        OUTPUT_EXAMPLES_PATH.mkdir(parents=True, exist_ok=True)

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

            base = f"{typ.class_name}-{ex}"
            json_dumper.dump(phenopacket, OUTPUT_EXAMPLES_PATH / f"{base}.json")
            yaml_dumper.dump(phenopacket, OUTPUT_EXAMPLES_PATH / f"{base}.yaml")
            rdflib_dumper.dump(
                phenopacket,
                schemaview=self.sv,
                prefix_map=DEFAULT_PREFIX_MAP,
                to_file=OUTPUT_EXAMPLES_PATH / f"{base}.ttl",
            )
