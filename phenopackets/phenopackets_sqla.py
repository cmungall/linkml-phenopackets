
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class Cohort(Base):
    """
    A group of individuals related in some phenotypic or genotypic aspect.
    """
    __tablename__ = 'Cohort'
    
    description = Column(Text())
    id = Column(Text(), primary_key=True)
    metaData_id = Column(Text(), ForeignKey('MetaData.id'))
    metaData = relationship("MetaData", uselist=False)
    
    
    # ManyToMany
    files = relationship( "File", secondary="Cohort_files")
    
    
    # ManyToMany
    members = relationship( "Phenopacket", secondary="Cohort_members")
    
    
    def __repr__(self):
        return f"Cohort(description={self.description},id={self.id},metaData_id={self.metaData_id},)"
        
    
        
    


class Family(Base):
    """
    Phenotype, sample and pedigree data required for a genomic diagnosis. Equivalent to the Genomics England InterpretationRequestRD https://github.com/genomicsengland/GelReportModels/blob/master/schemas/IDLs/org.gel.models.report.avro/5.0.0/InterpretationRequestRD.avdl
    """
    __tablename__ = 'Family'
    
    consanguinousParents = Column(Boolean())
    id = Column(Text(), primary_key=True)
    proband = Column(Text(), ForeignKey('Phenopacket.id'))
    metaData_id = Column(Text(), ForeignKey('MetaData.id'))
    metaData = relationship("MetaData", uselist=False)
    pedigree_id = Column(Text(), ForeignKey('Pedigree.id'))
    pedigree = relationship("Pedigree", uselist=False)
    
    
    # ManyToMany
    files = relationship( "File", secondary="Family_files")
    
    
    # ManyToMany
    relatives = relationship( "Phenopacket", secondary="Family_relatives")
    
    
    def __repr__(self):
        return f"Family(consanguinousParents={self.consanguinousParents},id={self.id},proband={self.proband},metaData_id={self.metaData_id},pedigree_id={self.pedigree_id},)"
        
    
        
    


class Phenopacket(Base):
    """
    An anonymous phenotypic description of an individual or biosample with potential genes of interest and/or diagnoses.  This is a bundle of high-level concepts with no specifically defined relational concepts. It is expected that the resources sharing the phenopackets will define and enforce their own semantics and level of requirements for included fields.
    """
    __tablename__ = 'Phenopacket'
    
    id = Column(Text(), primary_key=True)
    subject = Column(Text(), ForeignKey('Individual.id'))
    metaData_id = Column(Text(), ForeignKey('MetaData.id'))
    metaData = relationship("MetaData", uselist=False)
    
    
    # ManyToMany
    biosamples = relationship( "Biosample", secondary="Phenopacket_biosamples")
    
    
    # ManyToMany
    diseases = relationship( "Disease", secondary="Phenopacket_diseases")
    
    
    # ManyToMany
    files = relationship( "File", secondary="Phenopacket_files")
    
    
    # ManyToMany
    interpretations = relationship( "Interpretation", secondary="Phenopacket_interpretations")
    
    
    # ManyToMany
    measurements = relationship( "Measurement", secondary="Phenopacket_measurements")
    
    
    # ManyToMany
    medicalActions = relationship( "MedicalAction", secondary="Phenopacket_medicalActions")
    
    
    # ManyToMany
    phenotypicFeatures = relationship( "PhenotypicFeature", secondary="Phenopacket_phenotypicFeatures")
    
    
    def __repr__(self):
        return f"Phenopacket(id={self.id},subject={self.subject},metaData_id={self.metaData_id},)"
        
    
        
    


class PhenotypicFeature(Base):
    """
    An individual phenotypic feature, observed as either present or absent (negated), with possible onset, modifiers and frequency FHIR mapping: Condition (https://www.hl7.org/fhir/condition.html) or Observation (https://www.hl7.org/fhir/observation.html)
    """
    __tablename__ = 'PhenotypicFeature'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    description = Column(Text())
    excluded = Column(Boolean())
    severity = Column(Text(), ForeignKey('OntologyClass.id'))
    type = Column(Text(), ForeignKey('OntologyClass.id'))
    onset_id = Column(Text(), ForeignKey('TimeElement.id'))
    onset = relationship("TimeElement", uselist=False)
    resolution_id = Column(Text(), ForeignKey('TimeElement.id'))
    resolution = relationship("TimeElement", uselist=False)
    
    
    # ManyToMany
    evidence = relationship( "Evidence", secondary="PhenotypicFeature_evidence")
    
    
    # ManyToMany
    modifiers = relationship( "OntologyClass", secondary="PhenotypicFeature_modifiers")
    
    
    def __repr__(self):
        return f"PhenotypicFeature(id={self.id},description={self.description},excluded={self.excluded},severity={self.severity},type={self.type},onset_id={self.onset_id},resolution_id={self.resolution_id},)"
        
    
        
    


class Age(Base):
    """
    See http://build.fhir.org/datatypes and http://build.fhir.org/condition-definitions.html#Condition.onset_x_ In FHIR this is represented as a UCUM measurement - http://unitsofmeasure.org/trac/
    """
    __tablename__ = 'Age'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    iso8601duration = Column(Text())
    
    
    def __repr__(self):
        return f"Age(id={self.id},iso8601duration={self.iso8601duration},)"
        
    
        
    


class AgeRange(Base):
    """
    
    """
    __tablename__ = 'AgeRange'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    end_id = Column(Text(), ForeignKey('Age.id'))
    end = relationship("Age", uselist=False)
    start_id = Column(Text(), ForeignKey('Age.id'))
    start = relationship("Age", uselist=False)
    
    
    def __repr__(self):
        return f"AgeRange(id={self.id},end_id={self.end_id},start_id={self.start_id},)"
        
    
        
    


class Dictionary(Base):
    """
    
    """
    __tablename__ = 'Dictionary'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    
    
    def __repr__(self):
        return f"Dictionary(id={self.id},)"
        
    
        
    


class Evidence(Base):
    """
    FHIR mapping: Condition.evidence (https://www.hl7.org/fhir/condition-definitions.html#Condition.evidence)
    """
    __tablename__ = 'Evidence'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    evidenceCode = Column(Text(), ForeignKey('OntologyClass.id'))
    reference = Column(Text(), ForeignKey('ExternalReference.id'))
    
    
    def __repr__(self):
        return f"Evidence(id={self.id},evidenceCode={self.evidenceCode},reference={self.reference},)"
        
    
        
    


class ExternalReference(Base):
    """
    FHIR mapping: Reference (https://www.hl7.org/fhir/references.html)
    """
    __tablename__ = 'ExternalReference'
    
    description = Column(Text())
    id = Column(Text(), primary_key=True)
    reference = Column(Text(), ForeignKey('ExternalReference.id'))
    
    
    def __repr__(self):
        return f"ExternalReference(description={self.description},id={self.id},reference={self.reference},)"
        
    
        
    


class File(Base):
    """
    
    """
    __tablename__ = 'File'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    uri = Column(Text())
    fileAttributes_id = Column(Text(), ForeignKey('Dictionary.id'))
    fileAttributes = relationship("Dictionary", uselist=False)
    individualToFileIdentifiers_id = Column(Text(), ForeignKey('Dictionary.id'))
    individualToFileIdentifiers = relationship("Dictionary", uselist=False)
    
    
    def __repr__(self):
        return f"File(id={self.id},uri={self.uri},fileAttributes_id={self.fileAttributes_id},individualToFileIdentifiers_id={self.individualToFileIdentifiers_id},)"
        
    
        
    


class GestationalAge(Base):
    """
    
    """
    __tablename__ = 'GestationalAge'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    days = Column(Integer())
    weeks = Column(Integer())
    
    
    def __repr__(self):
        return f"GestationalAge(id={self.id},days={self.days},weeks={self.weeks},)"
        
    
        
    


class OntologyClass(Base):
    """
    A class (aka term, concept) in an ontology. FHIR mapping: CodeableConcept (http://www.hl7.org/fhir/datatypes.html#CodeableConcept) see also Coding (http://www.hl7.org/fhir/datatypes.html#Coding)
    """
    __tablename__ = 'OntologyClass'
    
    id = Column(Text(), primary_key=True)
    label = Column(Text())
    
    
    def __repr__(self):
        return f"OntologyClass(id={self.id},label={self.label},)"
        
    
        
    


class Procedure(Base):
    """
    A clinical procedure performed on a subject. By preference a single concept to indicate both the procedure and the body site should be used. In cases where this is not possible, the body site should be indicated using a separate ontology class. e.g. {"code":{"NCIT:C51585": "Biopsy of Soft Palate"}} {"code":{"NCIT:C28743": "Punch Biopsy"}, "body_site":{"UBERON:0003403": "skin of forearm"}} - a punch biopsy of the skin from the forearm FHIR mapping: Procedure (https://www.hl7.org/fhir/procedure.html)
    """
    __tablename__ = 'Procedure'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    bodySite = Column(Text(), ForeignKey('OntologyClass.id'))
    code = Column(Text(), ForeignKey('OntologyClass.id'))
    performed_id = Column(Text(), ForeignKey('TimeElement.id'))
    performed = relationship("TimeElement", uselist=False)
    
    
    def __repr__(self):
        return f"Procedure(id={self.id},bodySite={self.bodySite},code={self.code},performed_id={self.performed_id},)"
        
    
        
    


