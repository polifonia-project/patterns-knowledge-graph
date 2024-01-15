
# Command line for testing. Remove all the ttl and regenerate.

rm JAMS\*\*\*.jams; rm ..\patterns-knowledge-graph-datasets\RDF\*\*\*.ttl; python .\pattern2kg_pipeline.py


# drop db.

# Note current namespace: kb


curl.exe -X POST http://localhost:9999/blazegraph/namespace/kb/sparql --data-urlencode 'update=DROP ALL'

# (curl.exe if on windows, no need for .exe on a normal system)

# update with ttl files from Patterns and TUNES KGs:

curl.exe -X POST -H 'Content-Type:text/turtle' --data '@D:\vc\patterns-knowledge-graph\patterns-knowledge-graph-datasets\RDF\mtc_ann_rdf_cat.ttl' http://localhost:9999/blazegraph/namespace/kb/sparql
curl.exe -X POST -H 'Content-Type:text/turtle' --data '@D:\vc\patterns-knowledge-graph\patterns-knowledge-graph-datasets\RDF\thesession_annotated_subset_rdf_cat.ttl' http://localhost:9999/blazegraph/namespace/kb/sparql

curl.exe -X POST -H 'Content-Type:text/turtle' --data '@D:\vc\tunes-knowledge-graph\kg\tunes-collectionconcepts.ttl' http://localhost:9999/blazegraph/namespace/kb/sparql
curl.exe -X POST -H 'Content-Type:text/turtle' --data '@D:\vc\tunes-knowledge-graph\kg\tunes-thesession-collectionconcepts.ttl' http://localhost:9999/blazegraph/namespace/kb/sparql
curl.exe -X POST -H 'Content-Type:text/turtle' --data '@D:\vc\tunes-knowledge-graph\kg\tunes-thesession-entities.ttl' http://localhost:9999/blazegraph/namespace/kb/sparql
curl.exe -X POST -H 'Content-Type:text/turtle' --data '@D:\vc\tunes-knowledge-graph\kg\tunes-thesession-formtypes.ttl' http://localhost:9999/blazegraph/namespace/kb/sparql
curl.exe -X POST -H 'Content-Type:text/turtle' --data '@D:\vc\tunes-knowledge-graph\kg\tunes-thesession-tunes.ttl' http://localhost:9999/blazegraph/namespace/kb/sparql

# Run a query from command line:
# curl.exe -X POST -H "Content-Type:application/sparql-query" --data-binary "@../queries/count_patterns.sparql" http://localhost:9999/blazegraph/namespace/kb/sparql

# or for tsv output:

curl.exe -X POST -H "Content-Type:application/sparql-query" -H "Accept:text/tab-separated-values" --data-binary "@../queries/count_patterns.sparql" http://localhost:9999/blazegraph/namespace/kb/sparql

