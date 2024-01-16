
param(
    [String]$FilePath
)

curl.exe -X POST -H "Content-Type:application/sparql-query" -H "Accept:text/tab-separated-values" --data-binary "@$FilePath" http://localhost:9999/blazegraph/namespace/kb/sparql



