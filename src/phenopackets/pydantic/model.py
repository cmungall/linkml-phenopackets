from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.12.0"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'phenopackets',
     'description': 'Automatic translation of phenopackets protobuf to LinkML.',
     'id': 'https://w3id.org/linkml/phenopackets/phenopackets',
     'imports': ['linkml:types',
                 'cv_terms',
                 'base',
                 'biosample',
                 'disease',
                 'interpretation',
                 'individual',
                 'measurement',
                 'medical_action',
                 'meta_data',
                 'pedigree',
                 'phenotypic_feature'],
     'name': 'phenopackets',
     'prefixes': {'GENO': {'prefix_prefix': 'GENO',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/GENO_'},
                  'HP': {'prefix_prefix': 'HP',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/HP_'},
                  'LOINC': {'prefix_prefix': 'LOINC',
                            'prefix_reference': 'https://loinc.org/'},
                  'MONDO': {'prefix_prefix': 'MONDO',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/MONDO_'},
                  'NCIT': {'prefix_prefix': 'NCIT',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/NCIT_'},
                  'UBERON': {'prefix_prefix': 'UBERON',
                             'prefix_reference': 'http://purl.obolibrary.org/obo/UBERON_'},
                  'UCUM': {'prefix_prefix': 'UCUM',
                           'prefix_reference': 'http://unitsofmeasure.org/'},
                  'UO': {'prefix_prefix': 'UO',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/UO_'},
                  'argo': {'prefix_prefix': 'argo',
                           'prefix_reference': 'https://docs.icgc-argo.org/dictionary/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'phenopackets': {'prefix_prefix': 'phenopackets',
                                   'prefix_reference': 'https://w3id.org/linkml/phenopackets/phenopackets/'}},
     'source': 'https://github.com/phenopackets/phenopacket-schema/blob/2.0.0/src/main/proto/phenopackets/schema/v2/phenopackets.proto',
     'source_file': 'src/phenopackets/schema/phenopackets.yaml'} )

class AllelicStateTerms(str, Enum):
    HETEROZYGOUS = "HETEROZYGOUS"
    """
    heterozygous
    """
    HOMOZYGOUS = "HOMOZYGOUS"
    """
    homozygous
    """
    HEMIZYGOUS = "HEMIZYGOUS"
    """
    hemizygous
    """


class AssaysTerms(str, Enum):
    CREATINE_KINASE = "CREATINE_KINASE"
    """
    Creatine kinase [Enzymatic activity/volume] in Serum or Plasma
    """


class GenderTerms(str, Enum):
    IDENTIFIES_AS_MALE = "IDENTIFIES_AS_MALE"
    """
    Identifies as male
    """
    IDENTIFIES_AS_FEMALE = "IDENTIFIES_AS_FEMALE"
    """
    Identifies as female
    """
    FEMALE_TO_MALE_TRANSSEXUAL = "FEMALE_TO_MALE_TRANSSEXUAL"
    """
    Female-to-male transsexual
    """
    MALE_TO_FEMALE_TRANSSEXUAL = "MALE_TO_FEMALE_TRANSSEXUAL"
    """
    Male-to-female transsexual
    """
    IDENTIFIES_AS_NON_CONFORMING = "IDENTIFIES_AS_NON_CONFORMING"
    """
    Identifies as non-conforming
    """
    OTHER_GENDER = "OTHER_GENDER"
    """
    other
    """
    ASKED_BUT_UNKNOWN = "ASKED_BUT_UNKNOWN"
    """
    Asked but unknown
    """


class LateralityTerms(str, Enum):
    RIGHT = "RIGHT"
    """
    Right
    """
    LEFT = "LEFT"
    """
    Left
    """
    UNILATERAL = "UNILATERAL"
    """
    Unilateral
    """
    BILATERAL = "BILATERAL"
    """
    Bilateral
    """


class MedicalActionsTerms(str, Enum):
    ADVERSE_EVENT = "ADVERSE_EVENT"
    """
    Adverse Event
    """
    FOUR_TIMES_DAILY = "FOUR_TIMES_DAILY"
    """
    Four Times Daily
    """
    INTRA_ARTERIAL = "INTRA_ARTERIAL"
    """
    Intraarterial Route of Administration
    """
    IV_ADMINISTRATION = "IV_ADMINISTRATION"
    """
    Intravenous Route of Administration
    """
    ORAL_ADMINISTRATION = "ORAL_ADMINISTRATION"
    """
    Oral Route of Administration
    """
    ONCE = "ONCE"
    """
    Once
    """
    ONCE_DAILY = "ONCE_DAILY"
    """
    Once Daily
    """
    THREE_TIMES_DAILY = "THREE_TIMES_DAILY"
    """
    Three Times Daily
    """
    TWICE_DAILY = "TWICE_DAILY"
    """
    Twice Daily
    """


class OnsetTerms(str, Enum):
    ANTENATAL_ONSET = "ANTENATAL_ONSET"
    """
    Antenatal onset
    """
    EMBRYONAL_ONSET = "EMBRYONAL_ONSET"
    """
    Embryonal onset
    """
    FETAL_ONSET = "FETAL_ONSET"
    """
    Fetal onset
    """
    LATE_FIRST_TRIMESTER_ONSET = "LATE_FIRST_TRIMESTER_ONSET"
    """
    Late first trimester onset
    """
    SECOND_TRIMESTER_ONSET = "SECOND_TRIMESTER_ONSET"
    """
    Second trimester onset
    """
    THIRD_TRIMESTER_ONSET = "THIRD_TRIMESTER_ONSET"
    """
    Third trimester onset
    """
    CONGENITAL_ONSET = "CONGENITAL_ONSET"
    """
    Congenital onset
    """
    NEONATAL_ONSET = "NEONATAL_ONSET"
    """
    Neonatal onset
    """
    INFANTILE_ONSET = "INFANTILE_ONSET"
    """
    Infantile onset
    """
    CHILDHOOD_ONSET = "CHILDHOOD_ONSET"
    """
    Childhood onset
    """
    JUVENILE_ONSET = "JUVENILE_ONSET"
    """
    Juvenile onset
    """
    ADULT_ONSET = "ADULT_ONSET"
    """
    Adult onset
    """
    YOUNG_ADULT_ONSET = "YOUNG_ADULT_ONSET"
    """
    Young adult onset
    """
    EARLY_YOUNG_ADULT_ONSET = "EARLY_YOUNG_ADULT_ONSET"
    """
    Early young adult onset
    """
    INTERMEDIATE_YOUNG_ADULT_ONSET = "INTERMEDIATE_YOUNG_ADULT_ONSET"
    """
    Intermediate young adult onset
    """
    LATE_YOUNG_ADULT_ONSET = "LATE_YOUNG_ADULT_ONSET"
    """
    Late young adult onset
    """
    MIDDLE_AGE_ONSET = "MIDDLE_AGE_ONSET"
    """
    Middle age onset
    """
    LATE_ONSET = "LATE_ONSET"
    """
    Late onset
    """


class OrganTerms(str, Enum):
    BRAIN = "BRAIN"
    """
    brain
    """
    CEREBELLUM = "CEREBELLUM"
    """
    cerebellum
    """
    EAR = "EAR"
    """
    ear
    """
    EYE = "EYE"
    """
    eye
    """
    HEART = "HEART"
    """
    heart
    """
    KIDNEY = "KIDNEY"
    """
    kidney
    """
    LARGE_INTESTINE = "LARGE_INTESTINE"
    """
    large intestine
    """
    LIVER = "LIVER"
    """
    liver
    """
    LUNG = "LUNG"
    """
    lung
    """
    NOSE = "NOSE"
    """
    nose
    """
    SMALL_INTESTINE = "SMALL_INTESTINE"
    """
    small intestine
    """
    SPINAL_CORD = "SPINAL_CORD"
    """
    spinal cord
    """
    SPLEEN = "SPLEEN"
    """
    spleen
    """
    TONGUE = "TONGUE"
    """
    tongue
    """
    THYMUS = "THYMUS"
    """
    thymus
    """


class ResponseTerms(str, Enum):
    FAVORABLE = "FAVORABLE"
    """
    Favorable
    """
    UNFAVORABLE = "UNFAVORABLE"
    """
    Unfavorable
    """


class SpatialPatternTerms(str, Enum):
    PREDOMINANT_SMALL_JOINT_LOCALIZATION = "PREDOMINANT_SMALL_JOINT_LOCALIZATION"
    """
    Predominant small joint localization
    """
    POLYCYCLIC = "POLYCYCLIC"
    """
    Polycyclic
    """
    AXIAL = "AXIAL"
    """
    Axial
    """
    PERILOBULAR = "PERILOBULAR"
    """
    Perilobular
    """
    PARASEPTAL = "PARASEPTAL"
    """
    Paraseptal
    """
    BRONCHOCENTRIC = "BRONCHOCENTRIC"
    """
    Bronchocentric
    """
    CENTRILOBULAR = "CENTRILOBULAR"
    """
    Centrilobular
    """
    MILIARY = "MILIARY"
    """
    Miliary
    """
    GENERALIZED = "GENERALIZED"
    """
    Generalized
    """
    PERILYMPHATIC = "PERILYMPHATIC"
    """
    Perilymphatic
    """
    LOCALIZED = "LOCALIZED"
    """
    Localized
    """
    RETICULAR = "RETICULAR"
    """
    Reticular
    """
    DISTAL = "DISTAL"
    """
    Distal
    """
    CENTRAL = "CENTRAL"
    """
    Central
    """
    UPPER_BODY_PREDOMINANCE = "UPPER_BODY_PREDOMINANCE"
    """
    Upper-body predominance
    """
    JOINT_EXTENSOR_SURFACE_LOCALIZATION = "JOINT_EXTENSOR_SURFACE_LOCALIZATION"
    """
    Joint extensor surface localization
    """
    HERPETIFORM = "HERPETIFORM"
    """
    Herpetiform
    """
    MORBILLIFORM = "MORBILLIFORM"
    """
    Morbilliform
    """
    PERICENTRAL = "PERICENTRAL"
    """
    Pericentral
    """
    DERMATOMAL = "DERMATOMAL"
    """
    Dermatomal
    """
    MIDPERIPHERAL = "MIDPERIPHERAL"
    """
    Midperipheral
    """
    DISTRIBUTED_ALONG_BLASCHKO_LINES = "DISTRIBUTED_ALONG_BLASCHKO_LINES"
    """
    Distributed along Blaschko lines
    """
    ACRAL = "ACRAL"
    """
    Acral
    """
    PARACENTRAL = "PARACENTRAL"
    """
    Paracentral
    """
    LATERAL = "LATERAL"
    """
    Lateral
    """
    PERIPHERAL = "PERIPHERAL"
    """
    Peripheral
    """
    LOWER_BODY_PREDOMINANCE = "LOWER_BODY_PREDOMINANCE"
    """
    Lower-body predominance
    """
    DIFFUSE = "DIFFUSE"
    """
    Diffuse
    """
    PROXIMAL = "PROXIMAL"
    """
    Proximal
    """
    APICAL = "APICAL"
    """
    Apical
    """
    FOCAL = "FOCAL"
    """
    Focal
    """
    MULTIFOCAL = "MULTIFOCAL"
    """
    Multifocal
    """
    JOINT_FLEXOR_SURFACE_LOCALIZATION = "JOINT_FLEXOR_SURFACE_LOCALIZATION"
    """
    Jointflexorsurfacelocalization
    """


class UnitTerms(str, Enum):
    DEGREE = "DEGREE"
    """
    degree (plane angle)
    """
    DIOPTER = "DIOPTER"
    """
    diopter
    """
    GRAM = "GRAM"
    """
    gram
    """
    GRAM_PER_KG = "GRAM_PER_KG"
    """
    gram per kilogram
    """
    KILIGRAM = "KILIGRAM"
    """
    kiligram
    """
    LITER = "LITER"
    """
    liter
    """
    METER = "METER"
    """
    meter
    """
    MICROGRAM = "MICROGRAM"
    """
    microgram
    """
    MICROGRAM_PER_DECILITER = "MICROGRAM_PER_DECILITER"
    """
    microgram per deciliter
    """
    MICROGRAM_PER_LITER = "MICROGRAM_PER_LITER"
    """
    microgram per liter
    """
    MICROLITER = "MICROLITER"
    """
    microliter
    """
    MICROMETER = "MICROMETER"
    """
    micrometer
    """
    MILLIGRAM = "MILLIGRAM"
    """
    milligram
    """
    MILLIGRAM_PER_DAY = "MILLIGRAM_PER_DAY"
    """
    milligram per day
    """
    MILLIGRAM_PER_DL = "MILLIGRAM_PER_DL"
    """
    milligram per deciliter
    """
    MILLIGRAM_PER_KG = "MILLIGRAM_PER_KG"
    """
    milligram per kilogram
    """
    MILLILITER = "MILLILITER"
    """
    milliliter
    """
    MILLIMETER = "MILLIMETER"
    """
    millimeter
    """
    MILLIMETRES_OF_MERCURY = "MILLIMETRES_OF_MERCURY"
    """
    millimetres of mercury
    """
    MILLIMOLE = "MILLIMOLE"
    """
    millimole
    """
    MOLE = "MOLE"
    """
    mole
    """
    MOLE_PER_LITER = "MOLE_PER_LITER"
    """
    mole per liter
    """
    MOLE_PER_MILLILITER = "MOLE_PER_MILLILITER"
    """
    mole per milliliter
    """
    ENZYME_UNIT_PER_LITER = "ENZYME_UNIT_PER_LITER"
    """
    enzyme unit per liter
    """


class MondoDiseaseTerms(str):
    """
    Mondo Disease Ontology provides a comprehensive logically structured ontology of diseases that integrates multiple other disease ontologies.
    """
    pass


class NCITDiseaseTerms(str):
    """
    All disease terms from the NCI Thesaurus
    """
    pass


class NCITNeoplasmTerms(str):
    """
    All neoplasm terms from the NCI Thesaurus
    """
    pass


class HPOAbnormalityTerms(str):
    """
    The Human Phenotype Ontology (HPO) provides a comprehensive logical standard to describe and computationally analyze phenotypic abnormalities found in human disease.
    """
    pass


class UberonAnatomicalEntityTerms(str):
    """
    UBERON is an integrated cross-species ontology with classes representing a variety of anatomical entities.
    """
    pass


class HGNCGeneTerms(str):
    """
    The HUGO Gene Nomenclature Committee (HGNC) provides standard names, symbols, and IDs for human genes.
    """
    pass


class UOUnitTerms(str):
    """
    The Units of measurement ontology (denoted UO) provides terms for units commonly encountered in medical data. The following table shows some typical examples.
    """
    pass


class GENOZygosityTerms(str):
    """
    GENO is an ontology of genotypes their more fundamental sequence components. This enum refers to the zygosity subset of GENO
    """
    pass


class LOINCMeasurementTerms(str):
    """
    Logical Observation Identifiers Names and Codes (LOINC) is a database and universal standard for identifying medical laboratory observations. It can be used to denote clinical assays in the Measurement element.    examples:
    """
    pass


class MoleculeContext(str, Enum):
    unspecified_molecule_context = "unspecified_molecule_context"
    genomic = "genomic"
    transcript = "transcript"
    protein = "protein"


class AcmgPathogenicityClassification(str, Enum):
    NOT_PROVIDED = "NOT_PROVIDED"
    BENIGN = "BENIGN"
    LIKELY_BENIGN = "LIKELY_BENIGN"
    UNCERTAIN_SIGNIFICANCE = "UNCERTAIN_SIGNIFICANCE"
    LIKELY_PATHOGENIC = "LIKELY_PATHOGENIC"
    PATHOGENIC = "PATHOGENIC"


class InterpretationStatus(str, Enum):
    UNKNOWN_STATUS = "UNKNOWN_STATUS"
    REJECTED = "REJECTED"
    CANDIDATE = "CANDIDATE"
    CONTRIBUTORY = "CONTRIBUTORY"
    CAUSATIVE = "CAUSATIVE"


class ProgressStatus(str, Enum):
    UNKNOWN_PROGRESS = "UNKNOWN_PROGRESS"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    SOLVED = "SOLVED"
    UNSOLVED = "UNSOLVED"


class TherapeuticActionability(str, Enum):
    UNKNOWN_ACTIONABILITY = "UNKNOWN_ACTIONABILITY"
    NOT_ACTIONABLE = "NOT_ACTIONABLE"
    ACTIONABLE = "ACTIONABLE"


class KaryotypicSex(str, Enum):
    """
    Karyotypic sex of the individual
    """
    UNKNOWN_KARYOTYPE = "UNKNOWN_KARYOTYPE"
    XX = "XX"
    XY = "XY"
    XO = "XO"
    XXY = "XXY"
    XXX = "XXX"
    XXYY = "XXYY"
    XXXY = "XXXY"
    XXXX = "XXXX"
    XYY = "XYY"
    OTHER_KARYOTYPE = "OTHER_KARYOTYPE"


class Sex(str, Enum):
    """
    Sex of an individual FHIR mapping: AdministrativeGender (https://www.hl7.org/fhir/codesystem-administrative-gender.html)
    """
    UNKNOWN_SEX = "UNKNOWN_SEX"
    """
    Not assessed / available.
    """
    FEMALE = "FEMALE"
    """
    Female
    """
    MALE = "MALE"
    """
    Male
    """
    OTHER_SEX = "OTHER_SEX"
    """
    It is not possible, to accurately assess the applicability of MALE/FEMALE.
    """


class Status(str, Enum):
    """
    Default = false i.e. the individual is alive. MUST be true if
    """
    UNKNOWN_STATUS = "UNKNOWN_STATUS"
    ALIVE = "ALIVE"
    DECEASED = "DECEASED"


class DrugType(str, Enum):
    """
    A simplified version of ODHSI-DRUG_EXPOSURE
    """
    UNKNOWN_DRUG_TYPE = "UNKNOWN_DRUG_TYPE"
    PRESCRIPTION = "PRESCRIPTION"
    EHR_MEDICATION_LIST = "EHR_MEDICATION_LIST"
    ADMINISTRATION_RELATED_TO_PROCEDURE = "ADMINISTRATION_RELATED_TO_PROCEDURE"


class RegimenStatus(str, Enum):
    UNKNOWN_STATUS = "UNKNOWN_STATUS"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    DISCONTINUED = "DISCONTINUED"


class AffectedStatus(str, Enum):
    MISSING = "MISSING"
    UNAFFECTED = "UNAFFECTED"
    AFFECTED = "AFFECTED"



class Age(ConfiguredBaseModel):
    """
    See http://build.fhir.org/datatypes and http://build.fhir.org/condition-definitions.html#Condition.onset_x_ In FHIR this is represented as a UCUM measurement - http://unitsofmeasure.org/trac/
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base'})

    iso8601duration: Optional[str] = Field(default=None, description="""The :ref:`ISO 8601<metadata_date_time>` age of this object as ISO8601 duration or time intervals. e.g. P40Y10M05D)""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}}, 'domain_of': ['Age']} })


