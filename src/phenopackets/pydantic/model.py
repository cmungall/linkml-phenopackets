from __future__ import annotations 
from datetime import (
    datetime,
    date
)
from decimal import Decimal 
from enum import Enum 
import re
import sys
from typing import (
    Any,
    List,
    Literal,
    Dict,
    Optional,
    Union
)
from pydantic.version import VERSION  as PYDANTIC_VERSION 
if int(PYDANTIC_VERSION[0])>=2:
    from pydantic import (
        BaseModel,
        ConfigDict,
        Field,
        field_validator
    )
else:
    from pydantic import (
        BaseModel,
        Field,
        validator
    )

metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass


class AllelicStateTerms(str, Enum):
    # heterozygous
    HETEROZYGOUS = "HETEROZYGOUS"
    # homozygous
    HOMOZYGOUS = "HOMOZYGOUS"
    # hemizygous
    HEMIZYGOUS = "HEMIZYGOUS"


class AssaysTerms(str, Enum):
    # Creatine kinase [Enzymatic activity/volume] in Serum or Plasma
    CREATINE_KINASE = "CREATINE_KINASE"


class GenderTerms(str, Enum):
    # Identifies as male
    IDENTIFIES_AS_MALE = "IDENTIFIES_AS_MALE"
    # Identifies as female
    IDENTIFIES_AS_FEMALE = "IDENTIFIES_AS_FEMALE"
    # Female-to-male transsexual
    FEMALE_TO_MALE_TRANSSEXUAL = "FEMALE_TO_MALE_TRANSSEXUAL"
    # Male-to-female transsexual
    MALE_TO_FEMALE_TRANSSEXUAL = "MALE_TO_FEMALE_TRANSSEXUAL"
    # Identifies as non-conforming
    IDENTIFIES_AS_NON_CONFORMING = "IDENTIFIES_AS_NON_CONFORMING"
    # other
    OTHER_GENDER = "OTHER_GENDER"
    # Asked but unknown
    ASKED_BUT_UNKNOWN = "ASKED_BUT_UNKNOWN"


class LateralityTerms(str, Enum):
    # Right
    RIGHT = "RIGHT"
    # Left
    LEFT = "LEFT"
    # Unilateral
    UNILATERAL = "UNILATERAL"
    # Bilateral
    BILATERAL = "BILATERAL"


class MedicalActionsTerms(str, Enum):
    # Adverse Event
    ADVERSE_EVENT = "ADVERSE_EVENT"
    # Four Times Daily
    FOUR_TIMES_DAILY = "FOUR_TIMES_DAILY"
    # Intraarterial Route of Administration
    INTRA_ARTERIAL = "INTRA_ARTERIAL"
    # Intravenous Route of Administration
    IV_ADMINISTRATION = "IV_ADMINISTRATION"
    # Oral Route of Administration
    ORAL_ADMINISTRATION = "ORAL_ADMINISTRATION"
    # Once
    ONCE = "ONCE"
    # Once Daily
    ONCE_DAILY = "ONCE_DAILY"
    # Three Times Daily
    THREE_TIMES_DAILY = "THREE_TIMES_DAILY"
    # Twice Daily
    TWICE_DAILY = "TWICE_DAILY"


class OnsetTerms(str, Enum):
    # Antenatal onset
    ANTENATAL_ONSET = "ANTENATAL_ONSET"
    # Embryonal onset
    EMBRYONAL_ONSET = "EMBRYONAL_ONSET"
    # Fetal onset
    FETAL_ONSET = "FETAL_ONSET"
    # Late first trimester onset
    LATE_FIRST_TRIMESTER_ONSET = "LATE_FIRST_TRIMESTER_ONSET"
    # Second trimester onset
    SECOND_TRIMESTER_ONSET = "SECOND_TRIMESTER_ONSET"
    # Third trimester onset
    THIRD_TRIMESTER_ONSET = "THIRD_TRIMESTER_ONSET"
    # Congenital onset
    CONGENITAL_ONSET = "CONGENITAL_ONSET"
    # Neonatal onset
    NEONATAL_ONSET = "NEONATAL_ONSET"
    # Infantile onset
    INFANTILE_ONSET = "INFANTILE_ONSET"
    # Childhood onset
    CHILDHOOD_ONSET = "CHILDHOOD_ONSET"
    # Juvenile onset
    JUVENILE_ONSET = "JUVENILE_ONSET"
    # Adult onset
    ADULT_ONSET = "ADULT_ONSET"
    # Young adult onset
    YOUNG_ADULT_ONSET = "YOUNG_ADULT_ONSET"
    # Early young adult onset
    EARLY_YOUNG_ADULT_ONSET = "EARLY_YOUNG_ADULT_ONSET"
    # Intermediate young adult onset
    INTERMEDIATE_YOUNG_ADULT_ONSET = "INTERMEDIATE_YOUNG_ADULT_ONSET"
    # Late young adult onset
    LATE_YOUNG_ADULT_ONSET = "LATE_YOUNG_ADULT_ONSET"
    # Middle age onset
    MIDDLE_AGE_ONSET = "MIDDLE_AGE_ONSET"
    # Late onset
    LATE_ONSET = "LATE_ONSET"


class OrganTerms(str, Enum):
    # brain
    BRAIN = "BRAIN"
    # cerebellum
    CEREBELLUM = "CEREBELLUM"
    # ear
    EAR = "EAR"
    # eye
    EYE = "EYE"
    # heart
    HEART = "HEART"
    # kidney
    KIDNEY = "KIDNEY"
    # large intestine
    LARGE_INTESTINE = "LARGE_INTESTINE"
    # liver
    LIVER = "LIVER"
    # lung
    LUNG = "LUNG"
    # nose
    NOSE = "NOSE"
    # small intestine
    SMALL_INTESTINE = "SMALL_INTESTINE"
    # spinal cord
    SPINAL_CORD = "SPINAL_CORD"
    # spleen
    SPLEEN = "SPLEEN"
    # tongue
    TONGUE = "TONGUE"
    # thymus
    THYMUS = "THYMUS"


class ResponseTerms(str, Enum):
    # Favorable
    FAVORABLE = "FAVORABLE"
    # Unfavorable
    UNFAVORABLE = "UNFAVORABLE"


class SpatialPatternTerms(str, Enum):
    # Predominant small joint localization
    PREDOMINANT_SMALL_JOINT_LOCALIZATION = "PREDOMINANT_SMALL_JOINT_LOCALIZATION"
    # Polycyclic
    POLYCYCLIC = "POLYCYCLIC"
    # Axial
    AXIAL = "AXIAL"
    # Perilobular
    PERILOBULAR = "PERILOBULAR"
    # Paraseptal
    PARASEPTAL = "PARASEPTAL"
    # Bronchocentric
    BRONCHOCENTRIC = "BRONCHOCENTRIC"
    # Centrilobular
    CENTRILOBULAR = "CENTRILOBULAR"
    # Miliary
    MILIARY = "MILIARY"
    # Generalized
    GENERALIZED = "GENERALIZED"
    # Perilymphatic
    PERILYMPHATIC = "PERILYMPHATIC"
    # Localized
    LOCALIZED = "LOCALIZED"
    # Reticular
    RETICULAR = "RETICULAR"
    # Distal
    DISTAL = "DISTAL"
    # Central
    CENTRAL = "CENTRAL"
    # Upper-body predominance
    UPPER_BODY_PREDOMINANCE = "UPPER_BODY_PREDOMINANCE"
    # Joint extensor surface localization
    JOINT_EXTENSOR_SURFACE_LOCALIZATION = "JOINT_EXTENSOR_SURFACE_LOCALIZATION"
    # Herpetiform
    HERPETIFORM = "HERPETIFORM"
    # Morbilliform
    MORBILLIFORM = "MORBILLIFORM"
    # Pericentral
    PERICENTRAL = "PERICENTRAL"
    # Dermatomal
    DERMATOMAL = "DERMATOMAL"
    # Midperipheral
    MIDPERIPHERAL = "MIDPERIPHERAL"
    # Distributed along Blaschko lines
    DISTRIBUTED_ALONG_BLASCHKO_LINES = "DISTRIBUTED_ALONG_BLASCHKO_LINES"
    # Acral
    ACRAL = "ACRAL"
    # Paracentral
    PARACENTRAL = "PARACENTRAL"
    # Lateral
    LATERAL = "LATERAL"
    # Peripheral
    PERIPHERAL = "PERIPHERAL"
    # Lower-body predominance
    LOWER_BODY_PREDOMINANCE = "LOWER_BODY_PREDOMINANCE"
    # Diffuse
    DIFFUSE = "DIFFUSE"
    # Proximal
    PROXIMAL = "PROXIMAL"
    # Apical
    APICAL = "APICAL"
    # Focal
    FOCAL = "FOCAL"
    # Multifocal
    MULTIFOCAL = "MULTIFOCAL"
    # Jointflexorsurfacelocalization
    JOINT_FLEXOR_SURFACE_LOCALIZATION = "JOINT_FLEXOR_SURFACE_LOCALIZATION"