class TimeElement(Base):
    """
    
    """
    __tablename__ = 'TimeElement'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    ontologyClass = Column(Text(), ForeignKey('OntologyClass.id'))
    timestamp = Column(Text())
    age_id = Column(Text(), ForeignKey('Age.id'))
    age = relationship("Age", uselist=False)
    ageRange_id = Column(Text(), ForeignKey('AgeRange.id'))
    ageRange = relationship("AgeRange", uselist=False)
    gestationalAge_id = Column(Text(), ForeignKey('GestationalAge.id'))
    gestationalAge = relationship("GestationalAge", uselist=False)
    interval_id = Column(Text(), ForeignKey('TimeInterval.id'))
    interval = relationship("TimeInterval", uselist=False)
    
    
    def __repr__(self):
        return f"TimeElement(id={self.id},ontologyClass={self.ontologyClass},timestamp={self.timestamp},age_id={self.age_id},ageRange_id={self.ageRange_id},gestationalAge_id={self.gestationalAge_id},interval_id={self.interval_id},)"
        
    
        
    


class TimeInterval(Base):
    """
    
    """
    __tablename__ = 'TimeInterval'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    end_id = Column(Text(), ForeignKey('Age.id'))
    end = relationship("Age", uselist=False)
    start_id = Column(Text(), ForeignKey('Age.id'))
    start = relationship("Age", uselist=False)
    
    
    def __repr__(self):
        return f"TimeInterval(id={self.id},end_id={self.end_id},start_id={self.start_id},)"
        
    
        
    


class Timestamp(Base):
    """
    Protocol Buffers - Google's data interchange format Copyright 2008 Google Inc.  All rights reserved. https://developers.google.com/protocol-buffers/  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:  * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. * Neither the name of Google Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. A Timestamp represents a point in time independent of any time zone or local calendar, encoded as a count of seconds and fractions of seconds at nanosecond resolution. The count is relative to an epoch at UTC midnight on January 1, 1970, in the proleptic Gregorian calendar which extends the Gregorian calendar backwards to year one.  All minutes are 60 seconds long. Leap seconds are "smeared" so that no leap second table is needed for interpretation, using a [24-hour linear smear](https://developers.google.com/time/smear).  The range is from 0001-01-01T00:00:00Z to 9999-12-31T23:59:59.999999999Z. By restricting to that range, we ensure that we can convert to and from [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) date strings.  # Examples  Example 1: Compute Timestamp from POSIX `time()`.  Timestamp timestamp; timestamp.set_seconds(time(NULL)); timestamp.set_nanos(0);  Example 2: Compute Timestamp from POSIX `gettimeofday()`.  struct timeval tv; gettimeofday(&tv, NULL);  Timestamp timestamp; timestamp.set_seconds(tv.tv_sec); timestamp.set_nanos(tv.tv_usec * 1000);  Example 3: Compute Timestamp from Win32 `GetSystemTimeAsFileTime()`.  FILETIME ft; GetSystemTimeAsFileTime(&ft); UINT64 ticks = (((UINT64)ft.dwHighDateTime) << 32) | ft.dwLowDateTime;  // A Windows tick is 100 nanoseconds. Windows epoch 1601-01-01T00:00:00Z // is 11644473600 seconds before Unix epoch 1970-01-01T00:00:00Z. Timestamp timestamp; timestamp.set_seconds((INT64) ((ticks / 10000000) - 11644473600LL)); timestamp.set_nanos((INT32) ((ticks % 10000000) * 100));  Example 4: Compute Timestamp from Java `System.currentTimeMillis()`.  long millis = System.currentTimeMillis();  Timestamp timestamp = Timestamp.newBuilder().setSeconds(millis / 1000) .setNanos((int) ((millis % 1000) * 1000000)).build();   Example 5: Compute Timestamp from Java `Instant.now()`.  Instant now = Instant.now();  Timestamp timestamp = Timestamp.newBuilder().setSeconds(now.getEpochSecond()) .setNanos(now.getNano()).build();   Example 6: Compute Timestamp from current time in Python.  timestamp = Timestamp() timestamp.GetCurrentTime()  # JSON Mapping  In JSON format, the Timestamp type is encoded as a string in the [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) format. That is, the format is "{year}-{month}-{day}T{hour}:{min}:{sec}[.{frac_sec}]Z" where {year} is always expressed using four digits while {month}, {day}, {hour}, {min}, and {sec} are zero-padded to two digits each. The fractional seconds, which can go up to 9 digits (i.e. up to 1 nanosecond resolution), are optional. The "Z" suffix indicates the timezone ("UTC"); the timezone is required. A proto3 JSON serializer should always use UTC (as indicated by "Z") when printing the Timestamp type and a proto3 JSON parser should be able to accept both UTC and other timezones (as indicated by an offset).  For example, "2017-01-15T01:30:15.01Z" encodes 15.01 seconds past 01:30 UTC on January 15, 2017.  In JavaScript, one can convert a Date object to this format using the standard [toISOString()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString) method. In Python, a standard `datetime.datetime` object can be converted to this format using [`strftime`](https://docs.python.org/2/library/time.html#time.strftime) with the time format spec '%Y-%m-%dT%H:%M:%S.%fZ'. Likewise, in Java, one can use the Joda Time's [`ISODateTimeFormat.dateTime()`]( http://www.joda.org/joda-time/apidocs/org/joda/time/format/ISODateTimeFormat.html#dateTime%2D%2D ) to obtain a formatter capable of generating timestamps in this format.  
    """
    __tablename__ = 'Timestamp'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    nanos = Column(Integer())
    seconds = Column(Integer())
    
    
    def __repr__(self):
        return f"Timestamp(id={self.id},nanos={self.nanos},seconds={self.seconds},)"
        
    
        
    


class Pedigree(Base):
    """
    https://software.broadinstitute.org/gatk/documentation/article?id=11016
    """
    __tablename__ = 'Pedigree'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    
    
    # ManyToMany
    persons = relationship( "Person", secondary="Pedigree_persons")
    
    
    def __repr__(self):
        return f"Pedigree(id={self.id},)"
        
    
        
    


class Person(Base):
    """
    
    """
    __tablename__ = 'Person'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    affectedStatus = Column(Enum('AFFECTED', 'MISSING', 'UNAFFECTED', name='AffectedStatus'))
    familyId = Column(Text())
    individualId = Column(Text())
    maternalId = Column(Text())
    paternalId = Column(Text())
    sex = Column(Enum('FEMALE', 'MALE', 'OTHER_SEX', 'UNKNOWN_SEX', name='Sex'))
    
    
    def __repr__(self):
        return f"Person(id={self.id},affectedStatus={self.affectedStatus},familyId={self.familyId},individualId={self.individualId},maternalId={self.maternalId},paternalId={self.paternalId},sex={self.sex},)"
        
    
        
    


class Individual(Base):
    """
    An individual (or subject) typically corresponds to an individual human or another organism. FHIR mapping: Patient (https://www.hl7.org/fhir/patient.html).
    """
    __tablename__ = 'Individual'
    
    dateOfBirth = Column(Text())
    gender = Column(Text(), ForeignKey('OntologyClass.id'))
    id = Column(Text(), primary_key=True)
    karyotypicSex = Column(Enum('OTHER_KARYOTYPE', 'UNKNOWN_KARYOTYPE', 'XO', 'XX', 'XXX', 'XXXX', 'XXXY', 'XXY', 'XXYY', 'XY', 'XYY', name='KaryotypicSex'))
    sex = Column(Enum('FEMALE', 'MALE', 'OTHER_SEX', 'UNKNOWN_SEX', name='Sex'))
    taxonomy = Column(Text(), ForeignKey('OntologyClass.id'))
    timeAtLastEncounter_id = Column(Text(), ForeignKey('TimeElement.id'))
    timeAtLastEncounter = relationship("TimeElement", uselist=False)
    vitalStatus_id = Column(Text(), ForeignKey('VitalStatus.id'))
    vitalStatus = relationship("VitalStatus", uselist=False)
    
    
    alternateIds_rel = relationship( "IndividualAlternateIds" )
    alternateIds = association_proxy("alternateIds_rel", "alternateIds",
                                  creator=lambda x_: IndividualAlternateIds(alternateIds=x_))
    
    
    def __repr__(self):
        return f"Individual(dateOfBirth={self.dateOfBirth},gender={self.gender},id={self.id},karyotypicSex={self.karyotypicSex},sex={self.sex},taxonomy={self.taxonomy},timeAtLastEncounter_id={self.timeAtLastEncounter_id},vitalStatus_id={self.vitalStatus_id},)"
        
    
        
    


class VitalStatus(Base):
    """
    
    """
    __tablename__ = 'VitalStatus'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    causeOfDeath = Column(Text(), ForeignKey('OntologyClass.id'))
    status = Column(Enum('ALIVE', 'DECEASED', 'UNKNOWN_STATUS', name='Status'))
    survivalTimeInDays = Column(Integer())
    timeOfDeath_id = Column(Text(), ForeignKey('TimeElement.id'))
    timeOfDeath = relationship("TimeElement", uselist=False)
    
    
    def __repr__(self):
        return f"VitalStatus(id={self.id},causeOfDeath={self.causeOfDeath},status={self.status},survivalTimeInDays={self.survivalTimeInDays},timeOfDeath_id={self.timeOfDeath_id},)"
        
    
        
    