class AgeRange(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base'})

    end: Optional[Age] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['AgeRange',
                       'TimeInterval',
                       'CytobandInterval',
                       'SimpleInterval']} })
    start: Optional[Age] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['AgeRange',
                       'TimeInterval',
                       'CytobandInterval',
                       'SimpleInterval']} })


class DictionaryEntry(ConfiguredBaseModel):
    """
    An entry of a protobuf map<string, string> field. An attribute that holds a map is multivalued and inlined as a dictionary of its entries, which can be written as {key: value, ...}
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base'})

    key: str = Field(default=..., description="""The key of the map entry. Keys are unique within a map.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['DictionaryEntry']} })
    value: Optional[str] = Field(default=None, description="""The value of the map entry.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['DictionaryEntry',
                       'Measurement',
                       'Quantity',
                       'Any',
                       'IndefiniteRange',
                       'Number',
                       'Expression',
                       'Extension']} })


class Evidence(ConfiguredBaseModel):
    """
    FHIR mapping: Condition.evidence (https://www.hl7.org/fhir/condition-definitions.html#Condition.evidence)
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base'})

    evidenceCode: Optional[OntologyClass] = Field(default=None, description="""The encoded evidence type using, for example the Evidence & Conclusion Ontology (ECO - http://purl.obolibrary.org/obo/eco.owl) FHIR mapping: Condition.evidence.code""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Evidence']} })
    reference: Optional[ExternalReference] = Field(default=None, description="""FHIR mapping: Condition.evidence.detail""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Evidence', 'ExternalReference']} })


class ExternalReference(ConfiguredBaseModel):
    """
    FHIR mapping: Reference (https://www.hl7.org/fhir/references.html)
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base'})

    description: Optional[str] = Field(default=None, description="""Human readable title or display string for the reference FHIR mapping: Reference.display""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['ExternalReference',
                       'Measurement',
                       'PhenotypicFeature',
                       'Biosample',
                       'GeneDescriptor',
                       'VariationDescriptor',
                       'Cohort']} })
    id: Optional[str] = Field(default=None, description="""e.g. ISBN, PMID:123456, DOI:..., FHIR mapping: Reference.identifier""", json_schema_extra = { "linkml_meta": {'annotations': {'percent_encoded': {'tag': 'percent_encoded', 'value': True},
                         'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket']} })
    reference: Optional[str] = Field(default=None, description="""A full or partial URL pointing to the external reference if no commonly resolvable identifier can be used in the `id` field FHIR mapping Reference.reference""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Evidence', 'ExternalReference']} })


class File(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base'})

    fileAttributes: Optional[dict[str, Union[str, DictionaryEntry]]] = Field(default=None, description="""Map of attributes describing the file. For example the File format or genome assembly would be defied here. For genomic data files there MUST be a 'genomeAssembly' key.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}}, 'domain_of': ['File']} })
    individualToFileIdentifiers: Optional[dict[str, Union[str, DictionaryEntry]]] = Field(default=None, description="""A map of identifiers mapping an individual to a sample in the file. The key values must correspond to the Individual::id for the individuals in the message, the values must map to the samples in the file.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}}, 'domain_of': ['File']} })
    uri: Optional[str] = Field(default=None, description="""URI for the file e.g. file://data/genomes/file1.vcf.gz or https://opensnp.org/data/60.23andme-exome-vcf.231?1341012444""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}}, 'domain_of': ['File']} })


class GestationalAge(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base'})

    days: Optional[int] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['GestationalAge']} })
    weeks: Optional[int] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['GestationalAge']} })