class UnitTerms(str, Enum):
    # degree (plane angle)
    DEGREE = "DEGREE"
    # diopter
    DIOPTER = "DIOPTER"
    # gram
    GRAM = "GRAM"
    # gram per kilogram
    GRAM_PER_KG = "GRAM_PER_KG"
    # kiligram
    KILIGRAM = "KILIGRAM"
    # liter
    LITER = "LITER"
    # meter
    METER = "METER"
    # microgram
    MICROGRAM = "MICROGRAM"
    # microgram per deciliter
    MICROGRAM_PER_DECILITER = "MICROGRAM_PER_DECILITER"
    # microgram per liter
    MICROGRAM_PER_LITER = "MICROGRAM_PER_LITER"
    # microliter
    MICROLITER = "MICROLITER"
    # micrometer
    MICROMETER = "MICROMETER"
    # milligram
    MILLIGRAM = "MILLIGRAM"
    # milligram per day
    MILLIGRAM_PER_DAY = "MILLIGRAM_PER_DAY"
    # milligram per deciliter
    MILLIGRAM_PER_DL = "MILLIGRAM_PER_DL"
    # milligram per kilogram
    MILLIGRAM_PER_KG = "MILLIGRAM_PER_KG"
    # milliliter
    MILLILITER = "MILLILITER"
    # millimeter
    MILLIMETER = "MILLIMETER"
    # millimetres of mercury
    MILLIMETRES_OF_MERCURY = "MILLIMETRES_OF_MERCURY"
    # millimole
    MILLIMOLE = "MILLIMOLE"
    # mole
    MOLE = "MOLE"
    # mole per liter
    MOLE_PER_LITER = "MOLE_PER_LITER"
    # mole per milliliter
    MOLE_PER_MILLILITER = "MOLE_PER_MILLILITER"
    # enzyme unit per liter
    ENZYME_UNIT_PER_LITER = "ENZYME_UNIT_PER_LITER"


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
    genomic = "genomic"
    protein = "protein"
    transcript = "transcript"
    unspecified_molecule_context = "unspecified_molecule_context"


class AcmgPathogenicityClassification(str, Enum):
    BENIGN = "BENIGN"
    LIKELY_BENIGN = "LIKELY_BENIGN"
    LIKELY_PATHOGENIC = "LIKELY_PATHOGENIC"
    NOT_PROVIDED = "NOT_PROVIDED"
    PATHOGENIC = "PATHOGENIC"
    UNCERTAIN_SIGNIFICANCE = "UNCERTAIN_SIGNIFICANCE"


class InterpretationStatus(str, Enum):
    CANDIDATE = "CANDIDATE"
    CAUSATIVE = "CAUSATIVE"
    CONTRIBUTORY = "CONTRIBUTORY"
    REJECTED = "REJECTED"
    UNKNOWN_STATUS = "UNKNOWN_STATUS"