class MetaData(Base):
    """
    
    """
    __tablename__ = 'MetaData'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    created = Column(Text())
    createdBy = Column(Text())
    phenopacketSchemaVersion = Column(Text())
    submittedBy = Column(Text())
    
    
    # ManyToMany
    externalReferences = relationship( "ExternalReference", secondary="MetaData_externalReferences")
    
    
    # ManyToMany
    resources = relationship( "Resource", secondary="MetaData_resources")
    
    
    # ManyToMany
    updates = relationship( "Update", secondary="MetaData_updates")
    
    
    def __repr__(self):
        return f"MetaData(id={self.id},created={self.created},createdBy={self.createdBy},phenopacketSchemaVersion={self.phenopacketSchemaVersion},submittedBy={self.submittedBy},)"
        
    
        
    


class Resource(Base):
    """
    Description of an external resource used for referencing an object. For example the resource may be an ontology such as the HPO or SNOMED. FHIR mapping: CodeSystem (http://www.hl7.org/fhir/codesystem.html)
    """
    __tablename__ = 'Resource'
    
    id = Column(Text(), primary_key=True)
    iriPrefix = Column(Text())
    name = Column(Text())
    namespacePrefix = Column(Text())
    url = Column(Text())
    version = Column(Text())
    
    
    def __repr__(self):
        return f"Resource(id={self.id},iriPrefix={self.iriPrefix},name={self.name},namespacePrefix={self.namespacePrefix},url={self.url},version={self.version},)"
        
    
        
    


class Update(Base):
    """
    Information about when an update to a record occurred, who or what made the update and any pertinent information regarding the content and/or reason for the update
    """
    __tablename__ = 'Update'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    comment = Column(Text())
    timestamp = Column(Text())
    updatedBy = Column(Text())
    
    
    def __repr__(self):
        return f"Update(id={self.id},comment={self.comment},timestamp={self.timestamp},updatedBy={self.updatedBy},)"
        
    
        
    


class DoseInterval(Base):
    """
    e.g. 50mg/ml 3 times daily for two weeks
    """
    __tablename__ = 'DoseInterval'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    scheduleFrequency = Column(Text(), ForeignKey('OntologyClass.id'))
    interval_id = Column(Text(), ForeignKey('TimeInterval.id'))
    interval = relationship("TimeInterval", uselist=False)
    quantity_id = Column(Text(), ForeignKey('Quantity.id'))
    quantity = relationship("Quantity", uselist=False)
    
    
    def __repr__(self):
        return f"DoseInterval(id={self.id},scheduleFrequency={self.scheduleFrequency},interval_id={self.interval_id},quantity_id={self.quantity_id},)"
        
    
        
    


class MedicalAction(Base):
    """
    medication, procedure, other actions taken for clinical management
    """
    __tablename__ = 'MedicalAction'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    responseToTreatment = Column(Text(), ForeignKey('OntologyClass.id'))
    treatmentIntent = Column(Text(), ForeignKey('OntologyClass.id'))
    treatmentTarget = Column(Text(), ForeignKey('OntologyClass.id'))
    treatmentTerminationReason = Column(Text(), ForeignKey('OntologyClass.id'))
    procedure_id = Column(Text(), ForeignKey('Procedure.id'))
    procedure = relationship("Procedure", uselist=False)
    radiationTherapy_id = Column(Text(), ForeignKey('RadiationTherapy.id'))
    radiationTherapy = relationship("RadiationTherapy", uselist=False)
    therapeuticRegimen_id = Column(Text(), ForeignKey('TherapeuticRegimen.id'))
    therapeuticRegimen = relationship("TherapeuticRegimen", uselist=False)
    treatment_id = Column(Text(), ForeignKey('Treatment.id'))
    treatment = relationship("Treatment", uselist=False)
    
    
    # ManyToMany
    adverseEvents = relationship( "OntologyClass", secondary="MedicalAction_adverseEvents")
    
    
    def __repr__(self):
        return f"MedicalAction(id={self.id},responseToTreatment={self.responseToTreatment},treatmentIntent={self.treatmentIntent},treatmentTarget={self.treatmentTarget},treatmentTerminationReason={self.treatmentTerminationReason},procedure_id={self.procedure_id},radiationTherapy_id={self.radiationTherapy_id},therapeuticRegimen_id={self.therapeuticRegimen_id},treatment_id={self.treatment_id},)"
        
    
        
    


class RadiationTherapy(Base):
    """
    RadiationTherapy
    """
    __tablename__ = 'RadiationTherapy'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    bodySite = Column(Text(), ForeignKey('OntologyClass.id'))
    dosage = Column(Integer())
    fractions = Column(Integer())
    modality = Column(Text(), ForeignKey('OntologyClass.id'))
    
    
    def __repr__(self):
        return f"RadiationTherapy(id={self.id},bodySite={self.bodySite},dosage={self.dosage},fractions={self.fractions},modality={self.modality},)"
        
    
        
    


class TherapeuticRegimen(Base):
    """
    ARGO mapping radiation::radiation_therapy_type (missing)
    """
    __tablename__ = 'TherapeuticRegimen'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    externalReference = Column(Text(), ForeignKey('ExternalReference.id'))
    ontologyClass = Column(Text(), ForeignKey('OntologyClass.id'))
    regimenStatus = Column(Enum('COMPLETED', 'DISCONTINUED', 'STARTED', 'UNKNOWN_STATUS', name='RegimenStatus'))
    endTime_id = Column(Text(), ForeignKey('TimeElement.id'))
    endTime = relationship("TimeElement", uselist=False)
    startTime_id = Column(Text(), ForeignKey('TimeElement.id'))
    startTime = relationship("TimeElement", uselist=False)
    
    
    def __repr__(self):
        return f"TherapeuticRegimen(id={self.id},externalReference={self.externalReference},ontologyClass={self.ontologyClass},regimenStatus={self.regimenStatus},endTime_id={self.endTime_id},startTime_id={self.startTime_id},)"
        
    
        
    


class Treatment(Base):
    """
    ARGO mapping treatment::is_primary_treatment (missing) treatment with an agent, such as a drug
    """
    __tablename__ = 'Treatment'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    agent = Column(Text(), ForeignKey('OntologyClass.id'))
    drugType = Column(Enum('ADMINISTRATION_RELATED_TO_PROCEDURE', 'EHR_MEDICATION_LIST', 'PRESCRIPTION', 'UNKNOWN_DRUG_TYPE', name='DrugType'))
    routeOfAdministration = Column(Text(), ForeignKey('OntologyClass.id'))
    cumulativeDose_id = Column(Text(), ForeignKey('Quantity.id'))
    cumulativeDose = relationship("Quantity", uselist=False)
    
    
    # ManyToMany
    doseIntervals = relationship( "DoseInterval", secondary="Treatment_doseIntervals")
    
    
    def __repr__(self):
        return f"Treatment(id={self.id},agent={self.agent},drugType={self.drugType},routeOfAdministration={self.routeOfAdministration},cumulativeDose_id={self.cumulativeDose_id},)"
        
    
        
    


class ComplexValue(Base):
    """
    
    """
    __tablename__ = 'ComplexValue'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    
    
    # ManyToMany
    typedQuantities = relationship( "TypedQuantity", secondary="ComplexValue_typedQuantities")
    
    
    def __repr__(self):
        return f"ComplexValue(id={self.id},)"
        
    
        
    


class Measurement(Base):
    """
    FHIR mapping: Observation (https://www.hl7.org/fhir/observation.html)
    """
    __tablename__ = 'Measurement'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    assay = Column(Text(), ForeignKey('OntologyClass.id'))
    description = Column(Text())
    complexValue_id = Column(Text(), ForeignKey('ComplexValue.id'))
    complexValue = relationship("ComplexValue", uselist=False)
    procedure_id = Column(Text(), ForeignKey('Procedure.id'))
    procedure = relationship("Procedure", uselist=False)
    timeObserved_id = Column(Text(), ForeignKey('TimeElement.id'))
    timeObserved = relationship("TimeElement", uselist=False)
    value_id = Column(Text(), ForeignKey('Value.id'))
    value = relationship("Value", uselist=False)
    
    
    def __repr__(self):
        return f"Measurement(id={self.id},assay={self.assay},description={self.description},complexValue_id={self.complexValue_id},procedure_id={self.procedure_id},timeObserved_id={self.timeObserved_id},value_id={self.value_id},)"
        
    
        
    


class Quantity(Base):
    """
    
    """
    __tablename__ = 'Quantity'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    unit = Column(Text(), ForeignKey('OntologyClass.id'))
    referenceRange_id = Column(Text(), ForeignKey('ReferenceRange.id'))
    referenceRange = relationship("ReferenceRange", uselist=False)
    value_id = Column(Text(), ForeignKey('Value.id'))
    value = relationship("Value", uselist=False)
    
    
    def __repr__(self):
        return f"Quantity(id={self.id},unit={self.unit},referenceRange_id={self.referenceRange_id},value_id={self.value_id},)"
        
    
        
    


class ReferenceRange(Base):
    """
    
    """
    __tablename__ = 'ReferenceRange'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    high = Column(Float())
    low = Column(Float())
    unit = Column(Text(), ForeignKey('OntologyClass.id'))
    
    
    def __repr__(self):
        return f"ReferenceRange(id={self.id},high={self.high},low={self.low},unit={self.unit},)"
        
    
        
    


class TypedQuantity(Base):
    """
    For complex measurements, such as blood pressure where more than one component quantity is required to describe the measurement
    """
    __tablename__ = 'TypedQuantity'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    type = Column(Text(), ForeignKey('OntologyClass.id'))
    quantity_id = Column(Text(), ForeignKey('Quantity.id'))
    quantity = relationship("Quantity", uselist=False)
    
    
    def __repr__(self):
        return f"TypedQuantity(id={self.id},type={self.type},quantity_id={self.quantity_id},)"
        
    
        
    