class OntologyClass(ConfiguredBaseModel):
    """
    A class (aka term, concept) in an ontology. FHIR mapping: CodeableConcept (http://www.hl7.org/fhir/datatypes.html#CodeableConcept) see also Coding (http://www.hl7.org/fhir/datatypes.html#Coding)
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base'})

    id: str = Field(default=..., description="""a CURIE-style identifier e.g. HP:0100024, MP:0001284, UBERON:0001690. This is the primary key for the ontology class REQUIRED!""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket']} })
    label: Optional[str] = Field(default=None, description="""class label, aka name. E.g. \"Abnormality of cardiovascular system\"""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['OntologyClass', 'VariationDescriptor']} })


class Procedure(ConfiguredBaseModel):
    """
    A clinical procedure performed on a subject. By preference a single concept to indicate both the procedure and the body site should be used. In cases where this is not possible, the body site should be indicated using a separate ontology class. e.g. {\"code\":{\"NCIT:C51585\": \"Biopsy of Soft Palate\"}} {\"code\":{\"NCIT:C28743\": \"Punch Biopsy\"}, \"body_site\":{\"UBERON:0003403\": \"skin of forearm\"}} - a punch biopsy of the skin from the forearm FHIR mapping: Procedure (https://www.hl7.org/fhir/procedure.html)
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base'})

    bodySite: Optional[OntologyClass] = Field(default=None, description="""FHIR mapping: Procedure.bodySite""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Procedure', 'RadiationTherapy']} })
    code: Optional[OntologyClass] = Field(default=None, description="""FHIR mapping: Procedure.code""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Procedure']} })
    performed: Optional[TimeElement] = Field(default=None, description="""When the procedure was performed.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Procedure']} })


class TimeElement(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'element'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'gestationalAge': {'name': 'gestationalAge',
                                                                                                  'required': True}}},
                                                          {'slot_conditions': {'age': {'name': 'age',
                                                                                       'required': True}}},
                                                          {'slot_conditions': {'ageRange': {'name': 'ageRange',
                                                                                            'required': True}}},
                                                          {'slot_conditions': {'ontologyClass': {'name': 'ontologyClass',
                                                                                                 'required': True}}},
                                                          {'slot_conditions': {'timestamp': {'name': 'timestamp',
                                                                                             'required': True}}},
                                                          {'slot_conditions': {'interval': {'name': 'interval',
                                                                                            'required': True}}}]}}]})

    age: Optional[Age] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['TimeElement']} })
    ageRange: Optional[AgeRange] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['TimeElement']} })
    gestationalAge: Optional[GestationalAge] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['TimeElement']} })
    interval: Optional[TimeInterval] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['TimeElement', 'ChromosomeLocation', 'DoseInterval']} })
    ontologyClass: Optional[OntologyClass] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['TimeElement', 'Value', 'TherapeuticRegimen']} })
    timestamp: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['TimeElement', 'Update']} })


class TimeInterval(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/base'})

    end: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['AgeRange',
                       'TimeInterval',
                       'CytobandInterval',
                       'SimpleInterval']} })
    start: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['AgeRange',
                       'TimeInterval',
                       'CytobandInterval',
                       'SimpleInterval']} })


class ComplexValue(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/measurement'})

    typedQuantities: Optional[list[TypedQuantity]] = Field(default=None, description="""The quantities required to fully describe the complex value. For example the systolic and diastolic blood pressure quantities""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ComplexValue']} })


class Measurement(ConfiguredBaseModel):
    """
    FHIR mapping: Observation (https://www.hl7.org/fhir/observation.html)
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/measurement',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof',
                                              'value': 'measurement_value'}},
                    'comments': ['https://github.com/phenopackets/phenopacket-schema/issues/261 '
                                 'e.g. type: Increased circulating antibody level '
                                 '(HP:0010702) quantity: unit: Microgram per '
                                 'Milliliter (NCIT:C64572), value: 23456.0',
                                 'type:  body temperature (CMO:0000015) quantity: '
                                 'unit: Degrees Celsius (UO:0000027), value: 37.5 '
                                 'Degree Celsius (NCIT:C42559), value: 37.5'],
                    'description': 'type:  LOINC: 26515-7 Platelets [#/volume] in '
                                   'Blood value: quantity: unit: NCIT:C173275 (Count '
                                   'per Cubic Millimeter), value: 600,000',
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'value': {'name': 'value',
                                                                                         'required': True}}},
                                                          {'slot_conditions': {'complexValue': {'name': 'complexValue',
                                                                                                'required': True}}}]}}]})

    assay: Optional[OntologyClass] = Field(default=None, description="""An ontology class which describes the assay used to produce the measurement. For example \"body temperature\" (CMO:0000015) or \"Platelets [#/volume] in Blood\" (LOINC:26515-7) FHIR mapping: Observation.code""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Measurement']} })
    complexValue: Optional[ComplexValue] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['Measurement']} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the feature. Note this is not a acceptable place to document/describe the phenotype - the type and onset etc... fields should be used for this purpose.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'Measurement',
                       'PhenotypicFeature',
                       'Biosample',
                       'GeneDescriptor',
                       'VariationDescriptor',
                       'Cohort']} })
    procedure: Optional[Procedure] = Field(default=None, description="""Clinical procedure performed on the subject in order to produce the measurement.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['Measurement', 'Biosample', 'MedicalAction']} })
    timeObserved: Optional[TimeElement] = Field(default=None, description="""The time at which the measurement was made""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Measurement']} })
    value: Optional[Value] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['DictionaryEntry',
                       'Measurement',
                       'Quantity',
                       'Any',
                       'IndefiniteRange',
                       'Number',
                       'Expression',
                       'Extension']} })


