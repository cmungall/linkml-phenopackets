import logging
import subprocess
import sys
from typing import Optional, TextIO, List

import click
from linkml.validators import JsonSchemaDataValidator
import linkml.validator as linkml_validator
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SchemaDefinition
from oaklib import get_implementation_from_shorthand
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.io.streaming_yaml_writer import StreamingYamlWriter
from oaklib.utilities.obograph_utils import graph_to_image, default_stylemap_path

import phenopackets.utilities.io_utilities as ioutil
import phenopackets.utilities.ontology_utilities as ontutil
from phenopackets.datamodel import MAIN_SCHEMA_PATH
from phenopackets.datamodel.phenopackets import Phenopacket

logger = logging.getLogger(__name__)

input_path_argument = click.argument("input_path", required=True, type=click.Path())
multi_input_path_argument = click.argument("input_paths", required=True, nargs=-1, type=click.Path())
input_format_option = click.option(
    "-I",
    "--input-format",
    help=f"The string denoting the input format",
)
output_option = click.option(
    "-o",
    "--output",
    help="Path of SSSOM output file.",
)
output_format_option = click.option(
    "-O",
    "--output-format",
    help=f"Desired output format",
)
ontology_option = click.option(
    "--ontology",
    "-i",
    help="Path to an ontology file or OAK locator.",
)


def get_configuration(
    ontology: Optional[str],
) -> Optional[ontutil.OntologyConfiguration]:
    if ontology is None:
        return None
    oi = get_implementation_from_shorthand(ontology)
    return ontutil.OntologyConfiguration(default_ontology=oi)


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool):
    """Run the CLI."""
    logger = logging.getLogger()
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)


@main.command()
@input_format_option
@input_path_argument
@output_format_option
@output_option
@ontology_option
def migrate_obsoletes(
    input_path: TextIO,
    input_format: Optional[str],
    output_format: Optional[str],
    output: Optional[str],
    ontology: Optional[str],
):
    """Rewire all OntologyClass objects that have an obsoletion with replacement."""
    pkt = ioutil.load_phenopacket(input_path, input_format)
    conf = get_configuration(ontology)
    results = list(ontutil.migrate_obsoletes(pkt, configuration=conf))
    print(f"## Num results: {len(results)}")
    for result in results:
        print(f"## RESULT: {result}")
    ioutil.dump_phenopacket(pkt, output, output_format)


@main.command()
@input_format_option
@input_path_argument
@output_format_option
@output_option
@ontology_option
def update_labels(
    input_path: TextIO,
    input_format: Optional[str],
    output_format: Optional[str],
    output: Optional[str],
    ontology: Optional[str],
):
    """Rewire all OntologyClass objects to update labels."""
    pkt = ioutil.load_phenopacket(input_path, input_format)
    conf = get_configuration(ontology)
    results = list(ontutil.update_labels(pkt, configuration=conf))
    print(f"## Num results: {len(results)}")
    for result in results:
        print(f"## RESULT: {result}")
    ioutil.dump_phenopacket(pkt, output, output_format)


@main.command()
@input_format_option
@input_path_argument
@output_format_option
@output_option
@ontology_option
def normalize_curies(
    input_path: TextIO,
    input_format: Optional[str],
    output_format: Optional[str],
    output: Optional[str],
    ontology: Optional[str],
):
    """Rewire all OntologyClass objects to update labels."""
    pkt = ioutil.load_phenopacket(input_path, input_format)
    conf = get_configuration(ontology)
    results = list(ontutil.normalize_curies(pkt, configuration=conf))
    print(f"## Num results: {len(results)}")
    for result in results:
        print(f"## RESULT: {result}")
    ioutil.dump_phenopacket(pkt, output, output_format)


@main.command()
@input_format_option
@input_path_argument
@output_format_option
@output_option
def list_terms(
    input_path: TextIO,
    input_format: Optional[str],
    output_format: Optional[str],
    output: Optional[str],
):
    """Rewire all OntologyClass objects to update labels."""
    pkt = ioutil.load_phenopacket(input_path, input_format)
    results = list(ontutil.collect_ontology_classes(pkt))
    ioutil.dump_phenopacket(results, output, output_format)