class Value(Base):
    """
    
    """
    __tablename__ = 'Value'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    ontologyClass = Column(Text(), ForeignKey('OntologyClass.id'))
    quantity_id = Column(Text(), ForeignKey('Quantity.id'))
    quantity = relationship("Quantity", uselist=False)
    
    
    def __repr__(self):
        return f"Value(id={self.id},ontologyClass={self.ontologyClass},quantity_id={self.quantity_id},)"
        
    
        
    


class Diagnosis(Base):
    """
    
    """
    __tablename__ = 'Diagnosis'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    disease = Column(Text(), ForeignKey('OntologyClass.id'))
    
    
    # ManyToMany
    genomicInterpretations = relationship( "GenomicInterpretation", secondary="Diagnosis_genomicInterpretations")
    
    
    def __repr__(self):
        return f"Diagnosis(id={self.id},disease={self.disease},)"
        
    
        
    


class GenomicInterpretation(Base):
    """
    A statement about the contribution of a genomic element towards the observed phenotype. Note that this does not intend to encode any knowledge or results of specific computations.
    """
    __tablename__ = 'GenomicInterpretation'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    interpretationStatus = Column(Enum('CANDIDATE', 'CAUSATIVE', 'CONTRIBUTORY', 'REJECTED', 'UNKNOWN_STATUS', name='InterpretationStatus'))
    subjectOrBiosampleId = Column(Text())
    gene_id = Column(Text(), ForeignKey('GeneDescriptor.id'))
    gene = relationship("GeneDescriptor", uselist=False)
    variantInterpretation_id = Column(Text(), ForeignKey('VariantInterpretation.id'))
    variantInterpretation = relationship("VariantInterpretation", uselist=False)
    
    
    def __repr__(self):
        return f"GenomicInterpretation(id={self.id},interpretationStatus={self.interpretationStatus},subjectOrBiosampleId={self.subjectOrBiosampleId},gene_id={self.gene_id},variantInterpretation_id={self.variantInterpretation_id},)"
        
    
        
    


class Interpretation(Base):
    """
    
    """
    __tablename__ = 'Interpretation'
    
    id = Column(Text(), primary_key=True)
    progressStatus = Column(Enum('COMPLETED', 'IN_PROGRESS', 'SOLVED', 'UNKNOWN_PROGRESS', 'UNSOLVED', name='ProgressStatus'))
    summary = Column(Text())
    diagnosis_id = Column(Text(), ForeignKey('Diagnosis.id'))
    diagnosis = relationship("Diagnosis", uselist=False)
    
    
    def __repr__(self):
        return f"Interpretation(id={self.id},progressStatus={self.progressStatus},summary={self.summary},diagnosis_id={self.diagnosis_id},)"
        
    
        
    


class VariantInterpretation(Base):
    """
    
    """
    __tablename__ = 'VariantInterpretation'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    acmgPathogenicityClassification = Column(Enum('BENIGN', 'LIKELY_BENIGN', 'LIKELY_PATHOGENIC', 'NOT_PROVIDED', 'PATHOGENIC', 'UNCERTAIN_SIGNIFICANCE', name='AcmgPathogenicityClassification'))
    therapeuticActionability = Column(Enum('ACTIONABLE', 'NOT_ACTIONABLE', 'UNKNOWN_ACTIONABILITY', name='TherapeuticActionability'))
    variationDescriptor = Column(Text(), ForeignKey('VariationDescriptor.id'))
    
    
    def __repr__(self):
        return f"VariantInterpretation(id={self.id},acmgPathogenicityClassification={self.acmgPathogenicityClassification},therapeuticActionability={self.therapeuticActionability},variationDescriptor={self.variationDescriptor},)"
        
    
        
    


class Expression(Base):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#expression
    """
    __tablename__ = 'Expression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    syntax = Column(Text())
    version = Column(Text())
    value_id = Column(Text(), ForeignKey('Value.id'))
    value = relationship("Value", uselist=False)
    
    
    def __repr__(self):
        return f"Expression(id={self.id},syntax={self.syntax},version={self.version},value_id={self.value_id},)"
        
    
        
    


class Extension(Base):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#extension
    """
    __tablename__ = 'Extension'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    name = Column(Text())
    
    
    # ManyToMany
    value = relationship( "Value", secondary="Extension_value")
    
    
    def __repr__(self):
        return f"Extension(id={self.id},name={self.name},)"
        
    
        
    


