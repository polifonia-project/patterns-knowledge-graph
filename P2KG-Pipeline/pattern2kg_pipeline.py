import yaml
import pickle2jams as pickle2jams
import jams2rdf as jams2rdf
from kgdata_namedtuple import KG_Data
import os
import glob

class JAMSPipeline:
    # config = dict2jams_config = jams2rdf_config = []
    # directroy = pickle_file_name = ""
    def __init__(self):
        # this line will load the configuration settings from config.yml file
        self.config = yaml.safe_load(open("config/config.yml"))
        self.jams2rdf_config = yaml.safe_load(open("config/jams2rdf_config.yml"))

    def start_pipleline(self):
        # Step1 (dictionary_to_JAMS)
        genTunesJAMSFiles = pickle2jams.GenerateTunesJamsFile(self.config)
        # comment this line to test generation of RDF for few JAMS files
        genTunesJAMSFiles.createJAMSFilesUsingNewPickleFile()
        # Step2 (JAMS_2_RDF)
        jamsrdf = jams2rdf.JAMS2RDF(self.jams2rdf_config, self.config['directories']['JAMS_files_dir'],
                                    genTunesJAMSFiles)
        jamsrdf.iterateThroughDirectory()

def cat(rdf_dir, corpus_name):
    d = rdf_dir
    d = d.split("/") # not using os.sep, because our config uses /
    indir = os.sep.join(d[:-2])
    outfile = os.path.join(os.sep.join(d[:-3]), f"{corpus_name}_rdf_cat.ttl")
    concatenate_files(indir, ".ttl", outfile)
    print("")


# from ChatGPT
def concatenate_files(root_dir, suffix, output_file_path):
    print(f"concatenating files! {root_dir}")
    with open(output_file_path, 'w') as output_file:
        for dirpath, _, _ in os.walk(root_dir):
            print(f"processing directory {dirpath}")
            for filename in glob.glob(os.path.join(dirpath, f"*{suffix}")):
                with open(filename, 'r') as input_file:
                    output_file.write(input_file.read())
                    output_file.write("\n")

# from ChatGPT
def trim_path_components(path):
    components = path.split(os.sep)
    if len(components) < 3:
        raise ValueError("Path should have at least three components to remove.")
    return os.sep.join(components[1:-2])

def copy_configs(corpus, n):
    d = "config"
    src = os.path.join(d, f"config_{corpus}_{n}gram.yml")
    dest = os.path.join(d, "config.yml")
    print(f"copying config: {src} to {dest}")
    os.system(f"cp {src} {dest}")
    src = os.path.join(d, f"jams2rdf_config_{corpus}_{n}gram.yml")
    dest = os.path.join(d, "jams2rdf_config.yml")
    os.system(f"cp {src} {dest}")
    print(f"copying jams2rdf_config: {src} to {dest}")
    
if __name__ == "__main__":
    rdf_dir = ""
    for corpus in "mtc_ann", "thesession_annotated_subset":
        for n in (4, 5, 6):
            # if corpus != "thesession_annotated_subset": continue
            # if n == 4: continue
            copy_configs(corpus, n)
            JAMS_pipeline = JAMSPipeline()
            JAMS_pipeline.start_pipleline()
            rdf_dir = JAMS_pipeline.jams2rdf_config['directories']['rdf_directory']
        cat(rdf_dir, corpus)