class ProgressStatus(str, Enum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    SOLVED = "SOLVED"
    UNKNOWN_PROGRESS = "UNKNOWN_PROGRESS"
    UNSOLVED = "UNSOLVED"


class TherapeuticActionability(str, Enum):
    ACTIONABLE = "ACTIONABLE"
    NOT_ACTIONABLE = "NOT_ACTIONABLE"
    UNKNOWN_ACTIONABILITY = "UNKNOWN_ACTIONABILITY"


class KaryotypicSex(str, Enum):
    """
    Karyotypic sex of the individual
    """
    OTHER_KARYOTYPE = "OTHER_KARYOTYPE"
    UNKNOWN_KARYOTYPE = "UNKNOWN_KARYOTYPE"
    XO = "XO"
    XX = "XX"
    XXX = "XXX"
    XXXX = "XXXX"
    XXXY = "XXXY"
    XXY = "XXY"
    XXYY = "XXYY"
    XY = "XY"
    XYY = "XYY"


class Sex(str, Enum):
    """
    Sex of an individual FHIR mapping: AdministrativeGender (https://www.hl7.org/fhir/codesystem-administrative-gender.html)
    """
    # Female
    FEMALE = "FEMALE"
    # Male
    MALE = "MALE"
    # It is not possible, to accurately assess the applicability of MALE/FEMALE.
    OTHER_SEX = "OTHER_SEX"
    # Not assessed / available.
    UNKNOWN_SEX = "UNKNOWN_SEX"


class Status(str, Enum):
    """
    Default = false i.e. the individual is alive. MUST be true if
    """
    ALIVE = "ALIVE"
    DECEASED = "DECEASED"
    UNKNOWN_STATUS = "UNKNOWN_STATUS"


class DrugType(str, Enum):
    """
    A simplified version of ODHSI-DRUG_EXPOSURE
    """
    ADMINISTRATION_RELATED_TO_PROCEDURE = "ADMINISTRATION_RELATED_TO_PROCEDURE"
    EHR_MEDICATION_LIST = "EHR_MEDICATION_LIST"
    PRESCRIPTION = "PRESCRIPTION"
    UNKNOWN_DRUG_TYPE = "UNKNOWN_DRUG_TYPE"


class RegimenStatus(str, Enum):
    COMPLETED = "COMPLETED"
    DISCONTINUED = "DISCONTINUED"
    STARTED = "STARTED"
    UNKNOWN_STATUS = "UNKNOWN_STATUS"


class AffectedStatus(str, Enum):
    AFFECTED = "AFFECTED"
    MISSING = "MISSING"
    UNAFFECTED = "UNAFFECTED"


class Age(ConfiguredBaseModel):
    """
    See http://build.fhir.org/datatypes and http://build.fhir.org/condition-definitions.html#Condition.onset_x_ In FHIR this is represented as a UCUM measurement - http://unitsofmeasure.org/trac/
    """
    iso8601duration: Optional[str] = Field(None, description="""The :ref:`ISO 8601<metadata_date_time>` age of this object as ISO8601 duration or time intervals. e.g. P40Y10M05D)""")


class AgeRange(ConfiguredBaseModel):
    end: Optional[Age] = Field(None)
    start: Optional[Age] = Field(None)


class Dictionary(ConfiguredBaseModel):
    pass


class Evidence(ConfiguredBaseModel):
    """
    FHIR mapping: Condition.evidence (https://www.hl7.org/fhir/condition-definitions.html#Condition.evidence)
    """
    evidenceCode: Optional[OntologyClass] = Field(None, description="""The encoded evidence type using, for example the Evidence & Conclusion Ontology (ECO - http://purl.obolibrary.org/obo/eco.owl) FHIR mapping: Condition.evidence.code""")
    reference: Optional[ExternalReference] = Field(None, description="""FHIR mapping: Condition.evidence.detail""")


class ExternalReference(ConfiguredBaseModel):
    """
    FHIR mapping: Reference (https://www.hl7.org/fhir/references.html)
    """
    description: Optional[str] = Field(None, description="""Human readable title or display string for the reference FHIR mapping: Reference.display""")
    id: Optional[str] = Field(None, description="""e.g. ISBN, PMID:123456, DOI:..., FHIR mapping: Reference.identifier""")
    reference: Optional[str] = Field(None, description="""A full or partial URL pointing to the external reference if no commonly resolvable identifier can be used in the `id` field FHIR mapping Reference.reference""")


class File(ConfiguredBaseModel):
    fileAttributes: Optional[Dictionary] = Field(None, description="""Map of attributes describing the file. For example the File format or genome assembly would be defied here. For genomic data files there MUST be a 'genomeAssembly' key.""")
    individualToFileIdentifiers: Optional[Dictionary] = Field(None, description="""A map of identifiers mapping an individual to a sample in the file. The key values must correspond to the Individual::id for the individuals in the message, the values must map to the samples in the file.""")
    uri: Optional[str] = Field(None, description="""URI for the file e.g. file://data/genomes/file1.vcf.gz or https://opensnp.org/data/60.23andme-exome-vcf.231?1341012444""")


class GestationalAge(ConfiguredBaseModel):
    days: Optional[int] = Field(None)
    weeks: Optional[int] = Field(None)


class OntologyClass(ConfiguredBaseModel):
    """
    A class (aka term, concept) in an ontology. FHIR mapping: CodeableConcept (http://www.hl7.org/fhir/datatypes.html#CodeableConcept) see also Coding (http://www.hl7.org/fhir/datatypes.html#Coding)
    """
    id: str = Field(..., description="""a CURIE-style identifier e.g. HP:0100024, MP:0001284, UBERON:0001690. This is the primary key for the ontology class REQUIRED!""")
    label: Optional[str] = Field(None, description="""class label, aka name. E.g. \"Abnormality of cardiovascular system\"""")


class Procedure(ConfiguredBaseModel):
    """
    A clinical procedure performed on a subject. By preference a single concept to indicate both the procedure and the body site should be used. In cases where this is not possible, the body site should be indicated using a separate ontology class. e.g. {\"code\":{\"NCIT:C51585\": \"Biopsy of Soft Palate\"}} {\"code\":{\"NCIT:C28743\": \"Punch Biopsy\"}, \"body_site\":{\"UBERON:0003403\": \"skin of forearm\"}} - a punch biopsy of the skin from the forearm FHIR mapping: Procedure (https://www.hl7.org/fhir/procedure.html)
    """
    bodySite: Optional[OntologyClass] = Field(None, description="""FHIR mapping: Procedure.bodySite""")
    code: Optional[OntologyClass] = Field(None, description="""FHIR mapping: Procedure.code""")
    performed: Optional[TimeElement] = Field(None, description="""When the procedure was performed.""")


class TimeElement(ConfiguredBaseModel):
    age: Optional[Age] = Field(None)
    ageRange: Optional[AgeRange] = Field(None)
    gestationalAge: Optional[GestationalAge] = Field(None)
    interval: Optional[TimeInterval] = Field(None)
    ontologyClass: Optional[OntologyClass] = Field(None)
    timestamp: Optional[str] = Field(None)


class TimeInterval(ConfiguredBaseModel):
    end: Optional[str] = Field(None)
    start: Optional[str] = Field(None)


class ComplexValue(ConfiguredBaseModel):
    typedQuantities: Optional[List[TypedQuantity]] = Field(default_factory=list, description="""The quantities required to fully describe the complex value. For example the systolic and diastolic blood pressure quantities""")


class Measurement(ConfiguredBaseModel):
    """
    FHIR mapping: Observation (https://www.hl7.org/fhir/observation.html)
    """
    assay: Optional[OntologyClass] = Field(None, description="""An ontology class which describes the assay used to produce the measurement. For example \"body temperature\" (CMO:0000015) or \"Platelets [#/volume] in Blood\" (LOINC:26515-7) FHIR mapping: Observation.code""")
    complexValue: Optional[ComplexValue] = Field(None)
    description: Optional[str] = Field(None, description="""Free-text description of the feature. Note this is not a acceptable place to document/describe the phenotype - the type and onset etc... fields should be used for this purpose.""")
    procedure: Optional[Procedure] = Field(None, description="""Clinical procedure performed on the subject in order to produce the measurement.""")
    timeObserved: Optional[TimeElement] = Field(None, description="""The time at which the measurement was made""")
    value: Optional[Value] = Field(None)


class Quantity(ConfiguredBaseModel):
    referenceRange: Optional[ReferenceRange] = Field(None, description="""Reference range for the quantity e.g. The normal range of platelets is 150,000 to 450,000 platelets/uL.""")
    unit: Optional[OntologyClass] = Field(None, description="""For instance, NCIT subhierarchy, Unit of Measure (Code C25709), https://www.ebi.ac.uk/ols/ontologies/uo""")
    value: Optional[float] = Field(None, description="""the  value of the quantity in the units  e.g. 2.0 mg""")


class ReferenceRange(ConfiguredBaseModel):
    high: Optional[float] = Field(None)
    low: Optional[float] = Field(None)
    unit: Optional[OntologyClass] = Field(None)


class TypedQuantity(ConfiguredBaseModel):
    """
    For complex measurements, such as blood pressure where more than one component quantity is required to describe the measurement
    """
    quantity: Optional[Quantity] = Field(None, description="""e.g. mm Hg""")
    type: Optional[OntologyClass] = Field(None, description="""e.g. diastolic, systolic""")


class Value(ConfiguredBaseModel):
    ontologyClass: Optional[OntologyClass] = Field(None, description="""for use with things such as categories 'red', 'yellow' or 'absent'/'present'""")
    quantity: Optional[Quantity] = Field(None)


class PhenotypicFeature(ConfiguredBaseModel):
    """
    An individual phenotypic feature, observed as either present or absent (negated), with possible onset, modifiers and frequency FHIR mapping: Condition (https://www.hl7.org/fhir/condition.html) or Observation (https://www.hl7.org/fhir/observation.html)
    """
    description: Optional[str] = Field(None, description="""Free-text description of the phenotype. Note this is not a acceptable place to document/describe the phenotype - the type and onset etc... fields should be used for this purpose.""")
    evidence: Optional[List[Evidence]] = Field(default_factory=list, description="""Evidences for how the phenotype was determined.""")
    excluded: Optional[bool] = Field(None, description="""Flag to indicate whether the phenotype was observed or not. Default is 'false', in other words the phenotype was observed. Therefore it is only required in cases to indicate that the phenotype was looked for, but found to be absent. More formally, this modifier indicates the logical negation of the OntologyClass used in the 'type' field. *CAUTION* It is imperative to check this field for correct interpretation of the phenotype!""")
    modifiers: Optional[List[OntologyClass]] = Field(default_factory=list, description="""subclasses of HP:0012823 ! Clinical modifier apart from Severity HP:0012824 - Severity""")
    onset: Optional[TimeElement] = Field(None, description="""the values of this will come from the HPO onset hierarchy i.e. subclasses of HP:0003674 FHIR mapping: Condition.onset""")
    resolution: Optional[TimeElement] = Field(None)
    severity: Optional[OntologyClass] = Field(None, description="""Severity of the condition e.g. subclasses of HP:0012824-Severity or SNOMED:272141005-Severities FHIR mapping: Condition.severity""")
    type: Optional[OntologyClass] = Field(None, description="""The primary ontology class which describes the phenotype. For example \"HP:0001363\"  \"Craniosynostosis\" FHIR mapping: Condition.identifier""")


class Biosample(ConfiguredBaseModel):
    """
    A Biosample refers to a unit of biological material from which the substrate molecules (e.g. genomic DNA, RNA, proteins) for molecular analyses (e.g. sequencing, array hybridisation, mass-spectrometry) are extracted. Examples would be a tissue biopsy, a single cell from a culture for single cell genome sequencing or a protein fraction from a gradient centrifugation. Several instances (e.g. technical replicates) or types of experiments (e.g. genomic array as well as RNA-seq experiments) may refer to the same Biosample. FHIR mapping: Specimen (http://www.hl7.org/fhir/specimen.html).
    """
    derivedFromId: Optional[str] = Field(None, description="""The id of the parent biosample this biosample was derived from.""")
    description: Optional[str] = Field(None, description="""The biosample's description. This attribute contains human readable text. The \"description\" attributes should not contain any structured data.""")
    diagnosticMarkers: Optional[List[OntologyClass]] = Field(default_factory=list, description="""Clinically relevant bio markers. Most of the assays such as IHC are covered by the NCIT under the sub-hierarchy NCIT:C25294 (Laboratory Procedure). e.g. NCIT:C68748 (HER2/Neu Positive), NCIT:C131711 (Human Papillomavirus-18 Positive)""")
    files: Optional[List[File]] = Field(default_factory=list, description="""Pointer to the relevant file(s) for the biosample. Files relating to the entire individual e.g. a germline exome/genome should be associated with the Phenopacket rather than the Biosample it was derived from.""")
    histologicalDiagnosis: Optional[OntologyClass] = Field(None, description="""This is the pathologist’s diagnosis and may often represent a refinement of the clinical diagnosis given in the Patient/Clinical module. Should use the same terminology as diagnosis, but represent the pathologist’s findings. Normal samples would be tagged with the term \"NCIT:C38757\", \"Negative Finding\" ARGO mapping specimen::tumour_histological_type""")
    id: Optional[str] = Field(None, description="""biosamples SAMN08666232 Human Cell Atlas The Biosample id This is unique in the context of the server instance. ARGO mapping specimen::submitter_specimen_id""")
    individualId: Optional[str] = Field(None, description="""The id of the individual this biosample was derived from. ARGO mapping specimen::submitter_donor_id""")
    materialSample: Optional[OntologyClass] = Field(None, description="""This element can be used to specify the status of the sample. For instance, a status may be used as a normal control, often in combination with another sample that is thought to contain a pathological finding. We recommend use of ontology terms such as: EFO:0009654 (reference sample) or EFO:0009655 (abnormal sample) ARGO mapping sample_registration::tumour_normal_designation""")
    measurements: Optional[List[Measurement]] = Field(default_factory=list)
    pathologicalStage: Optional[OntologyClass] = Field(None, description="""ARGO mapping specimen::pathological_tumour_staging_system ARGO mapping specimen::pathological_stage_group""")
    pathologicalTnmFinding: Optional[List[OntologyClass]] = Field(default_factory=list, description="""ARGO mapping specimen::pathological_t_category ARGO mapping specimen::pathological_n_category ARGO mapping specimen::pathological_m_category""")
    phenotypicFeatures: Optional[List[PhenotypicFeature]] = Field(default_factory=list, description="""Phenotypic characteristics of the BioSample, for example histological findings of a biopsy.""")
    procedure: Optional[Procedure] = Field(None, description="""Clinical procedure performed on the subject in order to extract the biosample. ARGO mapping specimen::specimen_anatomic_location - Procedure::body_site ARGO mapping specimen::specimen_acquisition_interval - Procedure::time_performed""")
    sampleProcessing: Optional[OntologyClass] = Field(None, description="""Field to represent how the sample was processed. ARGO mapping specimen::specimen_processing""")
    sampleStorage: Optional[OntologyClass] = Field(None, description="""Field to represent how the sample was stored ARGO mapping specimen::specimen_storage""")
    sampleType: Optional[OntologyClass] = Field(None, description="""Recommended use of EFO term to describe the sample. e.g. Amplified DNA, ctDNA, Total RNA, Lung tissue, Cultured cells... ARGO mapping sample_registration::sample_type""")
    sampledTissue: Optional[OntologyClass] = Field(None, description="""UBERON class describing the tissue from which the specimen was collected. PDX-MI mapping: 'Specimen tumor tissue' FHIR mapping: Specimen.type ARGO mapping sample_registration::specimen_tissue_source""")
    taxonomy: Optional[OntologyClass] = Field(None, description="""NCBI taxonomic identifier (NCBITaxon) of the sample e.g. NCBITaxon:9606""")
    timeOfCollection: Optional[TimeElement] = Field(None, description="""An TimeElement describing either the age of the individual this biosample was derived from at the time of collection, or the time itself. See http://build.fhir.org/datatypes""")
    tumorGrade: Optional[OntologyClass] = Field(None, description="""Potentially a child term of NCIT:C28076 (Disease Grade Qualifier) or equivalent See https://www.cancer.gov/about-cancer/diagnosis-staging/prognosis/tumor-grade-fact-sheet""")
    tumorProgression: Optional[OntologyClass] = Field(None, description="""Is the specimen tissue from the primary tumor, a metastasis or a recurrence? Most likely a child term of NCIT:C7062 (Neoplasm by Special Category) NCIT:C3677 (Benign Neoplasm) NCIT:C84509 (Primary Malignant Neoplasm) NCIT:C95606 (Second Primary Malignant Neoplasm) NCIT:C3261 (Metastatic Neoplasm) NCIT:C4813 (Recurrent Malignant Neoplasm)""")


class Disease(ConfiguredBaseModel):
    """
    Message to indicate a disease (diagnosis) and its recorded onset.
    """
    clinicalTnmFinding: Optional[List[OntologyClass]] = Field(default_factory=list, description="""Cancer findings in the TNM system that is relevant to the diagnosis of cancer. See https://www.cancer.gov/about-cancer/diagnosis-staging/staging Valid values include child terms of NCIT:C48232 (Cancer TNM Finding) ARGO mapping primary_diagnosis::clinical_t_category ARGO mapping primary_diagnosis::clinical_n_category ARGO mapping primary_diagnosis::clinical_m_category""")
    diseaseStage: Optional[List[OntologyClass]] = Field(default_factory=list, description="""Disease staging, the extent to which a disease has developed. For cancers, see https://www.cancer.gov/about-cancer/diagnosis-staging/staging Valid values include child terms of NCIT:C28108 (Disease Stage Qualifier) ARGO mapping primary_diagnosis::clinical_tumour_staging_system ARGO mapping primary_diagnosis::clinical_stage_group""")
    excluded: Optional[bool] = Field(None, description="""Flag to indicate whether the disease was observed or not. Default is 'false', in other words the disease was observed. Therefore it is only required in cases to indicate that the disease was looked for, but found to be absent. More formally, this modifier indicates the logical negation of the OntologyClass used in the 'term' field. *CAUTION* It is imperative to check this field for correct interpretation of the disease!""")
    laterality: Optional[OntologyClass] = Field(None, description="""The term used to indicate laterality of diagnosis, if applicable. (Codelist reference: NCI CDE: 4122391)""")
    onset: Optional[TimeElement] = Field(None, description="""The onset of the disease. The values of this will come from the HPO onset hierarchy i.e. subclasses of HP:0003674 FHIR mapping: Condition.onset ARGO mapping primary_diagnosis::age_at_diagnosis""")
    primarySite: Optional[OntologyClass] = Field(None, description="""The text term used to describe the primary site of disease, as categorized by the World Health Organization's (WHO) International Classification of Diseases for Oncology (ICD-O). This categorization groups cases into general""")
    resolution: Optional[TimeElement] = Field(None)
    term: Optional[OntologyClass] = Field(None, description="""The identifier of this disease e.g. MONDO:0007043, OMIM:101600, Orphanet:710, DOID:14705 (note these are all equivalent) ARGO mapping primary_diagnosis::submitter_primary_diagnosis_id""")


class Any(ConfiguredBaseModel):
    """
    `Any` contains an arbitrary serialized protocol buffer message along with a URL that describes the type of the serialized message.  Protobuf library provides support to pack/unpack Any values in the form of utility functions or additional generated methods of the Any type.  Example 1: Pack and unpack a message in C++.  Foo foo = ...; Any any; any.PackFrom(foo); ... if (any.UnpackTo(&foo)) { ... }  Example 2: Pack and unpack a message in Java.  Foo foo = ...; Any any = Any.pack(foo); ... if (any.is(Foo.class)) { foo = any.unpack(Foo.class); }  Example 3: Pack and unpack a message in Python.  foo = Foo(...) any = Any() any.Pack(foo) ... if any.Is(Foo.DESCRIPTOR): any.Unpack(foo) ...  Example 4: Pack and unpack a message in Go  foo := &pb.Foo{...} any, err := anypb.New(foo) if err != nil { ... } ... foo := &pb.Foo{} if err := any.UnmarshalTo(foo); err != nil { ... }  The pack methods provided by protobuf library will by default use 'type.googleapis.com/full.type.name' as the type URL and the unpack methods only use the fully qualified type name after the last '/' in the type URL, for example \"foo.bar.com/x/y.z\" will yield type name \"y.z\".   JSON ==== The JSON representation of an `Any` value uses the regular representation of the deserialized, embedded message, with an additional field `@type` which contains the type URL. Example:  package google.profile; message Person { string first_name = 1; string last_name = 2; }  { \"@type\": \"type.googleapis.com/google.profile.Person\", \"firstName\": <string>, \"lastName\": <string> }  If the embedded message type is well-known and has a custom JSON representation, that representation will be embedded adding a field `value` which holds the custom JSON in addition to the `@type` field. Example (for message [google.protobuf.Duration][]):  { \"@type\": \"type.googleapis.com/google.protobuf.Duration\", \"value\": \"1.212s\" } 
    """
    typeUrl: Optional[str] = Field(None, description="""A URL/resource name that uniquely identifies the type of the serialized protocol buffer message. This string must contain at least one \"/\" character. The last segment of the URL's path must represent the fully qualified name of the type (as in `path/google.protobuf.Duration`). The name should be in a canonical form (e.g., leading \".\" is not accepted).  In practice, teams usually precompile into the binary all types that they expect it to use in the context of Any. However, for URLs which use the scheme `http`, `https`, or no scheme, one can optionally set up a type server that maps type URLs to message definitions as follows:  * If no scheme is provided, `https` is assumed. * An HTTP GET on the URL must yield a [google.protobuf.Type][] value in binary format, or produce an error. * Applications are allowed to cache lookup results based on the URL, or have them precompiled into a binary to avoid any lookup. Therefore, binary compatibility needs to be preserved on changes to types. (Use versioned type names to manage breaking changes.)  Note: this functionality is not currently available in the official protobuf release, and it is not used for type URLs beginning with type.googleapis.com.  Schemes other than `http`, `https` (or the empty scheme) might be used with implementation specific semantics. """)
    value: Optional[str] = Field(None, description="""Must be a valid serialized protocol buffer of the above specified type.""")


class Abundance(ConfiguredBaseModel):
    copyNumber: Optional[CopyNumber] = Field(None)


class Allele(ConfiguredBaseModel):
    chromosomeLocation: Optional[ChromosomeLocation] = Field(None)
    curie: Optional[str] = Field(None)
    derivedSequenceExpression: Optional[DerivedSequenceExpression] = Field(None)
    id: Optional[str] = Field(None)
    literalSequenceExpression: Optional[LiteralSequenceExpression] = Field(None)
    repeatedSequenceExpression: Optional[RepeatedSequenceExpression] = Field(None)
    sequenceLocation: Optional[SequenceLocation] = Field(None)


class ChromosomeLocation(ConfiguredBaseModel):
    chr: Optional[str] = Field(None)
    id: Optional[str] = Field(None)
    interval: Optional[CytobandInterval] = Field(None)
    speciesId: Optional[str] = Field(None)


class CopyNumber(ConfiguredBaseModel):
    allele: Optional[Allele] = Field(None)
    curie: Optional[str] = Field(None)
    definiteRange: Optional[DefiniteRange] = Field(None)
    derivedSequenceExpression: Optional[DerivedSequenceExpression] = Field(None)
    gene: Optional[Gene] = Field(None)
    haplotype: Optional[Haplotype] = Field(None)
    id: Optional[str] = Field(None)
    indefiniteRange: Optional[IndefiniteRange] = Field(None)
    literalSequenceExpression: Optional[LiteralSequenceExpression] = Field(None)
    number: Optional[Number] = Field(None)
    repeatedSequenceExpression: Optional[RepeatedSequenceExpression] = Field(None)


class CytobandInterval(ConfiguredBaseModel):
    end: Optional[str] = Field(None)
    start: Optional[str] = Field(None)


class DefiniteRange(ConfiguredBaseModel):
    max: Optional[int] = Field(None)
    min: Optional[int] = Field(None)


class DerivedSequenceExpression(ConfiguredBaseModel):
    location: Optional[SequenceLocation] = Field(None)
    reverseComplement: Optional[bool] = Field(None)


class Feature(ConfiguredBaseModel):
    gene: Optional[Gene] = Field(None)


class Gene(ConfiguredBaseModel):
    geneId: Optional[str] = Field(None)


class Haplotype(ConfiguredBaseModel):
    pass


class IndefiniteRange(ConfiguredBaseModel):
    comparator: Optional[str] = Field(None)
    value: Optional[int] = Field(None)


class LiteralSequenceExpression(ConfiguredBaseModel):
    sequence: Optional[str] = Field(None)


class Location(ConfiguredBaseModel):
    chromosomeLocation: Optional[ChromosomeLocation] = Field(None)
    sequenceLocation: Optional[SequenceLocation] = Field(None)


class Member(ConfiguredBaseModel):
    allele: Optional[Allele] = Field(None)
    copyNumber: Optional[CopyNumber] = Field(None)
    curie: Optional[str] = Field(None)
    haplotype: Optional[Haplotype] = Field(None)
    id: Optional[str] = Field(None)
    members: Optional[List[Member]] = Field(default_factory=list)
    text: Optional[Text] = Field(None)
    variationSet: Optional[VariationSet] = Field(None)


class MolecularVariation(ConfiguredBaseModel):
    allele: Optional[Allele] = Field(None)
    haplotype: Optional[Haplotype] = Field(None)


class Number(ConfiguredBaseModel):
    value: Optional[int] = Field(None)


class RepeatedSequenceExpression(ConfiguredBaseModel):
    definiteRange: Optional[DefiniteRange] = Field(None)
    derivedSequenceExpression: Optional[DerivedSequenceExpression] = Field(None)
    indefiniteRange: Optional[IndefiniteRange] = Field(None)
    literalSequenceExpression: Optional[LiteralSequenceExpression] = Field(None)
    number: Optional[Number] = Field(None)


class SequenceExpression(ConfiguredBaseModel):
    derivedSequenceExpression: Optional[DerivedSequenceExpression] = Field(None)
    literalSequenceExpression: Optional[LiteralSequenceExpression] = Field(None)
    repeatedSequenceExpression: Optional[RepeatedSequenceExpression] = Field(None)


class SequenceInterval(ConfiguredBaseModel):
    endDefiniteRange: Optional[DefiniteRange] = Field(None)
    endIndefiniteRange: Optional[IndefiniteRange] = Field(None)
    endNumber: Optional[Number] = Field(None)
    startDefiniteRange: Optional[DefiniteRange] = Field(None)
    startIndefiniteRange: Optional[IndefiniteRange] = Field(None)
    startNumber: Optional[Number] = Field(None)


class SequenceLocation(ConfiguredBaseModel):
    id: Optional[str] = Field(None)
    sequenceId: Optional[str] = Field(None)
    sequenceInterval: Optional[SequenceInterval] = Field(None)


class SequenceState(ConfiguredBaseModel):
    sequence: Optional[str] = Field(None)


class SimpleInterval(ConfiguredBaseModel):
    end: Optional[int] = Field(None)
    start: Optional[int] = Field(None)


class SystemicVariation(ConfiguredBaseModel):
    copyNumber: Optional[CopyNumber] = Field(None)


class Text(ConfiguredBaseModel):
    definition: Optional[str] = Field(None)
    id: Optional[str] = Field(None)


class UtilityVariation(ConfiguredBaseModel):
    text: Optional[Text] = Field(None)
    variationSet: Optional[VariationSet] = Field(None)


class Variation(ConfiguredBaseModel):
    allele: Optional[Allele] = Field(None)
    copyNumber: Optional[CopyNumber] = Field(None)
    haplotype: Optional[Haplotype] = Field(None)
    text: Optional[Text] = Field(None)
    variationSet: Optional[VariationSet] = Field(None)


class VariationSet(ConfiguredBaseModel):
    pass


class Expression(ConfiguredBaseModel):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#expression
    """
    syntax: Optional[str] = Field(None)
    value: Optional[str] = Field(None)
    version: Optional[str] = Field(None)


class Extension(ConfiguredBaseModel):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#extension
    """
    name: Optional[str] = Field(None)
    value: Optional[List[str]] = Field(default_factory=list)


class GeneDescriptor(ConfiguredBaseModel):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#gene-descriptor
    """
    alternateIds: Optional[List[str]] = Field(default_factory=list, description="""Alternate IDs (should be CURIE) for the same concept may be placed in alternate_ids""")
    alternateSymbols: Optional[List[str]] = Field(default_factory=list, description="""Takes the place of alternate_labels field in a generic descriptor""")
    description: Optional[str] = Field(None, description="""A free-text description of the value object""")
    symbol: Optional[str] = Field(None, description="""The primary gene symbol. Takes the place of the label field in a generic descriptor""")
    valueId: Optional[str] = Field(None, description="""The official gene identifier as designated by the organism gene nomenclature committee e.g. HGNC:3477 or MGI:2385071 This should be a CURIE linking the reference to a namespace where it can be retrieved. Mirrors the value_id field of a generic value object descriptor""")
    xrefs: Optional[List[str]] = Field(default_factory=list, description="""Related concept IDs (e.g. gene ortholog IDs) may be placed in xrefs""")


class VariationDescriptor(ConfiguredBaseModel):
    allelicState: Optional[OntologyClass] = Field(None, description="""We RECOMMEND that the allelic_state of variant be described by terms from the Genotype Ontology (GENO). These SHOULD descend from concept GENO:0000875.""")
    alternateLabels: Optional[List[str]] = Field(default_factory=list, description="""Common aliases for a variant, e.g. EGFR vIII, are alternate labels""")
    description: Optional[str] = Field(None)
    expressions: Optional[List[Expression]] = Field(default_factory=list, description="""HGVS, SPDI, and gnomAD-style strings should be represented as Expressions""")
    extensions: Optional[List[Extension]] = Field(default_factory=list)
    geneContext: Optional[GeneDescriptor] = Field(None, description="""A specific gene context that applies to this variant.""")
    id: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    moleculeContext: Optional[MoleculeContext] = Field(None, description="""The molecular context of the vrs variation. Must be one of “genomic”, “transcript”, or “protein”. Defaults to \"unspecified_molecule_context\"""")
    structuralType: Optional[OntologyClass] = Field(None, description="""The structural variant type associated with this variant, such as a substitution, deletion, or fusion. We RECOMMEND using a descendent term of SO:0001537.""")
    variation: Optional[Variation] = Field(None)
    vcfRecord: Optional[VcfRecord] = Field(None, description="""A VCF Record of the variant. This SHOULD be a single allele, the VCF genotype (GT) field should be represented in the allelic_state""")
    vrsRefAlleleSeq: Optional[str] = Field(None, description="""A Sequence corresponding to a “ref allele”, describing the sequence expected at a SequenceLocation reference.""")
    xrefs: Optional[List[str]] = Field(default_factory=list, description="""Allele registry, ClinVar, or other related IDs should be included as xrefs""")