class Quantity(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/measurement'})

    referenceRange: Optional[ReferenceRange] = Field(default=None, description="""Reference range for the quantity e.g. The normal range of platelets is 150,000 to 450,000 platelets/uL.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Quantity']} })
    unit: Optional[OntologyClass] = Field(default=None, description="""For instance, NCIT subhierarchy, Unit of Measure (Code C25709), https://www.ebi.ac.uk/ols/ontologies/uo""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Quantity', 'ReferenceRange']} })
    value: Optional[float] = Field(default=None, description="""the  value of the quantity in the units  e.g. 2.0 mg""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['DictionaryEntry',
                       'Measurement',
                       'Quantity',
                       'Any',
                       'IndefiniteRange',
                       'Number',
                       'Expression',
                       'Extension']} })


class ReferenceRange(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/measurement'})

    high: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['ReferenceRange']} })
    low: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['ReferenceRange']} })
    unit: Optional[OntologyClass] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Quantity', 'ReferenceRange']} })


class TypedQuantity(ConfiguredBaseModel):
    """
    For complex measurements, such as blood pressure where more than one component quantity is required to describe the measurement
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/measurement'})

    quantity: Optional[Quantity] = Field(default=None, description="""e.g. mm Hg""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['TypedQuantity', 'Value', 'DoseInterval']} })
    type: Optional[OntologyClass] = Field(default=None, description="""e.g. diastolic, systolic""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['TypedQuantity', 'PhenotypicFeature']} })


class Value(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/measurement',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'value'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'quantity': {'name': 'quantity',
                                                                                            'required': True}}},
                                                          {'slot_conditions': {'ontologyClass': {'name': 'ontologyClass',
                                                                                                 'required': True}}}]}}]})

    ontologyClass: Optional[OntologyClass] = Field(default=None, description="""for use with things such as categories 'red', 'yellow' or 'absent'/'present'""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['TimeElement', 'Value', 'TherapeuticRegimen']} })
    quantity: Optional[Quantity] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['TypedQuantity', 'Value', 'DoseInterval']} })


class PhenotypicFeature(ConfiguredBaseModel):
    """
    An individual phenotypic feature, observed as either present or absent (negated), with possible onset, modifiers and frequency FHIR mapping: Condition (https://www.hl7.org/fhir/condition.html) or Observation (https://www.hl7.org/fhir/observation.html)
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/phenotypic_feature'})

    description: Optional[str] = Field(default=None, description="""Free-text description of the phenotype. Note this is not a acceptable place to document/describe the phenotype - the type and onset etc... fields should be used for this purpose.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'Measurement',
                       'PhenotypicFeature',
                       'Biosample',
                       'GeneDescriptor',
                       'VariationDescriptor',
                       'Cohort']} })
    evidence: Optional[list[Evidence]] = Field(default=None, description="""Evidences for how the phenotype was determined.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 8}},
         'domain_of': ['PhenotypicFeature']} })
    excluded: Optional[bool] = Field(default=None, description="""Flag to indicate whether the phenotype was observed or not. Default is 'false', in other words the phenotype was observed. Therefore it is only required in cases to indicate that the phenotype was looked for, but found to be absent. More formally, this modifier indicates the logical negation of the OntologyClass used in the 'type' field. *CAUTION* It is imperative to check this field for correct interpretation of the phenotype!""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['PhenotypicFeature', 'Disease']} })
    modifiers: Optional[list[OntologyClass]] = Field(default=None, description="""subclasses of HP:0012823 ! Clinical modifier apart from Severity HP:0012824 - Severity""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['PhenotypicFeature']} })
    onset: Optional[TimeElement] = Field(default=None, description="""the values of this will come from the HPO onset hierarchy i.e. subclasses of HP:0003674 FHIR mapping: Condition.onset""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['PhenotypicFeature', 'Disease']} })
    resolution: Optional[TimeElement] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}},
         'domain_of': ['PhenotypicFeature', 'Disease']} })
    severity: Optional[OntologyClass] = Field(default=None, description="""Severity of the condition e.g. subclasses of HP:0012824-Severity or SNOMED:272141005-Severities FHIR mapping: Condition.severity""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['PhenotypicFeature']} })
    type: Optional[OntologyClass] = Field(default=None, description="""The primary ontology class which describes the phenotype. For example \"HP:0001363\"  \"Craniosynostosis\" FHIR mapping: Condition.identifier""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['TypedQuantity', 'PhenotypicFeature']} })


class Biosample(ConfiguredBaseModel):
    """
    A Biosample refers to a unit of biological material from which the substrate molecules (e.g. genomic DNA, RNA, proteins) for molecular analyses (e.g. sequencing, array hybridisation, mass-spectrometry) are extracted. Examples would be a tissue biopsy, a single cell from a culture for single cell genome sequencing or a protein fraction from a gradient centrifugation. Several instances (e.g. technical replicates) or types of experiments (e.g. genomic array as well as RNA-seq experiments) may refer to the same Biosample. FHIR mapping: Specimen (http://www.hl7.org/fhir/specimen.html).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['biosamples SAMN08666232 Human Cell Atlas'],
         'from_schema': 'https://w3id.org/linkml/phenopackets/biosample'})

    derivedFromId: Optional[str] = Field(default=None, description="""The id of the parent biosample this biosample was derived from.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Biosample']} })
    description: Optional[str] = Field(default=None, description="""The biosample's description. This attribute contains human readable text. The \"description\" attributes should not contain any structured data.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['ExternalReference',
                       'Measurement',
                       'PhenotypicFeature',
                       'Biosample',
                       'GeneDescriptor',
                       'VariationDescriptor',
                       'Cohort']} })
    diagnosticMarkers: Optional[list[OntologyClass]] = Field(default=None, description="""Clinically relevant bio markers. Most of the assays such as IHC are covered by the NCIT under the sub-hierarchy NCIT:C25294 (Laboratory Procedure). e.g. NCIT:C68748 (HER2/Neu Positive), NCIT:C131711 (Human Papillomavirus-18 Positive)""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 16}},
         'domain_of': ['Biosample']} })
    files: Optional[list[File]] = Field(default=None, description="""Pointer to the relevant file(s) for the biosample. Files relating to the entire individual e.g. a germline exome/genome should be associated with the Phenopacket rather than the Biosample it was derived from.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 18}},
         'domain_of': ['Biosample', 'Cohort', 'Family', 'Phenopacket']} })
    histologicalDiagnosis: Optional[OntologyClass] = Field(default=None, description="""This is the pathologist’s diagnosis and may often represent a refinement of the clinical diagnosis given in the Patient/Clinical module. Should use the same terminology as diagnosis, but represent the pathologist’s findings. Normal samples would be tagged with the term \"NCIT:C38757\", \"Negative Finding\" ARGO mapping specimen::tumour_histological_type""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 11}},
         'domain_of': ['Biosample'],
         'exact_mappings': ['ARGO:specimen.tumour_histological_type']} })
    id: Optional[str] = Field(default=None, description="""The Biosample id This is unique in the context of the server instance. ARGO mapping specimen::submitter_specimen_id""", json_schema_extra = { "linkml_meta": {'annotations': {'percent_encoded': {'tag': 'percent_encoded', 'value': True},
                         'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket'],
         'exact_mappings': ['ARGO:specimen.submitter_specimen_id']} })
    individualId: Optional[str] = Field(default=None, description="""The id of the individual this biosample was derived from. ARGO mapping specimen::submitter_donor_id""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Biosample', 'Person'],
         'exact_mappings': ['ARGO:specimen.submitter_donor_id']} })
    materialSample: Optional[OntologyClass] = Field(default=None, description="""This element can be used to specify the status of the sample. For instance, a status may be used as a normal control, often in combination with another sample that is thought to contain a pathological finding. We recommend use of ontology terms such as: EFO:0009654 (reference sample) or EFO:0009655 (abnormal sample) ARGO mapping sample_registration::tumour_normal_designation""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 19}},
         'domain_of': ['Biosample'],
         'exact_mappings': ['ARGO:sample_registration.tumour_normal_designation']} })
    measurements: Optional[list[Measurement]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 8}},
         'domain_of': ['Biosample', 'Phenopacket']} })
    pathologicalStage: Optional[OntologyClass] = Field(default=None, description="""ARGO mapping specimen::pathological_tumour_staging_system ARGO mapping specimen::pathological_stage_group""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 14}},
         'domain_of': ['Biosample'],
         'exact_mappings': ['ARGO:specimen.pathological_tumour_staging_system']} })
    pathologicalTnmFinding: Optional[list[OntologyClass]] = Field(default=None, description="""ARGO mapping specimen::pathological_t_category ARGO mapping specimen::pathological_n_category ARGO mapping specimen::pathological_m_category""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 15}},
         'domain_of': ['Biosample'],
         'exact_mappings': ['ARGO:specimen.pathological_t_category']} })
    phenotypicFeatures: Optional[list[PhenotypicFeature]] = Field(default=None, description="""Phenotypic characteristics of the BioSample, for example histological findings of a biopsy.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}},
         'domain_of': ['Biosample', 'Phenopacket']} })
    procedure: Optional[Procedure] = Field(default=None, description="""Clinical procedure performed on the subject in order to extract the biosample. ARGO mapping specimen::specimen_anatomic_location - Procedure::body_site ARGO mapping specimen::specimen_acquisition_interval - Procedure::time_performed""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 17}},
         'domain_of': ['Measurement', 'Biosample', 'MedicalAction'],
         'exact_mappings': ['ARGO:specimen.specimen_anatomic_location']} })
    sampleProcessing: Optional[OntologyClass] = Field(default=None, description="""Field to represent how the sample was processed. ARGO mapping specimen::specimen_processing""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 20}},
         'domain_of': ['Biosample'],
         'exact_mappings': ['ARGO:specimen.specimen_processing']} })
    sampleStorage: Optional[OntologyClass] = Field(default=None, description="""Field to represent how the sample was stored ARGO mapping specimen::specimen_storage""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 21}},
         'domain_of': ['Biosample'],
         'exact_mappings': ['ARGO:specimen.specimen_storage']} })
    sampleType: Optional[OntologyClass] = Field(default=None, description="""Recommended use of EFO term to describe the sample. e.g. Amplified DNA, ctDNA, Total RNA, Lung tissue, Cultured cells... ARGO mapping sample_registration::sample_type""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['Biosample'],
         'exact_mappings': ['ARGO:sample_registration.sample_type']} })
    sampledTissue: Optional[OntologyClass] = Field(default=None, description="""UBERON class describing the tissue from which the specimen was collected. PDX-MI mapping: 'Specimen tumor tissue' FHIR mapping: Specimen.type ARGO mapping sample_registration::specimen_tissue_source""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Biosample'],
         'exact_mappings': ['ARGO:sample_registration.specimen_tissue_source']} })
    taxonomy: Optional[OntologyClass] = Field(default=None, description="""NCBI taxonomic identifier (NCBITaxon) of the sample e.g. NCBITaxon:9606""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 9}},
         'domain_of': ['Biosample', 'Individual']} })
    timeOfCollection: Optional[TimeElement] = Field(default=None, description="""An TimeElement describing either the age of the individual this biosample was derived from at the time of collection, or the time itself. See http://build.fhir.org/datatypes""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 10}},
         'domain_of': ['Biosample']} })
    tumorGrade: Optional[OntologyClass] = Field(default=None, description="""Potentially a child term of NCIT:C28076 (Disease Grade Qualifier) or equivalent See https://www.cancer.gov/about-cancer/diagnosis-staging/prognosis/tumor-grade-fact-sheet""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 13}},
         'domain_of': ['Biosample']} })
    tumorProgression: Optional[OntologyClass] = Field(default=None, description="""Is the specimen tissue from the primary tumor, a metastasis or a recurrence? Most likely a child term of NCIT:C7062 (Neoplasm by Special Category) NCIT:C3677 (Benign Neoplasm) NCIT:C84509 (Primary Malignant Neoplasm) NCIT:C95606 (Second Primary Malignant Neoplasm) NCIT:C3261 (Metastatic Neoplasm) NCIT:C4813 (Recurrent Malignant Neoplasm)""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 12}},
         'domain_of': ['Biosample']} })


class Disease(ConfiguredBaseModel):
    """
    Message to indicate a disease (diagnosis) and its recorded onset.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/disease'})

    clinicalTnmFinding: Optional[list[OntologyClass]] = Field(default=None, description="""Cancer findings in the TNM system that is relevant to the diagnosis of cancer. See https://www.cancer.gov/about-cancer/diagnosis-staging/staging Valid values include child terms of NCIT:C48232 (Cancer TNM Finding) ARGO mapping primary_diagnosis::clinical_t_category ARGO mapping primary_diagnosis::clinical_n_category ARGO mapping primary_diagnosis::clinical_m_category""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['Disease'],
         'exact_mappings': ['ARGO:primary_diagnosis.clinical_t_category']} })
    diseaseStage: Optional[list[OntologyClass]] = Field(default=None, description="""Disease staging, the extent to which a disease has developed. For cancers, see https://www.cancer.gov/about-cancer/diagnosis-staging/staging Valid values include child terms of NCIT:C28108 (Disease Stage Qualifier) ARGO mapping primary_diagnosis::clinical_tumour_staging_system ARGO mapping primary_diagnosis::clinical_stage_group""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Disease'],
         'exact_mappings': ['ARGO:primary_diagnosis.clinical_tumour_staging_system']} })
    excluded: Optional[bool] = Field(default=None, description="""Flag to indicate whether the disease was observed or not. Default is 'false', in other words the disease was observed. Therefore it is only required in cases to indicate that the disease was looked for, but found to be absent. More formally, this modifier indicates the logical negation of the OntologyClass used in the 'term' field. *CAUTION* It is imperative to check this field for correct interpretation of the disease!""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['PhenotypicFeature', 'Disease']} })
    laterality: Optional[OntologyClass] = Field(default=None, description="""The term used to indicate laterality of diagnosis, if applicable. (Codelist reference: NCI CDE: 4122391)""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 8}}, 'domain_of': ['Disease']} })
    onset: Optional[TimeElement] = Field(default=None, description="""The onset of the disease. The values of this will come from the HPO onset hierarchy i.e. subclasses of HP:0003674 FHIR mapping: Condition.onset ARGO mapping primary_diagnosis::age_at_diagnosis""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['PhenotypicFeature', 'Disease'],
         'exact_mappings': ['ARGO:primary_diagnosis.age_at_diagnosis']} })
    primarySite: Optional[OntologyClass] = Field(default=None, description="""The text term used to describe the primary site of disease, as categorized by the World Health Organization's (WHO) International Classification of Diseases for Oncology (ICD-O). This categorization groups cases into general""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}}, 'domain_of': ['Disease']} })
    resolution: Optional[TimeElement] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['PhenotypicFeature', 'Disease']} })
    term: Optional[OntologyClass] = Field(default=None, description="""The identifier of this disease e.g. MONDO:0007043, OMIM:101600, Orphanet:710, DOID:14705 (note these are all equivalent) ARGO mapping primary_diagnosis::submitter_primary_diagnosis_id""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Disease'],
         'exact_mappings': ['ARGO:primary_diagnosis.submitter_primary_diagnosis_id']} })


class Any(ConfiguredBaseModel):
    """
    `Any` contains an arbitrary serialized protocol buffer message along with a URL that describes the type of the serialized message.  Protobuf library provides support to pack/unpack Any values in the form of utility functions or additional generated methods of the Any type.  Example 1: Pack and unpack a message in C++.  Foo foo = ...; Any any; any.PackFrom(foo); ... if (any.UnpackTo(&foo)) { ... }  Example 2: Pack and unpack a message in Java.  Foo foo = ...; Any any = Any.pack(foo); ... if (any.is(Foo.class)) { foo = any.unpack(Foo.class); }  Example 3: Pack and unpack a message in Python.  foo = Foo(...) any = Any() any.Pack(foo) ... if any.Is(Foo.DESCRIPTOR): any.Unpack(foo) ...  Example 4: Pack and unpack a message in Go  foo := &pb.Foo{...} any, err := anypb.New(foo) if err != nil { ... } ... foo := &pb.Foo{} if err := any.UnmarshalTo(foo); err != nil { ... }  The pack methods provided by protobuf library will by default use 'type.googleapis.com/full.type.name' as the type URL and the unpack methods only use the fully qualified type name after the last '/' in the type URL, for example \"foo.bar.com/x/y.z\" will yield type name \"y.z\".   JSON ==== The JSON representation of an `Any` value uses the regular representation of the deserialized, embedded message, with an additional field `@type` which contains the type URL. Example:  package google.profile; message Person { string first_name = 1; string last_name = 2; }  { \"@type\": \"type.googleapis.com/google.profile.Person\", \"firstName\": <string>, \"lastName\": <string> }  If the embedded message type is well-known and has a custom JSON representation, that representation will be embedded adding a field `value` which holds the custom JSON in addition to the `@type` field. Example (for message [google.protobuf.Duration][]):  { \"@type\": \"type.googleapis.com/google.protobuf.Duration\", \"value\": \"1.212s\" } 
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/any'})

    typeUrl: Optional[str] = Field(default=None, description="""A URL/resource name that uniquely identifies the type of the serialized protocol buffer message. This string must contain at least one \"/\" character. The last segment of the URL's path must represent the fully qualified name of the type (as in `path/google.protobuf.Duration`). The name should be in a canonical form (e.g., leading \".\" is not accepted).  In practice, teams usually precompile into the binary all types that they expect it to use in the context of Any. However, for URLs which use the scheme `http`, `https`, or no scheme, one can optionally set up a type server that maps type URLs to message definitions as follows:  * If no scheme is provided, `https` is assumed. * An HTTP GET on the URL must yield a [google.protobuf.Type][] value in binary format, or produce an error. * Applications are allowed to cache lookup results based on the URL, or have them precompiled into a binary to avoid any lookup. Therefore, binary compatibility needs to be preserved on changes to types. (Use versioned type names to manage breaking changes.)  Note: this functionality is not currently available in the official protobuf release, and it is not used for type URLs beginning with type.googleapis.com.  Schemes other than `http`, `https` (or the empty scheme) might be used with implementation specific semantics. """, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}}, 'domain_of': ['Any']} })
    value: Optional[str] = Field(default=None, description="""Must be a valid serialized protocol buffer of the above specified type.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['DictionaryEntry',
                       'Measurement',
                       'Quantity',
                       'Any',
                       'IndefiniteRange',
                       'Number',
                       'Expression',
                       'Extension']} })


class Abundance(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'abundance'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'copyNumber': {'name': 'copyNumber',
                                                                                              'required': True}}}]}}]})

    copyNumber: Optional[CopyNumber] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Abundance',
                       'SystemicVariation',
                       'Variation',
                       'VariationSetMember']} })


class Allele(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'location'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'curie': {'name': 'curie',
                                                                                         'required': True}}},
                                                          {'slot_conditions': {'chromosomeLocation': {'name': 'chromosomeLocation',
                                                                                                      'required': True}}},
                                                          {'slot_conditions': {'sequenceLocation': {'name': 'sequenceLocation',
                                                                                                    'required': True}}}]}},
                   {'annotations': {'oneof': {'tag': 'oneof', 'value': 'state'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'sequenceState': {'name': 'sequenceState',
                                                                                                 'required': True}}},
                                                          {'slot_conditions': {'literalSequenceExpression': {'name': 'literalSequenceExpression',
                                                                                                             'required': True}}},
                                                          {'slot_conditions': {'derivedSequenceExpression': {'name': 'derivedSequenceExpression',
                                                                                                             'required': True}}},
                                                          {'slot_conditions': {'repeatedSequenceExpression': {'name': 'repeatedSequenceExpression',
                                                                                                              'required': True}}}]}}]})

    Id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele',
                       'ChromosomeLocation',
                       'CopyNumber',
                       'Haplotype',
                       'SequenceLocation',
                       'Text',
                       'VariationSet']} })
    chromosomeLocation: Optional[ChromosomeLocation] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Allele', 'Location']} })
    curie: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Allele', 'CopyNumber', 'HaplotypeMember', 'VariationSetMember']} })
    derivedSequenceExpression: Optional[DerivedSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['Allele',
                       'CopyNumber',
                       'RepeatedSequenceExpression',
                       'SequenceExpression']} })
    literalSequenceExpression: Optional[LiteralSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Allele',
                       'CopyNumber',
                       'RepeatedSequenceExpression',
                       'SequenceExpression']} })
    repeatedSequenceExpression: Optional[RepeatedSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}},
         'domain_of': ['Allele', 'CopyNumber', 'SequenceExpression']} })
    sequenceLocation: Optional[SequenceLocation] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['Allele', 'Location']} })
    sequenceState: Optional[SequenceState] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 100}},
         'deprecated': 'Marked as deprecated (deprecated=true) in the protobuf '
                       'definition',
         'domain_of': ['Allele']} })


class ChromosomeLocation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    Id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele',
                       'ChromosomeLocation',
                       'CopyNumber',
                       'Haplotype',
                       'SequenceLocation',
                       'Text',
                       'VariationSet']} })
    chr: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['ChromosomeLocation']} })
    interval: Optional[CytobandInterval] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['TimeElement', 'ChromosomeLocation', 'DoseInterval']} })
    speciesId: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['ChromosomeLocation']} })


class CopyNumber(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'subject'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'allele': {'name': 'allele',
                                                                                          'required': True}}},
                                                          {'slot_conditions': {'haplotype': {'name': 'haplotype',
                                                                                             'required': True}}},
                                                          {'slot_conditions': {'gene': {'name': 'gene',
                                                                                        'required': True}}},
                                                          {'slot_conditions': {'literalSequenceExpression': {'name': 'literalSequenceExpression',
                                                                                                             'required': True}}},
                                                          {'slot_conditions': {'derivedSequenceExpression': {'name': 'derivedSequenceExpression',
                                                                                                             'required': True}}},
                                                          {'slot_conditions': {'repeatedSequenceExpression': {'name': 'repeatedSequenceExpression',
                                                                                                              'required': True}}},
                                                          {'slot_conditions': {'curie': {'name': 'curie',
                                                                                         'required': True}}}]}},
                   {'annotations': {'oneof': {'tag': 'oneof', 'value': 'copies'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'number': {'name': 'number',
                                                                                          'required': True}}},
                                                          {'slot_conditions': {'indefiniteRange': {'name': 'indefiniteRange',
                                                                                                   'required': True}}},
                                                          {'slot_conditions': {'definiteRange': {'name': 'definiteRange',
                                                                                                 'required': True}}}]}}]})

    Id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele',
                       'ChromosomeLocation',
                       'CopyNumber',
                       'Haplotype',
                       'SequenceLocation',
                       'Text',
                       'VariationSet']} })
    allele: Optional[Allele] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['CopyNumber',
                       'HaplotypeMember',
                       'MolecularVariation',
                       'Variation',
                       'VariationSetMember']} })
    curie: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 8}},
         'domain_of': ['Allele', 'CopyNumber', 'HaplotypeMember', 'VariationSetMember']} })
    definiteRange: Optional[DefiniteRange] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 11}},
         'domain_of': ['CopyNumber', 'RepeatedSequenceExpression']} })
    derivedSequenceExpression: Optional[DerivedSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['Allele',
                       'CopyNumber',
                       'RepeatedSequenceExpression',
                       'SequenceExpression']} })
    gene: Optional[Gene] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['CopyNumber', 'Feature', 'GenomicInterpretation']} })
    haplotype: Optional[Haplotype] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['CopyNumber',
                       'MolecularVariation',
                       'Variation',
                       'VariationSetMember']} })
    indefiniteRange: Optional[IndefiniteRange] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 10}},
         'domain_of': ['CopyNumber', 'RepeatedSequenceExpression']} })
    literalSequenceExpression: Optional[LiteralSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Allele',
                       'CopyNumber',
                       'RepeatedSequenceExpression',
                       'SequenceExpression']} })
    number: Optional[Number] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 9}},
         'domain_of': ['CopyNumber', 'RepeatedSequenceExpression']} })
    repeatedSequenceExpression: Optional[RepeatedSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}},
         'domain_of': ['Allele', 'CopyNumber', 'SequenceExpression']} })


class CytobandInterval(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    end: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['AgeRange',
                       'TimeInterval',
                       'CytobandInterval',
                       'SimpleInterval']} })
    start: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['AgeRange',
                       'TimeInterval',
                       'CytobandInterval',
                       'SimpleInterval']} })


class DefiniteRange(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    max: Optional[int] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['DefiniteRange']} })
    min: Optional[int] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['DefiniteRange']} })


class DerivedSequenceExpression(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    location: Optional[SequenceLocation] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['DerivedSequenceExpression']} })
    reverseComplement: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['DerivedSequenceExpression']} })


class Feature(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'feature'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'gene': {'name': 'gene',
                                                                                        'required': True}}}]}}]})

    gene: Optional[Gene] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['CopyNumber', 'Feature', 'GenomicInterpretation']} })


class Gene(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    geneId: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}}, 'domain_of': ['Gene']} })


class Haplotype(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    Id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele',
                       'ChromosomeLocation',
                       'CopyNumber',
                       'Haplotype',
                       'SequenceLocation',
                       'Text',
                       'VariationSet']} })
    members: Optional[list[HaplotypeMember]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Haplotype', 'VariationSet', 'Cohort']} })


class HaplotypeMember(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'value'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'allele': {'name': 'allele',
                                                                                          'required': True}}},
                                                          {'slot_conditions': {'curie': {'name': 'curie',
                                                                                         'required': True}}}]}}]})

    allele: Optional[Allele] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['CopyNumber',
                       'HaplotypeMember',
                       'MolecularVariation',
                       'Variation',
                       'VariationSetMember']} })
    curie: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Allele', 'CopyNumber', 'HaplotypeMember', 'VariationSetMember']} })


class IndefiniteRange(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    comparator: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['IndefiniteRange']} })
    value: Optional[int] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['DictionaryEntry',
                       'Measurement',
                       'Quantity',
                       'Any',
                       'IndefiniteRange',
                       'Number',
                       'Expression',
                       'Extension']} })


class LiteralSequenceExpression(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    sequence: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['LiteralSequenceExpression', 'SequenceState']} })


class Location(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'location'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'chromosomeLocation': {'name': 'chromosomeLocation',
                                                                                                      'required': True}}},
                                                          {'slot_conditions': {'sequenceLocation': {'name': 'sequenceLocation',
                                                                                                    'required': True}}}]}}]})

    chromosomeLocation: Optional[ChromosomeLocation] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele', 'Location']} })
    sequenceLocation: Optional[SequenceLocation] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Allele', 'Location']} })


class MolecularVariation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof',
                                              'value': 'molecular_variation'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'allele': {'name': 'allele',
                                                                                          'required': True}}},
                                                          {'slot_conditions': {'haplotype': {'name': 'haplotype',
                                                                                             'required': True}}}]}}]})

    allele: Optional[Allele] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['CopyNumber',
                       'HaplotypeMember',
                       'MolecularVariation',
                       'Variation',
                       'VariationSetMember']} })
    haplotype: Optional[Haplotype] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['CopyNumber',
                       'MolecularVariation',
                       'Variation',
                       'VariationSetMember']} })


class Number(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    value: Optional[int] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['DictionaryEntry',
                       'Measurement',
                       'Quantity',
                       'Any',
                       'IndefiniteRange',
                       'Number',
                       'Expression',
                       'Extension']} })


class RepeatedSequenceExpression(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'seq_expr'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'literalSequenceExpression': {'name': 'literalSequenceExpression',
                                                                                                             'required': True}}},
                                                          {'slot_conditions': {'derivedSequenceExpression': {'name': 'derivedSequenceExpression',
                                                                                                             'required': True}}}]}},
                   {'annotations': {'oneof': {'tag': 'oneof', 'value': 'count'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'number': {'name': 'number',
                                                                                          'required': True}}},
                                                          {'slot_conditions': {'indefiniteRange': {'name': 'indefiniteRange',
                                                                                                   'required': True}}},
                                                          {'slot_conditions': {'definiteRange': {'name': 'definiteRange',
                                                                                                 'required': True}}}]}}]})

    definiteRange: Optional[DefiniteRange] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['CopyNumber', 'RepeatedSequenceExpression']} })
    derivedSequenceExpression: Optional[DerivedSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Allele',
                       'CopyNumber',
                       'RepeatedSequenceExpression',
                       'SequenceExpression']} })
    indefiniteRange: Optional[IndefiniteRange] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['CopyNumber', 'RepeatedSequenceExpression']} })
    literalSequenceExpression: Optional[LiteralSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele',
                       'CopyNumber',
                       'RepeatedSequenceExpression',
                       'SequenceExpression']} })
    number: Optional[Number] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['CopyNumber', 'RepeatedSequenceExpression']} })


class SequenceExpression(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof',
                                              'value': 'sequence_expression'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'literalSequenceExpression': {'name': 'literalSequenceExpression',
                                                                                                             'required': True}}},
                                                          {'slot_conditions': {'derivedSequenceExpression': {'name': 'derivedSequenceExpression',
                                                                                                             'required': True}}},
                                                          {'slot_conditions': {'repeatedSequenceExpression': {'name': 'repeatedSequenceExpression',
                                                                                                              'required': True}}}]}}]})

    derivedSequenceExpression: Optional[DerivedSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Allele',
                       'CopyNumber',
                       'RepeatedSequenceExpression',
                       'SequenceExpression']} })
    literalSequenceExpression: Optional[LiteralSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele',
                       'CopyNumber',
                       'RepeatedSequenceExpression',
                       'SequenceExpression']} })
    repeatedSequenceExpression: Optional[RepeatedSequenceExpression] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Allele', 'CopyNumber', 'SequenceExpression']} })


class SequenceInterval(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'start'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'startNumber': {'name': 'startNumber',
                                                                                               'required': True}}},
                                                          {'slot_conditions': {'startIndefiniteRange': {'name': 'startIndefiniteRange',
                                                                                                        'required': True}}},
                                                          {'slot_conditions': {'startDefiniteRange': {'name': 'startDefiniteRange',
                                                                                                      'required': True}}}]}},
                   {'annotations': {'oneof': {'tag': 'oneof', 'value': 'end'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'endNumber': {'name': 'endNumber',
                                                                                             'required': True}}},
                                                          {'slot_conditions': {'endIndefiniteRange': {'name': 'endIndefiniteRange',
                                                                                                      'required': True}}},
                                                          {'slot_conditions': {'endDefiniteRange': {'name': 'endDefiniteRange',
                                                                                                    'required': True}}}]}}]})

    endDefiniteRange: Optional[DefiniteRange] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['SequenceInterval']} })
    endIndefiniteRange: Optional[IndefiniteRange] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['SequenceInterval']} })
    endNumber: Optional[Number] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['SequenceInterval']} })
    startDefiniteRange: Optional[DefiniteRange] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['SequenceInterval']} })
    startIndefiniteRange: Optional[IndefiniteRange] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['SequenceInterval']} })
    startNumber: Optional[Number] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['SequenceInterval']} })


class SequenceLocation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'interval'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'sequenceInterval': {'name': 'sequenceInterval',
                                                                                                    'required': True}}},
                                                          {'slot_conditions': {'simpleInterval': {'name': 'simpleInterval',
                                                                                                  'required': True}}}]}}]})

    Id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele',
                       'ChromosomeLocation',
                       'CopyNumber',
                       'Haplotype',
                       'SequenceLocation',
                       'Text',
                       'VariationSet']} })
    sequenceId: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['SequenceLocation']} })
    sequenceInterval: Optional[SequenceInterval] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['SequenceLocation']} })
    simpleInterval: Optional[SimpleInterval] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 100}},
         'deprecated': 'Marked as deprecated (deprecated=true) in the protobuf '
                       'definition',
         'domain_of': ['SequenceLocation']} })


class SequenceState(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    sequence: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['LiteralSequenceExpression', 'SequenceState']} })


class SimpleInterval(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    end: Optional[int] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['AgeRange',
                       'TimeInterval',
                       'CytobandInterval',
                       'SimpleInterval']} })
    start: Optional[int] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['AgeRange',
                       'TimeInterval',
                       'CytobandInterval',
                       'SimpleInterval']} })


class SystemicVariation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof',
                                              'value': 'systemic_variation'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'copyNumber': {'name': 'copyNumber',
                                                                                              'required': True}}}]}}]})

    copyNumber: Optional[CopyNumber] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Abundance',
                       'SystemicVariation',
                       'Variation',
                       'VariationSetMember']} })


class Text(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    Id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele',
                       'ChromosomeLocation',
                       'CopyNumber',
                       'Haplotype',
                       'SequenceLocation',
                       'Text',
                       'VariationSet']} })
    definition: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}}, 'domain_of': ['Text']} })


class UtilityVariation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof',
                                              'value': 'utility_variation'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'text': {'name': 'text',
                                                                                        'required': True}}},
                                                          {'slot_conditions': {'variationSet': {'name': 'variationSet',
                                                                                                'required': True}}}]}}]})

    text: Optional[Text] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['UtilityVariation', 'Variation', 'VariationSetMember']} })
    variationSet: Optional[VariationSet] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['UtilityVariation', 'Variation', 'VariationSetMember']} })


class Variation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'variation'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'allele': {'name': 'allele',
                                                                                          'required': True}}},
                                                          {'slot_conditions': {'haplotype': {'name': 'haplotype',
                                                                                             'required': True}}},
                                                          {'slot_conditions': {'copyNumber': {'name': 'copyNumber',
                                                                                              'required': True}}},
                                                          {'slot_conditions': {'text': {'name': 'text',
                                                                                        'required': True}}},
                                                          {'slot_conditions': {'variationSet': {'name': 'variationSet',
                                                                                                'required': True}}}]}}]})

    allele: Optional[Allele] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['CopyNumber',
                       'HaplotypeMember',
                       'MolecularVariation',
                       'Variation',
                       'VariationSetMember']} })
    copyNumber: Optional[CopyNumber] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Abundance',
                       'SystemicVariation',
                       'Variation',
                       'VariationSetMember']} })
    haplotype: Optional[Haplotype] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['CopyNumber',
                       'MolecularVariation',
                       'Variation',
                       'VariationSetMember']} })
    text: Optional[Text] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['UtilityVariation', 'Variation', 'VariationSetMember']} })
    variationSet: Optional[VariationSet] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['UtilityVariation', 'Variation', 'VariationSetMember']} })


class VariationSet(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs'})

    Id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele',
                       'ChromosomeLocation',
                       'CopyNumber',
                       'Haplotype',
                       'SequenceLocation',
                       'Text',
                       'VariationSet']} })
    members: Optional[list[VariationSetMember]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Haplotype', 'VariationSet', 'Cohort']} })


class VariationSetMember(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrs',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'value'}},
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'curie': {'name': 'curie',
                                                                                         'required': True}}},
                                                          {'slot_conditions': {'allele': {'name': 'allele',
                                                                                          'required': True}}},
                                                          {'slot_conditions': {'haplotype': {'name': 'haplotype',
                                                                                             'required': True}}},
                                                          {'slot_conditions': {'copyNumber': {'name': 'copyNumber',
                                                                                              'required': True}}},
                                                          {'slot_conditions': {'text': {'name': 'text',
                                                                                        'required': True}}},
                                                          {'slot_conditions': {'variationSet': {'name': 'variationSet',
                                                                                                'required': True}}}]}}]})

    allele: Optional[Allele] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['CopyNumber',
                       'HaplotypeMember',
                       'MolecularVariation',
                       'Variation',
                       'VariationSetMember']} })
    copyNumber: Optional[CopyNumber] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['Abundance',
                       'SystemicVariation',
                       'Variation',
                       'VariationSetMember']} })
    curie: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Allele', 'CopyNumber', 'HaplotypeMember', 'VariationSetMember']} })
    haplotype: Optional[Haplotype] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['CopyNumber',
                       'MolecularVariation',
                       'Variation',
                       'VariationSetMember']} })
    text: Optional[Text] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['UtilityVariation', 'Variation', 'VariationSetMember']} })
    variationSet: Optional[VariationSet] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['UtilityVariation', 'Variation', 'VariationSetMember']} })


class Expression(ConfiguredBaseModel):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#expression
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrsatile'})

    syntax: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Expression']} })
    value: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['DictionaryEntry',
                       'Measurement',
                       'Quantity',
                       'Any',
                       'IndefiniteRange',
                       'Number',
                       'Expression',
                       'Extension']} })
    version: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Expression', 'Resource']} })


class Extension(ConfiguredBaseModel):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#extension
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrsatile'})

    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Extension', 'Resource']} })
    value: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['DictionaryEntry',
                       'Measurement',
                       'Quantity',
                       'Any',
                       'IndefiniteRange',
                       'Number',
                       'Expression',
                       'Extension']} })


class GeneDescriptor(ConfiguredBaseModel):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#gene-descriptor
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrsatile'})

    alternateIds: Optional[list[str]] = Field(default=None, description="""Alternate IDs (should be CURIE) for the same concept may be placed in alternate_ids""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['GeneDescriptor', 'Individual']} })
    alternateSymbols: Optional[list[str]] = Field(default=None, description="""Takes the place of alternate_labels field in a generic descriptor""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['GeneDescriptor']} })
    description: Optional[str] = Field(default=None, description="""A free-text description of the value object""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['ExternalReference',
                       'Measurement',
                       'PhenotypicFeature',
                       'Biosample',
                       'GeneDescriptor',
                       'VariationDescriptor',
                       'Cohort']} })
    symbol: Optional[str] = Field(default=None, description="""The primary gene symbol. Takes the place of the label field in a generic descriptor""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['GeneDescriptor']} })
    valueId: Optional[str] = Field(default=None, description="""The official gene identifier as designated by the organism gene nomenclature committee e.g. HGNC:3477 or MGI:2385071 This should be a CURIE linking the reference to a namespace where it can be retrieved. Mirrors the value_id field of a generic value object descriptor""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['GeneDescriptor']} })
    xrefs: Optional[list[str]] = Field(default=None, description="""Related concept IDs (e.g. gene ortholog IDs) may be placed in xrefs""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['GeneDescriptor', 'VariationDescriptor']} })


class VariationDescriptor(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrsatile'})

    allelicState: Optional[OntologyClass] = Field(default=None, description="""We RECOMMEND that the allelic_state of variant be described by terms from the Genotype Ontology (GENO). These SHOULD descend from concept GENO:0000875.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 14}},
         'domain_of': ['VariationDescriptor']} })
    alternateLabels: Optional[list[str]] = Field(default=None, description="""Common aliases for a variant, e.g. EGFR vIII, are alternate labels""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 9}},
         'domain_of': ['VariationDescriptor']} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['ExternalReference',
                       'Measurement',
                       'PhenotypicFeature',
                       'Biosample',
                       'GeneDescriptor',
                       'VariationDescriptor',
                       'Cohort']} })
    expressions: Optional[list[Expression]] = Field(default=None, description="""HGVS, SPDI, and gnomAD-style strings should be represented as Expressions""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['VariationDescriptor']} })
    extensions: Optional[list[Extension]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 10}},
         'domain_of': ['VariationDescriptor']} })
    geneContext: Optional[GeneDescriptor] = Field(default=None, description="""A specific gene context that applies to this variant.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['VariationDescriptor']} })
    id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'percent_encoded': {'tag': 'percent_encoded', 'value': True},
                         'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket']} })
    label: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['OntologyClass', 'VariationDescriptor']} })
    moleculeContext: Optional[MoleculeContext] = Field(default=None, description="""The molecular context of the vrs variation. Must be one of “genomic”, “transcript”, or “protein”. Defaults to \"unspecified_molecule_context\"""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 11}},
         'domain_of': ['VariationDescriptor']} })
    structuralType: Optional[OntologyClass] = Field(default=None, description="""The structural variant type associated with this variant, such as a substitution, deletion, or fusion. We RECOMMEND using a descendent term of SO:0001537.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 12}},
         'domain_of': ['VariationDescriptor']} })
    variation: Optional[Variation] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['VariationDescriptor']} })
    vcfRecord: Optional[VcfRecord] = Field(default=None, description="""A VCF Record of the variant. This SHOULD be a single allele, the VCF genotype (GT) field should be represented in the allelic_state""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}},
         'domain_of': ['VariationDescriptor']} })
    vrsRefAlleleSeq: Optional[str] = Field(default=None, description="""A Sequence corresponding to a “ref allele”, describing the sequence expected at a SequenceLocation reference.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 13}},
         'domain_of': ['VariationDescriptor']} })
    xrefs: Optional[list[str]] = Field(default=None, description="""Allele registry, ClinVar, or other related IDs should be included as xrefs""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 8}},
         'domain_of': ['GeneDescriptor', 'VariationDescriptor']} })


