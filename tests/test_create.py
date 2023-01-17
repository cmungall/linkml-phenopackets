# -*- coding: utf-8 -*-
import os

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, rdflib_dumper

from phenopackets.datamodel import MAIN_SCHEMA_PATH
from phenopackets.datamodel.phenopackets import OntologyClass
from phenopackets.datamodel.phenopackets import Individual, VitalStatus
from phenopackets.datamodel.phenopackets import MetaData, Resource
from phenopackets.datamodel.phenopackets import Phenopacket
from phenopackets.datamodel.phenopackets import PhenotypicFeature

"""Test the module can be imported."""

import unittest


class TestCreate(unittest.TestCase):
    """A test case for create tests."""

    def test_create(self):
        r = Resource(id="ex:x", name="y")
        metadata = MetaData(resources=[])
        subject = Individual(
            id="ex:P123542", vitalStatus=VitalStatus(status="DECEASED")
        )
        fever_term = OntologyClass(id="HP:123", label="z")
        print(type(subject))
        phenopacket = Phenopacket(
            id="ex:packet1",
            subject=subject,
            phenotypicFeatures=[
                PhenotypicFeature(type=fever_term, description="fever")
            ],
            metaData=metadata,
        )
        print(json_dumper.dumps(phenopacket))
        sv = SchemaView(str(MAIN_SCHEMA_PATH))
        print(
            rdflib_dumper.dumps(
                phenopacket,
                schemaview=sv,
                prefix_map={
                    "HP": "http://purl.obolibrary.org/obo/HP_",
                    "ex": "https://example.org/",
                },
            )
        )