class VcfRecord(ConfiguredBaseModel):
    alt: Optional[str] = Field(None)
    chrom: Optional[str] = Field(None)
    filter: Optional[str] = Field(None)
    genomeAssembly: Optional[str] = Field(None)
    id: Optional[str] = Field(None)
    info: Optional[str] = Field(None)
    pos: Optional[int] = Field(None)
    qual: Optional[str] = Field(None)
    ref: Optional[str] = Field(None)


class Diagnosis(ConfiguredBaseModel):
    disease: Optional[OntologyClass] = Field(None, description="""The disease/condition assigned to the diagnosis.Details about this disease may be contained in the `diseases` field in the Phenopacket.""")
    genomicInterpretations: Optional[List[GenomicInterpretation]] = Field(default_factory=list, description="""genomic features containing the status of their contribution towards the diagnosis""")


class GenomicInterpretation(ConfiguredBaseModel):
    """
    A statement about the contribution of a genomic element towards the observed phenotype. Note that this does not intend to encode any knowledge or results of specific computations.
    """
    gene: Optional[GeneDescriptor] = Field(None)
    interpretationStatus: Optional[InterpretationStatus] = Field(None)
    subjectOrBiosampleId: Optional[str] = Field(None, description="""identifier for the subject of the interpretation. This MUST be the individual id or a biosample id of the enclosing phenopacket.""")
    variantInterpretation: Optional[VariantInterpretation] = Field(None)


