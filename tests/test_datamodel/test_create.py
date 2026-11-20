# -*- coding: utf-8 -*-
import json
import os

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, rdflib_dumper
from rdflib import Graph, Literal, URIRef

from phenopackets.datamodel import MAIN_SCHEMA_PATH
from phenopackets.datamodel.phenopackets import (Allele, Haplotype,
                                                 HaplotypeMember, Individual,
                                                 LiteralSequenceExpression,
                                                 MetaData, OntologyClass,
                                                 Phenopacket,
                                                 PhenotypicFeature, Resource,
                                                 VariationSet,
                                                 VariationSetMember,
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

    def test_create_variation_set(self):
        """A VRS Haplotype and a VariationSet have an identifier and members."""
        allele = Allele(
            Id="ga4gh:VA.1",
            curie="refseq:NC_000010.11",
            literalSequenceExpression=LiteralSequenceExpression(sequence="T"),
        )
        haplotype = Haplotype(
            Id="ga4gh:VH.1",
            members=[HaplotypeMember(allele=allele), HaplotypeMember(curie="ga4gh:VA.2")],
        )
        variation_set = VariationSet(
            members=[VariationSetMember(haplotype=haplotype), {"curie": "ga4gh:VA.3"}]
        )
        self.assertEqual("ga4gh:VA.3", variation_set.members[1].curie)
        # the attribute names are the names that protobuf uses in JSON
        dumped = json.loads(json_dumper.dumps(variation_set, inject_type=False))
        self.assertEqual("ga4gh:VH.1", dumped["members"][0]["haplotype"]["Id"])
        self.assertEqual(
            {"allele": {"Id": "ga4gh:VA.1", "curie": "refseq:NC_000010.11", "literalSequenceExpression": {"sequence": "T"}}},
            dumped["members"][0]["haplotype"]["members"][0],
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
