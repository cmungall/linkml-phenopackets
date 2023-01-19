# -*- coding: utf-8 -*-
import os

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, rdflib_dumper
from rdflib import Graph, Literal, URIRef

from phenopackets.datamodel import MAIN_SCHEMA_PATH
from phenopackets.datamodel.phenopackets import (Individual, MetaData,
                                                 OntologyClass, Phenopacket,
                                                 PhenotypicFeature, Resource,
                                                 VitalStatus)

"""Test the module can be imported."""

import unittest


class TestCreate(unittest.TestCase):
    """A test case for create tests."""

    def setUp(self) -> None:
        self.sv = SchemaView(str(MAIN_SCHEMA_PATH))

    def test_create_ontology_class(self):
        term = OntologyClass(id="HP:0001945", label="Fever")
        ttl = rdflib_dumper.dumps(
            term,
            schemaview=self.sv,
            prefix_map={
                "HP": "http://purl.obolibrary.org/obo/HP_",
            },
        )
        print(ttl)
        g = Graph()
        g.parse(data=ttl, format="turtle")
        for t in g.triples((None, None, None)):
            print(t)
        self.assertIn(
            Literal("Fever"),
            list(g.objects(URIRef("http://purl.obolibrary.org/obo/HP_0001945"))),
        )

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
        print(
            rdflib_dumper.dumps(
                phenopacket,
                schemaview=self.sv,
                prefix_map={
                    "HP": "http://purl.obolibrary.org/obo/HP_",
                    "ex": "https://example.org/",
                },
            )
        )