class VcfRecord(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/vrsatile'})

    alt: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['VcfRecord']} })
    chrom: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['VcfRecord']} })
    filter: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 8}},
         'domain_of': ['VcfRecord']} })
    genomeAssembly: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['VcfRecord']} })
    id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'percent_encoded': {'tag': 'percent_encoded', 'value': True},
                         'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket']} })
    info: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 9}},
         'domain_of': ['VcfRecord']} })
    pos: Optional[int] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['VcfRecord']} })
    qual: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}},
         'domain_of': ['VcfRecord']} })
    ref: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['VcfRecord']} })


class Diagnosis(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/interpretation'})

    disease: Optional[OntologyClass] = Field(default=None, description="""The disease/condition assigned to the diagnosis.Details about this disease may be contained in the `diseases` field in the Phenopacket.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Diagnosis']} })
    genomicInterpretations: Optional[list[GenomicInterpretation]] = Field(default=None, description="""genomic features containing the status of their contribution towards the diagnosis""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Diagnosis']} })


class GenomicInterpretation(ConfiguredBaseModel):
    """
    A statement about the contribution of a genomic element towards the observed phenotype. Note that this does not intend to encode any knowledge or results of specific computations.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/interpretation',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'call'}},
                    'description': 'Gene or variant identified in subject or biosample '
                                   'and interpreted in relation to the disease '
                                   "diagnosis. In this context athe 'gene' is a proxy "
                                   'for an unspecified alteration in the indicated '
                                   'gene.',
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'gene': {'name': 'gene',
                                                                                        'required': True}}},
                                                          {'slot_conditions': {'variantInterpretation': {'name': 'variantInterpretation',
                                                                                                         'required': True}}}]}}]})

    gene: Optional[GeneDescriptor] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['CopyNumber', 'Feature', 'GenomicInterpretation']} })
    interpretationStatus: Optional[InterpretationStatus] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['GenomicInterpretation']} })
    subjectOrBiosampleId: Optional[str] = Field(default=None, description="""identifier for the subject of the interpretation. This MUST be the individual id or a biosample id of the enclosing phenopacket.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['GenomicInterpretation']} })
    variantInterpretation: Optional[VariantInterpretation] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['GenomicInterpretation']} })