class GeneDescriptor(Base):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#gene-descriptor
    """
    __tablename__ = 'GeneDescriptor'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    description = Column(Text())
    symbol = Column(Text())
    valueId = Column(Text())
    
    
    alternateIds_rel = relationship( "GeneDescriptorAlternateIds" )
    alternateIds = association_proxy("alternateIds_rel", "alternateIds",
                                  creator=lambda x_: GeneDescriptorAlternateIds(alternateIds=x_))
    
    
    alternateSymbols_rel = relationship( "GeneDescriptorAlternateSymbols" )
    alternateSymbols = association_proxy("alternateSymbols_rel", "alternateSymbols",
                                  creator=lambda x_: GeneDescriptorAlternateSymbols(alternateSymbols=x_))
    
    
    xrefs_rel = relationship( "GeneDescriptorXrefs" )
    xrefs = association_proxy("xrefs_rel", "xrefs",
                                  creator=lambda x_: GeneDescriptorXrefs(xrefs=x_))
    
    
    def __repr__(self):
        return f"GeneDescriptor(id={self.id},description={self.description},symbol={self.symbol},valueId={self.valueId},)"
        
    
        
    


class VariationDescriptor(Base):
    """
    
    """
    __tablename__ = 'VariationDescriptor'
    
    allelicState = Column(Text(), ForeignKey('OntologyClass.id'))
    description = Column(Text())
    id = Column(Text(), primary_key=True)
    label = Column(Text())
    moleculeContext = Column(Enum('genomic', 'protein', 'transcript', 'unspecified_molecule_context', name='MoleculeContext'))
    structuralType = Column(Text(), ForeignKey('OntologyClass.id'))
    vcfRecord = Column(Text(), ForeignKey('VcfRecord.id'))
    vrsRefAlleleSeq = Column(Text())
    geneContext_id = Column(Text(), ForeignKey('GeneDescriptor.id'))
    geneContext = relationship("GeneDescriptor", uselist=False)
    variation_id = Column(Text(), ForeignKey('Variation.id'))
    variation = relationship("Variation", uselist=False)
    
    
    alternateLabels_rel = relationship( "VariationDescriptorAlternateLabels" )
    alternateLabels = association_proxy("alternateLabels_rel", "alternateLabels",
                                  creator=lambda x_: VariationDescriptorAlternateLabels(alternateLabels=x_))
    
    
    # ManyToMany
    expressions = relationship( "Expression", secondary="VariationDescriptor_expressions")
    
    
    # ManyToMany
    extensions = relationship( "Extension", secondary="VariationDescriptor_extensions")
    
    
    xrefs_rel = relationship( "VariationDescriptorXrefs" )
    xrefs = association_proxy("xrefs_rel", "xrefs",
                                  creator=lambda x_: VariationDescriptorXrefs(xrefs=x_))
    
    
    def __repr__(self):
        return f"VariationDescriptor(allelicState={self.allelicState},description={self.description},id={self.id},label={self.label},moleculeContext={self.moleculeContext},structuralType={self.structuralType},vcfRecord={self.vcfRecord},vrsRefAlleleSeq={self.vrsRefAlleleSeq},geneContext_id={self.geneContext_id},variation_id={self.variation_id},)"
        
    
        
    


class VcfRecord(Base):
    """
    
    """
    __tablename__ = 'VcfRecord'
    
    alt = Column(Text())
    chrom = Column(Text())
    filter = Column(Text())
    genomeAssembly = Column(Text())
    id = Column(Text(), primary_key=True)
    info = Column(Text())
    pos = Column(Integer())
    qual = Column(Text())
    ref = Column(Text())
    
    
    def __repr__(self):
        return f"VcfRecord(alt={self.alt},chrom={self.chrom},filter={self.filter},genomeAssembly={self.genomeAssembly},id={self.id},info={self.info},pos={self.pos},qual={self.qual},ref={self.ref},)"
        
    
        
    


class Abundance(Base):
    """
    
    """
    __tablename__ = 'Abundance'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    copyNumber = Column(Text(), ForeignKey('CopyNumber.id'))
    
    
    def __repr__(self):
        return f"Abundance(id={self.id},copyNumber={self.copyNumber},)"
        
    
        
    


class Allele(Base):
    """
    
    """
    __tablename__ = 'Allele'
    
    chromosomeLocation = Column(Text(), ForeignKey('ChromosomeLocation.id'))
    curie = Column(Text())
    id = Column(Text(), primary_key=True)
    sequenceLocation = Column(Text(), ForeignKey('SequenceLocation.id'))
    derivedSequenceExpression_id = Column(Text(), ForeignKey('DerivedSequenceExpression.id'))
    derivedSequenceExpression = relationship("DerivedSequenceExpression", uselist=False)
    literalSequenceExpression_id = Column(Text(), ForeignKey('LiteralSequenceExpression.id'))
    literalSequenceExpression = relationship("LiteralSequenceExpression", uselist=False)
    repeatedSequenceExpression_id = Column(Text(), ForeignKey('RepeatedSequenceExpression.id'))
    repeatedSequenceExpression = relationship("RepeatedSequenceExpression", uselist=False)
    
    
    def __repr__(self):
        return f"Allele(chromosomeLocation={self.chromosomeLocation},curie={self.curie},id={self.id},sequenceLocation={self.sequenceLocation},derivedSequenceExpression_id={self.derivedSequenceExpression_id},literalSequenceExpression_id={self.literalSequenceExpression_id},repeatedSequenceExpression_id={self.repeatedSequenceExpression_id},)"
        
    
        
    


class ChromosomeLocation(Base):
    """
    
    """
    __tablename__ = 'ChromosomeLocation'
    
    chr = Column(Text())
    id = Column(Text(), primary_key=True)
    speciesId = Column(Text())
    interval_id = Column(Text(), ForeignKey('TimeInterval.id'))
    interval = relationship("TimeInterval", uselist=False)
    
    
    def __repr__(self):
        return f"ChromosomeLocation(chr={self.chr},id={self.id},speciesId={self.speciesId},interval_id={self.interval_id},)"
        
    
        
    


class CopyNumber(Base):
    """
    
    """
    __tablename__ = 'CopyNumber'
    
    allele = Column(Text(), ForeignKey('Allele.id'))
    curie = Column(Text())
    id = Column(Text(), primary_key=True)
    definiteRange_id = Column(Text(), ForeignKey('DefiniteRange.id'))
    definiteRange = relationship("DefiniteRange", uselist=False)
    derivedSequenceExpression_id = Column(Text(), ForeignKey('DerivedSequenceExpression.id'))
    derivedSequenceExpression = relationship("DerivedSequenceExpression", uselist=False)
    gene_id = Column(Text(), ForeignKey('GeneDescriptor.id'))
    gene = relationship("GeneDescriptor", uselist=False)
    haplotype_id = Column(Text(), ForeignKey('Haplotype.id'))
    haplotype = relationship("Haplotype", uselist=False)
    indefiniteRange_id = Column(Text(), ForeignKey('IndefiniteRange.id'))
    indefiniteRange = relationship("IndefiniteRange", uselist=False)
    literalSequenceExpression_id = Column(Text(), ForeignKey('LiteralSequenceExpression.id'))
    literalSequenceExpression = relationship("LiteralSequenceExpression", uselist=False)
    number_id = Column(Text(), ForeignKey('Number.id'))
    number = relationship("Number", uselist=False)
    repeatedSequenceExpression_id = Column(Text(), ForeignKey('RepeatedSequenceExpression.id'))
    repeatedSequenceExpression = relationship("RepeatedSequenceExpression", uselist=False)
    
    
    def __repr__(self):
        return f"CopyNumber(allele={self.allele},curie={self.curie},id={self.id},definiteRange_id={self.definiteRange_id},derivedSequenceExpression_id={self.derivedSequenceExpression_id},gene_id={self.gene_id},haplotype_id={self.haplotype_id},indefiniteRange_id={self.indefiniteRange_id},literalSequenceExpression_id={self.literalSequenceExpression_id},number_id={self.number_id},repeatedSequenceExpression_id={self.repeatedSequenceExpression_id},)"
        
    
        
    


class CytobandInterval(Base):
    """
    
    """
    __tablename__ = 'CytobandInterval'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    end_id = Column(Text(), ForeignKey('Age.id'))
    end = relationship("Age", uselist=False)
    start_id = Column(Text(), ForeignKey('Age.id'))
    start = relationship("Age", uselist=False)
    
    
    def __repr__(self):
        return f"CytobandInterval(id={self.id},end_id={self.end_id},start_id={self.start_id},)"
        
    
        
    


class DefiniteRange(Base):
    """
    
    """
    __tablename__ = 'DefiniteRange'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    max = Column(Integer())
    min = Column(Integer())
    
    
    def __repr__(self):
        return f"DefiniteRange(id={self.id},max={self.max},min={self.min},)"
        
    
        
    


class DerivedSequenceExpression(Base):
    """
    
    """
    __tablename__ = 'DerivedSequenceExpression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    location = Column(Text(), ForeignKey('SequenceLocation.id'))
    reverseComplement = Column(Boolean())
    
    
    def __repr__(self):
        return f"DerivedSequenceExpression(id={self.id},location={self.location},reverseComplement={self.reverseComplement},)"
        
    
        
    


class Feature(Base):
    """
    
    """
    __tablename__ = 'Feature'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    gene_id = Column(Text(), ForeignKey('GeneDescriptor.id'))
    gene = relationship("GeneDescriptor", uselist=False)
    
    
    def __repr__(self):
        return f"Feature(id={self.id},gene_id={self.gene_id},)"
        
    
        
    


class Gene(Base):
    """
    
    """
    __tablename__ = 'Gene'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    geneId = Column(Text())
    
    
    def __repr__(self):
        return f"Gene(id={self.id},geneId={self.geneId},)"
        
    
        
    


class Haplotype(Base):
    """
    
    """
    __tablename__ = 'Haplotype'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    
    
    def __repr__(self):
        return f"Haplotype(id={self.id},)"
        
    
        
    


class IndefiniteRange(Base):
    """
    
    """
    __tablename__ = 'IndefiniteRange'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    comparator = Column(Text())
    value_id = Column(Text(), ForeignKey('Value.id'))
    value = relationship("Value", uselist=False)
    
    
    def __repr__(self):
        return f"IndefiniteRange(id={self.id},comparator={self.comparator},value_id={self.value_id},)"
        
    
        
    


class LiteralSequenceExpression(Base):
    """
    
    """
    __tablename__ = 'LiteralSequenceExpression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    sequence = Column(Text())
    
    
    def __repr__(self):
        return f"LiteralSequenceExpression(id={self.id},sequence={self.sequence},)"
        
    
        
    


class Location(Base):
    """
    
    """
    __tablename__ = 'Location'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    chromosomeLocation = Column(Text(), ForeignKey('ChromosomeLocation.id'))
    sequenceLocation = Column(Text(), ForeignKey('SequenceLocation.id'))
    
    
    def __repr__(self):
        return f"Location(id={self.id},chromosomeLocation={self.chromosomeLocation},sequenceLocation={self.sequenceLocation},)"
        
    
        
    


class Member(Base):
    """
    
    """
    __tablename__ = 'Member'
    
    allele = Column(Text(), ForeignKey('Allele.id'))
    copyNumber = Column(Text(), ForeignKey('CopyNumber.id'))
    curie = Column(Text())
    id = Column(Text(), primary_key=True)
    text = Column(Text(), ForeignKey('Text.id'))
    haplotype_id = Column(Text(), ForeignKey('Haplotype.id'))
    haplotype = relationship("Haplotype", uselist=False)
    variationSet_id = Column(Text(), ForeignKey('VariationSet.id'))
    variationSet = relationship("VariationSet", uselist=False)
    
    
    # ManyToMany
    members = relationship( "Phenopacket", secondary="Member_members")
    
    
    def __repr__(self):
        return f"Member(allele={self.allele},copyNumber={self.copyNumber},curie={self.curie},id={self.id},text={self.text},haplotype_id={self.haplotype_id},variationSet_id={self.variationSet_id},)"
        
    
        
    


class MolecularVariation(Base):
    """
    
    """
    __tablename__ = 'MolecularVariation'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    allele = Column(Text(), ForeignKey('Allele.id'))
    haplotype_id = Column(Text(), ForeignKey('Haplotype.id'))
    haplotype = relationship("Haplotype", uselist=False)
    
    
    def __repr__(self):
        return f"MolecularVariation(id={self.id},allele={self.allele},haplotype_id={self.haplotype_id},)"
        
    
        
    


class Number(Base):
    """
    
    """
    __tablename__ = 'Number'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    value_id = Column(Text(), ForeignKey('Value.id'))
    value = relationship("Value", uselist=False)
    
    
    def __repr__(self):
        return f"Number(id={self.id},value_id={self.value_id},)"
        
    
        
    


class RepeatedSequenceExpression(Base):
    """
    
    """
    __tablename__ = 'RepeatedSequenceExpression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    definiteRange_id = Column(Text(), ForeignKey('DefiniteRange.id'))
    definiteRange = relationship("DefiniteRange", uselist=False)
    derivedSequenceExpression_id = Column(Text(), ForeignKey('DerivedSequenceExpression.id'))
    derivedSequenceExpression = relationship("DerivedSequenceExpression", uselist=False)
    indefiniteRange_id = Column(Text(), ForeignKey('IndefiniteRange.id'))
    indefiniteRange = relationship("IndefiniteRange", uselist=False)
    literalSequenceExpression_id = Column(Text(), ForeignKey('LiteralSequenceExpression.id'))
    literalSequenceExpression = relationship("LiteralSequenceExpression", uselist=False)
    number_id = Column(Text(), ForeignKey('Number.id'))
    number = relationship("Number", uselist=False)
    
    
    def __repr__(self):
        return f"RepeatedSequenceExpression(id={self.id},definiteRange_id={self.definiteRange_id},derivedSequenceExpression_id={self.derivedSequenceExpression_id},indefiniteRange_id={self.indefiniteRange_id},literalSequenceExpression_id={self.literalSequenceExpression_id},number_id={self.number_id},)"
        
    
        
    


class SequenceExpression(Base):
    """
    
    """
    __tablename__ = 'SequenceExpression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    derivedSequenceExpression_id = Column(Text(), ForeignKey('DerivedSequenceExpression.id'))
    derivedSequenceExpression = relationship("DerivedSequenceExpression", uselist=False)
    literalSequenceExpression_id = Column(Text(), ForeignKey('LiteralSequenceExpression.id'))
    literalSequenceExpression = relationship("LiteralSequenceExpression", uselist=False)
    repeatedSequenceExpression_id = Column(Text(), ForeignKey('RepeatedSequenceExpression.id'))
    repeatedSequenceExpression = relationship("RepeatedSequenceExpression", uselist=False)
    
    
    def __repr__(self):
        return f"SequenceExpression(id={self.id},derivedSequenceExpression_id={self.derivedSequenceExpression_id},literalSequenceExpression_id={self.literalSequenceExpression_id},repeatedSequenceExpression_id={self.repeatedSequenceExpression_id},)"
        
    
        
    


class SequenceInterval(Base):
    """
    
    """
    __tablename__ = 'SequenceInterval'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    endDefiniteRange_id = Column(Text(), ForeignKey('DefiniteRange.id'))
    endDefiniteRange = relationship("DefiniteRange", uselist=False)
    endIndefiniteRange_id = Column(Text(), ForeignKey('IndefiniteRange.id'))
    endIndefiniteRange = relationship("IndefiniteRange", uselist=False)
    endNumber_id = Column(Text(), ForeignKey('Number.id'))
    endNumber = relationship("Number", uselist=False)
    startDefiniteRange_id = Column(Text(), ForeignKey('DefiniteRange.id'))
    startDefiniteRange = relationship("DefiniteRange", uselist=False)
    startIndefiniteRange_id = Column(Text(), ForeignKey('IndefiniteRange.id'))
    startIndefiniteRange = relationship("IndefiniteRange", uselist=False)
    startNumber_id = Column(Text(), ForeignKey('Number.id'))
    startNumber = relationship("Number", uselist=False)
    
    
    def __repr__(self):
        return f"SequenceInterval(id={self.id},endDefiniteRange_id={self.endDefiniteRange_id},endIndefiniteRange_id={self.endIndefiniteRange_id},endNumber_id={self.endNumber_id},startDefiniteRange_id={self.startDefiniteRange_id},startIndefiniteRange_id={self.startIndefiniteRange_id},startNumber_id={self.startNumber_id},)"
        
    
        
    


class SequenceLocation(Base):
    """
    
    """
    __tablename__ = 'SequenceLocation'
    
    id = Column(Text(), primary_key=True)
    sequenceId = Column(Text())
    sequenceInterval_id = Column(Text(), ForeignKey('SequenceInterval.id'))
    sequenceInterval = relationship("SequenceInterval", uselist=False)
    
    
    def __repr__(self):
        return f"SequenceLocation(id={self.id},sequenceId={self.sequenceId},sequenceInterval_id={self.sequenceInterval_id},)"
        
    
        
    


class SequenceState(Base):
    """
    
    """
    __tablename__ = 'SequenceState'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    sequence = Column(Text())
    
    
    def __repr__(self):
        return f"SequenceState(id={self.id},sequence={self.sequence},)"
        
    
        
    


class SimpleInterval(Base):
    """
    
    """
    __tablename__ = 'SimpleInterval'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    end_id = Column(Text(), ForeignKey('Age.id'))
    end = relationship("Age", uselist=False)
    start_id = Column(Text(), ForeignKey('Age.id'))
    start = relationship("Age", uselist=False)
    
    
    def __repr__(self):
        return f"SimpleInterval(id={self.id},end_id={self.end_id},start_id={self.start_id},)"
        
    
        
    


class SystemicVariation(Base):
    """
    
    """
    __tablename__ = 'SystemicVariation'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    copyNumber = Column(Text(), ForeignKey('CopyNumber.id'))
    
    
    def __repr__(self):
        return f"SystemicVariation(id={self.id},copyNumber={self.copyNumber},)"
        
    
        
    


class Text(Base):
    """
    
    """
    __tablename__ = 'Text'
    
    definition = Column(Text())
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"Text(definition={self.definition},id={self.id},)"
        
    
        
    


class UtilityVariation(Base):
    """
    
    """
    __tablename__ = 'UtilityVariation'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    text = Column(Text(), ForeignKey('Text.id'))
    variationSet_id = Column(Text(), ForeignKey('VariationSet.id'))
    variationSet = relationship("VariationSet", uselist=False)
    
    
    def __repr__(self):
        return f"UtilityVariation(id={self.id},text={self.text},variationSet_id={self.variationSet_id},)"
        
    
        
    


class Variation(Base):
    """
    
    """
    __tablename__ = 'Variation'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    allele = Column(Text(), ForeignKey('Allele.id'))
    copyNumber = Column(Text(), ForeignKey('CopyNumber.id'))
    text = Column(Text(), ForeignKey('Text.id'))
    haplotype_id = Column(Text(), ForeignKey('Haplotype.id'))
    haplotype = relationship("Haplotype", uselist=False)
    variationSet_id = Column(Text(), ForeignKey('VariationSet.id'))
    variationSet = relationship("VariationSet", uselist=False)
    
    
    def __repr__(self):
        return f"Variation(id={self.id},allele={self.allele},copyNumber={self.copyNumber},text={self.text},haplotype_id={self.haplotype_id},variationSet_id={self.variationSet_id},)"
        
    
        
    


class VariationSet(Base):
    """
    
    """
    __tablename__ = 'VariationSet'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    
    
    def __repr__(self):
        return f"VariationSet(id={self.id},)"
        
    
        
    


class Any(Base):
    """
    Protocol Buffers - Google's data interchange format Copyright 2008 Google Inc.  All rights reserved. https://developers.google.com/protocol-buffers/  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:  * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. * Neither the name of Google Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. `Any` contains an arbitrary serialized protocol buffer message along with a URL that describes the type of the serialized message.  Protobuf library provides support to pack/unpack Any values in the form of utility functions or additional generated methods of the Any type.  Example 1: Pack and unpack a message in C++.  Foo foo = ...; Any any; any.PackFrom(foo); ... if (any.UnpackTo(&foo)) { ... }  Example 2: Pack and unpack a message in Java.  Foo foo = ...; Any any = Any.pack(foo); ... if (any.is(Foo.class)) { foo = any.unpack(Foo.class); }  Example 3: Pack and unpack a message in Python.  foo = Foo(...) any = Any() any.Pack(foo) ... if any.Is(Foo.DESCRIPTOR): any.Unpack(foo) ...  Example 4: Pack and unpack a message in Go  foo := &pb.Foo{...} any, err := anypb.New(foo) if err != nil { ... } ... foo := &pb.Foo{} if err := any.UnmarshalTo(foo); err != nil { ... }  The pack methods provided by protobuf library will by default use 'type.googleapis.com/full.type.name' as the type URL and the unpack methods only use the fully qualified type name after the last '/' in the type URL, for example "foo.bar.com/x/y.z" will yield type name "y.z".   JSON ==== The JSON representation of an `Any` value uses the regular representation of the deserialized, embedded message, with an additional field `@type` which contains the type URL. Example:  package google.profile; message Person { string first_name = 1; string last_name = 2; }  { "@type": "type.googleapis.com/google.profile.Person", "firstName": <string>, "lastName": <string> }  If the embedded message type is well-known and has a custom JSON representation, that representation will be embedded adding a field `value` which holds the custom JSON in addition to the `@type` field. Example (for message [google.protobuf.Duration][]):  { "@type": "type.googleapis.com/google.protobuf.Duration", "value": "1.212s" } 
    """
    __tablename__ = 'Any'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    typeUrl = Column(Text())
    value_id = Column(Text(), ForeignKey('Value.id'))
    value = relationship("Value", uselist=False)
    
    
    def __repr__(self):
        return f"Any(id={self.id},typeUrl={self.typeUrl},value_id={self.value_id},)"
        
    
        
    


class Disease(Base):
    """
    Message to indicate a disease (diagnosis) and its recorded onset.
    """
    __tablename__ = 'Disease'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    excluded = Column(Boolean())
    laterality = Column(Text(), ForeignKey('OntologyClass.id'))
    primarySite = Column(Text(), ForeignKey('OntologyClass.id'))
    term = Column(Text(), ForeignKey('OntologyClass.id'))
    onset_id = Column(Text(), ForeignKey('TimeElement.id'))
    onset = relationship("TimeElement", uselist=False)
    resolution_id = Column(Text(), ForeignKey('TimeElement.id'))
    resolution = relationship("TimeElement", uselist=False)
    
    
    # ManyToMany
    clinicalTnmFinding = relationship( "OntologyClass", secondary="Disease_clinicalTnmFinding")
    
    
    # ManyToMany
    diseaseStage = relationship( "OntologyClass", secondary="Disease_diseaseStage")
    
    
    def __repr__(self):
        return f"Disease(id={self.id},excluded={self.excluded},laterality={self.laterality},primarySite={self.primarySite},term={self.term},onset_id={self.onset_id},resolution_id={self.resolution_id},)"
        
    
        
    


class Biosample(Base):
    """
    A Biosample refers to a unit of biological material from which the substrate molecules (e.g. genomic DNA, RNA, proteins) for molecular analyses (e.g. sequencing, array hybridisation, mass-spectrometry) are extracted. Examples would be a tissue biopsy, a single cell from a culture for single cell genome sequencing or a protein fraction from a gradient centrifugation. Several instances (e.g. technical replicates) or types of experiments (e.g. genomic array as well as RNA-seq experiments) may refer to the same Biosample. FHIR mapping: Specimen (http://www.hl7.org/fhir/specimen.html).
    """
    __tablename__ = 'Biosample'
    
    derivedFromId = Column(Text())
    description = Column(Text())
    histologicalDiagnosis = Column(Text(), ForeignKey('OntologyClass.id'))
    id = Column(Text(), primary_key=True)
    individualId = Column(Text())
    materialSample = Column(Text(), ForeignKey('OntologyClass.id'))
    pathologicalStage = Column(Text(), ForeignKey('OntologyClass.id'))
    sampleProcessing = Column(Text(), ForeignKey('OntologyClass.id'))
    sampleStorage = Column(Text(), ForeignKey('OntologyClass.id'))
    sampleType = Column(Text(), ForeignKey('OntologyClass.id'))
    sampledTissue = Column(Text(), ForeignKey('OntologyClass.id'))
    taxonomy = Column(Text(), ForeignKey('OntologyClass.id'))
    tumorGrade = Column(Text(), ForeignKey('OntologyClass.id'))
    tumorProgression = Column(Text(), ForeignKey('OntologyClass.id'))
    procedure_id = Column(Text(), ForeignKey('Procedure.id'))
    procedure = relationship("Procedure", uselist=False)
    timeOfCollection_id = Column(Text(), ForeignKey('TimeElement.id'))
    timeOfCollection = relationship("TimeElement", uselist=False)
    
    
    # ManyToMany
    diagnosticMarkers = relationship( "OntologyClass", secondary="Biosample_diagnosticMarkers")
    
    
    # ManyToMany
    files = relationship( "File", secondary="Biosample_files")
    
    
    # ManyToMany
    measurements = relationship( "Measurement", secondary="Biosample_measurements")
    
    
    # ManyToMany
    pathologicalTnmFinding = relationship( "OntologyClass", secondary="Biosample_pathologicalTnmFinding")
    
    
    # ManyToMany
    phenotypicFeatures = relationship( "PhenotypicFeature", secondary="Biosample_phenotypicFeatures")
    
    
    def __repr__(self):
        return f"Biosample(derivedFromId={self.derivedFromId},description={self.description},histologicalDiagnosis={self.histologicalDiagnosis},id={self.id},individualId={self.individualId},materialSample={self.materialSample},pathologicalStage={self.pathologicalStage},sampleProcessing={self.sampleProcessing},sampleStorage={self.sampleStorage},sampleType={self.sampleType},sampledTissue={self.sampledTissue},taxonomy={self.taxonomy},tumorGrade={self.tumorGrade},tumorProgression={self.tumorProgression},procedure_id={self.procedure_id},timeOfCollection_id={self.timeOfCollection_id},)"
        
    
        
    


class CohortFiles(Base):
    """
    
    """
    __tablename__ = 'Cohort_files'
    
    Cohort_id = Column(Text(), ForeignKey('Cohort.id'), primary_key=True)
    files_id = Column(Text(), ForeignKey('File.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Cohort_files(Cohort_id={self.Cohort_id},files_id={self.files_id},)"
        
    
        
    


class CohortMembers(Base):
    """
    
    """
    __tablename__ = 'Cohort_members'
    
    Cohort_id = Column(Text(), ForeignKey('Cohort.id'), primary_key=True)
    members = Column(Text(), ForeignKey('Phenopacket.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Cohort_members(Cohort_id={self.Cohort_id},members={self.members},)"
        
    
        
    


class FamilyFiles(Base):
    """
    
    """
    __tablename__ = 'Family_files'
    
    Family_id = Column(Text(), ForeignKey('Family.id'), primary_key=True)
    files_id = Column(Text(), ForeignKey('File.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Family_files(Family_id={self.Family_id},files_id={self.files_id},)"
        
    
        
    


class FamilyRelatives(Base):
    """
    
    """
    __tablename__ = 'Family_relatives'
    
    Family_id = Column(Text(), ForeignKey('Family.id'), primary_key=True)
    relatives = Column(Text(), ForeignKey('Phenopacket.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Family_relatives(Family_id={self.Family_id},relatives={self.relatives},)"
        
    
        
    


class PhenopacketBiosamples(Base):
    """
    
    """
    __tablename__ = 'Phenopacket_biosamples'
    
    Phenopacket_id = Column(Text(), ForeignKey('Phenopacket.id'), primary_key=True)
    biosamples = Column(Text(), ForeignKey('Biosample.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Phenopacket_biosamples(Phenopacket_id={self.Phenopacket_id},biosamples={self.biosamples},)"
        
    
        
    


class PhenopacketDiseases(Base):
    """
    
    """
    __tablename__ = 'Phenopacket_diseases'
    
    Phenopacket_id = Column(Text(), ForeignKey('Phenopacket.id'), primary_key=True)
    diseases_id = Column(Text(), ForeignKey('Disease.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Phenopacket_diseases(Phenopacket_id={self.Phenopacket_id},diseases_id={self.diseases_id},)"
        
    
        
    


class PhenopacketFiles(Base):
    """
    
    """
    __tablename__ = 'Phenopacket_files'
    
    Phenopacket_id = Column(Text(), ForeignKey('Phenopacket.id'), primary_key=True)
    files_id = Column(Text(), ForeignKey('File.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Phenopacket_files(Phenopacket_id={self.Phenopacket_id},files_id={self.files_id},)"
        
    
        
    


class PhenopacketInterpretations(Base):
    """
    
    """
    __tablename__ = 'Phenopacket_interpretations'
    
    Phenopacket_id = Column(Text(), ForeignKey('Phenopacket.id'), primary_key=True)
    interpretations = Column(Text(), ForeignKey('Interpretation.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Phenopacket_interpretations(Phenopacket_id={self.Phenopacket_id},interpretations={self.interpretations},)"
        
    
        
    


class PhenopacketMeasurements(Base):
    """
    
    """
    __tablename__ = 'Phenopacket_measurements'
    
    Phenopacket_id = Column(Text(), ForeignKey('Phenopacket.id'), primary_key=True)
    measurements_id = Column(Text(), ForeignKey('Measurement.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Phenopacket_measurements(Phenopacket_id={self.Phenopacket_id},measurements_id={self.measurements_id},)"
        
    
        
    


class PhenopacketMedicalActions(Base):
    """
    
    """
    __tablename__ = 'Phenopacket_medicalActions'
    
    Phenopacket_id = Column(Text(), ForeignKey('Phenopacket.id'), primary_key=True)
    medicalActions_id = Column(Text(), ForeignKey('MedicalAction.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Phenopacket_medicalActions(Phenopacket_id={self.Phenopacket_id},medicalActions_id={self.medicalActions_id},)"
        
    
        
    


class PhenopacketPhenotypicFeatures(Base):
    """
    
    """
    __tablename__ = 'Phenopacket_phenotypicFeatures'
    
    Phenopacket_id = Column(Text(), ForeignKey('Phenopacket.id'), primary_key=True)
    phenotypicFeatures_id = Column(Text(), ForeignKey('PhenotypicFeature.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Phenopacket_phenotypicFeatures(Phenopacket_id={self.Phenopacket_id},phenotypicFeatures_id={self.phenotypicFeatures_id},)"
        
    
        
    


class PhenotypicFeatureEvidence(Base):
    """
    
    """
    __tablename__ = 'PhenotypicFeature_evidence'
    
    PhenotypicFeature_id = Column(Text(), ForeignKey('PhenotypicFeature.id'), primary_key=True)
    evidence_id = Column(Text(), ForeignKey('Evidence.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"PhenotypicFeature_evidence(PhenotypicFeature_id={self.PhenotypicFeature_id},evidence_id={self.evidence_id},)"
        
    
        
    


class PhenotypicFeatureModifiers(Base):
    """
    
    """
    __tablename__ = 'PhenotypicFeature_modifiers'
    
    PhenotypicFeature_id = Column(Text(), ForeignKey('PhenotypicFeature.id'), primary_key=True)
    modifiers = Column(Text(), ForeignKey('OntologyClass.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"PhenotypicFeature_modifiers(PhenotypicFeature_id={self.PhenotypicFeature_id},modifiers={self.modifiers},)"
        
    
        
    


class PedigreePersons(Base):
    """
    
    """
    __tablename__ = 'Pedigree_persons'
    
    Pedigree_id = Column(Text(), ForeignKey('Pedigree.id'), primary_key=True)
    persons_id = Column(Text(), ForeignKey('Person.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Pedigree_persons(Pedigree_id={self.Pedigree_id},persons_id={self.persons_id},)"
        
    
        
    


class IndividualAlternateIds(Base):
    """
    
    """
    __tablename__ = 'Individual_alternateIds'
    
    Individual_id = Column(Text(), ForeignKey('Individual.id'), primary_key=True)
    alternateIds = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"Individual_alternateIds(Individual_id={self.Individual_id},alternateIds={self.alternateIds},)"
        
    
        
    


class MetaDataExternalReferences(Base):
    """
    
    """
    __tablename__ = 'MetaData_externalReferences'
    
    MetaData_id = Column(Text(), ForeignKey('MetaData.id'), primary_key=True)
    externalReferences = Column(Text(), ForeignKey('ExternalReference.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"MetaData_externalReferences(MetaData_id={self.MetaData_id},externalReferences={self.externalReferences},)"
        
    
        
    


class MetaDataResources(Base):
    """
    
    """
    __tablename__ = 'MetaData_resources'
    
    MetaData_id = Column(Text(), ForeignKey('MetaData.id'), primary_key=True)
    resources = Column(Text(), ForeignKey('Resource.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"MetaData_resources(MetaData_id={self.MetaData_id},resources={self.resources},)"
        
    
        
    


class MetaDataUpdates(Base):
    """
    
    """
    __tablename__ = 'MetaData_updates'
    
    MetaData_id = Column(Text(), ForeignKey('MetaData.id'), primary_key=True)
    updates_id = Column(Text(), ForeignKey('Update.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"MetaData_updates(MetaData_id={self.MetaData_id},updates_id={self.updates_id},)"
        
    
        
    


class MedicalActionAdverseEvents(Base):
    """
    
    """
    __tablename__ = 'MedicalAction_adverseEvents'
    
    MedicalAction_id = Column(Text(), ForeignKey('MedicalAction.id'), primary_key=True)
    adverseEvents = Column(Text(), ForeignKey('OntologyClass.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"MedicalAction_adverseEvents(MedicalAction_id={self.MedicalAction_id},adverseEvents={self.adverseEvents},)"
        
    
        
    


class TreatmentDoseIntervals(Base):
    """
    
    """
    __tablename__ = 'Treatment_doseIntervals'
    
    Treatment_id = Column(Text(), ForeignKey('Treatment.id'), primary_key=True)
    doseIntervals_id = Column(Text(), ForeignKey('DoseInterval.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Treatment_doseIntervals(Treatment_id={self.Treatment_id},doseIntervals_id={self.doseIntervals_id},)"
        
    
        
    


class ComplexValueTypedQuantities(Base):
    """
    
    """
    __tablename__ = 'ComplexValue_typedQuantities'
    
    ComplexValue_id = Column(Text(), ForeignKey('ComplexValue.id'), primary_key=True)
    typedQuantities_id = Column(Text(), ForeignKey('TypedQuantity.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"ComplexValue_typedQuantities(ComplexValue_id={self.ComplexValue_id},typedQuantities_id={self.typedQuantities_id},)"
        
    
        
    


class DiagnosisGenomicInterpretations(Base):
    """
    
    """
    __tablename__ = 'Diagnosis_genomicInterpretations'
    
    Diagnosis_id = Column(Text(), ForeignKey('Diagnosis.id'), primary_key=True)
    genomicInterpretations_id = Column(Text(), ForeignKey('GenomicInterpretation.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Diagnosis_genomicInterpretations(Diagnosis_id={self.Diagnosis_id},genomicInterpretations_id={self.genomicInterpretations_id},)"
        
    
        
    


class ExtensionValue(Base):
    """
    
    """
    __tablename__ = 'Extension_value'
    
    Extension_id = Column(Text(), ForeignKey('Extension.id'), primary_key=True)
    value_id = Column(Text(), ForeignKey('Value.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Extension_value(Extension_id={self.Extension_id},value_id={self.value_id},)"
        
    
        
    


class GeneDescriptorAlternateIds(Base):
    """
    
    """
    __tablename__ = 'GeneDescriptor_alternateIds'
    
    GeneDescriptor_id = Column(Text(), ForeignKey('GeneDescriptor.id'), primary_key=True)
    alternateIds = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"GeneDescriptor_alternateIds(GeneDescriptor_id={self.GeneDescriptor_id},alternateIds={self.alternateIds},)"
        
    
        
    


class GeneDescriptorAlternateSymbols(Base):
    """
    
    """
    __tablename__ = 'GeneDescriptor_alternateSymbols'
    
    GeneDescriptor_id = Column(Text(), ForeignKey('GeneDescriptor.id'), primary_key=True)
    alternateSymbols = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"GeneDescriptor_alternateSymbols(GeneDescriptor_id={self.GeneDescriptor_id},alternateSymbols={self.alternateSymbols},)"
        
    
        
    


class GeneDescriptorXrefs(Base):
    """
    
    """
    __tablename__ = 'GeneDescriptor_xrefs'
    
    GeneDescriptor_id = Column(Text(), ForeignKey('GeneDescriptor.id'), primary_key=True)
    xrefs = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"GeneDescriptor_xrefs(GeneDescriptor_id={self.GeneDescriptor_id},xrefs={self.xrefs},)"
        
    
        
    


class VariationDescriptorAlternateLabels(Base):
    """
    
    """
    __tablename__ = 'VariationDescriptor_alternateLabels'
    
    VariationDescriptor_id = Column(Text(), ForeignKey('VariationDescriptor.id'), primary_key=True)
    alternateLabels = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"VariationDescriptor_alternateLabels(VariationDescriptor_id={self.VariationDescriptor_id},alternateLabels={self.alternateLabels},)"
        
    
        
    


class VariationDescriptorExpressions(Base):
    """
    
    """
    __tablename__ = 'VariationDescriptor_expressions'
    
    VariationDescriptor_id = Column(Text(), ForeignKey('VariationDescriptor.id'), primary_key=True)
    expressions_id = Column(Text(), ForeignKey('Expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"VariationDescriptor_expressions(VariationDescriptor_id={self.VariationDescriptor_id},expressions_id={self.expressions_id},)"
        
    
        
    


class VariationDescriptorExtensions(Base):
    """
    
    """
    __tablename__ = 'VariationDescriptor_extensions'
    
    VariationDescriptor_id = Column(Text(), ForeignKey('VariationDescriptor.id'), primary_key=True)
    extensions_id = Column(Text(), ForeignKey('Extension.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"VariationDescriptor_extensions(VariationDescriptor_id={self.VariationDescriptor_id},extensions_id={self.extensions_id},)"
        
    
        
    


class VariationDescriptorXrefs(Base):
    """
    
    """
    __tablename__ = 'VariationDescriptor_xrefs'
    
    VariationDescriptor_id = Column(Text(), ForeignKey('VariationDescriptor.id'), primary_key=True)
    xrefs = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"VariationDescriptor_xrefs(VariationDescriptor_id={self.VariationDescriptor_id},xrefs={self.xrefs},)"
        
    
        
    


class MemberMembers(Base):
    """
    
    """
    __tablename__ = 'Member_members'
    
    Member_id = Column(Text(), ForeignKey('Member.id'), primary_key=True)
    members = Column(Text(), ForeignKey('Phenopacket.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Member_members(Member_id={self.Member_id},members={self.members},)"
        
    
        
    


class DiseaseClinicalTnmFinding(Base):
    """
    
    """
    __tablename__ = 'Disease_clinicalTnmFinding'
    
    Disease_id = Column(Text(), ForeignKey('Disease.id'), primary_key=True)
    clinicalTnmFinding = Column(Text(), ForeignKey('OntologyClass.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Disease_clinicalTnmFinding(Disease_id={self.Disease_id},clinicalTnmFinding={self.clinicalTnmFinding},)"
        
    
        
    


class DiseaseDiseaseStage(Base):
    """
    
    """
    __tablename__ = 'Disease_diseaseStage'
    
    Disease_id = Column(Text(), ForeignKey('Disease.id'), primary_key=True)
    diseaseStage = Column(Text(), ForeignKey('OntologyClass.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Disease_diseaseStage(Disease_id={self.Disease_id},diseaseStage={self.diseaseStage},)"
        
    
        
    


class BiosampleDiagnosticMarkers(Base):
    """
    
    """
    __tablename__ = 'Biosample_diagnosticMarkers'
    
    Biosample_id = Column(Text(), ForeignKey('Biosample.id'), primary_key=True)
    diagnosticMarkers = Column(Text(), ForeignKey('OntologyClass.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Biosample_diagnosticMarkers(Biosample_id={self.Biosample_id},diagnosticMarkers={self.diagnosticMarkers},)"
        
    
        
    


class BiosampleFiles(Base):
    """
    
    """
    __tablename__ = 'Biosample_files'
    
    Biosample_id = Column(Text(), ForeignKey('Biosample.id'), primary_key=True)
    files_id = Column(Text(), ForeignKey('File.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Biosample_files(Biosample_id={self.Biosample_id},files_id={self.files_id},)"
        
    
        
    


class BiosampleMeasurements(Base):
    """
    
    """
    __tablename__ = 'Biosample_measurements'
    
    Biosample_id = Column(Text(), ForeignKey('Biosample.id'), primary_key=True)
    measurements_id = Column(Text(), ForeignKey('Measurement.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Biosample_measurements(Biosample_id={self.Biosample_id},measurements_id={self.measurements_id},)"
        
    
        
    


class BiosamplePathologicalTnmFinding(Base):
    """
    
    """
    __tablename__ = 'Biosample_pathologicalTnmFinding'
    
    Biosample_id = Column(Text(), ForeignKey('Biosample.id'), primary_key=True)
    pathologicalTnmFinding = Column(Text(), ForeignKey('OntologyClass.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Biosample_pathologicalTnmFinding(Biosample_id={self.Biosample_id},pathologicalTnmFinding={self.pathologicalTnmFinding},)"
        
    
        
    


class BiosamplePhenotypicFeatures(Base):
    """
    
    """
    __tablename__ = 'Biosample_phenotypicFeatures'
    
    Biosample_id = Column(Text(), ForeignKey('Biosample.id'), primary_key=True)
    phenotypicFeatures_id = Column(Text(), ForeignKey('PhenotypicFeature.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"Biosample_phenotypicFeatures(Biosample_id={self.Biosample_id},phenotypicFeatures_id={self.phenotypicFeatures_id},)"
        
    
        
    


