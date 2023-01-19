import sys
from io import TextIOWrapper
from pathlib import Path
from typing import TextIO, Union, Type

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import (csv_dumper, json_dumper, rdflib_dumper,
                                    yaml_dumper)
from linkml_runtime.loaders import json_loader, rdflib_loader, yaml_loader

from phenopackets.datamodel import MAIN_SCHEMA_PATH
from phenopackets.datamodel.phenopackets import Family, Phenopacket


def load_phenopacket(
    path: Union[str, Path, TextIO], input_format: str = "json", target: Type = None
) -> Union[Phenopacket, Family]:
    """Load a Phenopacket from a JSON or YAML file."""
    if isinstance(path, Path):
        path = str(path)
    if target is None:
        if str(path).startswith("Phenopacket-"):
            target = Phenopacket
        elif str(path).startswith("Family-"):
            target = Family
        else:
            target = Phenopacket
    input_format = infer_format(path, input_format)
    if input_format == "json":
        return json_loader.load(path, target)
    if input_format == "yaml":
        return yaml_loader.load(path, target)
    if input_format == "ttl":
        sv = SchemaView(str(MAIN_SCHEMA_PATH))
        return rdflib_loader.load(path, schemaview=sv, target_class=target)
    raise ValueError(f"Cannot load format: {input_format}")


def dump_phenopacket(
    phenopacket: Union[Phenopacket, Family],
    output: Union[Path, str, TextIO],
    output_format: str = "json",
) -> None:
    """Dump a Phenopacket to a JSON or YAML file."""
    sv = SchemaView(str(MAIN_SCHEMA_PATH))
    if isinstance(output, Path):
        output = str(output)
    output_format = infer_format(output, output_format)
    if output_format == "json":
        if output is None:
            print(json_dumper.dumps(phenopacket, inject_type=False))
        else:
            json_dumper.dump(phenopacket, to_file=output)
    elif output_format == "yaml":
        if output is None:
            print(yaml_dumper.dumps(phenopacket))
        else:
            yaml_dumper.dump(phenopacket, to_file=output)
    elif output_format == "tsv":
        if output is None:
            print(csv_dumper.dumps({"x": phenopacket}, index_slot="x", schemaview=sv))
        else:
            csv_dumper.dump(phenopacket, to_file=output)
    elif output_format == "ttl":
        return rdflib_dumper.dump(phenopacket, schemaview=sv, to_file=output)
    else:
        raise ValueError(f"Cannot dump format: {output_format}")


def infer_format(path: Union[Path, str, TextIO], specified_format: str = None) -> str:
    """Infer the output format from the output file name."""
    if specified_format is not None:
        return specified_format
    if isinstance(path, Path):
        path = str(path)
    if not isinstance(path, str):
        return "json"
    if path.endswith(".json"):
        return "json"
    if path.endswith(".yaml"):
        return "yaml"
    if path.endswith(".ttl"):
        return "ttl"
    return "json"
