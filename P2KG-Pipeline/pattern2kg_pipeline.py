import yaml
import pickle2jams as pickle2jams
import jams2rdf as jams2rdf
from kgdata_namedtuple import KG_Data

class JAMSPipeline:
    config = dict2jams_config = jams2rdf_config = []
    directroy = pickle_file_name = ""
    def __init__(self):
        # this line will load the configuration settings from config.yml file
        self.config = yaml.safe_load(open("config/config.yml"))
        self.jams2rdf_config = yaml.safe_load(open("config/jams2rdf_config.yml"))

    # Step1 (Pickle_to_JAMS): This create JAMS files for each tune recording in  JSON file (created in step no.1)
    def pickle_to_JAMS(self) -> None:
        genTunesJAMSFiles = pickle2jams.GenerateTunesJamsFile(self.config)
        genTunesJAMSFiles.createJAMSFiles()

    # Step2 (JAMS_to_RDF): This method calls JAMS2RDF class for generating RDF files for JAMS files (created in step no.1)
    def JAMS_to_RDF(self) -> None:
        jamsrdf = jams2rdf.JAMS2RDF(self.jams2rdf_config, self.config['directories']['JAMS_files_dir'], genTunesJAMSFiles)
        jamsrdf.iterateThroughDirectory()

    def start_pipleline(self):
        # Step1 (dictionary_to_JAMS)
        genTunesJAMSFiles = pickle2jams.GenerateTunesJamsFile(self.config)
        # comment this line to test generation of RDF for few JAMS files
        genTunesJAMSFiles.createJAMSFilesUsingNewPickleFile()
        # Step2 (JAMS_2_RDF)
        jamsrdf = jams2rdf.JAMS2RDF(self.jams2rdf_config, self.config['directories']['JAMS_files_dir'],
                                    genTunesJAMSFiles)
        jamsrdf.iterateThroughDirectory()

if __name__ == "__main__":
    JAMS_pipeline = JAMSPipeline()
    JAMS_pipeline.start_pipleline()