class Interpretation(ConfiguredBaseModel):
    diagnosis: Optional[Diagnosis] = Field(None, description="""The diagnosis made in this interpretation""")
    id: Optional[str] = Field(None, description="""id of the interpretation""")
    progressStatus: Optional[ProgressStatus] = Field(None)
    summary: Optional[str] = Field(None)


class VariantInterpretation(ConfiguredBaseModel):
    acmgPathogenicityClassification: Optional[AcmgPathogenicityClassification] = Field(None)
    therapeuticActionability: Optional[TherapeuticActionability] = Field(None)
    variationDescriptor: Optional[VariationDescriptor] = Field(None)


class Individual(ConfiguredBaseModel):
    """
    An individual (or subject) typically corresponds to an individual human or another organism. FHIR mapping: Patient (https://www.hl7.org/fhir/patient.html).
    """
    alternateIds: Optional[List[str]] = Field(default_factory=list, description="""An optional list of alternative identifiers for this individual. This field is provided for the convenience of users who may have multiple mappings to an individual which they need to track.""")
    dateOfBirth: Optional[str] = Field(None, description="""The date of birth of the individual as an ISO8601 UTC timestamp - rounded down to the closest known year/month/day/hour/minute e.g. \"2018-03-01T00:00:00Z\" for someone born on an unknown day in March 2018 or \"2018-01-01T00:00:00Z\" for someone born on an unknown day in 2018 or empty if unknown/ not stated.""")
    gender: Optional[OntologyClass] = Field(None, description="""Self-identified gender""")
    id: Optional[str] = Field(None, description="""An identifier for the individual. This must be unique within the record. ARGO mapping donor::submitter_donor_id""")
    karyotypicSex: Optional[KaryotypicSex] = Field(None, description="""The karyotypic sex of the individual""")
    sex: Optional[Sex] = Field(None, description="""The phenotypic sex of the individual ARGO mapping sample_registration::gender (this is complicated as ARGO only have male/female/other which maps to the phenopacket Sex field)""")
    taxonomy: Optional[OntologyClass] = Field(None, description="""NCBI taxonomic identifier NCBITaxon e.g. NCBITaxon:9606 or NCBITaxon:1337 For resources where there may be more than one organism being studied it is advisable to indicate the taxonomic identifier of that organism, to its most specific level""")
    timeAtLastEncounter: Optional[TimeElement] = Field(None, description="""An TimeElement object describing the age of the individual at the last time of collection. The Age object allows the encoding of the age either as ISO8601 duration or time interval (preferred), or as ontology term object. See http://build.fhir.org/datatypes""")
    vitalStatus: Optional[VitalStatus] = Field(None, description="""Vital status of the individual. If not present it is assumed that the individual is alive. If present it will default to 'false' i.e. the individual was alive when the data was collected. ARGO mapping donor::vital_status""")


