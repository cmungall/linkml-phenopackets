# -*- coding: utf-8 -*-
import os
from pathlib import Path

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, rdflib_dumper
from linkml_runtime.loaders import json_loader

from phenopackets.datamodel import MAIN_SCHEMA_PATH
from phenopackets.datamodel.base import OntologyClass
from phenopackets.datamodel.individual import VitalStatus, Individual
from phenopackets.datamodel.meta_data import MetaData, Resource
from phenopackets.datamodel.phenopackets import Phenopacket, Family
from phenopackets.datamodel.phenotypic_feature import PhenotypicFeature

"""Test the module can be imported."""

import unittest

THIS_PATH = Path(__file__).parent
INPUT_PATH = THIS_PATH / "input" / "examples"

PHENOPACKET_EXAMPLES = [
    "thrombocytopenia2",
    #"pseudoexfoliation",
    #"holoprosencephaly5", # https://github.com/phenopackets/phenopacket-tools/issues/142
    #"duchenne", https://github.com/phenopackets/phenopacket-tools/issues/142
    "acute-myeloid-leukemia",
    "bethleham-myopathy",
    "covid",
    "marfan-simple",
    "marfan",
    #"retinoblastoma",  no id
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
    "UO": "http://purl.obolibrary.org/obo/UO_",
    "xsd": "http://www.w3.org/2001/XMLSchema#",  # TODO - should not be required
    "__base": "https://example.org/base/",
}


class TestExamples(unittest.TestCase):
    """Tests examples folder."""

    def test_schemaview(self):
        sv = SchemaView(str(MAIN_SCHEMA_PATH))
        slot = sv.induced_slot("reference", "ExternalReference")
        print(f"{slot.name} {slot.range} {slot.domain}")
        self.assertEqual(slot.range, "string")


    def test_examples(self):
        examples = [(Phenopacket, ex) for ex in PHENOPACKET_EXAMPLES] + [(Family, ex) for ex in FAMILY_EXAMPLES]
        for typ, ex in examples:
            print(f"EXAMPLE={ex} // {typ}")
            phenopacket = json_loader.load(
                f"{INPUT_PATH / ex}.json", target_class=typ
            )

            print(json_dumper.dumps(phenopacket))
            sv = SchemaView(str(MAIN_SCHEMA_PATH))
            sv.namespaces()._base = 'https://example.org/base/'
            print(
                rdflib_dumper.dumps(
                    phenopacket, schemaview=sv, prefix_map=DEFAULT_PREFIX_MAP
                )
            )
