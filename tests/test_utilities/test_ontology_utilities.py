# -*- coding: utf-8 -*-
import os
import unittest
from pathlib import Path

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, rdflib_dumper, yaml_dumper
from linkml_runtime.loaders import json_loader
from oaklib import get_implementation_from_shorthand

from phenopackets.datamodel import MAIN_SCHEMA_PATH
from phenopackets.datamodel.phenopackets import (Family, OntologyClass,
                                                 Phenopacket,
                                                 PhenotypicFeature)
from phenopackets.utilities.ontology_utilities import (OntologyConfiguration,
                                                       migrate_obsoletes,
                                                       update_labels, normalize_curies)
from tests import INPUT_PATH


class TestOntologyUtilities(unittest.TestCase):
    """Tests examples folder.

    Note: this test will soon become redundant with the new
    linkml-run-examples framework
    """

    def setUp(self) -> None:
        self.sv = SchemaView(str(MAIN_SCHEMA_PATH))
        self.sv.namespaces()._base = "https://example.org/base/"
        oi = get_implementation_from_shorthand(str(INPUT_PATH / "hp-subset.obo"))
        self.configuration = OntologyConfiguration(
            ontology_map={"HP": oi}, default_selector=None
        )

    def test_repair(self):
        oc = OntologyClass(id="HP:0100637", label="Neoplasia of the nose")
        pf = PhenotypicFeature(type=oc)
        replacements = list(migrate_obsoletes(pf, configuration=self.configuration))
        self.assertEqual(len(replacements), 1)
        self.assertEqual(replacements[0][0], "HP:0100637")
        self.assertEqual(oc.id, "HP:0012720")

    def test_update_label(self):
        oc = OntologyClass(id="HP:0012720", label="OLD LABEL")
        pf = PhenotypicFeature(type=oc)
        replacements = list(update_labels(pf, configuration=self.configuration))
        self.assertEqual(len(replacements), 1)
        self.assertEqual(oc.label, "Neoplasm of the nose")

    def test_normalize_curies(self):
        oc = OntologyClass(id="sctid:0012720")
        pf = PhenotypicFeature(type=oc)
        replacements = list(normalize_curies(pf, configuration=self.configuration))
        self.assertEqual(len(replacements), 1)
        print(replacements)
        print(oc)
        self.assertEqual(oc.id, "SNOMEDCT:0012720")
