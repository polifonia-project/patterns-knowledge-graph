# This script downloads a set of pickle files containing pattern information.
# So, this is a preliminary step in the pattern to knowledge graph pipeline.
# The pickle files are firstly created by the FoNN tools
# https://github.com/polifonia-project/folk_ngram_analysis/tree/master/FoNN/mtc_ann_corpus/kg_pipeline_output_data


import os
import requests

# These urls are for the MTC dataset
urls = {
    "mtc_ann/data/4gram_kg_data.pkl": "https://github.com/polifonia-project/folk_ngram_analysis/raw/master/FoNN/mtc_ann_corpus/kg_pipeline_output_data/4gram_kg_data.pkl"
    "mtc_ann/data/5gram_kg_data.pkl": "https://github.com/polifonia-project/folk_ngram_analysis/raw/master/FoNN/mtc_ann_corpus/kg_pipeline_output_data/5gram_kg_data.pkl"
    "mtc_ann/data/6gram_kg_data.pkl": "https://github.com/polifonia-project/folk_ngram_analysis/raw/master/FoNN/mtc_ann_corpus/kg_pipeline_output_data/6gram_kg_data.pkl"
    }

for filename in urls:
    url = urls[filename]
    response = requests.get(url)
    if response.status_code == 200:
        filepath = "inputs/" + filename  # Directory path to save the file
    
        with open(os.path.join(filepath, filename), "wb") as f:
            f.write(response.content)
    else:
        print("File download failed with status code:", response.status_code)
