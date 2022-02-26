# Auto generated from phenopackets.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-08-27 18:06
# Schema: pfx
#
# id: pfx
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Integer, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PFX = CurieNamespace('pfx', 'https://w3id.org/linkml/pfx')
DEFAULT_ = PFX


# Types

# Class references



@dataclass
class Age(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Age
    class_class_curie: ClassVar[str] = "pfx:Age"
    class_name: ClassVar[str] = "Age"
    class_model_uri: ClassVar[URIRef] = PFX.Age

    age: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.age is not None and not isinstance(self.age, str):
            self.age = str(self.age)

        super().__post_init__(**kwargs)


@dataclass
class OntologyClass(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.OntologyClass
    class_class_curie: ClassVar[str] = "pfx:OntologyClass"
    class_name: ClassVar[str] = "OntologyClass"
    class_model_uri: ClassVar[URIRef] = PFX.OntologyClass

    id: Optional[str] = None
    label: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass
class AgeRange(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.AgeRange
    class_class_curie: ClassVar[str] = "pfx:AgeRange"
    class_name: ClassVar[str] = "AgeRange"
    class_model_uri: ClassVar[URIRef] = PFX.AgeRange

    start: Optional[Union[dict, Age]] = None
    end: Optional[Union[dict, Age]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.start is not None and not isinstance(self.start, Age):
            self.start = Age(**as_dict(self.start))

        if self.end is not None and not isinstance(self.end, Age):
            self.end = Age(**as_dict(self.end))

        super().__post_init__(**kwargs)


@dataclass
class Evidence(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Evidence
    class_class_curie: ClassVar[str] = "pfx:Evidence"
    class_name: ClassVar[str] = "Evidence"
    class_model_uri: ClassVar[URIRef] = PFX.Evidence

    evidence_code: Optional[Union[dict, OntologyClass]] = None
    reference: Optional[Union[dict, "ExternalReference"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.evidence_code is not None and not isinstance(self.evidence_code, OntologyClass):
            self.evidence_code = OntologyClass(**as_dict(self.evidence_code))

        if self.reference is not None and not isinstance(self.reference, ExternalReference):
            self.reference = ExternalReference(**as_dict(self.reference))

        super().__post_init__(**kwargs)


@dataclass
class PhenotypicFeature(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.PhenotypicFeature
    class_class_curie: ClassVar[str] = "pfx:PhenotypicFeature"
    class_name: ClassVar[str] = "PhenotypicFeature"
    class_model_uri: ClassVar[URIRef] = PFX.PhenotypicFeature

    description: Optional[str] = None
    type: Optional[Union[dict, OntologyClass]] = None
    negated: Optional[Union[bool, Bool]] = None
    severity: Optional[Union[dict, OntologyClass]] = None
    modifiers: Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]] = empty_list()
    age_of_onset: Optional[Union[dict, Age]] = None
    age_range_of_onset: Optional[Union[dict, AgeRange]] = None
    class_of_onset: Optional[Union[dict, OntologyClass]] = None
    evidence: Optional[Union[Union[dict, Evidence], List[Union[dict, Evidence]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.type is not None and not isinstance(self.type, OntologyClass):
            self.type = OntologyClass(**as_dict(self.type))

        if self.negated is not None and not isinstance(self.negated, Bool):
            self.negated = Bool(self.negated)

        if self.severity is not None and not isinstance(self.severity, OntologyClass):
            self.severity = OntologyClass(**as_dict(self.severity))

        if not isinstance(self.modifiers, list):
            self.modifiers = [self.modifiers] if self.modifiers is not None else []
        self.modifiers = [v if isinstance(v, OntologyClass) else OntologyClass(**as_dict(v)) for v in self.modifiers]

        if self.age_of_onset is not None and not isinstance(self.age_of_onset, Age):
            self.age_of_onset = Age(**as_dict(self.age_of_onset))

        if self.age_range_of_onset is not None and not isinstance(self.age_range_of_onset, AgeRange):
            self.age_range_of_onset = AgeRange(**as_dict(self.age_range_of_onset))

        if self.class_of_onset is not None and not isinstance(self.class_of_onset, OntologyClass):
            self.class_of_onset = OntologyClass(**as_dict(self.class_of_onset))

        if not isinstance(self.evidence, list):
            self.evidence = [self.evidence] if self.evidence is not None else []
        self.evidence = [v if isinstance(v, Evidence) else Evidence(**as_dict(v)) for v in self.evidence]

        super().__post_init__(**kwargs)


@dataclass
class HgvsAllele(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.HgvsAllele
    class_class_curie: ClassVar[str] = "pfx:HgvsAllele"
    class_name: ClassVar[str] = "HgvsAllele"
    class_model_uri: ClassVar[URIRef] = PFX.HgvsAllele

    id: Optional[str] = None
    hgvs: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.hgvs is not None and not isinstance(self.hgvs, str):
            self.hgvs = str(self.hgvs)

        super().__post_init__(**kwargs)


@dataclass
class VcfAllele(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.VcfAllele
    class_class_curie: ClassVar[str] = "pfx:VcfAllele"
    class_name: ClassVar[str] = "VcfAllele"
    class_model_uri: ClassVar[URIRef] = PFX.VcfAllele

    vcf_version: Optional[str] = None
    genome_assembly: Optional[str] = None
    id: Optional[str] = None
    chr: Optional[str] = None
    pos: Optional[int] = None
    ref: Optional[str] = None
    alt: Optional[str] = None
    info: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.vcf_version is not None and not isinstance(self.vcf_version, str):
            self.vcf_version = str(self.vcf_version)

        if self.genome_assembly is not None and not isinstance(self.genome_assembly, str):
            self.genome_assembly = str(self.genome_assembly)

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.chr is not None and not isinstance(self.chr, str):
            self.chr = str(self.chr)

        if self.pos is not None and not isinstance(self.pos, int):
            self.pos = int(self.pos)

        if self.ref is not None and not isinstance(self.ref, str):
            self.ref = str(self.ref)

        if self.alt is not None and not isinstance(self.alt, str):
            self.alt = str(self.alt)

        if self.info is not None and not isinstance(self.info, str):
            self.info = str(self.info)

        super().__post_init__(**kwargs)


@dataclass
class SpdiAllele(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.SpdiAllele
    class_class_curie: ClassVar[str] = "pfx:SpdiAllele"
    class_name: ClassVar[str] = "SpdiAllele"
    class_model_uri: ClassVar[URIRef] = PFX.SpdiAllele

    id: Optional[str] = None
    seq_id: Optional[str] = None
    position: Optional[int] = None
    deleted_sequence: Optional[str] = None
    inserted_sequence: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.seq_id is not None and not isinstance(self.seq_id, str):
            self.seq_id = str(self.seq_id)

        if self.position is not None and not isinstance(self.position, int):
            self.position = int(self.position)

        if self.deleted_sequence is not None and not isinstance(self.deleted_sequence, str):
            self.deleted_sequence = str(self.deleted_sequence)

        if self.inserted_sequence is not None and not isinstance(self.inserted_sequence, str):
            self.inserted_sequence = str(self.inserted_sequence)

        super().__post_init__(**kwargs)


@dataclass
class IscnAllele(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.IscnAllele
    class_class_curie: ClassVar[str] = "pfx:IscnAllele"
    class_name: ClassVar[str] = "IscnAllele"
    class_model_uri: ClassVar[URIRef] = PFX.IscnAllele

    id: Optional[str] = None
    iscn: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.iscn is not None and not isinstance(self.iscn, str):
            self.iscn = str(self.iscn)

        super().__post_init__(**kwargs)


@dataclass
class Variant(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Variant
    class_class_curie: ClassVar[str] = "pfx:Variant"
    class_name: ClassVar[str] = "Variant"
    class_model_uri: ClassVar[URIRef] = PFX.Variant

    hgvs_allele: Optional[Union[dict, HgvsAllele]] = None
    vcf_allele: Optional[Union[dict, VcfAllele]] = None
    spdi_allele: Optional[Union[dict, SpdiAllele]] = None
    iscn_allele: Optional[Union[dict, IscnAllele]] = None
    zygosity: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.hgvs_allele is not None and not isinstance(self.hgvs_allele, HgvsAllele):
            self.hgvs_allele = HgvsAllele(**as_dict(self.hgvs_allele))

        if self.vcf_allele is not None and not isinstance(self.vcf_allele, VcfAllele):
            self.vcf_allele = VcfAllele(**as_dict(self.vcf_allele))

        if self.spdi_allele is not None and not isinstance(self.spdi_allele, SpdiAllele):
            self.spdi_allele = SpdiAllele(**as_dict(self.spdi_allele))

        if self.iscn_allele is not None and not isinstance(self.iscn_allele, IscnAllele):
            self.iscn_allele = IscnAllele(**as_dict(self.iscn_allele))

        if self.zygosity is not None and not isinstance(self.zygosity, OntologyClass):
            self.zygosity = OntologyClass(**as_dict(self.zygosity))

        super().__post_init__(**kwargs)


@dataclass
class HtsFile(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.HtsFile
    class_class_curie: ClassVar[str] = "pfx:HtsFile"
    class_name: ClassVar[str] = "HtsFile"
    class_model_uri: ClassVar[URIRef] = PFX.HtsFile

    uri: Optional[str] = None
    description: Optional[str] = None
    hts_format: Optional[Union[str, "HtsFormatOptions"]] = None
    genome_assembly: Optional[str] = None
    individual_to_sample_identifiers: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.uri is not None and not isinstance(self.uri, str):
            self.uri = str(self.uri)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.hts_format is not None and not isinstance(self.hts_format, HtsFormatOptions):
            self.hts_format = HtsFormatOptions(self.hts_format)

        if self.genome_assembly is not None and not isinstance(self.genome_assembly, str):
            self.genome_assembly = str(self.genome_assembly)

        if self.individual_to_sample_identifiers is not None and not isinstance(self.individual_to_sample_identifiers, str):
            self.individual_to_sample_identifiers = str(self.individual_to_sample_identifiers)

        super().__post_init__(**kwargs)


@dataclass
class Timestamp(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Timestamp
    class_class_curie: ClassVar[str] = "pfx:Timestamp"
    class_name: ClassVar[str] = "Timestamp"
    class_model_uri: ClassVar[URIRef] = PFX.Timestamp

    seconds: Optional[int] = None
    nanos: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.seconds is not None and not isinstance(self.seconds, int):
            self.seconds = int(self.seconds)

        if self.nanos is not None and not isinstance(self.nanos, int):
            self.nanos = int(self.nanos)

        super().__post_init__(**kwargs)


@dataclass
class ExternalReference(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.ExternalReference
    class_class_curie: ClassVar[str] = "pfx:ExternalReference"
    class_name: ClassVar[str] = "ExternalReference"
    class_model_uri: ClassVar[URIRef] = PFX.ExternalReference

    id: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class Individual(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Individual
    class_class_curie: ClassVar[str] = "pfx:Individual"
    class_name: ClassVar[str] = "Individual"
    class_model_uri: ClassVar[URIRef] = PFX.Individual

    id: Optional[str] = None
    alternate_ids: Optional[Union[str, List[str]]] = empty_list()
    date_of_birth: Optional[Union[dict, Timestamp]] = None
    age_at_collection: Optional[Union[dict, Age]] = None
    age_range_at_collection: Optional[Union[dict, AgeRange]] = None
    sex: Optional[Union[str, "SexOptions"]] = None
    karyotypic_sex: Optional[Union[str, "KaryotypicSexOptions"]] = None
    taxonomy: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if not isinstance(self.alternate_ids, list):
            self.alternate_ids = [self.alternate_ids] if self.alternate_ids is not None else []
        self.alternate_ids = [v if isinstance(v, str) else str(v) for v in self.alternate_ids]

        if self.date_of_birth is not None and not isinstance(self.date_of_birth, Timestamp):
            self.date_of_birth = Timestamp(**as_dict(self.date_of_birth))

        if self.age_at_collection is not None and not isinstance(self.age_at_collection, Age):
            self.age_at_collection = Age(**as_dict(self.age_at_collection))

        if self.age_range_at_collection is not None and not isinstance(self.age_range_at_collection, AgeRange):
            self.age_range_at_collection = AgeRange(**as_dict(self.age_range_at_collection))

        if self.sex is not None and not isinstance(self.sex, SexOptions):
            self.sex = SexOptions(self.sex)

        if self.karyotypic_sex is not None and not isinstance(self.karyotypic_sex, KaryotypicSexOptions):
            self.karyotypic_sex = KaryotypicSexOptions(self.karyotypic_sex)

        if self.taxonomy is not None and not isinstance(self.taxonomy, OntologyClass):
            self.taxonomy = OntologyClass(**as_dict(self.taxonomy))

        super().__post_init__(**kwargs)


@dataclass
class Procedure(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Procedure
    class_class_curie: ClassVar[str] = "pfx:Procedure"
    class_name: ClassVar[str] = "Procedure"
    class_model_uri: ClassVar[URIRef] = PFX.Procedure

    code: Optional[Union[dict, OntologyClass]] = None
    body_site: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.code is not None and not isinstance(self.code, OntologyClass):
            self.code = OntologyClass(**as_dict(self.code))

        if self.body_site is not None and not isinstance(self.body_site, OntologyClass):
            self.body_site = OntologyClass(**as_dict(self.body_site))

        super().__post_init__(**kwargs)


@dataclass
class Biosample(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Biosample
    class_class_curie: ClassVar[str] = "pfx:Biosample"
    class_name: ClassVar[str] = "Biosample"
    class_model_uri: ClassVar[URIRef] = PFX.Biosample

    id: Optional[str] = None
    individual_id: Optional[str] = None
    description: Optional[str] = None
    sampled_tissue: Optional[Union[dict, OntologyClass]] = None
    phenotypic_features: Optional[Union[Union[dict, PhenotypicFeature], List[Union[dict, PhenotypicFeature]]]] = empty_list()
    taxonomy: Optional[Union[dict, OntologyClass]] = None
    age_of_individual_at_collection: Optional[Union[dict, Age]] = None
    age_range_of_individual_at_collection: Optional[Union[dict, AgeRange]] = None
    histological_diagnosis: Optional[Union[dict, OntologyClass]] = None
    tumor_progression: Optional[Union[dict, OntologyClass]] = None
    tumor_grade: Optional[Union[dict, OntologyClass]] = None
    diagnostic_markers: Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]] = empty_list()
    procedure: Optional[Union[dict, Procedure]] = None
    hts_files: Optional[Union[Union[dict, HtsFile], List[Union[dict, HtsFile]]]] = empty_list()
    variants: Optional[Union[Union[dict, Variant], List[Union[dict, Variant]]]] = empty_list()
    is_control_sample: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.individual_id is not None and not isinstance(self.individual_id, str):
            self.individual_id = str(self.individual_id)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.sampled_tissue is not None and not isinstance(self.sampled_tissue, OntologyClass):
            self.sampled_tissue = OntologyClass(**as_dict(self.sampled_tissue))

        if not isinstance(self.phenotypic_features, list):
            self.phenotypic_features = [self.phenotypic_features] if self.phenotypic_features is not None else []
        self.phenotypic_features = [v if isinstance(v, PhenotypicFeature) else PhenotypicFeature(**as_dict(v)) for v in self.phenotypic_features]

        if self.taxonomy is not None and not isinstance(self.taxonomy, OntologyClass):
            self.taxonomy = OntologyClass(**as_dict(self.taxonomy))

        if self.age_of_individual_at_collection is not None and not isinstance(self.age_of_individual_at_collection, Age):
            self.age_of_individual_at_collection = Age(**as_dict(self.age_of_individual_at_collection))

        if self.age_range_of_individual_at_collection is not None and not isinstance(self.age_range_of_individual_at_collection, AgeRange):
            self.age_range_of_individual_at_collection = AgeRange(**as_dict(self.age_range_of_individual_at_collection))

        if self.histological_diagnosis is not None and not isinstance(self.histological_diagnosis, OntologyClass):
            self.histological_diagnosis = OntologyClass(**as_dict(self.histological_diagnosis))

        if self.tumor_progression is not None and not isinstance(self.tumor_progression, OntologyClass):
            self.tumor_progression = OntologyClass(**as_dict(self.tumor_progression))

        if self.tumor_grade is not None and not isinstance(self.tumor_grade, OntologyClass):
            self.tumor_grade = OntologyClass(**as_dict(self.tumor_grade))

        if not isinstance(self.diagnostic_markers, list):
            self.diagnostic_markers = [self.diagnostic_markers] if self.diagnostic_markers is not None else []
        self.diagnostic_markers = [v if isinstance(v, OntologyClass) else OntologyClass(**as_dict(v)) for v in self.diagnostic_markers]

        if self.procedure is not None and not isinstance(self.procedure, Procedure):
            self.procedure = Procedure(**as_dict(self.procedure))

        if not isinstance(self.hts_files, list):
            self.hts_files = [self.hts_files] if self.hts_files is not None else []
        self.hts_files = [v if isinstance(v, HtsFile) else HtsFile(**as_dict(v)) for v in self.hts_files]

        if not isinstance(self.variants, list):
            self.variants = [self.variants] if self.variants is not None else []
        self.variants = [v if isinstance(v, Variant) else Variant(**as_dict(v)) for v in self.variants]

        if self.is_control_sample is not None and not isinstance(self.is_control_sample, Bool):
            self.is_control_sample = Bool(self.is_control_sample)

        super().__post_init__(**kwargs)


@dataclass
class Gene(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Gene
    class_class_curie: ClassVar[str] = "pfx:Gene"
    class_name: ClassVar[str] = "Gene"
    class_model_uri: ClassVar[URIRef] = PFX.Gene

    id: Optional[str] = None
    alternate_ids: Optional[Union[str, List[str]]] = empty_list()
    symbol: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if not isinstance(self.alternate_ids, list):
            self.alternate_ids = [self.alternate_ids] if self.alternate_ids is not None else []
        self.alternate_ids = [v if isinstance(v, str) else str(v) for v in self.alternate_ids]

        if self.symbol is not None and not isinstance(self.symbol, str):
            self.symbol = str(self.symbol)

        super().__post_init__(**kwargs)


@dataclass
class Disease(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Disease
    class_class_curie: ClassVar[str] = "pfx:Disease"
    class_name: ClassVar[str] = "Disease"
    class_model_uri: ClassVar[URIRef] = PFX.Disease

    term: Optional[Union[dict, OntologyClass]] = None
    age_of_onset: Optional[Union[dict, Age]] = None
    age_range_of_onset: Optional[Union[dict, AgeRange]] = None
    class_of_onset: Optional[Union[dict, OntologyClass]] = None
    disease_stage: Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]] = empty_list()
    tnm_finding: Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.term is not None and not isinstance(self.term, OntologyClass):
            self.term = OntologyClass(**as_dict(self.term))

        if self.age_of_onset is not None and not isinstance(self.age_of_onset, Age):
            self.age_of_onset = Age(**as_dict(self.age_of_onset))

        if self.age_range_of_onset is not None and not isinstance(self.age_range_of_onset, AgeRange):
            self.age_range_of_onset = AgeRange(**as_dict(self.age_range_of_onset))

        if self.class_of_onset is not None and not isinstance(self.class_of_onset, OntologyClass):
            self.class_of_onset = OntologyClass(**as_dict(self.class_of_onset))

        if not isinstance(self.disease_stage, list):
            self.disease_stage = [self.disease_stage] if self.disease_stage is not None else []
        self.disease_stage = [v if isinstance(v, OntologyClass) else OntologyClass(**as_dict(v)) for v in self.disease_stage]

        if not isinstance(self.tnm_finding, list):
            self.tnm_finding = [self.tnm_finding] if self.tnm_finding is not None else []
        self.tnm_finding = [v if isinstance(v, OntologyClass) else OntologyClass(**as_dict(v)) for v in self.tnm_finding]

        super().__post_init__(**kwargs)


@dataclass
class Phenopacket(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Phenopacket
    class_class_curie: ClassVar[str] = "pfx:Phenopacket"
    class_name: ClassVar[str] = "Phenopacket"
    class_model_uri: ClassVar[URIRef] = PFX.Phenopacket

    id: Optional[str] = None
    subject: Optional[Union[dict, Individual]] = None
    phenotypic_features: Optional[Union[Union[dict, PhenotypicFeature], List[Union[dict, PhenotypicFeature]]]] = empty_list()
    biosamples: Optional[Union[Union[dict, Biosample], List[Union[dict, Biosample]]]] = empty_list()
    genes: Optional[Union[Union[dict, Gene], List[Union[dict, Gene]]]] = empty_list()
    variants: Optional[Union[Union[dict, Variant], List[Union[dict, Variant]]]] = empty_list()
    diseases: Optional[Union[Union[dict, Disease], List[Union[dict, Disease]]]] = empty_list()
    hts_files: Optional[Union[Union[dict, HtsFile], List[Union[dict, HtsFile]]]] = empty_list()
    meta_data: Optional[Union[dict, "MetaData"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.subject is not None and not isinstance(self.subject, Individual):
            self.subject = Individual(**as_dict(self.subject))

        if not isinstance(self.phenotypic_features, list):
            self.phenotypic_features = [self.phenotypic_features] if self.phenotypic_features is not None else []
        self.phenotypic_features = [v if isinstance(v, PhenotypicFeature) else PhenotypicFeature(**as_dict(v)) for v in self.phenotypic_features]

        if not isinstance(self.biosamples, list):
            self.biosamples = [self.biosamples] if self.biosamples is not None else []
        self.biosamples = [v if isinstance(v, Biosample) else Biosample(**as_dict(v)) for v in self.biosamples]

        if not isinstance(self.genes, list):
            self.genes = [self.genes] if self.genes is not None else []
        self.genes = [v if isinstance(v, Gene) else Gene(**as_dict(v)) for v in self.genes]

        if not isinstance(self.variants, list):
            self.variants = [self.variants] if self.variants is not None else []
        self.variants = [v if isinstance(v, Variant) else Variant(**as_dict(v)) for v in self.variants]

        if not isinstance(self.diseases, list):
            self.diseases = [self.diseases] if self.diseases is not None else []
        self.diseases = [v if isinstance(v, Disease) else Disease(**as_dict(v)) for v in self.diseases]

        if not isinstance(self.hts_files, list):
            self.hts_files = [self.hts_files] if self.hts_files is not None else []
        self.hts_files = [v if isinstance(v, HtsFile) else HtsFile(**as_dict(v)) for v in self.hts_files]

        if self.meta_data is not None and not isinstance(self.meta_data, MetaData):
            self.meta_data = MetaData(**as_dict(self.meta_data))

        super().__post_init__(**kwargs)


@dataclass
class Resource(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Resource
    class_class_curie: ClassVar[str] = "pfx:Resource"
    class_name: ClassVar[str] = "Resource"
    class_model_uri: ClassVar[URIRef] = PFX.Resource

    id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None
    namespace_prefix: Optional[str] = None
    iri_prefix: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.url is not None and not isinstance(self.url, str):
            self.url = str(self.url)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.namespace_prefix is not None and not isinstance(self.namespace_prefix, str):
            self.namespace_prefix = str(self.namespace_prefix)

        if self.iri_prefix is not None and not isinstance(self.iri_prefix, str):
            self.iri_prefix = str(self.iri_prefix)

        super().__post_init__(**kwargs)


@dataclass
class Update(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Update
    class_class_curie: ClassVar[str] = "pfx:Update"
    class_name: ClassVar[str] = "Update"
    class_model_uri: ClassVar[URIRef] = PFX.Update

    timestamp: Optional[Union[dict, Timestamp]] = None
    updated_by: Optional[str] = None
    comment: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.timestamp is not None and not isinstance(self.timestamp, Timestamp):
            self.timestamp = Timestamp(**as_dict(self.timestamp))

        if self.updated_by is not None and not isinstance(self.updated_by, str):
            self.updated_by = str(self.updated_by)

        if self.comment is not None and not isinstance(self.comment, str):
            self.comment = str(self.comment)

        super().__post_init__(**kwargs)


@dataclass
class MetaData(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.MetaData
    class_class_curie: ClassVar[str] = "pfx:MetaData"
    class_name: ClassVar[str] = "MetaData"
    class_model_uri: ClassVar[URIRef] = PFX.MetaData

    created: Optional[Union[dict, Timestamp]] = None
    created_by: Optional[str] = None
    submitted_by: Optional[str] = None
    resources: Optional[Union[Union[dict, Resource], List[Union[dict, Resource]]]] = empty_list()
    updates: Optional[Union[Union[dict, Update], List[Union[dict, Update]]]] = empty_list()
    phenopacket_schema_version: Optional[str] = None
    external_references: Optional[Union[Union[dict, ExternalReference], List[Union[dict, ExternalReference]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.created is not None and not isinstance(self.created, Timestamp):
            self.created = Timestamp(**as_dict(self.created))

        if self.created_by is not None and not isinstance(self.created_by, str):
            self.created_by = str(self.created_by)

        if self.submitted_by is not None and not isinstance(self.submitted_by, str):
            self.submitted_by = str(self.submitted_by)

        if not isinstance(self.resources, list):
            self.resources = [self.resources] if self.resources is not None else []
        self.resources = [v if isinstance(v, Resource) else Resource(**as_dict(v)) for v in self.resources]

        if not isinstance(self.updates, list):
            self.updates = [self.updates] if self.updates is not None else []
        self.updates = [v if isinstance(v, Update) else Update(**as_dict(v)) for v in self.updates]

        if self.phenopacket_schema_version is not None and not isinstance(self.phenopacket_schema_version, str):
            self.phenopacket_schema_version = str(self.phenopacket_schema_version)

        if not isinstance(self.external_references, list):
            self.external_references = [self.external_references] if self.external_references is not None else []
        self.external_references = [v if isinstance(v, ExternalReference) else ExternalReference(**as_dict(v)) for v in self.external_references]

        super().__post_init__(**kwargs)


@dataclass
class Person(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Person
    class_class_curie: ClassVar[str] = "pfx:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PFX.Person

    family_id: Optional[str] = None
    individual_id: Optional[str] = None
    paternal_id: Optional[str] = None
    maternal_id: Optional[str] = None
    sex: Optional[Union[str, "SexOptions"]] = None
    affected_status: Optional[Union[str, "AffectedStatusOptions"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.family_id is not None and not isinstance(self.family_id, str):
            self.family_id = str(self.family_id)

        if self.individual_id is not None and not isinstance(self.individual_id, str):
            self.individual_id = str(self.individual_id)

        if self.paternal_id is not None and not isinstance(self.paternal_id, str):
            self.paternal_id = str(self.paternal_id)

        if self.maternal_id is not None and not isinstance(self.maternal_id, str):
            self.maternal_id = str(self.maternal_id)

        if self.sex is not None and not isinstance(self.sex, SexOptions):
            self.sex = SexOptions(self.sex)

        if self.affected_status is not None and not isinstance(self.affected_status, AffectedStatusOptions):
            self.affected_status = AffectedStatusOptions(self.affected_status)

        super().__post_init__(**kwargs)


@dataclass
class Pedigree(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Pedigree
    class_class_curie: ClassVar[str] = "pfx:Pedigree"
    class_name: ClassVar[str] = "Pedigree"
    class_model_uri: ClassVar[URIRef] = PFX.Pedigree

    persons: Optional[Union[Union[dict, Person], List[Union[dict, Person]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.persons, list):
            self.persons = [self.persons] if self.persons is not None else []
        self.persons = [v if isinstance(v, Person) else Person(**as_dict(v)) for v in self.persons]

        super().__post_init__(**kwargs)


@dataclass
class Family(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Family
    class_class_curie: ClassVar[str] = "pfx:Family"
    class_name: ClassVar[str] = "Family"
    class_model_uri: ClassVar[URIRef] = PFX.Family

    id: Optional[str] = None
    proband: Optional[Union[dict, Phenopacket]] = None
    relatives: Optional[Union[Union[dict, Phenopacket], List[Union[dict, Phenopacket]]]] = empty_list()
    pedigree: Optional[Union[dict, Pedigree]] = None
    hts_files: Optional[Union[Union[dict, HtsFile], List[Union[dict, HtsFile]]]] = empty_list()
    meta_data: Optional[Union[dict, MetaData]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.proband is not None and not isinstance(self.proband, Phenopacket):
            self.proband = Phenopacket(**as_dict(self.proband))

        if not isinstance(self.relatives, list):
            self.relatives = [self.relatives] if self.relatives is not None else []
        self.relatives = [v if isinstance(v, Phenopacket) else Phenopacket(**as_dict(v)) for v in self.relatives]

        if self.pedigree is not None and not isinstance(self.pedigree, Pedigree):
            self.pedigree = Pedigree(**as_dict(self.pedigree))

        if not isinstance(self.hts_files, list):
            self.hts_files = [self.hts_files] if self.hts_files is not None else []
        self.hts_files = [v if isinstance(v, HtsFile) else HtsFile(**as_dict(v)) for v in self.hts_files]

        if self.meta_data is not None and not isinstance(self.meta_data, MetaData):
            self.meta_data = MetaData(**as_dict(self.meta_data))

        super().__post_init__(**kwargs)


@dataclass
class Cohort(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PFX.Cohort
    class_class_curie: ClassVar[str] = "pfx:Cohort"
    class_name: ClassVar[str] = "Cohort"
    class_model_uri: ClassVar[URIRef] = PFX.Cohort

    id: Optional[str] = None
    description: Optional[str] = None
    members: Optional[Union[Union[dict, Phenopacket], List[Union[dict, Phenopacket]]]] = empty_list()
    hts_files: Optional[Union[Union[dict, HtsFile], List[Union[dict, HtsFile]]]] = empty_list()
    meta_data: Optional[Union[dict, MetaData]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.members, list):
            self.members = [self.members] if self.members is not None else []
        self.members = [v if isinstance(v, Phenopacket) else Phenopacket(**as_dict(v)) for v in self.members]

        if not isinstance(self.hts_files, list):
            self.hts_files = [self.hts_files] if self.hts_files is not None else []
        self.hts_files = [v if isinstance(v, HtsFile) else HtsFile(**as_dict(v)) for v in self.hts_files]

        if self.meta_data is not None and not isinstance(self.meta_data, MetaData):
            self.meta_data = MetaData(**as_dict(self.meta_data))

        super().__post_init__(**kwargs)


# Enumerations
class HtsFormatOptions(EnumDefinitionImpl):

    UNKNOWN = PermissibleValue(text="UNKNOWN")
    SAM = PermissibleValue(text="SAM")
    BAM = PermissibleValue(text="BAM")
    CRAM = PermissibleValue(text="CRAM")
    VCF = PermissibleValue(text="VCF")
    BCF = PermissibleValue(text="BCF")
    GVCF = PermissibleValue(text="GVCF")
    FASTQ = PermissibleValue(text="FASTQ")

    _defn = EnumDefinition(
        name="HtsFormatOptions",
    )

class SexOptions(EnumDefinitionImpl):

    UNKNOWN_SEX = PermissibleValue(text="UNKNOWN_SEX")
    FEMALE = PermissibleValue(text="FEMALE")
    MALE = PermissibleValue(text="MALE")
    OTHER_SEX = PermissibleValue(text="OTHER_SEX")

    _defn = EnumDefinition(
        name="SexOptions",
    )

class KaryotypicSexOptions(EnumDefinitionImpl):

    UNKNOWN_KARYOTYPE = PermissibleValue(text="UNKNOWN_KARYOTYPE")
    XX = PermissibleValue(text="XX")
    XY = PermissibleValue(text="XY")
    XO = PermissibleValue(text="XO")
    XXY = PermissibleValue(text="XXY")
    XXX = PermissibleValue(text="XXX")
    XXYY = PermissibleValue(text="XXYY")
    XXXY = PermissibleValue(text="XXXY")
    XXXX = PermissibleValue(text="XXXX")
    XYY = PermissibleValue(text="XYY")
    OTHER_KARYOTYPE = PermissibleValue(text="OTHER_KARYOTYPE")

    _defn = EnumDefinition(
        name="KaryotypicSexOptions",
    )

class AffectedStatusOptions(EnumDefinitionImpl):

    MISSING = PermissibleValue(text="MISSING")
    UNAFFECTED = PermissibleValue(text="UNAFFECTED")
    AFFECTED = PermissibleValue(text="AFFECTED")

    _defn = EnumDefinition(
        name="AffectedStatusOptions",
    )

# Slots
class slots:
    pass

slots.age = Slot(uri=PFX.age, name="age", curie=PFX.curie('age'),
                   model_uri=PFX.age, domain=None, range=Optional[str])

slots.id = Slot(uri=PFX.id, name="id", curie=PFX.curie('id'),
                   model_uri=PFX.id, domain=None, range=Optional[str])

slots.label = Slot(uri=PFX.label, name="label", curie=PFX.curie('label'),
                   model_uri=PFX.label, domain=None, range=Optional[str])

slots.start = Slot(uri=PFX.start, name="start", curie=PFX.curie('start'),
                   model_uri=PFX.start, domain=None, range=Optional[Union[dict, Age]])

slots.end = Slot(uri=PFX.end, name="end", curie=PFX.curie('end'),
                   model_uri=PFX.end, domain=None, range=Optional[Union[dict, Age]])

slots.description = Slot(uri=PFX.description, name="description", curie=PFX.curie('description'),
                   model_uri=PFX.description, domain=None, range=Optional[str])

slots.type = Slot(uri=PFX.type, name="type", curie=PFX.curie('type'),
                   model_uri=PFX.type, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.negated = Slot(uri=PFX.negated, name="negated", curie=PFX.curie('negated'),
                   model_uri=PFX.negated, domain=None, range=Optional[Union[bool, Bool]])

slots.severity = Slot(uri=PFX.severity, name="severity", curie=PFX.curie('severity'),
                   model_uri=PFX.severity, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.modifiers = Slot(uri=PFX.modifiers, name="modifiers", curie=PFX.curie('modifiers'),
                   model_uri=PFX.modifiers, domain=None, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.age_of_onset = Slot(uri=PFX.age_of_onset, name="age_of_onset", curie=PFX.curie('age_of_onset'),
                   model_uri=PFX.age_of_onset, domain=None, range=Optional[Union[dict, Age]])

slots.age_range_of_onset = Slot(uri=PFX.age_range_of_onset, name="age_range_of_onset", curie=PFX.curie('age_range_of_onset'),
                   model_uri=PFX.age_range_of_onset, domain=None, range=Optional[Union[dict, AgeRange]])

slots.class_of_onset = Slot(uri=PFX.class_of_onset, name="class_of_onset", curie=PFX.curie('class_of_onset'),
                   model_uri=PFX.class_of_onset, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.evidence_code = Slot(uri=PFX.evidence_code, name="evidence_code", curie=PFX.curie('evidence_code'),
                   model_uri=PFX.evidence_code, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.reference = Slot(uri=PFX.reference, name="reference", curie=PFX.curie('reference'),
                   model_uri=PFX.reference, domain=None, range=Optional[Union[dict, ExternalReference]])

slots.evidence = Slot(uri=PFX.evidence, name="evidence", curie=PFX.curie('evidence'),
                   model_uri=PFX.evidence, domain=None, range=Optional[Union[Union[dict, Evidence], List[Union[dict, Evidence]]]])

slots.hgvs = Slot(uri=PFX.hgvs, name="hgvs", curie=PFX.curie('hgvs'),
                   model_uri=PFX.hgvs, domain=None, range=Optional[str])

slots.hgvs_allele = Slot(uri=PFX.hgvs_allele, name="hgvs_allele", curie=PFX.curie('hgvs_allele'),
                   model_uri=PFX.hgvs_allele, domain=None, range=Optional[Union[dict, HgvsAllele]])

slots.vcf_version = Slot(uri=PFX.vcf_version, name="vcf_version", curie=PFX.curie('vcf_version'),
                   model_uri=PFX.vcf_version, domain=None, range=Optional[str])

slots.genome_assembly = Slot(uri=PFX.genome_assembly, name="genome_assembly", curie=PFX.curie('genome_assembly'),
                   model_uri=PFX.genome_assembly, domain=None, range=Optional[str])

slots.chr = Slot(uri=PFX.chr, name="chr", curie=PFX.curie('chr'),
                   model_uri=PFX.chr, domain=None, range=Optional[str])

slots.pos = Slot(uri=PFX.pos, name="pos", curie=PFX.curie('pos'),
                   model_uri=PFX.pos, domain=None, range=Optional[int])

slots.ref = Slot(uri=PFX.ref, name="ref", curie=PFX.curie('ref'),
                   model_uri=PFX.ref, domain=None, range=Optional[str])

slots.alt = Slot(uri=PFX.alt, name="alt", curie=PFX.curie('alt'),
                   model_uri=PFX.alt, domain=None, range=Optional[str])

slots.info = Slot(uri=PFX.info, name="info", curie=PFX.curie('info'),
                   model_uri=PFX.info, domain=None, range=Optional[str])

slots.vcf_allele = Slot(uri=PFX.vcf_allele, name="vcf_allele", curie=PFX.curie('vcf_allele'),
                   model_uri=PFX.vcf_allele, domain=None, range=Optional[Union[dict, VcfAllele]])

slots.seq_id = Slot(uri=PFX.seq_id, name="seq_id", curie=PFX.curie('seq_id'),
                   model_uri=PFX.seq_id, domain=None, range=Optional[str])

slots.position = Slot(uri=PFX.position, name="position", curie=PFX.curie('position'),
                   model_uri=PFX.position, domain=None, range=Optional[int])

slots.deleted_sequence = Slot(uri=PFX.deleted_sequence, name="deleted_sequence", curie=PFX.curie('deleted_sequence'),
                   model_uri=PFX.deleted_sequence, domain=None, range=Optional[str])

slots.inserted_sequence = Slot(uri=PFX.inserted_sequence, name="inserted_sequence", curie=PFX.curie('inserted_sequence'),
                   model_uri=PFX.inserted_sequence, domain=None, range=Optional[str])

slots.spdi_allele = Slot(uri=PFX.spdi_allele, name="spdi_allele", curie=PFX.curie('spdi_allele'),
                   model_uri=PFX.spdi_allele, domain=None, range=Optional[Union[dict, SpdiAllele]])

slots.iscn = Slot(uri=PFX.iscn, name="iscn", curie=PFX.curie('iscn'),
                   model_uri=PFX.iscn, domain=None, range=Optional[str])

slots.iscn_allele = Slot(uri=PFX.iscn_allele, name="iscn_allele", curie=PFX.curie('iscn_allele'),
                   model_uri=PFX.iscn_allele, domain=None, range=Optional[Union[dict, IscnAllele]])

slots.zygosity = Slot(uri=PFX.zygosity, name="zygosity", curie=PFX.curie('zygosity'),
                   model_uri=PFX.zygosity, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.uri = Slot(uri=PFX.uri, name="uri", curie=PFX.curie('uri'),
                   model_uri=PFX.uri, domain=None, range=Optional[str])

slots.hts_format = Slot(uri=PFX.hts_format, name="hts_format", curie=PFX.curie('hts_format'),
                   model_uri=PFX.hts_format, domain=None, range=Optional[Union[str, "HtsFormatOptions"]])

slots.individual_to_sample_identifiers = Slot(uri=PFX.individual_to_sample_identifiers, name="individual_to_sample_identifiers", curie=PFX.curie('individual_to_sample_identifiers'),
                   model_uri=PFX.individual_to_sample_identifiers, domain=None, range=Optional[str])

slots.seconds = Slot(uri=PFX.seconds, name="seconds", curie=PFX.curie('seconds'),
                   model_uri=PFX.seconds, domain=None, range=Optional[int])

slots.nanos = Slot(uri=PFX.nanos, name="nanos", curie=PFX.curie('nanos'),
                   model_uri=PFX.nanos, domain=None, range=Optional[int])

slots.alternate_ids = Slot(uri=PFX.alternate_ids, name="alternate_ids", curie=PFX.curie('alternate_ids'),
                   model_uri=PFX.alternate_ids, domain=None, range=Optional[Union[str, List[str]]])

slots.date_of_birth = Slot(uri=PFX.date_of_birth, name="date_of_birth", curie=PFX.curie('date_of_birth'),
                   model_uri=PFX.date_of_birth, domain=None, range=Optional[Union[dict, Timestamp]])

slots.age_at_collection = Slot(uri=PFX.age_at_collection, name="age_at_collection", curie=PFX.curie('age_at_collection'),
                   model_uri=PFX.age_at_collection, domain=None, range=Optional[Union[dict, Age]])

slots.age_range_at_collection = Slot(uri=PFX.age_range_at_collection, name="age_range_at_collection", curie=PFX.curie('age_range_at_collection'),
                   model_uri=PFX.age_range_at_collection, domain=None, range=Optional[Union[dict, AgeRange]])

slots.sex = Slot(uri=PFX.sex, name="sex", curie=PFX.curie('sex'),
                   model_uri=PFX.sex, domain=None, range=Optional[Union[str, "SexOptions"]])

slots.karyotypic_sex = Slot(uri=PFX.karyotypic_sex, name="karyotypic_sex", curie=PFX.curie('karyotypic_sex'),
                   model_uri=PFX.karyotypic_sex, domain=None, range=Optional[Union[str, "KaryotypicSexOptions"]])

slots.taxonomy = Slot(uri=PFX.taxonomy, name="taxonomy", curie=PFX.curie('taxonomy'),
                   model_uri=PFX.taxonomy, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.subject = Slot(uri=PFX.subject, name="subject", curie=PFX.curie('subject'),
                   model_uri=PFX.subject, domain=None, range=Optional[Union[dict, Individual]])

slots.phenotypic_features = Slot(uri=PFX.phenotypic_features, name="phenotypic_features", curie=PFX.curie('phenotypic_features'),
                   model_uri=PFX.phenotypic_features, domain=None, range=Optional[Union[Union[dict, PhenotypicFeature], List[Union[dict, PhenotypicFeature]]]])

slots.individual_id = Slot(uri=PFX.individual_id, name="individual_id", curie=PFX.curie('individual_id'),
                   model_uri=PFX.individual_id, domain=None, range=Optional[str])

slots.sampled_tissue = Slot(uri=PFX.sampled_tissue, name="sampled_tissue", curie=PFX.curie('sampled_tissue'),
                   model_uri=PFX.sampled_tissue, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.age_of_individual_at_collection = Slot(uri=PFX.age_of_individual_at_collection, name="age_of_individual_at_collection", curie=PFX.curie('age_of_individual_at_collection'),
                   model_uri=PFX.age_of_individual_at_collection, domain=None, range=Optional[Union[dict, Age]])

slots.age_range_of_individual_at_collection = Slot(uri=PFX.age_range_of_individual_at_collection, name="age_range_of_individual_at_collection", curie=PFX.curie('age_range_of_individual_at_collection'),
                   model_uri=PFX.age_range_of_individual_at_collection, domain=None, range=Optional[Union[dict, AgeRange]])

slots.histological_diagnosis = Slot(uri=PFX.histological_diagnosis, name="histological_diagnosis", curie=PFX.curie('histological_diagnosis'),
                   model_uri=PFX.histological_diagnosis, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.tumor_progression = Slot(uri=PFX.tumor_progression, name="tumor_progression", curie=PFX.curie('tumor_progression'),
                   model_uri=PFX.tumor_progression, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.tumor_grade = Slot(uri=PFX.tumor_grade, name="tumor_grade", curie=PFX.curie('tumor_grade'),
                   model_uri=PFX.tumor_grade, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.diagnostic_markers = Slot(uri=PFX.diagnostic_markers, name="diagnostic_markers", curie=PFX.curie('diagnostic_markers'),
                   model_uri=PFX.diagnostic_markers, domain=None, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.code = Slot(uri=PFX.code, name="code", curie=PFX.curie('code'),
                   model_uri=PFX.code, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.body_site = Slot(uri=PFX.body_site, name="body_site", curie=PFX.curie('body_site'),
                   model_uri=PFX.body_site, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.procedure = Slot(uri=PFX.procedure, name="procedure", curie=PFX.curie('procedure'),
                   model_uri=PFX.procedure, domain=None, range=Optional[Union[dict, Procedure]])

slots.hts_files = Slot(uri=PFX.hts_files, name="hts_files", curie=PFX.curie('hts_files'),
                   model_uri=PFX.hts_files, domain=None, range=Optional[Union[Union[dict, HtsFile], List[Union[dict, HtsFile]]]])

slots.variants = Slot(uri=PFX.variants, name="variants", curie=PFX.curie('variants'),
                   model_uri=PFX.variants, domain=None, range=Optional[Union[Union[dict, Variant], List[Union[dict, Variant]]]])

slots.is_control_sample = Slot(uri=PFX.is_control_sample, name="is_control_sample", curie=PFX.curie('is_control_sample'),
                   model_uri=PFX.is_control_sample, domain=None, range=Optional[Union[bool, Bool]])

slots.biosamples = Slot(uri=PFX.biosamples, name="biosamples", curie=PFX.curie('biosamples'),
                   model_uri=PFX.biosamples, domain=None, range=Optional[Union[Union[dict, Biosample], List[Union[dict, Biosample]]]])

slots.symbol = Slot(uri=PFX.symbol, name="symbol", curie=PFX.curie('symbol'),
                   model_uri=PFX.symbol, domain=None, range=Optional[str])

slots.genes = Slot(uri=PFX.genes, name="genes", curie=PFX.curie('genes'),
                   model_uri=PFX.genes, domain=None, range=Optional[Union[Union[dict, Gene], List[Union[dict, Gene]]]])

slots.term = Slot(uri=PFX.term, name="term", curie=PFX.curie('term'),
                   model_uri=PFX.term, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.disease_stage = Slot(uri=PFX.disease_stage, name="disease_stage", curie=PFX.curie('disease_stage'),
                   model_uri=PFX.disease_stage, domain=None, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.tnm_finding = Slot(uri=PFX.tnm_finding, name="tnm_finding", curie=PFX.curie('tnm_finding'),
                   model_uri=PFX.tnm_finding, domain=None, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.diseases = Slot(uri=PFX.diseases, name="diseases", curie=PFX.curie('diseases'),
                   model_uri=PFX.diseases, domain=None, range=Optional[Union[Union[dict, Disease], List[Union[dict, Disease]]]])

slots.meta_data = Slot(uri=PFX.meta_data, name="meta_data", curie=PFX.curie('meta_data'),
                   model_uri=PFX.meta_data, domain=None, range=Optional[Union[dict, MetaData]])

slots.created = Slot(uri=PFX.created, name="created", curie=PFX.curie('created'),
                   model_uri=PFX.created, domain=None, range=Optional[Union[dict, Timestamp]])

slots.created_by = Slot(uri=PFX.created_by, name="created_by", curie=PFX.curie('created_by'),
                   model_uri=PFX.created_by, domain=None, range=Optional[str])

slots.submitted_by = Slot(uri=PFX.submitted_by, name="submitted_by", curie=PFX.curie('submitted_by'),
                   model_uri=PFX.submitted_by, domain=None, range=Optional[str])

slots.name = Slot(uri=PFX.name, name="name", curie=PFX.curie('name'),
                   model_uri=PFX.name, domain=None, range=Optional[str])

slots.url = Slot(uri=PFX.url, name="url", curie=PFX.curie('url'),
                   model_uri=PFX.url, domain=None, range=Optional[str])

slots.version = Slot(uri=PFX.version, name="version", curie=PFX.curie('version'),
                   model_uri=PFX.version, domain=None, range=Optional[str])

slots.namespace_prefix = Slot(uri=PFX.namespace_prefix, name="namespace_prefix", curie=PFX.curie('namespace_prefix'),
                   model_uri=PFX.namespace_prefix, domain=None, range=Optional[str])

slots.iri_prefix = Slot(uri=PFX.iri_prefix, name="iri_prefix", curie=PFX.curie('iri_prefix'),
                   model_uri=PFX.iri_prefix, domain=None, range=Optional[str])

slots.resources = Slot(uri=PFX.resources, name="resources", curie=PFX.curie('resources'),
                   model_uri=PFX.resources, domain=None, range=Optional[Union[Union[dict, Resource], List[Union[dict, Resource]]]])

slots.timestamp = Slot(uri=PFX.timestamp, name="timestamp", curie=PFX.curie('timestamp'),
                   model_uri=PFX.timestamp, domain=None, range=Optional[Union[dict, Timestamp]])

slots.updated_by = Slot(uri=PFX.updated_by, name="updated_by", curie=PFX.curie('updated_by'),
                   model_uri=PFX.updated_by, domain=None, range=Optional[str])

slots.comment = Slot(uri=PFX.comment, name="comment", curie=PFX.curie('comment'),
                   model_uri=PFX.comment, domain=None, range=Optional[str])

slots.updates = Slot(uri=PFX.updates, name="updates", curie=PFX.curie('updates'),
                   model_uri=PFX.updates, domain=None, range=Optional[Union[Union[dict, Update], List[Union[dict, Update]]]])

slots.phenopacket_schema_version = Slot(uri=PFX.phenopacket_schema_version, name="phenopacket_schema_version", curie=PFX.curie('phenopacket_schema_version'),
                   model_uri=PFX.phenopacket_schema_version, domain=None, range=Optional[str])

slots.external_references = Slot(uri=PFX.external_references, name="external_references", curie=PFX.curie('external_references'),
                   model_uri=PFX.external_references, domain=None, range=Optional[Union[Union[dict, ExternalReference], List[Union[dict, ExternalReference]]]])

slots.proband = Slot(uri=PFX.proband, name="proband", curie=PFX.curie('proband'),
                   model_uri=PFX.proband, domain=None, range=Optional[Union[dict, Phenopacket]])

slots.relatives = Slot(uri=PFX.relatives, name="relatives", curie=PFX.curie('relatives'),
                   model_uri=PFX.relatives, domain=None, range=Optional[Union[Union[dict, Phenopacket], List[Union[dict, Phenopacket]]]])

slots.family_id = Slot(uri=PFX.family_id, name="family_id", curie=PFX.curie('family_id'),
                   model_uri=PFX.family_id, domain=None, range=Optional[str])

slots.paternal_id = Slot(uri=PFX.paternal_id, name="paternal_id", curie=PFX.curie('paternal_id'),
                   model_uri=PFX.paternal_id, domain=None, range=Optional[str])

slots.maternal_id = Slot(uri=PFX.maternal_id, name="maternal_id", curie=PFX.curie('maternal_id'),
                   model_uri=PFX.maternal_id, domain=None, range=Optional[str])

slots.affected_status = Slot(uri=PFX.affected_status, name="affected_status", curie=PFX.curie('affected_status'),
                   model_uri=PFX.affected_status, domain=None, range=Optional[Union[str, "AffectedStatusOptions"]])

slots.persons = Slot(uri=PFX.persons, name="persons", curie=PFX.curie('persons'),
                   model_uri=PFX.persons, domain=None, range=Optional[Union[Union[dict, Person], List[Union[dict, Person]]]])

slots.pedigree = Slot(uri=PFX.pedigree, name="pedigree", curie=PFX.curie('pedigree'),
                   model_uri=PFX.pedigree, domain=None, range=Optional[Union[dict, Pedigree]])

slots.members = Slot(uri=PFX.members, name="members", curie=PFX.curie('members'),
                   model_uri=PFX.members, domain=None, range=Optional[Union[Union[dict, Phenopacket], List[Union[dict, Phenopacket]]]])

slots.Age_age = Slot(uri=PFX.age, name="Age_age", curie=PFX.curie('age'),
                   model_uri=PFX.Age_age, domain=Age, range=Optional[str])

slots.OntologyClass_id = Slot(uri=PFX.id, name="OntologyClass_id", curie=PFX.curie('id'),
                   model_uri=PFX.OntologyClass_id, domain=OntologyClass, range=Optional[str])

slots.OntologyClass_label = Slot(uri=PFX.label, name="OntologyClass_label", curie=PFX.curie('label'),
                   model_uri=PFX.OntologyClass_label, domain=OntologyClass, range=Optional[str])

slots.AgeRange_start = Slot(uri=PFX.start, name="AgeRange_start", curie=PFX.curie('start'),
                   model_uri=PFX.AgeRange_start, domain=AgeRange, range=Optional[Union[dict, Age]])

slots.AgeRange_end = Slot(uri=PFX.end, name="AgeRange_end", curie=PFX.curie('end'),
                   model_uri=PFX.AgeRange_end, domain=AgeRange, range=Optional[Union[dict, Age]])

slots.Evidence_evidence_code = Slot(uri=PFX.evidence_code, name="Evidence_evidence_code", curie=PFX.curie('evidence_code'),
                   model_uri=PFX.Evidence_evidence_code, domain=Evidence, range=Optional[Union[dict, OntologyClass]])

slots.Evidence_reference = Slot(uri=PFX.reference, name="Evidence_reference", curie=PFX.curie('reference'),
                   model_uri=PFX.Evidence_reference, domain=Evidence, range=Optional[Union[dict, "ExternalReference"]])

slots.PhenotypicFeature_description = Slot(uri=PFX.description, name="PhenotypicFeature_description", curie=PFX.curie('description'),
                   model_uri=PFX.PhenotypicFeature_description, domain=PhenotypicFeature, range=Optional[str])

slots.PhenotypicFeature_type = Slot(uri=PFX.type, name="PhenotypicFeature_type", curie=PFX.curie('type'),
                   model_uri=PFX.PhenotypicFeature_type, domain=PhenotypicFeature, range=Optional[Union[dict, OntologyClass]])

slots.PhenotypicFeature_negated = Slot(uri=PFX.negated, name="PhenotypicFeature_negated", curie=PFX.curie('negated'),
                   model_uri=PFX.PhenotypicFeature_negated, domain=PhenotypicFeature, range=Optional[Union[bool, Bool]])

slots.PhenotypicFeature_severity = Slot(uri=PFX.severity, name="PhenotypicFeature_severity", curie=PFX.curie('severity'),
                   model_uri=PFX.PhenotypicFeature_severity, domain=PhenotypicFeature, range=Optional[Union[dict, OntologyClass]])

slots.PhenotypicFeature_modifiers = Slot(uri=PFX.modifiers, name="PhenotypicFeature_modifiers", curie=PFX.curie('modifiers'),
                   model_uri=PFX.PhenotypicFeature_modifiers, domain=PhenotypicFeature, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.PhenotypicFeature_age_of_onset = Slot(uri=PFX.age_of_onset, name="PhenotypicFeature_age_of_onset", curie=PFX.curie('age_of_onset'),
                   model_uri=PFX.PhenotypicFeature_age_of_onset, domain=PhenotypicFeature, range=Optional[Union[dict, Age]])

slots.PhenotypicFeature_age_range_of_onset = Slot(uri=PFX.age_range_of_onset, name="PhenotypicFeature_age_range_of_onset", curie=PFX.curie('age_range_of_onset'),
                   model_uri=PFX.PhenotypicFeature_age_range_of_onset, domain=PhenotypicFeature, range=Optional[Union[dict, AgeRange]])

slots.PhenotypicFeature_class_of_onset = Slot(uri=PFX.class_of_onset, name="PhenotypicFeature_class_of_onset", curie=PFX.curie('class_of_onset'),
                   model_uri=PFX.PhenotypicFeature_class_of_onset, domain=PhenotypicFeature, range=Optional[Union[dict, OntologyClass]])

slots.PhenotypicFeature_evidence = Slot(uri=PFX.evidence, name="PhenotypicFeature_evidence", curie=PFX.curie('evidence'),
                   model_uri=PFX.PhenotypicFeature_evidence, domain=PhenotypicFeature, range=Optional[Union[Union[dict, Evidence], List[Union[dict, Evidence]]]])

slots.HgvsAllele_id = Slot(uri=PFX.id, name="HgvsAllele_id", curie=PFX.curie('id'),
                   model_uri=PFX.HgvsAllele_id, domain=HgvsAllele, range=Optional[str])

slots.HgvsAllele_hgvs = Slot(uri=PFX.hgvs, name="HgvsAllele_hgvs", curie=PFX.curie('hgvs'),
                   model_uri=PFX.HgvsAllele_hgvs, domain=HgvsAllele, range=Optional[str])

slots.VcfAllele_vcf_version = Slot(uri=PFX.vcf_version, name="VcfAllele_vcf_version", curie=PFX.curie('vcf_version'),
                   model_uri=PFX.VcfAllele_vcf_version, domain=VcfAllele, range=Optional[str])

slots.VcfAllele_genome_assembly = Slot(uri=PFX.genome_assembly, name="VcfAllele_genome_assembly", curie=PFX.curie('genome_assembly'),
                   model_uri=PFX.VcfAllele_genome_assembly, domain=VcfAllele, range=Optional[str])

slots.VcfAllele_id = Slot(uri=PFX.id, name="VcfAllele_id", curie=PFX.curie('id'),
                   model_uri=PFX.VcfAllele_id, domain=VcfAllele, range=Optional[str])

slots.VcfAllele_chr = Slot(uri=PFX.chr, name="VcfAllele_chr", curie=PFX.curie('chr'),
                   model_uri=PFX.VcfAllele_chr, domain=VcfAllele, range=Optional[str])

slots.VcfAllele_pos = Slot(uri=PFX.pos, name="VcfAllele_pos", curie=PFX.curie('pos'),
                   model_uri=PFX.VcfAllele_pos, domain=VcfAllele, range=Optional[int])

slots.VcfAllele_ref = Slot(uri=PFX.ref, name="VcfAllele_ref", curie=PFX.curie('ref'),
                   model_uri=PFX.VcfAllele_ref, domain=VcfAllele, range=Optional[str])

slots.VcfAllele_alt = Slot(uri=PFX.alt, name="VcfAllele_alt", curie=PFX.curie('alt'),
                   model_uri=PFX.VcfAllele_alt, domain=VcfAllele, range=Optional[str])

slots.VcfAllele_info = Slot(uri=PFX.info, name="VcfAllele_info", curie=PFX.curie('info'),
                   model_uri=PFX.VcfAllele_info, domain=VcfAllele, range=Optional[str])

slots.SpdiAllele_id = Slot(uri=PFX.id, name="SpdiAllele_id", curie=PFX.curie('id'),
                   model_uri=PFX.SpdiAllele_id, domain=SpdiAllele, range=Optional[str])

slots.SpdiAllele_seq_id = Slot(uri=PFX.seq_id, name="SpdiAllele_seq_id", curie=PFX.curie('seq_id'),
                   model_uri=PFX.SpdiAllele_seq_id, domain=SpdiAllele, range=Optional[str])

slots.SpdiAllele_position = Slot(uri=PFX.position, name="SpdiAllele_position", curie=PFX.curie('position'),
                   model_uri=PFX.SpdiAllele_position, domain=SpdiAllele, range=Optional[int])

slots.SpdiAllele_deleted_sequence = Slot(uri=PFX.deleted_sequence, name="SpdiAllele_deleted_sequence", curie=PFX.curie('deleted_sequence'),
                   model_uri=PFX.SpdiAllele_deleted_sequence, domain=SpdiAllele, range=Optional[str])

slots.SpdiAllele_inserted_sequence = Slot(uri=PFX.inserted_sequence, name="SpdiAllele_inserted_sequence", curie=PFX.curie('inserted_sequence'),
                   model_uri=PFX.SpdiAllele_inserted_sequence, domain=SpdiAllele, range=Optional[str])

slots.IscnAllele_id = Slot(uri=PFX.id, name="IscnAllele_id", curie=PFX.curie('id'),
                   model_uri=PFX.IscnAllele_id, domain=IscnAllele, range=Optional[str])

slots.IscnAllele_iscn = Slot(uri=PFX.iscn, name="IscnAllele_iscn", curie=PFX.curie('iscn'),
                   model_uri=PFX.IscnAllele_iscn, domain=IscnAllele, range=Optional[str])

slots.Variant_hgvs_allele = Slot(uri=PFX.hgvs_allele, name="Variant_hgvs_allele", curie=PFX.curie('hgvs_allele'),
                   model_uri=PFX.Variant_hgvs_allele, domain=Variant, range=Optional[Union[dict, HgvsAllele]])

slots.Variant_vcf_allele = Slot(uri=PFX.vcf_allele, name="Variant_vcf_allele", curie=PFX.curie('vcf_allele'),
                   model_uri=PFX.Variant_vcf_allele, domain=Variant, range=Optional[Union[dict, VcfAllele]])

slots.Variant_spdi_allele = Slot(uri=PFX.spdi_allele, name="Variant_spdi_allele", curie=PFX.curie('spdi_allele'),
                   model_uri=PFX.Variant_spdi_allele, domain=Variant, range=Optional[Union[dict, SpdiAllele]])

slots.Variant_iscn_allele = Slot(uri=PFX.iscn_allele, name="Variant_iscn_allele", curie=PFX.curie('iscn_allele'),
                   model_uri=PFX.Variant_iscn_allele, domain=Variant, range=Optional[Union[dict, IscnAllele]])

slots.Variant_zygosity = Slot(uri=PFX.zygosity, name="Variant_zygosity", curie=PFX.curie('zygosity'),
                   model_uri=PFX.Variant_zygosity, domain=Variant, range=Optional[Union[dict, OntologyClass]])

slots.HtsFile_uri = Slot(uri=PFX.uri, name="HtsFile_uri", curie=PFX.curie('uri'),
                   model_uri=PFX.HtsFile_uri, domain=HtsFile, range=Optional[str])

slots.HtsFile_description = Slot(uri=PFX.description, name="HtsFile_description", curie=PFX.curie('description'),
                   model_uri=PFX.HtsFile_description, domain=HtsFile, range=Optional[str])

slots.HtsFile_hts_format = Slot(uri=PFX.hts_format, name="HtsFile_hts_format", curie=PFX.curie('hts_format'),
                   model_uri=PFX.HtsFile_hts_format, domain=HtsFile, range=Optional[Union[str, "HtsFormatOptions"]])

slots.HtsFile_genome_assembly = Slot(uri=PFX.genome_assembly, name="HtsFile_genome_assembly", curie=PFX.curie('genome_assembly'),
                   model_uri=PFX.HtsFile_genome_assembly, domain=HtsFile, range=Optional[str])

slots.HtsFile_individual_to_sample_identifiers = Slot(uri=PFX.individual_to_sample_identifiers, name="HtsFile_individual_to_sample_identifiers", curie=PFX.curie('individual_to_sample_identifiers'),
                   model_uri=PFX.HtsFile_individual_to_sample_identifiers, domain=HtsFile, range=Optional[str])

slots.Timestamp_seconds = Slot(uri=PFX.seconds, name="Timestamp_seconds", curie=PFX.curie('seconds'),
                   model_uri=PFX.Timestamp_seconds, domain=Timestamp, range=Optional[int])

slots.Timestamp_nanos = Slot(uri=PFX.nanos, name="Timestamp_nanos", curie=PFX.curie('nanos'),
                   model_uri=PFX.Timestamp_nanos, domain=Timestamp, range=Optional[int])

slots.ExternalReference_id = Slot(uri=PFX.id, name="ExternalReference_id", curie=PFX.curie('id'),
                   model_uri=PFX.ExternalReference_id, domain=ExternalReference, range=Optional[str])

slots.ExternalReference_description = Slot(uri=PFX.description, name="ExternalReference_description", curie=PFX.curie('description'),
                   model_uri=PFX.ExternalReference_description, domain=ExternalReference, range=Optional[str])

slots.Individual_id = Slot(uri=PFX.id, name="Individual_id", curie=PFX.curie('id'),
                   model_uri=PFX.Individual_id, domain=Individual, range=Optional[str])

slots.Individual_alternate_ids = Slot(uri=PFX.alternate_ids, name="Individual_alternate_ids", curie=PFX.curie('alternate_ids'),
                   model_uri=PFX.Individual_alternate_ids, domain=Individual, range=Optional[Union[str, List[str]]])

slots.Individual_date_of_birth = Slot(uri=PFX.date_of_birth, name="Individual_date_of_birth", curie=PFX.curie('date_of_birth'),
                   model_uri=PFX.Individual_date_of_birth, domain=Individual, range=Optional[Union[dict, Timestamp]])

slots.Individual_age_at_collection = Slot(uri=PFX.age_at_collection, name="Individual_age_at_collection", curie=PFX.curie('age_at_collection'),
                   model_uri=PFX.Individual_age_at_collection, domain=Individual, range=Optional[Union[dict, Age]])

slots.Individual_age_range_at_collection = Slot(uri=PFX.age_range_at_collection, name="Individual_age_range_at_collection", curie=PFX.curie('age_range_at_collection'),
                   model_uri=PFX.Individual_age_range_at_collection, domain=Individual, range=Optional[Union[dict, AgeRange]])

slots.Individual_sex = Slot(uri=PFX.sex, name="Individual_sex", curie=PFX.curie('sex'),
                   model_uri=PFX.Individual_sex, domain=Individual, range=Optional[Union[str, "SexOptions"]])

slots.Individual_karyotypic_sex = Slot(uri=PFX.karyotypic_sex, name="Individual_karyotypic_sex", curie=PFX.curie('karyotypic_sex'),
                   model_uri=PFX.Individual_karyotypic_sex, domain=Individual, range=Optional[Union[str, "KaryotypicSexOptions"]])

slots.Individual_taxonomy = Slot(uri=PFX.taxonomy, name="Individual_taxonomy", curie=PFX.curie('taxonomy'),
                   model_uri=PFX.Individual_taxonomy, domain=Individual, range=Optional[Union[dict, OntologyClass]])

slots.Procedure_code = Slot(uri=PFX.code, name="Procedure_code", curie=PFX.curie('code'),
                   model_uri=PFX.Procedure_code, domain=Procedure, range=Optional[Union[dict, OntologyClass]])

slots.Procedure_body_site = Slot(uri=PFX.body_site, name="Procedure_body_site", curie=PFX.curie('body_site'),
                   model_uri=PFX.Procedure_body_site, domain=Procedure, range=Optional[Union[dict, OntologyClass]])

slots.Biosample_id = Slot(uri=PFX.id, name="Biosample_id", curie=PFX.curie('id'),
                   model_uri=PFX.Biosample_id, domain=Biosample, range=Optional[str])

slots.Biosample_individual_id = Slot(uri=PFX.individual_id, name="Biosample_individual_id", curie=PFX.curie('individual_id'),
                   model_uri=PFX.Biosample_individual_id, domain=Biosample, range=Optional[str])

slots.Biosample_description = Slot(uri=PFX.description, name="Biosample_description", curie=PFX.curie('description'),
                   model_uri=PFX.Biosample_description, domain=Biosample, range=Optional[str])

slots.Biosample_sampled_tissue = Slot(uri=PFX.sampled_tissue, name="Biosample_sampled_tissue", curie=PFX.curie('sampled_tissue'),
                   model_uri=PFX.Biosample_sampled_tissue, domain=Biosample, range=Optional[Union[dict, OntologyClass]])

slots.Biosample_phenotypic_features = Slot(uri=PFX.phenotypic_features, name="Biosample_phenotypic_features", curie=PFX.curie('phenotypic_features'),
                   model_uri=PFX.Biosample_phenotypic_features, domain=Biosample, range=Optional[Union[Union[dict, PhenotypicFeature], List[Union[dict, PhenotypicFeature]]]])

slots.Biosample_taxonomy = Slot(uri=PFX.taxonomy, name="Biosample_taxonomy", curie=PFX.curie('taxonomy'),
                   model_uri=PFX.Biosample_taxonomy, domain=Biosample, range=Optional[Union[dict, OntologyClass]])

slots.Biosample_age_of_individual_at_collection = Slot(uri=PFX.age_of_individual_at_collection, name="Biosample_age_of_individual_at_collection", curie=PFX.curie('age_of_individual_at_collection'),
                   model_uri=PFX.Biosample_age_of_individual_at_collection, domain=Biosample, range=Optional[Union[dict, Age]])

slots.Biosample_age_range_of_individual_at_collection = Slot(uri=PFX.age_range_of_individual_at_collection, name="Biosample_age_range_of_individual_at_collection", curie=PFX.curie('age_range_of_individual_at_collection'),
                   model_uri=PFX.Biosample_age_range_of_individual_at_collection, domain=Biosample, range=Optional[Union[dict, AgeRange]])

slots.Biosample_histological_diagnosis = Slot(uri=PFX.histological_diagnosis, name="Biosample_histological_diagnosis", curie=PFX.curie('histological_diagnosis'),
                   model_uri=PFX.Biosample_histological_diagnosis, domain=Biosample, range=Optional[Union[dict, OntologyClass]])

slots.Biosample_tumor_progression = Slot(uri=PFX.tumor_progression, name="Biosample_tumor_progression", curie=PFX.curie('tumor_progression'),
                   model_uri=PFX.Biosample_tumor_progression, domain=Biosample, range=Optional[Union[dict, OntologyClass]])

slots.Biosample_tumor_grade = Slot(uri=PFX.tumor_grade, name="Biosample_tumor_grade", curie=PFX.curie('tumor_grade'),
                   model_uri=PFX.Biosample_tumor_grade, domain=Biosample, range=Optional[Union[dict, OntologyClass]])

slots.Biosample_diagnostic_markers = Slot(uri=PFX.diagnostic_markers, name="Biosample_diagnostic_markers", curie=PFX.curie('diagnostic_markers'),
                   model_uri=PFX.Biosample_diagnostic_markers, domain=Biosample, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.Biosample_procedure = Slot(uri=PFX.procedure, name="Biosample_procedure", curie=PFX.curie('procedure'),
                   model_uri=PFX.Biosample_procedure, domain=Biosample, range=Optional[Union[dict, Procedure]])

slots.Biosample_hts_files = Slot(uri=PFX.hts_files, name="Biosample_hts_files", curie=PFX.curie('hts_files'),
                   model_uri=PFX.Biosample_hts_files, domain=Biosample, range=Optional[Union[Union[dict, HtsFile], List[Union[dict, HtsFile]]]])

slots.Biosample_variants = Slot(uri=PFX.variants, name="Biosample_variants", curie=PFX.curie('variants'),
                   model_uri=PFX.Biosample_variants, domain=Biosample, range=Optional[Union[Union[dict, Variant], List[Union[dict, Variant]]]])

slots.Biosample_is_control_sample = Slot(uri=PFX.is_control_sample, name="Biosample_is_control_sample", curie=PFX.curie('is_control_sample'),
                   model_uri=PFX.Biosample_is_control_sample, domain=Biosample, range=Optional[Union[bool, Bool]])

slots.Gene_id = Slot(uri=PFX.id, name="Gene_id", curie=PFX.curie('id'),
                   model_uri=PFX.Gene_id, domain=Gene, range=Optional[str])

slots.Gene_alternate_ids = Slot(uri=PFX.alternate_ids, name="Gene_alternate_ids", curie=PFX.curie('alternate_ids'),
                   model_uri=PFX.Gene_alternate_ids, domain=Gene, range=Optional[Union[str, List[str]]])

slots.Gene_symbol = Slot(uri=PFX.symbol, name="Gene_symbol", curie=PFX.curie('symbol'),
                   model_uri=PFX.Gene_symbol, domain=Gene, range=Optional[str])

slots.Disease_term = Slot(uri=PFX.term, name="Disease_term", curie=PFX.curie('term'),
                   model_uri=PFX.Disease_term, domain=Disease, range=Optional[Union[dict, OntologyClass]])

slots.Disease_age_of_onset = Slot(uri=PFX.age_of_onset, name="Disease_age_of_onset", curie=PFX.curie('age_of_onset'),
                   model_uri=PFX.Disease_age_of_onset, domain=Disease, range=Optional[Union[dict, Age]])

slots.Disease_age_range_of_onset = Slot(uri=PFX.age_range_of_onset, name="Disease_age_range_of_onset", curie=PFX.curie('age_range_of_onset'),
                   model_uri=PFX.Disease_age_range_of_onset, domain=Disease, range=Optional[Union[dict, AgeRange]])

slots.Disease_class_of_onset = Slot(uri=PFX.class_of_onset, name="Disease_class_of_onset", curie=PFX.curie('class_of_onset'),
                   model_uri=PFX.Disease_class_of_onset, domain=Disease, range=Optional[Union[dict, OntologyClass]])

slots.Disease_disease_stage = Slot(uri=PFX.disease_stage, name="Disease_disease_stage", curie=PFX.curie('disease_stage'),
                   model_uri=PFX.Disease_disease_stage, domain=Disease, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.Disease_tnm_finding = Slot(uri=PFX.tnm_finding, name="Disease_tnm_finding", curie=PFX.curie('tnm_finding'),
                   model_uri=PFX.Disease_tnm_finding, domain=Disease, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.Phenopacket_id = Slot(uri=PFX.id, name="Phenopacket_id", curie=PFX.curie('id'),
                   model_uri=PFX.Phenopacket_id, domain=Phenopacket, range=Optional[str])

slots.Phenopacket_subject = Slot(uri=PFX.subject, name="Phenopacket_subject", curie=PFX.curie('subject'),
                   model_uri=PFX.Phenopacket_subject, domain=Phenopacket, range=Optional[Union[dict, Individual]])

slots.Phenopacket_phenotypic_features = Slot(uri=PFX.phenotypic_features, name="Phenopacket_phenotypic_features", curie=PFX.curie('phenotypic_features'),
                   model_uri=PFX.Phenopacket_phenotypic_features, domain=Phenopacket, range=Optional[Union[Union[dict, PhenotypicFeature], List[Union[dict, PhenotypicFeature]]]])

slots.Phenopacket_biosamples = Slot(uri=PFX.biosamples, name="Phenopacket_biosamples", curie=PFX.curie('biosamples'),
                   model_uri=PFX.Phenopacket_biosamples, domain=Phenopacket, range=Optional[Union[Union[dict, Biosample], List[Union[dict, Biosample]]]])

slots.Phenopacket_genes = Slot(uri=PFX.genes, name="Phenopacket_genes", curie=PFX.curie('genes'),
                   model_uri=PFX.Phenopacket_genes, domain=Phenopacket, range=Optional[Union[Union[dict, Gene], List[Union[dict, Gene]]]])

slots.Phenopacket_variants = Slot(uri=PFX.variants, name="Phenopacket_variants", curie=PFX.curie('variants'),
                   model_uri=PFX.Phenopacket_variants, domain=Phenopacket, range=Optional[Union[Union[dict, Variant], List[Union[dict, Variant]]]])

slots.Phenopacket_diseases = Slot(uri=PFX.diseases, name="Phenopacket_diseases", curie=PFX.curie('diseases'),
                   model_uri=PFX.Phenopacket_diseases, domain=Phenopacket, range=Optional[Union[Union[dict, Disease], List[Union[dict, Disease]]]])

slots.Phenopacket_hts_files = Slot(uri=PFX.hts_files, name="Phenopacket_hts_files", curie=PFX.curie('hts_files'),
                   model_uri=PFX.Phenopacket_hts_files, domain=Phenopacket, range=Optional[Union[Union[dict, HtsFile], List[Union[dict, HtsFile]]]])

slots.Phenopacket_meta_data = Slot(uri=PFX.meta_data, name="Phenopacket_meta_data", curie=PFX.curie('meta_data'),
                   model_uri=PFX.Phenopacket_meta_data, domain=Phenopacket, range=Optional[Union[dict, "MetaData"]])

slots.Resource_id = Slot(uri=PFX.id, name="Resource_id", curie=PFX.curie('id'),
                   model_uri=PFX.Resource_id, domain=Resource, range=Optional[str])

slots.Resource_name = Slot(uri=PFX.name, name="Resource_name", curie=PFX.curie('name'),
                   model_uri=PFX.Resource_name, domain=Resource, range=Optional[str])

slots.Resource_url = Slot(uri=PFX.url, name="Resource_url", curie=PFX.curie('url'),
                   model_uri=PFX.Resource_url, domain=Resource, range=Optional[str])

slots.Resource_version = Slot(uri=PFX.version, name="Resource_version", curie=PFX.curie('version'),
                   model_uri=PFX.Resource_version, domain=Resource, range=Optional[str])

slots.Resource_namespace_prefix = Slot(uri=PFX.namespace_prefix, name="Resource_namespace_prefix", curie=PFX.curie('namespace_prefix'),
                   model_uri=PFX.Resource_namespace_prefix, domain=Resource, range=Optional[str])

slots.Resource_iri_prefix = Slot(uri=PFX.iri_prefix, name="Resource_iri_prefix", curie=PFX.curie('iri_prefix'),
                   model_uri=PFX.Resource_iri_prefix, domain=Resource, range=Optional[str])

slots.Update_timestamp = Slot(uri=PFX.timestamp, name="Update_timestamp", curie=PFX.curie('timestamp'),
                   model_uri=PFX.Update_timestamp, domain=Update, range=Optional[Union[dict, Timestamp]])

slots.Update_updated_by = Slot(uri=PFX.updated_by, name="Update_updated_by", curie=PFX.curie('updated_by'),
                   model_uri=PFX.Update_updated_by, domain=Update, range=Optional[str])

slots.Update_comment = Slot(uri=PFX.comment, name="Update_comment", curie=PFX.curie('comment'),
                   model_uri=PFX.Update_comment, domain=Update, range=Optional[str])

slots.MetaData_created = Slot(uri=PFX.created, name="MetaData_created", curie=PFX.curie('created'),
                   model_uri=PFX.MetaData_created, domain=MetaData, range=Optional[Union[dict, Timestamp]])

slots.MetaData_created_by = Slot(uri=PFX.created_by, name="MetaData_created_by", curie=PFX.curie('created_by'),
                   model_uri=PFX.MetaData_created_by, domain=MetaData, range=Optional[str])

slots.MetaData_submitted_by = Slot(uri=PFX.submitted_by, name="MetaData_submitted_by", curie=PFX.curie('submitted_by'),
                   model_uri=PFX.MetaData_submitted_by, domain=MetaData, range=Optional[str])

slots.MetaData_resources = Slot(uri=PFX.resources, name="MetaData_resources", curie=PFX.curie('resources'),
                   model_uri=PFX.MetaData_resources, domain=MetaData, range=Optional[Union[Union[dict, Resource], List[Union[dict, Resource]]]])

slots.MetaData_updates = Slot(uri=PFX.updates, name="MetaData_updates", curie=PFX.curie('updates'),
                   model_uri=PFX.MetaData_updates, domain=MetaData, range=Optional[Union[Union[dict, Update], List[Union[dict, Update]]]])

slots.MetaData_phenopacket_schema_version = Slot(uri=PFX.phenopacket_schema_version, name="MetaData_phenopacket_schema_version", curie=PFX.curie('phenopacket_schema_version'),
                   model_uri=PFX.MetaData_phenopacket_schema_version, domain=MetaData, range=Optional[str])

slots.MetaData_external_references = Slot(uri=PFX.external_references, name="MetaData_external_references", curie=PFX.curie('external_references'),
                   model_uri=PFX.MetaData_external_references, domain=MetaData, range=Optional[Union[Union[dict, ExternalReference], List[Union[dict, ExternalReference]]]])

slots.Person_family_id = Slot(uri=PFX.family_id, name="Person_family_id", curie=PFX.curie('family_id'),
                   model_uri=PFX.Person_family_id, domain=Person, range=Optional[str])

slots.Person_individual_id = Slot(uri=PFX.individual_id, name="Person_individual_id", curie=PFX.curie('individual_id'),
                   model_uri=PFX.Person_individual_id, domain=Person, range=Optional[str])

slots.Person_paternal_id = Slot(uri=PFX.paternal_id, name="Person_paternal_id", curie=PFX.curie('paternal_id'),
                   model_uri=PFX.Person_paternal_id, domain=Person, range=Optional[str])

slots.Person_maternal_id = Slot(uri=PFX.maternal_id, name="Person_maternal_id", curie=PFX.curie('maternal_id'),
                   model_uri=PFX.Person_maternal_id, domain=Person, range=Optional[str])

slots.Person_sex = Slot(uri=PFX.sex, name="Person_sex", curie=PFX.curie('sex'),
                   model_uri=PFX.Person_sex, domain=Person, range=Optional[Union[str, "SexOptions"]])

slots.Person_affected_status = Slot(uri=PFX.affected_status, name="Person_affected_status", curie=PFX.curie('affected_status'),
                   model_uri=PFX.Person_affected_status, domain=Person, range=Optional[Union[str, "AffectedStatusOptions"]])

slots.Pedigree_persons = Slot(uri=PFX.persons, name="Pedigree_persons", curie=PFX.curie('persons'),
                   model_uri=PFX.Pedigree_persons, domain=Pedigree, range=Optional[Union[Union[dict, Person], List[Union[dict, Person]]]])

slots.Family_id = Slot(uri=PFX.id, name="Family_id", curie=PFX.curie('id'),
                   model_uri=PFX.Family_id, domain=Family, range=Optional[str])

slots.Family_proband = Slot(uri=PFX.proband, name="Family_proband", curie=PFX.curie('proband'),
                   model_uri=PFX.Family_proband, domain=Family, range=Optional[Union[dict, Phenopacket]])

slots.Family_relatives = Slot(uri=PFX.relatives, name="Family_relatives", curie=PFX.curie('relatives'),
                   model_uri=PFX.Family_relatives, domain=Family, range=Optional[Union[Union[dict, Phenopacket], List[Union[dict, Phenopacket]]]])

slots.Family_pedigree = Slot(uri=PFX.pedigree, name="Family_pedigree", curie=PFX.curie('pedigree'),
                   model_uri=PFX.Family_pedigree, domain=Family, range=Optional[Union[dict, Pedigree]])

slots.Family_hts_files = Slot(uri=PFX.hts_files, name="Family_hts_files", curie=PFX.curie('hts_files'),
                   model_uri=PFX.Family_hts_files, domain=Family, range=Optional[Union[Union[dict, HtsFile], List[Union[dict, HtsFile]]]])

slots.Family_meta_data = Slot(uri=PFX.meta_data, name="Family_meta_data", curie=PFX.curie('meta_data'),
                   model_uri=PFX.Family_meta_data, domain=Family, range=Optional[Union[dict, MetaData]])

slots.Cohort_id = Slot(uri=PFX.id, name="Cohort_id", curie=PFX.curie('id'),
                   model_uri=PFX.Cohort_id, domain=Cohort, range=Optional[str])

slots.Cohort_description = Slot(uri=PFX.description, name="Cohort_description", curie=PFX.curie('description'),
                   model_uri=PFX.Cohort_description, domain=Cohort, range=Optional[str])

slots.Cohort_members = Slot(uri=PFX.members, name="Cohort_members", curie=PFX.curie('members'),
                   model_uri=PFX.Cohort_members, domain=Cohort, range=Optional[Union[Union[dict, Phenopacket], List[Union[dict, Phenopacket]]]])

slots.Cohort_hts_files = Slot(uri=PFX.hts_files, name="Cohort_hts_files", curie=PFX.curie('hts_files'),
                   model_uri=PFX.Cohort_hts_files, domain=Cohort, range=Optional[Union[Union[dict, HtsFile], List[Union[dict, HtsFile]]]])

slots.Cohort_meta_data = Slot(uri=PFX.meta_data, name="Cohort_meta_data", curie=PFX.curie('meta_data'),
                   model_uri=PFX.Cohort_meta_data, domain=Cohort, range=Optional[Union[dict, MetaData]])