class Interpretation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/interpretation'})

    diagnosis: Optional[Diagnosis] = Field(default=None, description="""The diagnosis made in this interpretation""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Interpretation']} })
    id: Optional[str] = Field(default=None, description="""id of the interpretation""", json_schema_extra = { "linkml_meta": {'annotations': {'percent_encoded': {'tag': 'percent_encoded', 'value': True},
                         'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket']} })
    progressStatus: Optional[ProgressStatus] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Interpretation']} })
    summary: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['Interpretation']} })


class VariantInterpretation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/interpretation'})

    acmgPathogenicityClassification: Optional[AcmgPathogenicityClassification] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['VariantInterpretation']} })
    therapeuticActionability: Optional[TherapeuticActionability] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['VariantInterpretation']} })
    variationDescriptor: Optional[VariationDescriptor] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['VariantInterpretation']} })


class Individual(ConfiguredBaseModel):
    """
    An individual (or subject) typically corresponds to an individual human or another organism. FHIR mapping: Patient (https://www.hl7.org/fhir/patient.html).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/individual'})

    alternateIds: Optional[list[str]] = Field(default=None, description="""An optional list of alternative identifiers for this individual. This field is provided for the convenience of users who may have multiple mappings to an individual which they need to track.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['GeneDescriptor', 'Individual']} })
    dateOfBirth: Optional[str] = Field(default=None, description="""The date of birth of the individual as an ISO8601 UTC timestamp - rounded down to the closest known year/month/day/hour/minute e.g. \"2018-03-01T00:00:00Z\" for someone born on an unknown day in March 2018 or \"2018-01-01T00:00:00Z\" for someone born on an unknown day in 2018 or empty if unknown/ not stated.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Individual']} })
    gender: Optional[OntologyClass] = Field(default=None, description="""Self-identified gender""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 8}},
         'domain_of': ['Individual']} })
    id: Optional[str] = Field(default=None, description="""An identifier for the individual. This must be unique within the record. ARGO mapping donor::submitter_donor_id""", json_schema_extra = { "linkml_meta": {'annotations': {'percent_encoded': {'tag': 'percent_encoded', 'value': True},
                         'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket'],
         'exact_mappings': ['ARGO:donor.submitter_donor_id']} })
    karyotypicSex: Optional[KaryotypicSex] = Field(default=None, description="""The karyotypic sex of the individual""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}},
         'domain_of': ['Individual']} })
    sex: Optional[Sex] = Field(default=None, description="""The phenotypic sex of the individual ARGO mapping sample_registration::gender (this is complicated as ARGO only have male/female/other which maps to the phenopacket Sex field)""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['Individual', 'Person'],
         'exact_mappings': ['ARGO:sample_registration.gender']} })
    taxonomy: Optional[OntologyClass] = Field(default=None, description="""NCBI taxonomic identifier NCBITaxon e.g. NCBITaxon:9606 or NCBITaxon:1337 For resources where there may be more than one organism being studied it is advisable to indicate the taxonomic identifier of that organism, to its most specific level""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 9}},
         'domain_of': ['Biosample', 'Individual']} })
    timeAtLastEncounter: Optional[TimeElement] = Field(default=None, description="""An TimeElement object describing the age of the individual at the last time of collection. The Age object allows the encoding of the age either as ISO8601 duration or time interval (preferred), or as ontology term object. See http://build.fhir.org/datatypes""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['Individual']} })
    vitalStatus: Optional[VitalStatus] = Field(default=None, description="""Vital status of the individual. If not present it is assumed that the individual is alive. If present it will default to 'false' i.e. the individual was alive when the data was collected. ARGO mapping donor::vital_status""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Individual'],
         'exact_mappings': ['ARGO:donor.vital_status']} })