class VitalStatus(ConfiguredBaseModel):
    causeOfDeath: Optional[OntologyClass] = Field(None, description="""ARGO mapping donor::cause_of_death""")
    status: Optional[Status] = Field(None)
    survivalTimeInDays: Optional[int] = Field(None, description="""ARGO mapping donor::survival_time""")
    timeOfDeath: Optional[TimeElement] = Field(None)


class DoseInterval(ConfiguredBaseModel):
    """
    e.g. 50mg/ml 3 times daily for two weeks
    """
    interval: Optional[TimeInterval] = Field(None)
    quantity: Optional[Quantity] = Field(None)
    scheduleFrequency: Optional[OntologyClass] = Field(None)


class MedicalAction(ConfiguredBaseModel):
    """
    medication, procedure, other actions taken for clinical management
    """
    adverseEvents: Optional[List[OntologyClass]] = Field(default_factory=list, description="""ARGO mapping treatment::adverse_events""")
    procedure: Optional[Procedure] = Field(None)
    radiationTherapy: Optional[RadiationTherapy] = Field(None)
    responseToTreatment: Optional[OntologyClass] = Field(None, description="""ARGO mapping treatment::response_to_treatment""")
    therapeuticRegimen: Optional[TherapeuticRegimen] = Field(None)
    treatment: Optional[Treatment] = Field(None)
    treatmentIntent: Optional[OntologyClass] = Field(None, description="""Whether the intention of the treatment was curative, palliative, ARGO mapping treatment::treatment_intent""")
    treatmentTarget: Optional[OntologyClass] = Field(None, description="""The condition or disease that this treatment was intended to address. FHIR mapping Procedure::reasonCode""")
    treatmentTerminationReason: Optional[OntologyClass] = Field(None, description="""ARGO mapping treatment::treatment_outcome""")


