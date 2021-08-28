

CREATE TABLE "Age" (
	age TEXT, 
	PRIMARY KEY (age)
);

CREATE TABLE "AgeRange" (
	start TEXT, 
	"end" TEXT, 
	PRIMARY KEY (start, "end")
);

CREATE TABLE "Biosample" (
	id TEXT, 
	individual_id TEXT, 
	description TEXT, 
	sampled_tissue TEXT, 
	phenotypic_features TEXT, 
	taxonomy TEXT, 
	age_of_individual_at_collection TEXT, 
	age_range_of_individual_at_collection TEXT, 
	histological_diagnosis TEXT, 
	tumor_progression TEXT, 
	tumor_grade TEXT, 
	diagnostic_markers TEXT, 
	procedure TEXT, 
	hts_files TEXT, 
	variants TEXT, 
	is_control_sample BOOLEAN, 
	PRIMARY KEY (id, individual_id, description, sampled_tissue, phenotypic_features, taxonomy, age_of_individual_at_collection, age_range_of_individual_at_collection, histological_diagnosis, tumor_progression, tumor_grade, diagnostic_markers, procedure, hts_files, variants, is_control_sample)
);

CREATE TABLE "Cohort" (
	id TEXT, 
	description TEXT, 
	members TEXT, 
	hts_files TEXT, 
	meta_data TEXT, 
	PRIMARY KEY (id, description, members, hts_files, meta_data)
);

CREATE TABLE "Disease" (
	term TEXT, 
	age_of_onset TEXT, 
	age_range_of_onset TEXT, 
	class_of_onset TEXT, 
	disease_stage TEXT, 
	tnm_finding TEXT, 
	PRIMARY KEY (term, age_of_onset, age_range_of_onset, class_of_onset, disease_stage, tnm_finding)
);

CREATE TABLE "Evidence" (
	evidence_code TEXT, 
	reference TEXT, 
	PRIMARY KEY (evidence_code, reference)
);

CREATE TABLE "ExternalReference" (
	id TEXT, 
	description TEXT, 
	PRIMARY KEY (id, description)
);

CREATE TABLE "Family" (
	id TEXT, 
	proband TEXT, 
	relatives TEXT, 
	pedigree TEXT, 
	hts_files TEXT, 
	meta_data TEXT, 
	PRIMARY KEY (id, proband, relatives, pedigree, hts_files, meta_data)
);

CREATE TABLE "Gene" (
	id TEXT, 
	alternate_ids TEXT, 
	symbol TEXT, 
	PRIMARY KEY (id, alternate_ids, symbol)
);

CREATE TABLE "HgvsAllele" (
	id TEXT, 
	hgvs TEXT, 
	PRIMARY KEY (id, hgvs)
);

CREATE TABLE "HtsFile" (
	uri TEXT, 
	description TEXT, 
	hts_format VARCHAR(7), 
	genome_assembly TEXT, 
	individual_to_sample_identifiers TEXT, 
	PRIMARY KEY (uri, description, hts_format, genome_assembly, individual_to_sample_identifiers)
);

CREATE TABLE "Individual" (
	id TEXT, 
	alternate_ids TEXT, 
	date_of_birth TEXT, 
	age_at_collection TEXT, 
	age_range_at_collection TEXT, 
	sex VARCHAR(11), 
	karyotypic_sex VARCHAR(17), 
	taxonomy TEXT, 
	PRIMARY KEY (id, alternate_ids, date_of_birth, age_at_collection, age_range_at_collection, sex, karyotypic_sex, taxonomy)
);

CREATE TABLE "IscnAllele" (
	id TEXT, 
	iscn TEXT, 
	PRIMARY KEY (id, iscn)
);

CREATE TABLE "MetaData" (
	created TEXT, 
	created_by TEXT, 
	submitted_by TEXT, 
	resources TEXT, 
	updates TEXT, 
	phenopacket_schema_version TEXT, 
	external_references TEXT, 
	PRIMARY KEY (created, created_by, submitted_by, resources, updates, phenopacket_schema_version, external_references)
);

CREATE TABLE "OntologyClass" (
	id TEXT, 
	label TEXT, 
	PRIMARY KEY (id, label)
);

CREATE TABLE "Pedigree" (
	persons TEXT, 
	PRIMARY KEY (persons)
);

CREATE TABLE "Person" (
	family_id TEXT, 
	individual_id TEXT, 
	paternal_id TEXT, 
	maternal_id TEXT, 
	sex VARCHAR(11), 
	affected_status VARCHAR(10), 
	PRIMARY KEY (family_id, individual_id, paternal_id, maternal_id, sex, affected_status)
);

CREATE TABLE "Phenopacket" (
	id TEXT, 
	subject TEXT, 
	phenotypic_features TEXT, 
	biosamples TEXT, 
	genes TEXT, 
	variants TEXT, 
	diseases TEXT, 
	hts_files TEXT, 
	meta_data TEXT, 
	PRIMARY KEY (id, subject, phenotypic_features, biosamples, genes, variants, diseases, hts_files, meta_data)
);

CREATE TABLE "PhenotypicFeature" (
	description TEXT, 
	type TEXT, 
	negated BOOLEAN, 
	severity TEXT, 
	modifiers TEXT, 
	age_of_onset TEXT, 
	age_range_of_onset TEXT, 
	class_of_onset TEXT, 
	evidence TEXT, 
	PRIMARY KEY (description, type, negated, severity, modifiers, age_of_onset, age_range_of_onset, class_of_onset, evidence)
);

CREATE TABLE "Procedure" (
	code TEXT, 
	body_site TEXT, 
	PRIMARY KEY (code, body_site)
);

CREATE TABLE "Resource" (
	id TEXT, 
	name TEXT, 
	url TEXT, 
	version TEXT, 
	namespace_prefix TEXT, 
	iri_prefix TEXT, 
	PRIMARY KEY (id, name, url, version, namespace_prefix, iri_prefix)
);

CREATE TABLE "SpdiAllele" (
	id TEXT, 
	seq_id TEXT, 
	position INTEGER, 
	deleted_sequence TEXT, 
	inserted_sequence TEXT, 
	PRIMARY KEY (id, seq_id, position, deleted_sequence, inserted_sequence)
);

CREATE TABLE "Timestamp" (
	seconds INTEGER, 
	nanos INTEGER, 
	PRIMARY KEY (seconds, nanos)
);

CREATE TABLE "Update" (
	timestamp TEXT, 
	updated_by TEXT, 
	comment TEXT, 
	PRIMARY KEY (timestamp, updated_by, comment)
);

CREATE TABLE "Variant" (
	hgvs_allele TEXT, 
	vcf_allele TEXT, 
	spdi_allele TEXT, 
	iscn_allele TEXT, 
	zygosity TEXT, 
	PRIMARY KEY (hgvs_allele, vcf_allele, spdi_allele, iscn_allele, zygosity)
);

CREATE TABLE "VcfAllele" (
	vcf_version TEXT, 
	genome_assembly TEXT, 
	id TEXT, 
	chr TEXT, 
	pos INTEGER, 
	ref TEXT, 
	alt TEXT, 
	info TEXT, 
	PRIMARY KEY (vcf_version, genome_assembly, id, chr, pos, ref, alt, info)
);