class VitalStatus(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/individual'})

    causeOfDeath: Optional[OntologyClass] = Field(default=None, description="""ARGO mapping donor::cause_of_death""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['VitalStatus'],
         'exact_mappings': ['ARGO:donor.cause_of_death']} })
    status: Optional[Status] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['VitalStatus']} })
    survivalTimeInDays: Optional[int] = Field(default=None, description="""ARGO mapping donor::survival_time""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['VitalStatus'],
         'exact_mappings': ['ARGO:donor.survival_time']} })
    timeOfDeath: Optional[TimeElement] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['VitalStatus']} })


class DoseInterval(ConfiguredBaseModel):
    """
    e.g. 50mg/ml 3 times daily for two weeks
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/medical_action'})

    interval: Optional[TimeInterval] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['TimeElement', 'ChromosomeLocation', 'DoseInterval']} })
    quantity: Optional[Quantity] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['TypedQuantity', 'Value', 'DoseInterval']} })
    scheduleFrequency: Optional[OntologyClass] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['DoseInterval']} })


class MedicalAction(ConfiguredBaseModel):
    """
    medication, procedure, other actions taken for clinical management
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['ARGO mapping treatment::is_primary_treatment (missing)'],
         'from_schema': 'https://w3id.org/linkml/phenopackets/medical_action',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'action'}},
                    'description': 'ARGO mapping treatment::treatment_type',
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'procedure': {'name': 'procedure',
                                                                                             'required': True}}},
                                                          {'slot_conditions': {'treatment': {'name': 'treatment',
                                                                                             'required': True}}},
                                                          {'slot_conditions': {'radiationTherapy': {'name': 'radiationTherapy',
                                                                                                    'required': True}}},
                                                          {'slot_conditions': {'therapeuticRegimen': {'name': 'therapeuticRegimen',
                                                                                                      'required': True}}}]}}]})

    adverseEvents: Optional[list[OntologyClass]] = Field(default=None, description="""ARGO mapping treatment::adverse_events""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 8}},
         'domain_of': ['MedicalAction'],
         'exact_mappings': ['ARGO:treatment.adverse_events']} })
    procedure: Optional[Procedure] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Measurement', 'Biosample', 'MedicalAction']} })
    radiationTherapy: Optional[RadiationTherapy] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['MedicalAction']} })
    responseToTreatment: Optional[OntologyClass] = Field(default=None, description="""ARGO mapping treatment::response_to_treatment""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}},
         'domain_of': ['MedicalAction'],
         'exact_mappings': ['ARGO:treatment.response_to_treatment']} })
    therapeuticRegimen: Optional[TherapeuticRegimen] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['MedicalAction']} })
    treatment: Optional[Treatment] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['MedicalAction']} })
    treatmentIntent: Optional[OntologyClass] = Field(default=None, description="""Whether the intention of the treatment was curative, palliative, ARGO mapping treatment::treatment_intent""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['MedicalAction'],
         'exact_mappings': ['ARGO:treatment.treatment_intent']} })
    treatmentTarget: Optional[OntologyClass] = Field(default=None, description="""The condition or disease that this treatment was intended to address. FHIR mapping Procedure::reasonCode""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['MedicalAction']} })
    treatmentTerminationReason: Optional[OntologyClass] = Field(default=None, description="""ARGO mapping treatment::treatment_outcome""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 9}},
         'domain_of': ['MedicalAction'],
         'exact_mappings': ['ARGO:treatment.treatment_outcome']} })


class RadiationTherapy(ConfiguredBaseModel):
    """
    RadiationTherapy
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['ARGO mapping radiation::radiation_therapy_type (missing)'],
         'from_schema': 'https://w3id.org/linkml/phenopackets/medical_action'})

    bodySite: OntologyClass = Field(default=..., description="""The anatomical site where radiation therapy was administered. REQUIRED. ARGO mapping radiation::anatomical_site_irradiated""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Procedure', 'RadiationTherapy'],
         'exact_mappings': ['ARGO:radiation.anatomical_site_irradiated']} })
    dosage: int = Field(default=..., description="""The total dose given in units of Gray (Gy). REQUIRED. ARGO mapping radiation::radiation_therapy_dosage""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['RadiationTherapy'],
         'exact_mappings': ['ARGO:radiation.radiation_therapy_dosage']} })
    fractions: int = Field(default=..., description="""The total number of fractions delivered as part of treatment. REQUIRED. ARGO mapping radiation::radiation_therapy_fractions""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['RadiationTherapy'],
         'exact_mappings': ['ARGO:radiation.radiation_therapy_fractions']} })
    modality: OntologyClass = Field(default=..., description="""The modality of radiation therapy (e.g., electron, photon,…). REQUIRED. ARGO mapping radiation::radiation_therapy_modality""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['RadiationTherapy'],
         'exact_mappings': ['ARGO:radiation.radiation_therapy_modality']} })


class TherapeuticRegimen(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/medical_action',
         'rules': [{'annotations': {'oneof': {'tag': 'oneof', 'value': 'identifier'}},
                    'description': 'https://ctep.cancer.gov/protocolDevelopment/policies_nomenclature.htm',
                    'postconditions': {'exactly_one_of': [{'slot_conditions': {'externalReference': {'name': 'externalReference',
                                                                                                     'required': True}}},
                                                          {'slot_conditions': {'ontologyClass': {'name': 'ontologyClass',
                                                                                                 'required': True}}}]}}]})

    endTime: Optional[TimeElement] = Field(default=None, description="""end time can be empty which would indicate ongoing""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['TherapeuticRegimen']} })
    externalReference: Optional[ExternalReference] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['TherapeuticRegimen']} })
    ontologyClass: Optional[OntologyClass] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['TimeElement', 'Value', 'TherapeuticRegimen']} })
    regimenStatus: Optional[RegimenStatus] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['TherapeuticRegimen']} })
    startTime: Optional[TimeElement] = Field(default=None, description="""possibly undefined;""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['TherapeuticRegimen']} })


class Treatment(ConfiguredBaseModel):
    """
    treatment with an agent, such as a drug
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/medical_action'})

    agent: Optional[OntologyClass] = Field(default=None, description="""for instance, DrugCentral, RxNorm Drugbank concept""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Treatment']} })
    cumulativeDose: Optional[Quantity] = Field(default=None, description="""ARGO mapping chemotherapy::cumulative_drug_dosage""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Treatment'],
         'exact_mappings': ['ARGO:chemotherapy.cumulative_drug_dosage']} })
    doseIntervals: Optional[list[DoseInterval]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Treatment']} })
    drugType: Optional[DrugType] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['Treatment']} })
    routeOfAdministration: Optional[OntologyClass] = Field(default=None, description="""For instance, NCIT subhierarchy: Route of Administration (Code C38114)""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Treatment']} })


class Timestamp(ConfiguredBaseModel):
    """
    A Timestamp represents a point in time independent of any time zone or local calendar, encoded as a count of seconds and fractions of seconds at nanosecond resolution. The count is relative to an epoch at UTC midnight on January 1, 1970, in the proleptic Gregorian calendar which extends the Gregorian calendar backwards to year one.  All minutes are 60 seconds long. Leap seconds are \"smeared\" so that no leap second table is needed for interpretation, using a [24-hour linear smear](https://developers.google.com/time/smear).  The range is from 0001-01-01T00:00:00Z to 9999-12-31T23:59:59.999999999Z. By restricting to that range, we ensure that we can convert to and from [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) date strings.  # Examples  Example 1: Compute Timestamp from POSIX `time()`.  Timestamp timestamp; timestamp.set_seconds(time(NULL)); timestamp.set_nanos(0);  Example 2: Compute Timestamp from POSIX `gettimeofday()`.  struct timeval tv; gettimeofday(&tv, NULL);  Timestamp timestamp; timestamp.set_seconds(tv.tv_sec); timestamp.set_nanos(tv.tv_usec * 1000);  Example 3: Compute Timestamp from Win32 `GetSystemTimeAsFileTime()`.  FILETIME ft; GetSystemTimeAsFileTime(&ft); UINT64 ticks = (((UINT64)ft.dwHighDateTime) << 32) | ft.dwLowDateTime;  // A Windows tick is 100 nanoseconds. Windows epoch 1601-01-01T00:00:00Z // is 11644473600 seconds before Unix epoch 1970-01-01T00:00:00Z. Timestamp timestamp; timestamp.set_seconds((INT64) ((ticks / 10000000) - 11644473600LL)); timestamp.set_nanos((INT32) ((ticks % 10000000) * 100));  Example 4: Compute Timestamp from Java `System.currentTimeMillis()`.  long millis = System.currentTimeMillis();  Timestamp timestamp = Timestamp.newBuilder().setSeconds(millis / 1000) .setNanos((int) ((millis % 1000) * 1000000)).build();   Example 5: Compute Timestamp from Java `Instant.now()`.  Instant now = Instant.now();  Timestamp timestamp = Timestamp.newBuilder().setSeconds(now.getEpochSecond()) .setNanos(now.getNano()).build();   Example 6: Compute Timestamp from current time in Python.  timestamp = Timestamp() timestamp.GetCurrentTime()  # JSON Mapping  In JSON format, the Timestamp type is encoded as a string in the [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) format. That is, the format is \"{year}-{month}-{day}T{hour}:{min}:{sec}[.{frac_sec}]Z\" where {year} is always expressed using four digits while {month}, {day}, {hour}, {min}, and {sec} are zero-padded to two digits each. The fractional seconds, which can go up to 9 digits (i.e. up to 1 nanosecond resolution), are optional. The \"Z\" suffix indicates the timezone (\"UTC\"); the timezone is required. A proto3 JSON serializer should always use UTC (as indicated by \"Z\") when printing the Timestamp type and a proto3 JSON parser should be able to accept both UTC and other timezones (as indicated by an offset).  For example, \"2017-01-15T01:30:15.01Z\" encodes 15.01 seconds past 01:30 UTC on January 15, 2017.  In JavaScript, one can convert a Date object to this format using the standard [toISOString()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString) method. In Python, a standard `datetime.datetime` object can be converted to this format using [`strftime`](https://docs.python.org/2/library/time.html#time.strftime) with the time format spec '%Y-%m-%dT%H:%M:%S.%fZ'. Likewise, in Java, one can use the Joda Time's [`ISODateTimeFormat.dateTime()`]( http://www.joda.org/joda-time/apidocs/org/joda/time/format/ISODateTimeFormat.html#dateTime%2D%2D ) to obtain a formatter capable of generating timestamps in this format.  
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/timestamp'})

    nanos: Optional[int] = Field(default=None, description="""Non-negative fractions of a second at nanosecond resolution. Negative second values with fractions must still have non-negative nanos values that count forward in time. Must be from 0 to 999,999,999 inclusive.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Timestamp']} })
    seconds: Optional[int] = Field(default=None, description="""Represents seconds of UTC time since Unix epoch 1970-01-01T00:00:00Z. Must be from 0001-01-01T00:00:00Z to 9999-12-31T23:59:59Z inclusive.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Timestamp']} })


class MetaData(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/meta_data'})

    created: Optional[str] = Field(default=None, description="""ISO8601 UTC timestamp for when this phenopacket was created in ISO \"2018-03-01T00:00:00Z\"""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['MetaData']} })
    createdBy: Optional[str] = Field(default=None, description="""some kind of identifier for the contributor/ program ARGO sample_registration::program_id""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['MetaData']} })
    externalReferences: Optional[list[ExternalReference]] = Field(default=None, description="""External identifiers for this message. These are considered different representation of the same record, not records which are in some other relation with the record at hand. For example this might be a PubMed reference to a study in which the individuals are reported.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}},
         'domain_of': ['MetaData']} })
    phenopacketSchemaVersion: Optional[str] = Field(default=None, description="""phenopacket-schema-version used to create this phenopacket""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['MetaData']} })
    resources: Optional[list[Resource]] = Field(default=None, description="""a listing of the ontologies and resources referenced in the phenopacket""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['MetaData']} })
    submittedBy: Optional[str] = Field(default=None, description="""information about the person/organisation/network that has submitted this phenopacket""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['MetaData']} })
    updates: Optional[list[Update]] = Field(default=None, description="""An OPTIONAL list of Updates to the phenopacket.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['MetaData']} })


