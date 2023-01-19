import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

import curies
from bioregistry import normalize_curie, is_valid_curie
from linkml_runtime.utils.yamlutils import YAMLRoot
from oaklib.datamodels.vocabulary import TERM_REPLACED_BY
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.selector import get_implementation_from_shorthand

from phenopackets.datamodel.phenopackets import OntologyClass, Phenopacket

REPLACEMENT = Tuple[str, str]

logger = logging.getLogger(__name__)


@dataclass
class OntologyConfiguration:
    """
    Configuration for an ontology.
    """

    ontology_map: Dict[str, BasicOntologyInterface] = None
    """Maps from ontology prefix to an OAK ontology interface"""

    default_ontology: Optional[BasicOntologyInterface] = None
    """If set, then any ontology ID not in the map will use this"""

    default_selector: Optional[str] = field(default_factory=lambda: "sqlite:obo")
    """For any ontology not in the map, use this selector to create an interface"""


def migrate_obsoletes(
    obj: YAMLRoot, configuration: OntologyConfiguration = None
) -> Iterable[REPLACEMENT]:
    """
    Migrate obsolete terms to their replacements for all OntologyClass objects.
    """
    yield from walk_object_tree(obj, (apply_obsoletion_replacement, configuration))


def update_labels(
    obj: YAMLRoot, configuration: OntologyConfiguration = None
) -> Iterable[REPLACEMENT]:
    """
    Update labels for all OntologyClass objects.
    """
    yield from walk_object_tree(obj, (apply_update_label, configuration))


def normalize_curies(
    obj: YAMLRoot, configuration: OntologyConfiguration = None
) -> Iterable[REPLACEMENT]:
    """
    Update labels for all OntologyClass objects.
    """
    yield from walk_object_tree(obj, (apply_normalize_curie, configuration))


def validate_ontology_classes(
    obj: YAMLRoot, configuration: OntologyConfiguration = None
) -> Iterable[REPLACEMENT]:
    """
    Apply validation on all classes
    """
    yield from walk_object_tree(obj, (apply_validate, configuration))


def collect_ontology_classes(
    obj: YAMLRoot, configuration: OntologyConfiguration = None
) -> Iterable[OntologyClass]:
    """
    Yields all ontology classes
    """

    def f(oc, _):
        yield oc

    yield from walk_object_tree(obj, (f, configuration))


def walk_object_tree(obj: YAMLRoot, func: Tuple[Callable, Any]) -> Iterable:
    """
    Walks the object tree, applying func to all OntologyClass objects.
    """
    if isinstance(obj, OntologyClass):
        method, arg = func
        yield from method(obj, arg)
    if not isinstance(obj, YAMLRoot):
        return
    for k, v in obj.__dict__.items():
        if isinstance(v, list):
            for item in v:
                yield from walk_object_tree(item, func)
        elif isinstance(v, dict):
            for item in v.values():
                yield from walk_object_tree(item, func)
        elif isinstance(v, YAMLRoot):
            yield from walk_object_tree(v, func)


def get_handle(
    oc: OntologyClass, configuration: OntologyConfiguration = None
) -> Optional[BasicOntologyInterface]:
    """
    Given a phenopackets.OntologyClass object, return the OAK handle.
    """
    if ":" not in oc.id:
        logger.error(f"OntologyClass.id must be a CURIE: {oc.id}")
        return None
    prefix, local_id = oc.id.split(":", 1)
    if configuration is None:
        selector = "sqlite:obo"
    else:
        if configuration.ontology_map is not None:
            if prefix in configuration.ontology_map:
                return configuration.ontology_map[prefix]
        if configuration.default_ontology:
            return configuration.default_ontology
        selector = configuration.default_selector
    if selector is None:
        return None
    locator = f"{selector}:{prefix.lower()}"
    try:
        return get_implementation_from_shorthand(locator)
    except Exception as e:
        logger.warning(f"Could not get handle for {oc.id} using {locator}: {e}")
        return None


def apply_obsoletion_replacement(
    oc: OntologyClass, configuration: OntologyConfiguration = None
) -> Iterable[REPLACEMENT]:
    oi = get_handle(oc, configuration)
    if oi is None:
        return
    all_obsoletes = list(oi.obsoletes(include_merged=True))
    curr_id = oc.id
    if curr_id in all_obsoletes:
        for _, rel, candidate in oi.obsoletes_migration_relationships([curr_id]):
            if rel == TERM_REPLACED_BY:
                oc.id = candidate
                oc.label = oi.label(candidate)
                yield curr_id, oc.id
                return
        raise ValueError(f"Could not repair {oc.id}")


def apply_update_label(
    oc: OntologyClass, configuration: OntologyConfiguration = None
) -> Iterable[REPLACEMENT]:
    oi = get_handle(oc, configuration)
    if oi is None:
        return
    lbl = oi.label(oc.id)
    if lbl and lbl != oc.label:
        orig = oc.label
        oc.label = lbl
        yield orig, oc.label


def apply_normalize_curie(
    oc: OntologyClass, configuration: OntologyConfiguration = None
) -> Iterable[Tuple[str,str]]:
    if ":" not in oc.id:
        logger.error(f"OntologyClass.id must be a CURIE: {oc.id}")
        return None
    normalized_id = normalize_curie(oc.id)
    if normalized_id.lower() != oc.id.lower():
        original_id = oc.id
        oc.id = normalized_id.upper()
        yield original_id, oc.id


def apply_validate(
    oc: OntologyClass, configuration: OntologyConfiguration = None
) -> Iterable[Tuple[str,str]]:
    for r in apply_normalize_curie(oc, configuration):
        yield oc.id, "CURIE"
    normalized_id = normalize_curie(oc.id)
    if normalized_id:
        if not is_valid_curie(normalized_id):
            yield oc.id, "CURIE_PREFIX"
    else:
        yield oc.id, "CURIE"
    oi = get_handle(oc, configuration)
    if oi is None:
        return
    if not oi.label(oc.id):
        yield oc.id, "label"
    if oc.id in oi.obsoletes(include_merged=True):
        yield oc.id, "obsolete"