class RadiationTherapy(ConfiguredBaseModel):
    """
    RadiationTherapy
    """
    bodySite: OntologyClass = Field(..., description="""The anatomical site where radiation therapy was administered. REQUIRED. ARGO mapping radiation::anatomical_site_irradiated""")
    dosage: int = Field(..., description="""The total dose given in units of Gray (Gy). REQUIRED. ARGO mapping radiation::radiation_therapy_dosage""")
    fractions: int = Field(..., description="""The total number of fractions delivered as part of treatment. REQUIRED. ARGO mapping radiation::radiation_therapy_fractions""")
    modality: OntologyClass = Field(..., description="""The modality of radiation therapy (e.g., electron, photon,…). REQUIRED. ARGO mapping radiation::radiation_therapy_modality""")


class TherapeuticRegimen(ConfiguredBaseModel):
    """
    ARGO mapping radiation::radiation_therapy_type (missing)
    """
    endTime: Optional[TimeElement] = Field(None, description="""end time can be empty which would indicate ongoing""")
    externalReference: Optional[ExternalReference] = Field(None)
    ontologyClass: Optional[OntologyClass] = Field(None)
    regimenStatus: Optional[RegimenStatus] = Field(None)
    startTime: Optional[TimeElement] = Field(None, description="""possibly undefined;""")


class Treatment(ConfiguredBaseModel):
    """
    ARGO mapping treatment::is_primary_treatment (missing) treatment with an agent, such as a drug
    """
    agent: Optional[OntologyClass] = Field(None)
    cumulativeDose: Optional[Quantity] = Field(None, description="""ARGO mapping chemotherapy::cumulative_drug_dosage""")
    doseIntervals: Optional[List[DoseInterval]] = Field(default_factory=list)
    drugType: Optional[DrugType] = Field(None)
    routeOfAdministration: Optional[OntologyClass] = Field(None)


class Timestamp(ConfiguredBaseModel):
    """
    A Timestamp represents a point in time independent of any time zone or local calendar, encoded as a count of seconds and fractions of seconds at nanosecond resolution. The count is relative to an epoch at UTC midnight on January 1, 1970, in the proleptic Gregorian calendar which extends the Gregorian calendar backwards to year one.  All minutes are 60 seconds long. Leap seconds are \"smeared\" so that no leap second table is needed for interpretation, using a [24-hour linear smear](https://developers.google.com/time/smear).  The range is from 0001-01-01T00:00:00Z to 9999-12-31T23:59:59.999999999Z. By restricting to that range, we ensure that we can convert to and from [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) date strings.  # Examples  Example 1: Compute Timestamp from POSIX `time()`.  Timestamp timestamp; timestamp.set_seconds(time(NULL)); timestamp.set_nanos(0);  Example 2: Compute Timestamp from POSIX `gettimeofday()`.  struct timeval tv; gettimeofday(&tv, NULL);  Timestamp timestamp; timestamp.set_seconds(tv.tv_sec); timestamp.set_nanos(tv.tv_usec * 1000);  Example 3: Compute Timestamp from Win32 `GetSystemTimeAsFileTime()`.  FILETIME ft; GetSystemTimeAsFileTime(&ft); UINT64 ticks = (((UINT64)ft.dwHighDateTime) << 32) | ft.dwLowDateTime;  // A Windows tick is 100 nanoseconds. Windows epoch 1601-01-01T00:00:00Z // is 11644473600 seconds before Unix epoch 1970-01-01T00:00:00Z. Timestamp timestamp; timestamp.set_seconds((INT64) ((ticks / 10000000) - 11644473600LL)); timestamp.set_nanos((INT32) ((ticks % 10000000) * 100));  Example 4: Compute Timestamp from Java `System.currentTimeMillis()`.  long millis = System.currentTimeMillis();  Timestamp timestamp = Timestamp.newBuilder().setSeconds(millis / 1000) .setNanos((int) ((millis % 1000) * 1000000)).build();   Example 5: Compute Timestamp from Java `Instant.now()`.  Instant now = Instant.now();  Timestamp timestamp = Timestamp.newBuilder().setSeconds(now.getEpochSecond()) .setNanos(now.getNano()).build();   Example 6: Compute Timestamp from current time in Python.  timestamp = Timestamp() timestamp.GetCurrentTime()  # JSON Mapping  In JSON format, the Timestamp type is encoded as a string in the [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) format. That is, the format is \"{year}-{month}-{day}T{hour}:{min}:{sec}[.{frac_sec}]Z\" where {year} is always expressed using four digits while {month}, {day}, {hour}, {min}, and {sec} are zero-padded to two digits each. The fractional seconds, which can go up to 9 digits (i.e. up to 1 nanosecond resolution), are optional. The \"Z\" suffix indicates the timezone (\"UTC\"); the timezone is required. A proto3 JSON serializer should always use UTC (as indicated by \"Z\") when printing the Timestamp type and a proto3 JSON parser should be able to accept both UTC and other timezones (as indicated by an offset).  For example, \"2017-01-15T01:30:15.01Z\" encodes 15.01 seconds past 01:30 UTC on January 15, 2017.  In JavaScript, one can convert a Date object to this format using the standard [toISOString()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString) method. In Python, a standard `datetime.datetime` object can be converted to this format using [`strftime`](https://docs.python.org/2/library/time.html#time.strftime) with the time format spec '%Y-%m-%dT%H:%M:%S.%fZ'. Likewise, in Java, one can use the Joda Time's [`ISODateTimeFormat.dateTime()`]( http://www.joda.org/joda-time/apidocs/org/joda/time/format/ISODateTimeFormat.html#dateTime%2D%2D ) to obtain a formatter capable of generating timestamps in this format.  
    """
    nanos: Optional[int] = Field(None, description="""Non-negative fractions of a second at nanosecond resolution. Negative second values with fractions must still have non-negative nanos values that count forward in time. Must be from 0 to 999,999,999 inclusive.""")
    seconds: Optional[int] = Field(None, description="""Represents seconds of UTC time since Unix epoch 1970-01-01T00:00:00Z. Must be from 0001-01-01T00:00:00Z to 9999-12-31T23:59:59Z inclusive.""")


