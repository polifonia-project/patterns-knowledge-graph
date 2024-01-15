---
container-id: patterns-knowledge-graph
name: Patterns Knowledge Graph
description: Knowledge graph containing data about patterns extracted using the [FONN tools](https://github.com/polifonia-project/folk_ngram_analysis), and software for creating that knowledge graph
type: Project
release-date: 07/06/2023
release-number: v0.1.0
work-package:
- WP3
project: polifonia-project
bibliography:
bibliography:
- main-publication: "Forthcoming paper in SWODCH 2023"
- publication: 
  - "Polifonia Deliverable 3.4"
related-components:
  - folk_ngram_analysis
links:
- https://github.com/polifonia-project/patterns-knowledge-graph
- https://zenodo.org/record/ (TODO)
credits:
- https://github.com/ashahidkhattak
- https://github.com/jmmcd
- https://github.com/danDiamo
funder:
  - name: Horizon 2020 Framework Programme
    url: https://cordis.europa.eu/programme/id/H2020-EC
    grant-agreement: "https://cordis.europa.eu/project/id/101004746"
credits: "This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement N. 101004746."
has-part:
  - P2KG-Pipeline
  - patterns-knowledge-graph-datasets
---

# Abstract and highlights
The Patterns Knowledge Graph contains data about patterns in folk / traditional music. The patterns are those extracted using the [FONN tools](https://github.com/polifonia-project/folk_ngram_analysis).

* Allows exploration of patterns as linked open data
* Multiple corpora, multiple definitions of patterns (e.g. $n$=(4, 5, 6), accent-level versus note-level)
* Running public SPARQL endpoint and MELODY data stories as demonstrations.

## Data Sources
The PatternKG currently contains pattern data extracted from two important repositories:

* MTC-ANN, Meertens Tune Collections - Annotated. This set of 360 tunes from the Dutch folk tradition contains tune family annotations. See https://www.liederenbank.nl/mtc/
* The Session (annotated subset). This set of 315 tunes in 10 tune families is from the Irish folk tradition. The Session itself is 40k tunes, crowd-sourced. This subset has been chosen and annotated with tune family information based on the musicological literature. See https://thesession.org/ for the original (large) collection. 
 
The tune family annotation of *The Session* (315 tunes) is published here for the first time. It was carried out by Danny Diamond based on the musicological literature with extensive manual checking.


## Requirements and installation

1. Use `pip install -r requirements.txt` to install the necessary libraries. They are:

```
PyYAML
rdflib
jams
```

2. You will also need to install SPARQL-Anything. We are currently using version 0.6.0 (see https://github.com/polifonia-project/patterns-knowledge-graph/issues/1). Download the 0.6.0 jar file from: https://github.com/SPARQL-Anything/sparql.anything/releases, and copy it to the `sparql-anything` directory here in the `patterns-knowledge-graph` repo.

## Running the software

Then, you can run the software by running:

```
cd P2KG-Pipeline
python pattern2kg_pipeline.py
```

It will read the data (metadata in csv format, and pattern occurrences in pickle format) from `inputs/`. It will write out the knowledge graph to the `RDF` directory in `.ttl` files.

## Testing locally

You can run Blazegraph locally to test your Knowledge Graph. Download it from: `https://blazegraph.com/` and put it (e.g.) into a `/test` directory. From there run, e.g.:

`shell
$ java -server -Xmx4g -jar blazegraph.jar
`

And it will start a UI in the browser. From there you can upload the `.ttl` files and issue test queries.

# Deployment 

To instead deploy, we copy our `.ttl` to the Polifonia server https://polifonia.disi.unibo.it/fonn/sparql, which provides the data via a public SPARQL endpoint. 

## We also provide some data stories via MELODY:

* https://projects.dharc.unibo.it/melody/fonn/statistics_on_the_session_annotated_subset_and_meertens_tune_collections_mtcann_pattern_kg
* https://projects.dharc.unibo.it/melody/fonn/tune_families_in_the_session_and_mtcann

Anyone can create new MELODY data stories, using the same SPARQL endpoint. See https://projects.dharc.unibo.it/melody/ for more information.

## Bringing your own data

If you have pattern information and metadata representing some new corpus, you can copy it to a subdirectory in `inputs/` before starting, and it will be processed. The metadata should be in csv format, with at least an `identifiers` field (string), a `title` field (string; can be empty), and a `tune family` field (string). 


## Citing this repository

If you would like to use this software and knowledge graph, please cite this repository as follows:

```
@software{shahid_patternkg_2023,
	address = {Galway, Ireland},
	title = {Pattern Knowledge Graph},
	shorttitle = {{PatternKG}},
	url = {https://github.com/polifonia-project/patterns-knowledge-graph},
	publisher = {University of Galway},
	author = {Shahid, Abdul and Diamond, Danny and McDermott, James},
	year = {2023},
}
```



[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8034504.svg)](https://doi.org/10.5281/zenodo.8034504)

This Pattern KG and associated software in this repository form part of Polifonia Deliverable D3.5, part of WP3.
