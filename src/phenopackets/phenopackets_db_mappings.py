from dataclasses import dataclass, field
from typing import List

from sqlalchemy import (Column, ForeignKey, Integer, MetaData, String, Table,
                        Text)
from sqlalchemy.orm import registry, relationship

mapper_registry = registry()
metadata = MetaData()

from phenopackets.phenopackets import *

tbl_Age = Table(
    "Age",
    metadata,
    Column("age", Text, primary_key=True),
)
tbl_AgeRange = Table(
    "AgeRange",
    metadata,
    Column("start", Text, primary_key=True),
    Column("end", Text, primary_key=True),
)
tbl_Biosample = Table(
    "Biosample",
    metadata,
    Column("id", Text, primary_key=True),
    Column("individual_id", Text, primary_key=True),
    Column("description", Text, primary_key=True),
    Column("sampled_tissue", Text, primary_key=True),
    Column("phenotypic_features", Text, primary_key=True),
    Column("taxonomy", Text, primary_key=True),
    Column("age_of_individual_at_collection", Text, primary_key=True),
    Column("age_range_of_individual_at_collection", Text, primary_key=True),
    Column("histological_diagnosis", Text, primary_key=True),
    Column("tumor_progression", Text, primary_key=True),
    Column("tumor_grade", Text, primary_key=True),
    Column("diagnostic_markers", Text, primary_key=True),
    Column("procedure", Text, primary_key=True),
    Column("hts_files", Text, primary_key=True),
    Column("variants", Text, primary_key=True),
    Column("is_control_sample", Text, primary_key=True),
)
tbl_Cohort = Table(
    "Cohort",
    metadata,
    Column("id", Text, primary_key=True),
    Column("description", Text, primary_key=True),
    Column("members", Text, primary_key=True),
    Column("hts_files", Text, primary_key=True),
    Column("meta_data", Text, primary_key=True),
)
tbl_Disease = Table(
    "Disease",
    metadata,
    Column("term", Text, primary_key=True),
    Column("age_of_onset", Text, primary_key=True),
    Column("age_range_of_onset", Text, primary_key=True),
    Column("class_of_onset", Text, primary_key=True),
    Column("disease_stage", Text, primary_key=True),
    Column("tnm_finding", Text, primary_key=True),
)
tbl_Evidence = Table(
    "Evidence",
    metadata,
    Column("evidence_code", Text, primary_key=True),
    Column("reference", Text, primary_key=True),
)
tbl_ExternalReference = Table(
    "ExternalReference",
    metadata,
    Column("id", Text, primary_key=True),
    Column("description", Text, primary_key=True),
)
tbl_Family = Table(
    "Family",
    metadata,
    Column("id", Text, primary_key=True),
    Column("proband", Text, primary_key=True),
    Column("relatives", Text, primary_key=True),
    Column("pedigree", Text, primary_key=True),
    Column("hts_files", Text, primary_key=True),
    Column("meta_data", Text, primary_key=True),
)
tbl_Gene = Table(
    "Gene",
    metadata,
    Column("id", Text, primary_key=True),
    Column("alternate_ids", Text, primary_key=True),
    Column("symbol", Text, primary_key=True),
)
tbl_HgvsAllele = Table(
    "HgvsAllele",
    metadata,
    Column("id", Text, primary_key=True),
    Column("hgvs", Text, primary_key=True),
)
tbl_HtsFile = Table(
    "HtsFile",
    metadata,
    Column("uri", Text, primary_key=True),
    Column("description", Text, primary_key=True),
    Column("hts_format", Text, primary_key=True),
    Column("genome_assembly", Text, primary_key=True),
    Column("individual_to_sample_identifiers", Text, primary_key=True),
)
tbl_Individual = Table(
    "Individual",
    metadata,
    Column("id", Text, primary_key=True),
    Column("alternate_ids", Text, primary_key=True),
    Column("date_of_birth", Text, primary_key=True),
    Column("age_at_collection", Text, primary_key=True),
    Column("age_range_at_collection", Text, primary_key=True),
    Column("sex", Text, primary_key=True),
    Column("karyotypic_sex", Text, primary_key=True),
    Column("taxonomy", Text, primary_key=True),
)
tbl_IscnAllele = Table(
    "IscnAllele",
    metadata,
    Column("id", Text, primary_key=True),
    Column("iscn", Text, primary_key=True),
)
tbl_MetaData = Table(
    "MetaData",
    metadata,
    Column("created", Text, primary_key=True),
    Column("created_by", Text, primary_key=True),
    Column("submitted_by", Text, primary_key=True),
    Column("resources", Text, primary_key=True),
    Column("updates", Text, primary_key=True),
    Column("phenopacket_schema_version", Text, primary_key=True),
    Column("external_references", Text, primary_key=True),
)
tbl_OntologyClass = Table(
    "OntologyClass",
    metadata,
    Column("id", Text, primary_key=True),
    Column("label", Text, primary_key=True),
)
tbl_Pedigree = Table(
    "Pedigree",
    metadata,
    Column("persons", Text, primary_key=True),
)
tbl_Person = Table(
    "Person",
    metadata,
    Column("family_id", Text, primary_key=True),
    Column("individual_id", Text, primary_key=True),
    Column("paternal_id", Text, primary_key=True),
    Column("maternal_id", Text, primary_key=True),
    Column("sex", Text, primary_key=True),
    Column("affected_status", Text, primary_key=True),
)
tbl_Phenopacket = Table(
    "Phenopacket",
    metadata,
    Column("id", Text, primary_key=True),
    Column("subject", Text, primary_key=True),
    Column("phenotypic_features", Text, primary_key=True),
    Column("biosamples", Text, primary_key=True),
    Column("genes", Text, primary_key=True),
    Column("variants", Text, primary_key=True),
    Column("diseases", Text, primary_key=True),
    Column("hts_files", Text, primary_key=True),
    Column("meta_data", Text, primary_key=True),
)
tbl_PhenotypicFeature = Table(
    "PhenotypicFeature",
    metadata,
    Column("description", Text, primary_key=True),
    Column("type", Text, primary_key=True),
    Column("negated", Text, primary_key=True),
    Column("severity", Text, primary_key=True),
    Column("modifiers", Text, primary_key=True),
    Column("age_of_onset", Text, primary_key=True),
    Column("age_range_of_onset", Text, primary_key=True),
    Column("class_of_onset", Text, primary_key=True),
    Column("evidence", Text, primary_key=True),
)
tbl_Procedure = Table(
    "Procedure",
    metadata,
    Column("code", Text, primary_key=True),
    Column("body_site", Text, primary_key=True),
)
tbl_Resource = Table(
    "Resource",
    metadata,
    Column("id", Text, primary_key=True),
    Column("name", Text, primary_key=True),
    Column("url", Text, primary_key=True),
    Column("version", Text, primary_key=True),
    Column("namespace_prefix", Text, primary_key=True),
    Column("iri_prefix", Text, primary_key=True),
)
tbl_SpdiAllele = Table(
    "SpdiAllele",
    metadata,
    Column("id", Text, primary_key=True),
    Column("seq_id", Text, primary_key=True),
    Column("position", Text, primary_key=True),
    Column("deleted_sequence", Text, primary_key=True),
    Column("inserted_sequence", Text, primary_key=True),
)
tbl_Timestamp = Table(
    "Timestamp",
    metadata,
    Column("seconds", Text, primary_key=True),
    Column("nanos", Text, primary_key=True),
)
tbl_Update = Table(
    "Update",
    metadata,
    Column("timestamp", Text, primary_key=True),
    Column("updated_by", Text, primary_key=True),
    Column("comment", Text, primary_key=True),
)
tbl_Variant = Table(
    "Variant",
    metadata,
    Column("hgvs_allele", Text, primary_key=True),
    Column("vcf_allele", Text, primary_key=True),
    Column("spdi_allele", Text, primary_key=True),
    Column("iscn_allele", Text, primary_key=True),
    Column("zygosity", Text, primary_key=True),
)
tbl_VcfAllele = Table(
    "VcfAllele",
    metadata,
    Column("vcf_version", Text, primary_key=True),
    Column("genome_assembly", Text, primary_key=True),
    Column("id", Text, primary_key=True),
    Column("chr", Text, primary_key=True),
    Column("pos", Text, primary_key=True),
    Column("ref", Text, primary_key=True),
    Column("alt", Text, primary_key=True),
    Column("info", Text, primary_key=True),
)
mapper_registry.map_imperatively(Age, tbl_Age, properties={})
mapper_registry.map_imperatively(AgeRange, tbl_AgeRange, properties={})
mapper_registry.map_imperatively(Biosample, tbl_Biosample, properties={})
mapper_registry.map_imperatively(Cohort, tbl_Cohort, properties={})
mapper_registry.map_imperatively(Disease, tbl_Disease, properties={})
mapper_registry.map_imperatively(Evidence, tbl_Evidence, properties={})
mapper_registry.map_imperatively(
    ExternalReference, tbl_ExternalReference, properties={}
)
mapper_registry.map_imperatively(Family, tbl_Family, properties={})
mapper_registry.map_imperatively(Gene, tbl_Gene, properties={})
mapper_registry.map_imperatively(HgvsAllele, tbl_HgvsAllele, properties={})
mapper_registry.map_imperatively(HtsFile, tbl_HtsFile, properties={})
mapper_registry.map_imperatively(Individual, tbl_Individual, properties={})
mapper_registry.map_imperatively(IscnAllele, tbl_IscnAllele, properties={})
mapper_registry.map_imperatively(MetaData, tbl_MetaData, properties={})
mapper_registry.map_imperatively(OntologyClass, tbl_OntologyClass, properties={})
mapper_registry.map_imperatively(Pedigree, tbl_Pedigree, properties={})
mapper_registry.map_imperatively(Person, tbl_Person, properties={})
mapper_registry.map_imperatively(Phenopacket, tbl_Phenopacket, properties={})
mapper_registry.map_imperatively(
    PhenotypicFeature, tbl_PhenotypicFeature, properties={}
)
mapper_registry.map_imperatively(Procedure, tbl_Procedure, properties={})
mapper_registry.map_imperatively(Resource, tbl_Resource, properties={})
mapper_registry.map_imperatively(SpdiAllele, tbl_SpdiAllele, properties={})
mapper_registry.map_imperatively(Timestamp, tbl_Timestamp, properties={})
mapper_registry.map_imperatively(Update, tbl_Update, properties={})
mapper_registry.map_imperatively(Variant, tbl_Variant, properties={})
mapper_registry.map_imperatively(VcfAllele, tbl_VcfAllele, properties={})
