# Introduction

This is NOT the official GA4GH Phenopackets schema. For the true phenopackets see <http://phenopackets.org/>

## About

This is a [LinkML](https://linkml.io/) rendering of the Phenopackets schema. It demonstrates what the LinkML
tooling adds to the Protobuf source: additional validation, Python classes, and conversion to and from RDF.

The schema corresponds to [release 2.0.0](https://github.com/phenopackets/phenopacket-schema/releases/tag/2.0.0)
of phenopacket-schema. It is not edited by hand: a script converts the protobuf files of that release. The
[README](https://github.com/cmungall/linkml-phenopackets#readme) of the repository describes how to generate it
again, and lists the
[differences from protobuf](https://github.com/cmungall/linkml-phenopackets#differences-from-protobuf).

Only the enumerations of ontology terms, such as [HPOAbnormalityTerms](HPOAbnormalityTerms.md), are curated by hand,
in [cv_terms.yaml](https://github.com/cmungall/linkml-phenopackets/blob/main/src/phenopackets/schema/cv_terms.yaml).

## On this site

 * The [index](index.md) lists the classes, slots, enumerations and types of the schema. These pages are
   generated from the schema.
 * The [schema diagram](schema-diagram.md) shows all classes and the relationships between them.
 * The notebooks show how to [validate](notebooks/LinkML-Validate.ipynb) a phenopacket, how to use the
   [Pydantic classes](notebooks/Pydantic.ipynb), how to check and repair ontology terms
   [using OAK](notebooks/OAK.ipynb), and how to [generate RDF](notebooks/Generating-RDF.ipynb).

## Generated artefacts

The following are generated from the schema, and are kept in the
[repository](https://github.com/cmungall/linkml-phenopackets):

 * Python dataclasses and Pydantic classes
 * JSON-Schema
 * GraphQL
 * JSON-LD context
 * a spreadsheet of the classes and their attributes
