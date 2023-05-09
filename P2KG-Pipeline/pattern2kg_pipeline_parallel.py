import yaml
import pickle2dict as ptrn2dict
import pickle2jams as pickle2jams
import jams2rdf as jams2rdf
from multiprocessing import Process
import logging
from typing import NamedTuple

KG_Data = NamedTuple('KG_Data', [
    ('id_number', str),
    ('tune_title', str),
    ('tune_family', str),
    ('feature', str),
    ('level', str),
    ('n_vals', tuple),
    ('duration_beats', int),
    ('locations', dict),
    ('feature_sequence_data', list)
])

class JAMSPipeline:
    config = dict2jams_config = jams2rdf_config = []
    directroy = pickle_file_name = ""
    def __init__(self):
        # this line will load the configuration settings from config.yml file
        self.config = yaml.safe_load(open("config/config.yml"))
        self.jams2rdf_config = yaml.safe_load(open("config/jams2rdf_config.yml"))

        self.direcoty = self.config['directories']['music_pattern_directory']

    # Step1 (Pickle_to_JAMS): This create JAMS files for each tune recording in  JSON file (created in step no.1)
    def pickle_to_JAMS(self) -> None:
        genTunesJAMSFiles = pickle2jams.GenerateTunesJamsFile(self.config)
        genTunesJAMSFiles.createJAMSFiles()

    # Step2 (JAMS_to_RDF): This method calls JAMS2RDF class for generating RDF files for JAMS files (created in step no.1)
    def JAMS_to_RDF(self) -> None:
        jamsrdf = jams2rdf.JAMS2RDF(self.jams2rdf_config, self.config['directories']['JAMS_files_dir'])
        jamsrdf.iterateThroughDirectory()

    def start_pipleline(self):
        genTunesJAMSFiles = pickle2jams.GenerateTunesJamsFile(self.config)
        p1 = Process(genTunesJAMSFiles.createJAMSFilesUsingNewPickleFile())
        p1.start()
        jamsrdf = jams2rdf.JAMS2RDF(self.jams2rdf_config, self.config['directories']['JAMS_files_dir'], genTunesJAMSFiles)
        p2 = Process(target=jamsrdf.iterateThroughDirectory)
        p2.start()

if __name__ == "__main__":
    JAMS_pipeline = JAMSPipeline()
    JAMS_pipeline.start_pipleline()