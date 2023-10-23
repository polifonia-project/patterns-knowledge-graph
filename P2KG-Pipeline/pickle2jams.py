import json
import pickle
import pandas as pd
import time
import jams
import re
import yaml
import os
import logging
import glob
import sys

from kgdata_namedtuple import KG_Data


# Generating JAMS files the given pickle file.
class GenerateTunesJamsFile:
    config = tunes_metadata = []
    pickle_pattern_information = ()
    KG_Data = None
    def __init__(self,  config):
        print("The first step of JAMS Pipeline stated: pickle to JAMS creation")
        self.listOfTunes = []
        self.path = ""
        self.config = config
        if not os.path.isdir(self.config['directories']['JAMS_files_dir']):
            os.makedirs(self.config['directories']['JAMS_files_dir'])

        self.__read_relevant_files()

    def __read_relevant_files(self):

        # read one or more pickle files. each pickle is a list of KG_Data. We extend.
        pkl_filename = self.config['directories']['pickle_pattern_information']
        print("pkl_filename", pkl_filename)
        pkl_filenames = glob.glob(pkl_filename)
        print("pkl_filenames", pkl_filenames)
        pattern_info_kg_data = []
        for pkl_filename in pkl_filenames:
            pattern_info_kg_data.extend(self.__read_file(pkl_filename))

        # create a DataFrame
        self.pickle_pattern_information = pd.DataFrame.from_records(
            [x for x in pattern_info_kg_data],
            columns=KG_Data._fields
        )
        # print(self.pickle_pattern_information.head())

        # read the metadata csv
        self.tunes_metadata = self.__read_file(self.config["directories"]["metadata_csv_file"], "csv")

    # getter method
    def get_jams_files_completions_status(self):
        return self.jams_files_completions_status

    def __read_file(self, fileName, type='pickle'):
        try:
            if type == 'pickle':
                with open(fileName, 'rb') as f:
                    data = pickle.load(f)
            else:
                data = pd.read_csv(fileName, encoding='utf-8', dtype={"identifiers": "string", "title": "string", "transcriber": "string", "publication_date": "string"})
                data = data.fillna('') # no NaNs please
            return data
        except KeyError: # TODO if a key is missing in the pickle, we'll get a partial pickle... this should not pass silently.
            # Key is not present
            pass



    def __open_pattern_freq_df_file(self, filePath):
        data = self.__read_file(filePath)
        data = data.reset_index(level=0)
        columns = data.columns
        self.listOfTunes = columns[1:-1]
        print("Total JAMS files to be created from the pickle file: ", len(self.listOfTunes))
        self.filtered_df = data #[data["freq"] >= 2]

    def __setCurrentTuneJamsMetadata(self, tuneRow):
        dir = self.config['directories']['schemas_directory']
        schema = self.config['directories']['schema_file']
        corpus = self.config['jams_annotations']['corpus_name']
        schema_file_name = dir+'/'+schema
        jams.schema.add_namespace(schema_file_name)
        tuneJAMSFile = jams.JAMS()
        feature_sequence_data = str(tuneRow['data'])

        tuneJAMSFile.file_metadata.identifiers = {
            "tune-corpus": corpus,
            "url": self.config['jams_annotations']['tune_base_url']+tuneRow["identifiers"]
        }

        # print(self.tunes_metadata)

        if (len(self.tunes_metadata) > 1):

            # changed from using int(identifiers) to using just title, for MTC, for now
            metadata_row = self.tunes_metadata.loc[self.tunes_metadata['identifiers'] == tuneRow["identifiers"]]
            if len(metadata_row) == 0:
                logging.warning(f'No match: no matching row') # TODO improve error / warning messages
                print(self.tunes_metadata['identifiers'])
                print(tuneRow["identifiers"])
                sys.exit()

            elif len(metadata_row) > 1:
                logging.warning(f'Overmatch: more than one matching row')
                print(tuneRow["identifiers"])
                sys.exit()
                
            else:

                metadata_row = metadata_row.iloc[0] 
                tuneJAMSFile.sandbox.content = metadata_row["score"] if "score" in metadata_row else "" # raw abc score
                tuneJAMSFile.sandbox.feature_data = feature_sequence_data
                # tuneJAMSFile.sandbox.transcriber = metadata_row["transcriber"] if "transcriber" in metadata_row else "" # abc Z "transcription"
                tuneJAMSFile.sandbox.tunetype = metadata_row["R"] if "R" in metadata_row else "" # abc R "rhythm" eg jig, reel 
                tuneJAMSFile.sandbox.tunefamily = metadata_row["tune_family"] if "tune_family" in metadata_row else "" # 
                tuneJAMSFile.sandbox.key = metadata_row["K"] if "K" in metadata_row else "" # abc K, ie key
                tuneJAMSFile.sandbox.timesig = metadata_row["M"] if "M" in metadata_row else "" # abc M, ie meter
                tuneJAMSFile.sandbox.year = metadata_row["date"] if "date" in metadata_row else "" # date -> year in MTC
                tuneJAMSFile.sandbox.tuneid = str(tuneRow["identifiers"])
                #title = re.sub(r'\d+', '', metadata_row["title"]).strip() # TODO fix this hard-coded digit removal
                title = metadata_row["title"]
                tuneJAMSFile.sandbox.formatted_title = title
                tuneJAMSFile.file_metadata.title = title

        tuneJAMSFile.file_metadata.title = metadata_row["title"]
        tuneJAMSFile.file_metadata.release = "n-grams patterns-kg 1.0"
        tuneJAMSFile.file_metadata.duration = float(tuneRow['duration'])
        tuneJAMSFile.sandbox.type = "score"
        tuneJAMSFile.sandbox.expanded = "true"
        tuneJAMSFile.sandbox.composers = []
        return tuneJAMSFile

    def __createJAMSAnnotation(self, name_space):
        pattern_annotation = jams.Annotation(namespace=name_space)
        pattern_annotation.annotation_metadata.annotator.name = self.config['jams_annotations']['annotator_name']
        pattern_annotation.annotation_metadata.data_source = self.config['jams_annotations']['data_source']
        pattern_annotation.annotation_metadata.corpus = self.config['jams_annotations']['tune_base_url']
        pattern_annotation.annotation_metadata.version = self.config['jams_annotations']['version']
        pattern_annotation.annotation_metadata.curator.name = self.config['jams_annotations']['annotator_name']
        pattern_annotation.annotation_metadata.curator.email = self.config['jams_annotations']['email']
        pattern_annotation.annotation_metadata.annotation_tools = self.config['jams_annotations']['annotation_tools']
        pattern_annotation.annotation_metadata.annotation_rules = None
        pattern_annotation.annotation_metadata.validation = None
        return pattern_annotation

    # Deprecated function
    def getTuneId(self, tuneName):
        re.findall(r'\d+$', tuneName)
        tuneNumber = re.findall(r'\d+$', tuneName)
        return str(tuneNumber[0])

    # Deprecated function
    def getMorphedTuneId(self, tuneName):
        re.findall(r'\d+', tuneName)
        tuneNumber = re.findall(r'\d+', tuneName)
        return str("".join(tuneNumber))

    def createJAMSFilesUsingNewPickleFile(self):
        counter = 1
        blank_count = 0
        for index, tuneRow in self.pickle_pattern_information.iterrows():
            print(counter, tuneRow['identifiers'])
            tuneJAMSFile = self.__setCurrentTuneJamsMetadata(tuneRow)
            pattern_annotation = self.__createJAMSAnnotation(self.config['jams_annotations']['schema_name'])
            pattern_details =  tuneRow['pattern_locations']

            for pattern, pattern_locations in pattern_details.items():
                for location in pattern_locations:
                    pattern_dict = {
                        "pattern_id": str(tuneRow['identifiers']), # is this the tune id or pattern id?
                        "pattern_content": str(pattern).strip("()"),
                        "pattern_type": self.config['jams_annotations']['pattern_type'], # should be constructed on the fly, but for now its coded in the config
                        "pattern_frequency": len(pattern_locations),
                        "pattern_complexity": round(len(set(pattern)) / len(pattern), 2),
                        "pattern_length": len(pattern),
                    }
                    pattern_annotation.append(time=location, duration=0.0, value=pattern_dict, confidence=1)

            counter = counter + 1
            tuneJAMSFile.annotations.append(pattern_annotation)
            outfilename = self.config['directories']['JAMS_files_dir'] + tuneRow['identifiers'] + ".jams"
            print("Saving to " + outfilename)
            tuneJAMSFile.save(outfilename, strict=False)

            if counter > 2: # just for testing
                break


if __name__ == "__main__":
    config = yaml.safe_load(open("config/config.yml"))
    genJAMSFiles = GenerateTunesJamsFile(config)
    genJAMSFiles.createJAMSFilesUsingNewPickleFile()
