

CREATE TABLE "Age" (
	iso8601duration TEXT, 
	PRIMARY KEY (iso8601duration)
);

CREATE TABLE "AgeRange" (
	"end" TEXT, 
	start TEXT, 
	PRIMARY KEY ("end", start)
);

CREATE TABLE "Any" (
	"typeUrl" TEXT, 
	value TEXT, 
	PRIMARY KEY ("typeUrl", value)
);

CREATE TABLE "ChromosomeLocation" (
	chr TEXT, 
	id TEXT NOT NULL, 
	interval TEXT, 
	"speciesId" TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Cohort" (
	description TEXT, 
	files TEXT, 
	id TEXT NOT NULL, 
	members TEXT, 
	"metaData" TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE "ComplexValue" (
	"typedQuantities" TEXT, 
	PRIMARY KEY ("typedQuantities")
);

CREATE TABLE "CytobandInterval" (
	"end" TEXT, 
	start TEXT, 
	PRIMARY KEY ("end", start)
);

CREATE TABLE "DefiniteRange" (
	max INTEGER, 
	min INTEGER, 
	PRIMARY KEY (max, min)
);

CREATE TABLE "ExternalReference" (
	description TEXT, 
	id TEXT NOT NULL, 
	reference TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Feature" (
	gene TEXT, 
	PRIMARY KEY (gene)
);

CREATE TABLE "File" (
	"fileAttributes" TEXT, 
	"individualToFileIdentifiers" TEXT, 
	uri TEXT, 
	PRIMARY KEY ("fileAttributes", "individualToFileIdentifiers", uri)
);

CREATE TABLE "Gene" (
	"geneId" TEXT, 
	PRIMARY KEY ("geneId")
);

CREATE TABLE "GeneDescriptor" (
	"alternateIds" TEXT, 
	"alternateSymbols" TEXT, 
	description TEXT, 
	symbol TEXT, 
	"valueId" TEXT, 
	xrefs TEXT, 
	PRIMARY KEY ("alternateIds", "alternateSymbols", description, symbol, "valueId", xrefs)
);

CREATE TABLE "GenomicInterpretation" (
	gene TEXT, 
	"interpretationStatus" VARCHAR(14), 
	"subjectOrBiosampleId" TEXT, 
	"variantInterpretation" TEXT, 
	PRIMARY KEY (gene, "interpretationStatus", "subjectOrBiosampleId", "variantInterpretation")
);

CREATE TABLE "GestationalAge" (
	days INTEGER, 
	weeks INTEGER, 
	PRIMARY KEY (days, weeks)
);

CREATE TABLE "IndefiniteRange" (
	comparator TEXT, 
	value INTEGER, 
	PRIMARY KEY (comparator, value)
);

CREATE TABLE "LiteralSequenceExpression" (
	sequence TEXT, 
	PRIMARY KEY (sequence)
);

CREATE TABLE "MetaData" (
	created TEXT, 
	"createdBy" TEXT, 
	"externalReferences" TEXT, 
	"phenopacketSchemaVersion" TEXT, 
	resources TEXT, 
	"submittedBy" TEXT, 
	updates TEXT, 
	PRIMARY KEY (created, "createdBy", "externalReferences", "phenopacketSchemaVersion", resources, "submittedBy", updates)
);

CREATE TABLE "Number" (
	value INTEGER, 
	PRIMARY KEY (value)
);

CREATE TABLE "OntologyClass" (
	id TEXT NOT NULL, 
	label TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Pedigree" (
	persons TEXT, 
	PRIMARY KEY (persons)
);

CREATE TABLE "Person" (
	"affectedStatus" VARCHAR(10), 
	"familyId" TEXT, 
	"individualId" TEXT, 
	"maternalId" TEXT, 
	"paternalId" TEXT, 
	sex VARCHAR(11), 
	PRIMARY KEY ("affectedStatus", "familyId", "individualId", "maternalId", "paternalId", sex)
);

CREATE TABLE "RepeatedSequenceExpression" (
	"definiteRange" TEXT, 
	"derivedSequenceExpression" TEXT, 
	"indefiniteRange" TEXT, 
	"literalSequenceExpression" TEXT, 
	number TEXT, 
	PRIMARY KEY ("definiteRange", "derivedSequenceExpression", "indefiniteRange", "literalSequenceExpression", number)
);

CREATE TABLE "Resource" (
	id TEXT NOT NULL, 
	"iriPrefix" TEXT, 
	name TEXT, 
	"namespacePrefix" TEXT, 
	url TEXT, 
	version TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "SequenceExpression" (
	"derivedSequenceExpression" TEXT, 
	"literalSequenceExpression" TEXT, 
	"repeatedSequenceExpression" TEXT, 
	PRIMARY KEY ("derivedSequenceExpression", "literalSequenceExpression", "repeatedSequenceExpression")
);

CREATE TABLE "SequenceInterval" (
	"endDefiniteRange" TEXT, 
	"endIndefiniteRange" TEXT, 
	"endNumber" TEXT, 
	"startDefiniteRange" TEXT, 
	"startIndefiniteRange" TEXT, 
	"startNumber" TEXT, 
	PRIMARY KEY ("endDefiniteRange", "endIndefiniteRange", "endNumber", "startDefiniteRange", "startIndefiniteRange", "startNumber")
);

CREATE TABLE "SequenceLocation" (
	id TEXT NOT NULL, 
	"sequenceId" TEXT, 
	"sequenceInterval" TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "SequenceState" (
	sequence TEXT, 
	PRIMARY KEY (sequence)
);

CREATE TABLE "SimpleInterval" (
	"end" INTEGER, 
	start INTEGER, 
	PRIMARY KEY ("end", start)
);

CREATE TABLE "Text" (
	definition TEXT, 
	id TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE "TimeInterval" (
	"end" TEXT, 
	start TEXT, 
	PRIMARY KEY ("end", start)
);

CREATE TABLE "Timestamp" (
	nanos INTEGER, 
	seconds INTEGER, 
	PRIMARY KEY (nanos, seconds)
);

CREATE TABLE "Update" (
	comment TEXT, 
	timestamp TEXT NOT NULL, 
	"updatedBy" TEXT, 
	PRIMARY KEY (comment, timestamp, "updatedBy")
);

CREATE TABLE "VcfRecord" (
	alt TEXT, 
	chrom TEXT, 
	filter TEXT, 
	"genomeAssembly" TEXT, 
	id TEXT NOT NULL, 
	info TEXT, 
	pos INTEGER, 
	qual TEXT, 
	ref TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Allele" (
	"chromosomeLocation" TEXT, 
	curie TEXT, 
	"derivedSequenceExpression" TEXT, 
	id TEXT NOT NULL, 
	"literalSequenceExpression" TEXT, 
	"repeatedSequenceExpression" TEXT, 
	"sequenceLocation" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY("chromosomeLocation") REFERENCES "ChromosomeLocation" (id), 
	FOREIGN KEY("sequenceLocation") REFERENCES "SequenceLocation" (id)
);

CREATE TABLE "DerivedSequenceExpression" (
	location TEXT, 
	"reverseComplement" BOOLEAN, 
	PRIMARY KEY (location, "reverseComplement"), 
	FOREIGN KEY(location) REFERENCES "SequenceLocation" (id)
);

CREATE TABLE "Diagnosis" (
	disease TEXT, 
	"genomicInterpretations" TEXT, 
	PRIMARY KEY (disease, "genomicInterpretations"), 
	FOREIGN KEY(disease) REFERENCES "OntologyClass" (id)
);

CREATE TABLE "DoseInterval" (
	interval TEXT, 
	quantity TEXT, 
	"scheduleFrequency" TEXT, 
	PRIMARY KEY (interval, quantity, "scheduleFrequency"), 
	FOREIGN KEY("scheduleFrequency") REFERENCES "OntologyClass" (id)
);

CREATE TABLE "Evidence" (
	"evidenceCode" TEXT, 
	reference TEXT, 
	PRIMARY KEY ("evidenceCode", reference), 
	FOREIGN KEY("evidenceCode") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY(reference) REFERENCES "ExternalReference" (id)
);

CREATE TABLE "Individual" (
	"dateOfBirth" TEXT, 
	gender TEXT, 
	id TEXT NOT NULL, 
	"karyotypicSex" VARCHAR(17), 
	sex VARCHAR(11), 
	taxonomy TEXT, 
	"timeAtLastEncounter" TEXT, 
	"vitalStatus" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(gender) REFERENCES "OntologyClass" (id), 
	FOREIGN KEY(taxonomy) REFERENCES "OntologyClass" (id)
);

CREATE TABLE "Location" (
	"chromosomeLocation" TEXT, 
	"sequenceLocation" TEXT, 
	PRIMARY KEY ("chromosomeLocation", "sequenceLocation"), 
	FOREIGN KEY("chromosomeLocation") REFERENCES "ChromosomeLocation" (id), 
	FOREIGN KEY("sequenceLocation") REFERENCES "SequenceLocation" (id)
);

CREATE TABLE "Measurement" (
	assay TEXT, 
	"complexValue" TEXT, 
	description TEXT, 
	procedure TEXT, 
	"timeObserved" TEXT, 
	value TEXT, 
	PRIMARY KEY (assay, "complexValue", description, procedure, "timeObserved", value), 
	FOREIGN KEY(assay) REFERENCES "OntologyClass" (id)
);

CREATE TABLE "PhenotypicFeature" (
	description TEXT, 
	evidence TEXT, 
	excluded BOOLEAN, 
	modifiers TEXT, 
	onset TEXT, 
	resolution TEXT, 
	severity TEXT, 
	type TEXT, 
	PRIMARY KEY (description, evidence, excluded, modifiers, onset, resolution, severity, type), 
	FOREIGN KEY(severity) REFERENCES "OntologyClass" (id), 
	FOREIGN KEY(type) REFERENCES "OntologyClass" (id)
);

CREATE TABLE "Procedure" (
	"bodySite" TEXT, 
	code TEXT, 
	performed TEXT, 
	PRIMARY KEY ("bodySite", code, performed), 
	FOREIGN KEY("bodySite") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY(code) REFERENCES "OntologyClass" (id)
);

CREATE TABLE "Quantity" (
	"referenceRange" TEXT, 
	unit TEXT, 
	value FLOAT, 
	PRIMARY KEY ("referenceRange", unit, value), 
	FOREIGN KEY(unit) REFERENCES "OntologyClass" (id)
);

CREATE TABLE "RadiationTherapy" (
	"bodySite" TEXT NOT NULL, 
	dosage INTEGER NOT NULL, 
	fractions INTEGER NOT NULL, 
	modality TEXT NOT NULL, 
	PRIMARY KEY ("bodySite", dosage, fractions, modality), 
	FOREIGN KEY("bodySite") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY(modality) REFERENCES "OntologyClass" (id)
);

CREATE TABLE "ReferenceRange" (
	high FLOAT, 
	low FLOAT, 
	unit TEXT, 
	PRIMARY KEY (high, low, unit), 
	FOREIGN KEY(unit) REFERENCES "OntologyClass" (id)
);

CREATE TABLE "TherapeuticRegimen" (
	"endTime" TEXT, 
	"externalReference" TEXT, 
	"ontologyClass" TEXT, 
	"regimenStatus" VARCHAR(14), 
	"startTime" TEXT, 
	PRIMARY KEY ("endTime", "externalReference", "ontologyClass", "regimenStatus", "startTime"), 
	FOREIGN KEY("externalReference") REFERENCES "ExternalReference" (id), 
	FOREIGN KEY("ontologyClass") REFERENCES "OntologyClass" (id)
);

CREATE TABLE "TimeElement" (
	age TEXT, 
	"ageRange" TEXT, 
	"gestationalAge" TEXT, 
	interval TEXT, 
	"ontologyClass" TEXT, 
	timestamp TEXT, 
	PRIMARY KEY (age, "ageRange", "gestationalAge", interval, "ontologyClass", timestamp), 
	FOREIGN KEY("ontologyClass") REFERENCES "OntologyClass" (id)
);

CREATE TABLE "Treatment" (
	agent TEXT, 
	"cumulativeDose" TEXT, 
	"doseIntervals" TEXT, 
	"drugType" VARCHAR(35), 
	"routeOfAdministration" TEXT, 
	PRIMARY KEY (agent, "cumulativeDose", "doseIntervals", "drugType", "routeOfAdministration"), 
	FOREIGN KEY(agent) REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("routeOfAdministration") REFERENCES "OntologyClass" (id)
);

CREATE TABLE "TypedQuantity" (
	quantity TEXT, 
	type TEXT, 
	PRIMARY KEY (quantity, type), 
	FOREIGN KEY(type) REFERENCES "OntologyClass" (id)
);

CREATE TABLE "UtilityVariation" (
	text TEXT, 
	"variationSet" TEXT, 
	PRIMARY KEY (text, "variationSet"), 
	FOREIGN KEY(text) REFERENCES "Text" (id)
);

CREATE TABLE "Value" (
	"ontologyClass" TEXT, 
	quantity TEXT, 
	PRIMARY KEY ("ontologyClass", quantity), 
	FOREIGN KEY("ontologyClass") REFERENCES "OntologyClass" (id)
);

CREATE TABLE "VariationDescriptor" (
	"allelicState" TEXT, 
	description TEXT, 
	"geneContext" TEXT, 
	id TEXT NOT NULL, 
	label TEXT, 
	"moleculeContext" VARCHAR(28), 
	"structuralType" TEXT, 
	variation TEXT, 
	"vcfRecord" TEXT, 
	"vrsRefAlleleSeq" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY("allelicState") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("structuralType") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("vcfRecord") REFERENCES "VcfRecord" (id)
);

CREATE TABLE "VitalStatus" (
	"causeOfDeath" TEXT, 
	status VARCHAR(14), 
	"survivalTimeInDays" INTEGER, 
	"timeOfDeath" TEXT, 
	PRIMARY KEY ("causeOfDeath", status, "survivalTimeInDays", "timeOfDeath"), 
	FOREIGN KEY("causeOfDeath") REFERENCES "OntologyClass" (id)
);

CREATE TABLE "CopyNumber" (
	allele TEXT, 
	curie TEXT, 
	"definiteRange" TEXT, 
	"derivedSequenceExpression" TEXT, 
	gene TEXT, 
	haplotype TEXT, 
	id TEXT NOT NULL, 
	"indefiniteRange" TEXT, 
	"literalSequenceExpression" TEXT, 
	number TEXT, 
	"repeatedSequenceExpression" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(allele) REFERENCES "Allele" (id)
);

CREATE TABLE "Expression" (
	syntax TEXT, 
	value TEXT, 
	version TEXT, 
	"VariationDescriptor_id" TEXT, 
	PRIMARY KEY (syntax, value, version, "VariationDescriptor_id"), 
	FOREIGN KEY("VariationDescriptor_id") REFERENCES "VariationDescriptor" (id)
);

CREATE TABLE "Extension" (
	name TEXT, 
	value TEXT, 
	"VariationDescriptor_id" TEXT, 
	PRIMARY KEY (name, value, "VariationDescriptor_id"), 
	FOREIGN KEY("VariationDescriptor_id") REFERENCES "VariationDescriptor" (id)
);

CREATE TABLE "MolecularVariation" (
	allele TEXT, 
	haplotype TEXT, 
	PRIMARY KEY (allele, haplotype), 
	FOREIGN KEY(allele) REFERENCES "Allele" (id)
);

CREATE TABLE "Phenopacket" (
	files TEXT, 
	id TEXT NOT NULL, 
	measurements TEXT, 
	"metaData" TEXT NOT NULL, 
	"phenotypicFeatures" TEXT, 
	subject TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(subject) REFERENCES "Individual" (id)
);

CREATE TABLE "VariantInterpretation" (
	"acmgPathogenicityClassification" VARCHAR(22), 
	"therapeuticActionability" VARCHAR(21), 
	"variationDescriptor" TEXT, 
	PRIMARY KEY ("acmgPathogenicityClassification", "therapeuticActionability", "variationDescriptor"), 
	FOREIGN KEY("variationDescriptor") REFERENCES "VariationDescriptor" (id)
);

CREATE TABLE "Individual_alternateIds" (
	backref_id TEXT, 
	"alternateIds" TEXT, 
	PRIMARY KEY (backref_id, "alternateIds"), 
	FOREIGN KEY(backref_id) REFERENCES "Individual" (id)
);

CREATE TABLE "VariationDescriptor_alternateLabels" (
	backref_id TEXT, 
	"alternateLabels" TEXT, 
	PRIMARY KEY (backref_id, "alternateLabels"), 
	FOREIGN KEY(backref_id) REFERENCES "VariationDescriptor" (id)
);

CREATE TABLE "VariationDescriptor_xrefs" (
	backref_id TEXT, 
	xrefs TEXT, 
	PRIMARY KEY (backref_id, xrefs), 
	FOREIGN KEY(backref_id) REFERENCES "VariationDescriptor" (id)
);

CREATE TABLE "Abundance" (
	"copyNumber" TEXT, 
	PRIMARY KEY ("copyNumber"), 
	FOREIGN KEY("copyNumber") REFERENCES "CopyNumber" (id)
);

CREATE TABLE "Biosample" (
	"derivedFromId" TEXT, 
	description TEXT, 
	"diagnosticMarkers" TEXT, 
	files TEXT, 
	"histologicalDiagnosis" TEXT, 
	id TEXT NOT NULL, 
	"individualId" TEXT, 
	"materialSample" TEXT, 
	measurements TEXT, 
	"pathologicalStage" TEXT, 
	"pathologicalTnmFinding" TEXT, 
	"phenotypicFeatures" TEXT, 
	procedure TEXT, 
	"sampleProcessing" TEXT, 
	"sampleStorage" TEXT, 
	"sampleType" TEXT, 
	"sampledTissue" TEXT, 
	taxonomy TEXT, 
	"timeOfCollection" TEXT, 
	"tumorGrade" TEXT, 
	"tumorProgression" TEXT, 
	"Phenopacket_id" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY("histologicalDiagnosis") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("materialSample") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("pathologicalStage") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("sampleProcessing") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("sampleStorage") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("sampleType") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("sampledTissue") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY(taxonomy) REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("tumorGrade") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("tumorProgression") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("Phenopacket_id") REFERENCES "Phenopacket" (id)
);

CREATE TABLE "Disease" (
	"clinicalTnmFinding" TEXT, 
	"diseaseStage" TEXT, 
	excluded BOOLEAN, 
	laterality TEXT, 
	onset TEXT, 
	"primarySite" TEXT, 
	resolution TEXT, 
	term TEXT, 
	"Phenopacket_id" TEXT, 
	PRIMARY KEY ("clinicalTnmFinding", "diseaseStage", excluded, laterality, onset, "primarySite", resolution, term, "Phenopacket_id"), 
	FOREIGN KEY(laterality) REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("primarySite") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY(term) REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("Phenopacket_id") REFERENCES "Phenopacket" (id)
);

CREATE TABLE "Family" (
	"consanguinousParents" BOOLEAN, 
	files TEXT, 
	id TEXT NOT NULL, 
	"metaData" TEXT NOT NULL, 
	pedigree TEXT, 
	proband TEXT, 
	relatives TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(proband) REFERENCES "Phenopacket" (id)
);

CREATE TABLE "Interpretation" (
	diagnosis TEXT, 
	id TEXT NOT NULL, 
	"progressStatus" VARCHAR(16), 
	summary TEXT, 
	"Phenopacket_id" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY("Phenopacket_id") REFERENCES "Phenopacket" (id)
);

CREATE TABLE "MedicalAction" (
	"adverseEvents" TEXT, 
	procedure TEXT, 
	"radiationTherapy" TEXT, 
	"responseToTreatment" TEXT, 
	"therapeuticRegimen" TEXT, 
	treatment TEXT, 
	"treatmentIntent" TEXT, 
	"treatmentTarget" TEXT, 
	"treatmentTerminationReason" TEXT, 
	"Phenopacket_id" TEXT, 
	PRIMARY KEY ("adverseEvents", procedure, "radiationTherapy", "responseToTreatment", "therapeuticRegimen", treatment, "treatmentIntent", "treatmentTarget", "treatmentTerminationReason", "Phenopacket_id"), 
	FOREIGN KEY("responseToTreatment") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("treatmentIntent") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("treatmentTarget") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("treatmentTerminationReason") REFERENCES "OntologyClass" (id), 
	FOREIGN KEY("Phenopacket_id") REFERENCES "Phenopacket" (id)
);

CREATE TABLE "Member" (
	allele TEXT, 
	"copyNumber" TEXT, 
	curie TEXT, 
	haplotype TEXT, 
	id TEXT NOT NULL, 
	text TEXT, 
	"variationSet" TEXT, 
	"Member_id" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(allele) REFERENCES "Allele" (id), 
	FOREIGN KEY("copyNumber") REFERENCES "CopyNumber" (id), 
	FOREIGN KEY(text) REFERENCES "Text" (id), 
	FOREIGN KEY("Member_id") REFERENCES "Member" (id)
);

CREATE TABLE "SystemicVariation" (
	"copyNumber" TEXT, 
	PRIMARY KEY ("copyNumber"), 
	FOREIGN KEY("copyNumber") REFERENCES "CopyNumber" (id)
);

CREATE TABLE "Variation" (
	allele TEXT, 
	"copyNumber" TEXT, 
	haplotype TEXT, 
	text TEXT, 
	"variationSet" TEXT, 
	PRIMARY KEY (allele, "copyNumber", haplotype, text, "variationSet"), 
	FOREIGN KEY(allele) REFERENCES "Allele" (id), 
	FOREIGN KEY("copyNumber") REFERENCES "CopyNumber" (id), 
	FOREIGN KEY(text) REFERENCES "Text" (id)
);
