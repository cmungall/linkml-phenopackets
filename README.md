# Phenopackets EXPERIMENTAL linkml schema

Browse the schema here:

 * https://cmungall.github.io/linkml-phenopackets/

Note the linkml markdown rendering is still incomplete, for a full schema, see

 * [src/schema](src/schema)

## How was this made?

I tried multiple different paths to auto-convert protobuf to linkml,
including going via jsonschema as an intermediary, but using existing
libraries proved to be problematic form multiple reasons.

In the end I wrote some hacky proto2linkml code (caution: overly fitted to phenopackets).

We maintain linkml customizations separately, so if the proto changes we can easily re-run

## Ontology Enhancements

The file cv_terms.yaml is hand-curated, rather than derived from the YAML

It is based on: https://phenopacket-schema.readthedocs.io/en/latest/recommended-ontologies.html

## Limitations

### Alternate actions: anyofs

The anyofs in the protobuf are translated to `exactly_one_of` in
linkml, which is the correct translation. However, when this is
translated to jsonschema it is "flattened out". this means the json
schema is not able to catch cases where people specify more than one
of the specified actions
