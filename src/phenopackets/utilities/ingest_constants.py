"""
Ingests constants from http://phenopackets.org/phenopacket-tools/constants.html
"""
import csv
from typing import List
import click
import yaml
from linkml.utils.schema_builder import SchemaBuilder
from linkml_runtime.linkml_model import PermissibleValue
from linkml_runtime.utils.formatutils import camelcase
from linkml_runtime.utils.schema_as_dict import schema_as_dict

PREFIX_NAMESPACES = [
    ("UCUM", "http://unitsofmeasure.org/"),
    ("OBI", "http://purl.obolibrary.org/obo/OBI_"),
    ("HP", "http://purl.obolibrary.org/obo/HP_"),
    ("MP", "http://purl.obolibrary.org/obo/MP_"),
    ("GO", "http://purl.obolibrary.org/obo/GO_"),
    ("CHEBI", "http://purl.obolibrary.org/obo/CHEBI_"),
    ("NCIT", "http://purl.obolibrary.org/obo/NCIT_"),
    ("UO", "http://purl.obolibrary.org/obo/UO_"),
    ("PATO", "http://purl.obolibrary.org/obo/PATO_"),
    ("EFO", "http://purl.obolibrary.org/obo/EFO_"),
    ("GENO", "http://purl.obolibrary.org/obo/GENO_"),
    ("LOINC", "https://loinc.org/"),
    ("UBERON", "http://purl.obolibrary.org/obo/UBERON_"),
]


def ingest_all_constants(filenames: List[str]) -> SchemaBuilder:
    sb = SchemaBuilder("constants")
    sb.schema.id = "https://w3id.org/linkml/phenopackets/constants"
    for filename in filenames:
        ingest_constants(filename, sb)
    return sb

def ingest_constants(filename: str, sb: SchemaBuilder):
    basename = filename.split("/")[-1].split(".")[0]
    enum_name = f"{camelcase(basename)}Terms"
    sb.add_enum(enum_name)
    enum = sb.schema.enums[enum_name]
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for line in reader:
            pv = PermissibleValue(
                text=line['variable.name'],
                description=line['ontology.label'],
                meaning=line['ontology.id'],
            )
            enum.permissible_values[pv.text] = pv

@click.command()
@click.argument('inputs', nargs=-1)
def ingest(inputs):
    """Ingests constants to LinkML YAML.

    Example:

        ingest-constants ../phenopacket-tools/constants/*.tsv
    """
    sb = ingest_all_constants(inputs)
    sb.add_defaults()
    for prefix, ns in PREFIX_NAMESPACES:
        sb.add_prefix(prefix, ns)
    schema = sb.schema
    sdict = schema_as_dict(schema)
    print(yaml.safe_dump(sdict, sort_keys=False))


if __name__ == '__main__':
    ingest()