---
component-id: P2KG Pipeline
name: P2KG - Pattern to Knowledge graph JAMS Pipline
description: This code takes the patterns generate by the FoNN tool in the form of pickle file and then creates knowledge graph of the all the patterns found in different tunes.
type: Repository
release-date: 01/12/2022
release-number: v0.1.0.1-dev
work-package: 
- WP3
licence:  CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
links:
- https://github.com/polifonia-project/P2KG-JAMS Pipeline
- https://zenodo.org/record/
credits:
- https://github.com/danDiamo
- https://github.com/ashahidkhattak
- https://github.com/jmmcd
---

# P2KG - Patterns to Knowledge Graph JAMS Pipeline
- Targeting the goals of Polifonia WP3 package, P2KG JAMS Pipeline creates the knowledge graph of the patterns generate by [FoNN](https://github.com/polifonia-project/folk_ngram_analysis). The details of directory and files are given below:
- **Directories**
  - ``config`` 
    - ``config.yml`` => this file contains configurations related to pickle file location and JAMS annotations such as ``music_pattern_directory`` and ``corpus_name`` etc. You need to update these settings before executing the pipeline 
    - ``jams2rdf_config.yml`` => this file contains JAMS to RDF process settings, for example, ``rdf_directory`` instruct code where to create the rdf files.
  - ``music_patterns_pickle``
    - ``thesession_27_04_23_kg_data.pkl`` => this file contains pattern information in each tune. This file must follow the following structure
      - ``id_number`` => contains the tune id
      - ``tune_title`` => contains the tune title information
      - ``tune_family`` => tune family information
      - ``feature`` => such as "diatonic pitch class"
      - ``level`` => information such as "accent" or "note" level
      - ``n_vals`` => n-gram information such as "(4, 5, 6)"
      - ``duration_beats`` => the tune duration length, e.g. 34
      - ``locations`` => pattern information should follow this structure, Dictionay of patterns in tuple and then its locations in a the list, e.g., "{(3, 4, 3, 2): [0, 8], (4, 3, 2, 3): [1, 9]}" 
      - ``feature_sequence_data``=> feature sequent data, list of pitch class values, [3, 4, 3, .... ] 
    - ``thesession_metadata.csv`` => This file contains metadata of each tune, it should follow the following structure
      - ``X`` => contains the tune id
      - ``title``=> contains the tune title information
      - ``Z`` => transcriber of the tune
      - ``R`` => tunetype information
      - ``M`` => timesignature information
      - ``K`` => key of the tune
      - ``score`` => content of the tune in the form of ABC notation 
      - ``Formatted_title`` => clean tune title's information
  - ``schemas``
    - ``pattern_fonn.json`` => this is a JAMS schema file, it is required for creating proper JAMS file. For each tune (in the pickle file) a corresponding JAMS file will be generated.
  - ``sparql_anything``
    - ``jams_ontology_pattern.sparql`` => this is the query the SPARQL Anything Engine require to create an RDF file for a given JAMS file. 
    - ``sa.jar`` => this is SPARQL Anything engine, you can download the latest release from [SPARQL-Anything GitHub link](https://github.com/SPARQL-Anything/sparql.anything/releases/tag/v0.8.0).  
  - ``tests`` => this folder contain test cases (TODO- to be developed) 
  - ``JAMS``=> .jams file will be created in this folder for a corpus, for example, all The Session corpus files will go inside "thesession" folder
  - ``RDF`` => All RDF files, .ttl files will be created inside this folder. for example, all The Session corpus files will go inside "thesession" folder
  
NOTE: Apart from these folders, you will find the following important .py files 

  ``pattern2kg_pipeline.py`` => this is the starting file, you can start process by executing this file. It will first create all the jams files and then it will create rdf files
  
  ``pattern2kg_pipeline_parallel.py`` => this file can be used if you want to execute the whole process in parallel (parallelized version of the above file). However, most of the time you will not need to run this file.
  
  ``pickle2jams.py``=> this file is responsible for creating .jams files in the JAMS folder
  
  ``jams2rdf.py`` => this file is responsible for creating .ttl files in the RDF folder 
    
## P2KG JAMS Pipeline:
1. **P2KG - General Steps**
   * 1.1. Input: Patterns generated using FoNN in the form of pickle file.
   * 1.2. Process: [JAMS Annotation] (https://jams.readthedocs.io/en/stable/) - JAMS files are created using custom pattern schema, you can find in the ``schema`` folder. 
   * 1.3. Process: [SPARQL Anything Engine] (https://sparql-anything.cc/) - It takes JAMS file and create KG. 
   * 1.4. Output: Knowledge Graph of pattern is created, a demo of created KG can be accessed on [polifonia server] (https://polifonia.disi.unibo.it/fonn/sparql). 
   
## P2KG - Requirements

To ensure P2KG runs correctly, please install the following libraries:

``` pip install -r requirements.txt ```

##  Attribution

If you use the code in this repository, please cite this software as follow: 
```
@software{patterns2Kg_jams_pipeline_2022,
	address = {Galway, Ireland},
	title = {{P2KG} - {P}attern-2-{KG} {Knowledge Graph}},
	shorttitle = {{P2KG}},
	url = {https://github.com/polifonia-project/P2KG},
	publisher = {National University of Ireland, Galway},
	author = {Shahid Abdul, Diamond Danny, McDermott, James and Pushkar Jajoria},
	year = {2022},
}
```

## License
This work is licensed under CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
