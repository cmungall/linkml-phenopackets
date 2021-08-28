# Introduction

This is a draft schema for GO-CAMs for demo purposes

## Links

![img](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7012280/bin/nihms-1067180-f0002.jpg)

 * https://cmungall.github.io/linkml-gocam/
 * https://github.com/cmungall/linkml-gocam

See in particular the tests folder

## About

This is a draft for demo purposes.

It is a LinkML rendering of the GO-CAM schema. The only thing that is edited is the gocam.yaml file in the src/schema folder.

Various artefacts are generated:

 * Python dataclasses
 * JSON-Schema
 * GraphQL
 * ShEx (but see notes below)
 * JSON-LD context

More will be generated in future, e.g. SQL DDL, APIs, grcl queries

## Python Datamodel

Here we show an example of using the Python object model to create a portion of [Figure3](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7012280/figure/F3/), specifically this fragment:

![image](https://user-images.githubusercontent.com/50745/113606303-aeb00300-95fc-11eb-8f9f-95c13609a032.png)


```python
WNT_SIGNALING = 'GO:0060070' ## canonical Wnt signaling pathway
RECEPTOR_LIGAND = 'GO:0048018' ## receptor ligand activity
RECEPTOR_ACTIVITY = 'GO:0042813' ## Wnt-activated receptor activity
EXTRACELLULAR = 'GO:0005615' ## extracellular space
PM = 'GO:0005886' ## plasma membrane
WNT3 = 'UniprotKB:P56703'
FZD1 = 'UniprotKB:Q9UP38'

m = Model(id=id('m1'),
                  title='test title',
                  contributor=['orcid:123', 'orcid:234'],
                  state=ModelStateEnum.production)
        print(f'Model = {m.id}')
        p1 = BiologicalProcess(id=id('p1'), type=WNT_SIGNALING)
        c1 = AnatomicalEntity(id=id('c1'), type=EXTRACELLULAR,
                              category=AnatomicalEntityCategory.CellularAnatomicalEntity)
        c2 = AnatomicalEntity(id=id('c2'), type=PM,
                              category=AnatomicalEntityCategory.CellularAnatomicalEntity)
        g1 = InformationBiomacromolecule(id=id('g1'), type=WNT3,
                                         category=InformationBiomacromoleculeCategory.GeneOrReferenceProtein)
        g2 = InformationBiomacromolecule(id=id('g2'), type=FZD1,
                                         category=InformationBiomacromoleculeCategory.GeneOrReferenceProtein)
        a2 = MolecularActivity(id=id('a2'), type=RECEPTOR_ACTIVITY,
                               enabled_by=EnabledByAssociation(object=g2.id),
                               occurs_in=OccursInAssociation(object=c2.id),
                               part_of=ProcessPartOfAssociation(object=p1.id))
        a1 = MolecularActivity(id=id('a1'), type=RECEPTOR_LIGAND,
                               enabled_by=EnabledByAssociation(object=g1.id),
                               occurs_in=OccursInAssociation(object=c1.id),
                               causes=CausesAssociation(predicate='regulates',
                                                        object=id('a2')))

        m.molecular_activity_set = [a1, a2]
        m.information_biomacromolecule_set = [g1, g2]
        jsonld = dumps(m, cntxt)
        print(jsonld)
```

Of course, one would generally not write code like this - to obtain
python objects we would use an adapter to get from files/database, or
it would sit at the end of a CRUD API. The code above is just for
illustration purposes.

## JSON Serialization

See the jsonschema folder in GitHub, but note that the JSON-Schema is generated from the LinkML

Additionally, conversion from Pythjon objects to JSON-Schema with appropriate inlining is handled automatically

### Models

The model contains basic metadata, it also is a holder for various *sets* of GO-CAM entities:


```json
{
  "id": "model:m1",
  "title": "test title",
  "contributor": [
    "orcid:123",
    "orcid:234"
  ],
  "state": {
    "text": "production"
  },
  "molecular_activity_set": [ ...],
  "biological_process_set": [ ...],
  "information_biomacromolecule_set": [ ...],
  ...
}
```

See the Model class in the schema docs

### Basic "Annoton"

A molecular activity corresponds identically to the model in the paper. In the JSON serialization we inline each relationship for convenience:

```
 "molecular_activity_set": [
    {
      "id": "model:a1",
      "type": "GO:0048018",
      "causes": {
        "object": "model:a2",
        "has_evidence": {
          "id": "model:e6",
          "evidence_type": "ECO:nnn",
          "reference": [
            "PMID:1234"
          ]
        },
        "predicate": "regulates"
      },
      "enabled_by": {
        "object": "model:g1",
        "has_evidence": {
          "id": "model:e4",
          "evidence_type": "ECO:nnn",
          "reference": [
            "PMID:1234"
          ]
        }
      },
      "occurs_in": {
        "object": "model:c1",
        "has_evidence": {
          "id": "model:e5",
          "evidence_type": "ECO:nnn",
          "reference": [
            "PMID:1234"
          ]
        }
      }
    },
```


## Differences from current RDF/OWL and go-cam-shapes.shex

Although this model has a direct JSON-LD/RDF serialization via LinkML there are some differences

(note also that this repo contains auto-generated ShEx from this model which will naturally differ)

### Adherence to original specification

This model aims to be simple and to serve as a substrate for programmatic exchange, APIs, serialization.

The ShEx contains many additional classes that are useful for
validation according to specific GO BPs and MFs, but we leave these
out of this model.


### GO-CAM entities are explicitly part of a model

The top level object is a Model, which in addition to holding metadata (title etc), is a holder for all of the different GO-CAM elements:

```json
{
  "id": "model:m1",
  "title": "test title",
  "contributor": [
    "orcid:123",
    "orcid:234"
  ],
  "state": {
    "text": "production"
  },
  "molecular_activity_set": [
    {
      "id": "model:a1",
      "type": "GO:0048018",
      "causes": {
        "object": "model:a2",
        "predicate": "regulates"
      },
      "enabled_by": {
        "object": "model:g1"
      },
      "occurs_in": {
        "object": "model:c1"
      }
    },
    {
      "id": "model:a2",
      "type": "GO:0042813",
      "part_of": {
        "object": "model:p1"
      },
      "enabled_by": {
        "object": "model:g2"
      },
      "occurs_in": {
        "object": "model:c2"
      }
    }
  ],
  "information_biomacromolecule_set": [
    {
      "id": "model:g1",
      "type": "UniprotKB:P56703",
      "category": "GeneOrReferenceProtein"
    },
```

### Reification

This model uses RDF reification for simplicity for now, not OWL annotation
