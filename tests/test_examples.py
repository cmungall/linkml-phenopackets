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
from phenopackets.datamodel.phenopackets import Phenopacket
from phenopackets.datamodel.phenotypic_feature import PhenotypicFeature

"""Test the module can be imported."""

import unittest

THIS_PATH = Path(__file__).parent
INPUT_PATH = THIS_PATH / "input"

EXAMPLES = [
    "acute-myeloid-leukemia",
    "bethleham-myopathy",
    "covid",
    "marfan-simple",
    "marfan",
    #"retinoblastoma",
    "squamous-cell-esophageal-carcinoma",
    "thrombocytopenia2",
    "urothelial-cancer",
]

class TestExamples(unittest.TestCase):
    """Tests examples folder."""

    def test_examples(self):
        for ex in EXAMPLES:
            phenopacket = json_loader.load(f"{INPUT_PATH / ex}.json", target_class=Phenopacket)

            print(json_dumper.dumps(phenopacket))
            #sv = SchemaView(str(MAIN_SCHEMA_PATH))
            #print(rdflib_dumper.dumps(phenopacket, schemaview=sv, prefix_map={'HP': 'http://purl.obolibrary.org/obo/HP_',
            #                                                                      'ex': 'https://example.org/',
            #                                                                        'MONDO': 'http://purl.obolibrary.org/obo/MONDO_',
            #                                                                  'UBERON': 'http://purl.obolibrary.org/obo/UBERON_',
            #                                                                  'NCBITaxon': 'http://purl.obolibrary.org/obo/NCBITaxon_',
            #                                                                  'NCIT': 'http://purl.obolibrary.org/obo/NCIT_',
            #                                                                  'EFO': 'http://www.ebi.ac.uk/efo/EFO_',
            #                                                                  '__base': 'https://example.org/base/'}))