class MetaData(ConfiguredBaseModel):
    created: Optional[str] = Field(None, description="""ISO8601 UTC timestamp for when this phenopacket was created in ISO \"2018-03-01T00:00:00Z\"""")
    createdBy: Optional[str] = Field(None, description="""some kind of identifier for the contributor/ program ARGO sample_registration::program_id""")
    externalReferences: Optional[List[ExternalReference]] = Field(default_factory=list, description="""External identifiers for this message. These are considered different representation of the same record, not records which are in some other relation with the record at hand. For example this might be a PubMed reference to a study in which the individuals are reported.""")
    phenopacketSchemaVersion: Optional[str] = Field(None, description="""phenopacket-schema-version used to create this phenopacket""")
    resources: Optional[List[Resource]] = Field(default_factory=list, description="""a listing of the ontologies and resources referenced in the phenopacket""")
    submittedBy: Optional[str] = Field(None, description="""information about the person/organisation/network that has submitted this phenopacket""")
    updates: Optional[List[Update]] = Field(default_factory=list, description="""An OPTIONAL list of Updates to the phenopacket.""")


class Resource(ConfiguredBaseModel):
    """
    Description of an external resource used for referencing an object. For example the resource may be an ontology such as the HPO or SNOMED. FHIR mapping: CodeSystem (http://www.hl7.org/fhir/codesystem.html)
    """
    id: Optional[str] = Field(None, description="""for OBO Ontologies, the value of this string MUST always be the official OBO ID, which is always equivalent to the ID prefix in lower case. Examples: hp, go, mp, mondo Consult http://obofoundry.org for a complete list For other ontologies (e.g. SNOMED), use the prefix in identifiers.org""")
    iriPrefix: Optional[str] = Field(None, description="""Full IRI prefix which can be used with the namespace_prefix and the OntologyClass::id to resolve to an IRI for a term. Tools such as the curie-util (https://github.com/prefixcommons/curie-util) can utilise this to produce fully-resolvable IRIs for an OntologyClass. e.g. Using the HPO term encoding the concept of 'Severe' OntologyClass: id: 'HP:0012828' label: 'Severe' Resource: namespace_prefix: 'HP' iri_prefix: 'http://purl.obolibrary.org/obo/HP_' the term can be resolved to http://purl.obolibrary.org/obo/HP_0012828""")
    name: Optional[str] = Field(None, description="""e.g. The Human Phenotype Ontology for OBO Ontologies, the value of this string SHOULD be the same as the title field on http://obofoundry.org however, this field is purely for information purposes and software should not encode any assumptions""")
    namespacePrefix: Optional[str] = Field(None, description="""The prefix used in the CURIE of an OntologyClass e.g. HP, MP, ECO For example an HPO term will have a CURIE like this - HP:0012828 which should be used in combination with the iri_prefix to form a fully-resolvable IRI""")
    url: Optional[str] = Field(None, description="""For OBO ontologies, this should always be the PURL, e.g. http://purl.obolibrary.org/obo/hp.owl, http://purl.obolibrary.org/obo/hp.obo""")
    version: Optional[str] = Field(None, description="""for OBO ontologies, this should be the versionIRI""")


class Update(ConfiguredBaseModel):
    """
    Information about when an update to a record occurred, who or what made the update and any pertinent information regarding the content and/or reason for the update
    """
    comment: Optional[str] = Field(None, description="""Textual comment about the changes made to the content and/or reason for the update. OPTIONAL""")
    timestamp: str = Field(..., description="""ISO8601 UTC timestamps at which this record was updated, in the format YYYY-MM-DDTHH:MM:SS.SSSZ e.g. 2007-12-03T10:15:30.00Z REQUIRED""")
    updatedBy: Optional[str] = Field(None, description="""Information about the person/organisation/network that has updated the phenopacket. OPTIONAL""")


class Pedigree(ConfiguredBaseModel):
    """
    https://software.broadinstitute.org/gatk/documentation/article?id=11016
    """
    persons: Optional[List[Person]] = Field(default_factory=list)


class Person(ConfiguredBaseModel):
    affectedStatus: Optional[AffectedStatus] = Field(None)
    familyId: Optional[str] = Field(None)
    individualId: Optional[str] = Field(None)
    maternalId: Optional[str] = Field(None)
    paternalId: Optional[str] = Field(None)
    sex: Optional[Sex] = Field(None)


class Cohort(ConfiguredBaseModel):
    """
    A group of individuals related in some phenotypic or genotypic aspect.
    """
    description: Optional[str] = Field(None)
    files: Optional[List[File]] = Field(default_factory=list, description="""Pointer to relevant file(s) for the cohort. Files relating exclusively to individual phenopackets should be contained in the Phenopacket.""")
    id: Optional[str] = Field(None)
    members: Optional[List[Phenopacket]] = Field(default_factory=list)
    metaData: MetaData = Field(..., description="""Structured definitions of the resources and ontologies used within the phenopacket. REQUIRED""")


class Family(ConfiguredBaseModel):
    """
    Phenotype, sample and pedigree data required for a genomic diagnosis. Equivalent to the Genomics England InterpretationRequestRD https://github.com/genomicsengland/GelReportModels/blob/master/schemas/IDLs/org.gel.models.report.avro/5.0.0/InterpretationRequestRD.avdl
    """
    consanguinousParents: Optional[bool] = Field(None, description="""flag to indicate that the parents of the proband are consanguinous""")
    files: Optional[List[File]] = Field(default_factory=list, description="""Pointer to the relevant file(s) for the family. These should be files relating to one or more of the family members e.g a multi-sample VCF. Files relating exclusively to individual phenopackets should be contained in the Phenopacket.""")
    id: Optional[str] = Field(None, description="""An identifier specific for this family.""")
    metaData: MetaData = Field(..., description="""Structured definitions of the resources and ontologies used within the phenopacket. REQUIRED""")
    pedigree: Optional[Pedigree] = Field(None, description="""The pedigree defining the relations between the proband and their relatives. Pedigree.individual_id should map to the PhenoPacket.Individual.id""")
    proband: Optional[Phenopacket] = Field(None, description="""The individual representing the focus of this packet - e.g. the proband in rare disease cases or cancer patient""")
    relatives: Optional[List[Phenopacket]] = Field(default_factory=list, description="""Individuals related in some way to the patient. For instance, the individuals may be genetically related or may be members of a cohort. If this field is used, then  it is expected that a pedigree will be included for genetically related individuals for use cases such as genomic diagnostics. If a phenopacket is being used to describe one member of a cohort, then in general one phenopacket will be created for each of the individuals in the cohort.""")


class Phenopacket(ConfiguredBaseModel):
    """
    An anonymous phenotypic description of an individual or biosample with potential genes of interest and/or diagnoses.  This is a bundle of high-level concepts with no specifically defined relational concepts. It is expected that the resources sharing the phenopackets will define and enforce their own semantics and level of requirements for included fields.
    """
    biosamples: Optional[List[Biosample]] = Field(default_factory=list, description="""Biosample(s) derived from the patient or a collection of biosamples in isolation""")
    diseases: Optional[List[Disease]] = Field(default_factory=list, description="""Field for disease identifiers - could be used for listing either diagnosed or suspected conditions. The resources using these fields should define what this represents in their context.""")
    files: Optional[List[File]] = Field(default_factory=list, description="""Pointer to the relevant file(s) for the individual""")
    id: Optional[str] = Field(None, description="""An identifier specific for this phenopacket.""")
    interpretations: Optional[List[Interpretation]] = Field(default_factory=list)
    measurements: Optional[List[Measurement]] = Field(default_factory=list, description="""Quantifiable measurements related to the individual""")
    medicalActions: Optional[List[MedicalAction]] = Field(default_factory=list)
    metaData: MetaData = Field(..., description="""Structured definitions of the resources and ontologies used within the phenopacket. REQUIRED""")
    phenotypicFeatures: Optional[List[PhenotypicFeature]] = Field(default_factory=list, description="""Phenotypic features relating to the subject of the phenopacket""")
    subject: Optional[Individual] = Field(None, description="""The individual representing the focus of this packet - e.g. the proband in rare disease cases or cancer patient""")


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Age.model_rebuild()
AgeRange.model_rebuild()
Dictionary.model_rebuild()
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
IndefiniteRange.model_rebuild()
LiteralSequenceExpression.model_rebuild()
Location.model_rebuild()
Member.model_rebuild()
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