class Resource(ConfiguredBaseModel):
    """
    Description of an external resource used for referencing an object. For example the resource may be an ontology such as the HPO or SNOMED. FHIR mapping: CodeSystem (http://www.hl7.org/fhir/codesystem.html)
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/meta_data'})

    id: Optional[str] = Field(default=None, description="""for OBO Ontologies, the value of this string MUST always be the official OBO ID, which is always equivalent to the ID prefix in lower case. Examples: hp, go, mp, mondo Consult http://obofoundry.org for a complete list For other ontologies (e.g. SNOMED), use the prefix in identifiers.org""", json_schema_extra = { "linkml_meta": {'annotations': {'percent_encoded': {'tag': 'percent_encoded', 'value': True},
                         'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket']} })
    iriPrefix: Optional[str] = Field(default=None, description="""Full IRI prefix which can be used with the namespace_prefix and the OntologyClass::id to resolve to an IRI for a term. Tools such as the curie-util (https://github.com/prefixcommons/curie-util) can utilise this to produce fully-resolvable IRIs for an OntologyClass. e.g. Using the HPO term encoding the concept of 'Severe' OntologyClass: id: 'HP:0012828' label: 'Severe' Resource: namespace_prefix: 'HP' iri_prefix: 'http://purl.obolibrary.org/obo/HP_' the term can be resolved to http://purl.obolibrary.org/obo/HP_0012828""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['Resource']} })
    name: Optional[str] = Field(default=None, description="""e.g. The Human Phenotype Ontology for OBO Ontologies, the value of this string SHOULD be the same as the title field on http://obofoundry.org however, this field is purely for information purposes and software should not encode any assumptions""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Extension', 'Resource']} })
    namespacePrefix: Optional[str] = Field(default=None, description="""The prefix used in the CURIE of an OntologyClass e.g. HP, MP, ECO For example an HPO term will have a CURIE like this - HP:0012828 which should be used in combination with the iri_prefix to form a fully-resolvable IRI""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Resource']} })
    url: Optional[str] = Field(default=None, description="""For OBO ontologies, this should always be the PURL, e.g. http://purl.obolibrary.org/obo/hp.owl, http://purl.obolibrary.org/obo/hp.obo""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Resource']} })
    version: Optional[str] = Field(default=None, description="""for OBO ontologies, this should be the versionIRI""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['Expression', 'Resource']} })


class Update(ConfiguredBaseModel):
    """
    Information about when an update to a record occurred, who or what made the update and any pertinent information regarding the content and/or reason for the update
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/meta_data'})

    comment: Optional[str] = Field(default=None, description="""Textual comment about the changes made to the content and/or reason for the update. OPTIONAL""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}}, 'domain_of': ['Update']} })
    timestamp: str = Field(default=..., description="""ISO8601 UTC timestamps at which this record was updated, in the format YYYY-MM-DDTHH:MM:SS.SSSZ e.g. 2007-12-03T10:15:30.00Z REQUIRED""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['TimeElement', 'Update']} })
    updatedBy: Optional[str] = Field(default=None, description="""Information about the person/organisation/network that has updated the phenopacket. OPTIONAL""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}}, 'domain_of': ['Update']} })


class Pedigree(ConfiguredBaseModel):
    """
    https://software.broadinstitute.org/gatk/documentation/article?id=11016
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/pedigree'})

    persons: Optional[list[Person]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['Pedigree']} })


class Person(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/pedigree'})

    affectedStatus: Optional[AffectedStatus] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}}, 'domain_of': ['Person']} })
    familyId: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 1}}, 'domain_of': ['Person']} })
    individualId: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Biosample', 'Person']} })
    maternalId: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}}, 'domain_of': ['Person']} })
    paternalId: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}}, 'domain_of': ['Person']} })
    sex: Optional[Sex] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Individual', 'Person']} })


class Cohort(ConfiguredBaseModel):
    """
    A group of individuals related in some phenotypic or genotypic aspect.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/phenopackets'})

    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['ExternalReference',
                       'Measurement',
                       'PhenotypicFeature',
                       'Biosample',
                       'GeneDescriptor',
                       'VariationDescriptor',
                       'Cohort']} })
    files: Optional[list[File]] = Field(default=None, description="""Pointer to relevant file(s) for the cohort. Files relating exclusively to individual phenopackets should be contained in the Phenopacket.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['Biosample', 'Cohort', 'Family', 'Phenopacket']} })
    id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'percent_encoded': {'tag': 'percent_encoded', 'value': True},
                         'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket']} })
    members: Optional[list[Phenopacket]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Haplotype', 'VariationSet', 'Cohort']} })
    metaData: MetaData = Field(default=..., description="""Structured definitions of the resources and ontologies used within the phenopacket. REQUIRED""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Cohort', 'Family', 'Phenopacket']} })


class Family(ConfiguredBaseModel):
    """
    Phenotype, sample and pedigree data required for a genomic diagnosis. Equivalent to the Genomics England InterpretationRequestRD https://github.com/genomicsengland/GelReportModels/blob/master/schemas/IDLs/org.gel.models.report.avro/5.0.0/InterpretationRequestRD.avdl
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/phenopackets'})

    consanguinousParents: Optional[bool] = Field(default=None, description="""flag to indicate that the parents of the proband are consanguinous""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}}, 'domain_of': ['Family']} })
    files: Optional[list[File]] = Field(default=None, description="""Pointer to the relevant file(s) for the family. These should be files relating to one or more of the family members e.g a multi-sample VCF. Files relating exclusively to individual phenopackets should be contained in the Phenopacket.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Biosample', 'Cohort', 'Family', 'Phenopacket']} })
    id: Optional[str] = Field(default=None, description="""An identifier specific for this family.""", json_schema_extra = { "linkml_meta": {'annotations': {'percent_encoded': {'tag': 'percent_encoded', 'value': True},
                         'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket']} })
    metaData: MetaData = Field(default=..., description="""Structured definitions of the resources and ontologies used within the phenopacket. REQUIRED""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['Cohort', 'Family', 'Phenopacket']} })
    pedigree: Optional[Pedigree] = Field(default=None, description="""The pedigree defining the relations between the proband and their relatives. Pedigree.individual_id should map to the PhenoPacket.Individual.id""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}}, 'domain_of': ['Family']} })
    proband: Optional[Phenopacket] = Field(default=None, description="""The individual representing the focus of this packet - e.g. the proband in rare disease cases or cancer patient""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}}, 'domain_of': ['Family']} })
    relatives: Optional[list[Phenopacket]] = Field(default=None, description="""Individuals related in some way to the patient. For instance, the individuals may be genetically related or may be members of a cohort. If this field is used, then  it is expected that a pedigree will be included for genetically related individuals for use cases such as genomic diagnostics. If a phenopacket is being used to describe one member of a cohort, then in general one phenopacket will be created for each of the individuals in the cohort.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}}, 'domain_of': ['Family']} })


class Phenopacket(ConfiguredBaseModel):
    """
    An anonymous phenotypic description of an individual or biosample with potential genes of interest and/or diagnoses.  This is a bundle of high-level concepts with no specifically defined relational concepts. It is expected that the resources sharing the phenopackets will define and enforce their own semantics and level of requirements for included fields.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/phenopackets/phenopackets',
         'tree_root': True})

    biosamples: Optional[list[Biosample]] = Field(default=None, description="""Biosample(s) derived from the patient or a collection of biosamples in isolation""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 5}},
         'domain_of': ['Phenopacket']} })
    diseases: Optional[list[Disease]] = Field(default=None, description="""Field for disease identifiers - could be used for listing either diagnosed or suspected conditions. The resources using these fields should define what this represents in their context.""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 7}},
         'domain_of': ['Phenopacket']} })
    files: Optional[list[File]] = Field(default=None, description="""Pointer to the relevant file(s) for the individual""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 10}},
         'domain_of': ['Biosample', 'Cohort', 'Family', 'Phenopacket']} })
    id: Optional[str] = Field(default=None, description="""An identifier specific for this phenopacket.""", json_schema_extra = { "linkml_meta": {'annotations': {'percent_encoded': {'tag': 'percent_encoded', 'value': True},
                         'rank': {'tag': 'rank', 'value': 1}},
         'domain_of': ['ExternalReference',
                       'OntologyClass',
                       'Biosample',
                       'VariationDescriptor',
                       'VcfRecord',
                       'Interpretation',
                       'Individual',
                       'Resource',
                       'Cohort',
                       'Family',
                       'Phenopacket']} })
    interpretations: Optional[list[Interpretation]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 6}},
         'domain_of': ['Phenopacket']} })
    measurements: Optional[list[Measurement]] = Field(default=None, description="""Quantifiable measurements related to the individual""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 4}},
         'domain_of': ['Biosample', 'Phenopacket']} })
    medicalActions: Optional[list[MedicalAction]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 9}},
         'domain_of': ['Phenopacket']} })
    metaData: MetaData = Field(default=..., description="""Structured definitions of the resources and ontologies used within the phenopacket. REQUIRED""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 11}},
         'domain_of': ['Cohort', 'Family', 'Phenopacket']} })
    phenotypicFeatures: Optional[list[PhenotypicFeature]] = Field(default=None, description="""Phenotypic features relating to the subject of the phenopacket""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 3}},
         'domain_of': ['Biosample', 'Phenopacket']} })
    subject: Optional[Individual] = Field(default=None, description="""The individual representing the focus of this packet - e.g. the proband in rare disease cases or cancer patient""", json_schema_extra = { "linkml_meta": {'annotations': {'rank': {'tag': 'rank', 'value': 2}},
         'domain_of': ['Phenopacket']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Age.model_rebuild()
AgeRange.model_rebuild()
DictionaryEntry.model_rebuild()
Evidence.model_rebuild()
ExternalReference.model_rebuild()
File.model_rebuild()
GestationalAge.model_rebuild()
OntologyClass.model_rebuild()
Procedure.model_rebuild()
TimeElement.model_rebuild()
TimeInterval.model_rebuild()
ComplexValue.model_rebuild()
Measurement.model_rebuild()
Quantity.model_rebuild()
ReferenceRange.model_rebuild()
TypedQuantity.model_rebuild()
Value.model_rebuild()
PhenotypicFeature.model_rebuild()
Biosample.model_rebuild()
Disease.model_rebuild()
Any.model_rebuild()
Abundance.model_rebuild()
Allele.model_rebuild()
ChromosomeLocation.model_rebuild()
CopyNumber.model_rebuild()
CytobandInterval.model_rebuild()
DefiniteRange.model_rebuild()
DerivedSequenceExpression.model_rebuild()
Feature.model_rebuild()
Gene.model_rebuild()
Haplotype.model_rebuild()
HaplotypeMember.model_rebuild()
IndefiniteRange.model_rebuild()
LiteralSequenceExpression.model_rebuild()
Location.model_rebuild()
MolecularVariation.model_rebuild()
Number.model_rebuild()
RepeatedSequenceExpression.model_rebuild()
SequenceExpression.model_rebuild()
SequenceInterval.model_rebuild()
SequenceLocation.model_rebuild()
SequenceState.model_rebuild()
SimpleInterval.model_rebuild()
SystemicVariation.model_rebuild()
Text.model_rebuild()
UtilityVariation.model_rebuild()
Variation.model_rebuild()
VariationSet.model_rebuild()
VariationSetMember.model_rebuild()
Expression.model_rebuild()
Extension.model_rebuild()
GeneDescriptor.model_rebuild()
VariationDescriptor.model_rebuild()
VcfRecord.model_rebuild()
Diagnosis.model_rebuild()
GenomicInterpretation.model_rebuild()
Interpretation.model_rebuild()
VariantInterpretation.model_rebuild()
Individual.model_rebuild()
VitalStatus.model_rebuild()
DoseInterval.model_rebuild()
MedicalAction.model_rebuild()
RadiationTherapy.model_rebuild()
TherapeuticRegimen.model_rebuild()
Treatment.model_rebuild()
Timestamp.model_rebuild()
MetaData.model_rebuild()
Resource.model_rebuild()
Update.model_rebuild()
Pedigree.model_rebuild()
Person.model_rebuild()
Cohort.model_rebuild()
Family.model_rebuild()
Phenopacket.model_rebuild()