@main.command()
@input_format_option
@multi_input_path_argument
@output_format_option
@output_option
@ontology_option
def validate(
    input_paths: List[TextIO],
    input_format: Optional[str],
    output_format: Optional[str],
    output: Optional[str],
    ontology: Optional[str],
):
    """Validate a collection of phenopackets."""
    conf = get_configuration(ontology)
    schema_location = str(MAIN_SCHEMA_PATH)
    sv = SchemaView(schema_location)
    schema = sv.schema
    errs = []
    for input_path in input_paths:
        click.echo(f"## Validating {input_path}")
        pkt = ioutil.load_phenopacket(input_path, input_format)
        report = linkml_validator.validate(pkt, schema)
        for result in report.results:
            click.echo(f"## LinkML Validation Messages:")
            click.echo(f"[{result.severity.value}] [{result.instance_index}]")
            errs.append((input_path, result.message))
        for r in ontutil.validate_ontology_classes(pkt, configuration=conf):
            click.echo(f"## Ontology Validation Messages: {r}")
            errs.append((input_path, r))
    click.echo(f"Errors: {len(errs)}")
    if errs:
        sys.exit(1)



def xxxxvalidate(
    input_paths: List[TextIO],
    input_format: Optional[str],
    output_format: Optional[str],
    output: Optional[str],
    ontology: Optional[str],
):
    """Validate a collection of phenopackets."""
    conf = get_configuration(ontology)
    schema_location = str(MAIN_SCHEMA_PATH)
    validator = JsonSchemaDataValidator(schema_location)
    errs = []
    for input_path in input_paths:
        print(f"## Validating {input_path}")
        pkt = ioutil.load_phenopacket(input_path, input_format)
        try:
            validator.validate_object(pkt)
        except Exception as e:
            logger.error(f"## ERROR: {e}")
            errs.append((input_path, e))
        for r in ontutil.validate_ontology_classes(pkt, configuration=conf):
            print(f"## ERROR: {r}")
            errs.append((input_path, r))
    print(f"Errors: {len(errs)}")
    if errs:
        raise ValueError(f"Validation failed: {errs}")


@main.command()
@input_format_option
@input_path_argument
@output_format_option
@output_option
@ontology_option
def viz(
    input_path: TextIO,
    input_format: Optional[str],
    output_format: Optional[str],
    output: Optional[str],
    ontology: Optional[str],
):
    """Rewire all OntologyClass objects to update labels."""
    conf = get_configuration(ontology)
    stylemap = default_stylemap_path()
    ont = conf.default_ontology
    if not isinstance(ont, SemanticSimilarityInterface):
        raise ValueError("Ontology does not support semantic similarity")
    pkt = ioutil.load_phenopacket(input_path, input_format)
    seeds = [c.id for c in ontutil.collect_ontology_classes(pkt)]
    if not isinstance(ont, OboGraphInterface):
        raise ValueError("Ontology does not support OBO Graphs")
    graph = ont.ancestor_graph(seeds, predicates=[IS_A])
    imgfile = graph_to_image(
        graph, seeds=seeds, imgfile=output, stylemap=stylemap
    )
    if True:
        subprocess.run(["open", imgfile])


@main.command()
@input_format_option
@multi_input_path_argument
@output_format_option
@output_option
@ontology_option
def compare(
    input_paths: List[TextIO],
    input_format: Optional[str],
    output_format: Optional[str],
    output: Optional[str],
    ontology: Optional[str],
):
    """Rewire all OntologyClass objects to update labels."""
    conf = get_configuration(ontology)
    ont = conf.default_ontology
    if not isinstance(ont, SemanticSimilarityInterface):
        raise ValueError("Ontology does not support semantic similarity")
    pkts = [ioutil.load_phenopacket(input_path, input_format) for input_path in input_paths]
    def terms(pkt: Phenopacket) -> List[str]:
        return [c.id for c in ontutil.collect_ontology_classes(pkt1) if c.id.startswith("HP:")]
    w = StreamingYamlWriter()
    for i in range(len(pkts)):
        pkt1 = pkts[i]
        terms1 = terms(pkt1)
        if not terms1:
            continue
        for j in range(i + 1, len(pkts)):
            pkt2 = pkts[j]
            terms2 = terms(pkt2)
            if not terms2:
                continue
            print(f"COMPARISON: {terms1} vs {terms2}")
            sim = ont.termset_pairwise_similarity(terms1, terms2, predicates=[IS_A])
            w.emit(sim)



if __name__ == "__main__":
    main()
