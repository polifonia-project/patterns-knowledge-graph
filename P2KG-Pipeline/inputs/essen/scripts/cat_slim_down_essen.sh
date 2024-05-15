find . -type f -name "*.ttl" ! -name "*deut*" ! -name "*shanx*" ! -name "*han*" -exec cat {} + | grep -v "@prefix" > combined_output.ttl
cat prefix_head.ttl combined_output.ttl > ../essen_rdf_cat.ttl