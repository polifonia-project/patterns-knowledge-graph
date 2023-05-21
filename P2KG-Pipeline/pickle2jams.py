import json
import pickle
import pandas as pd
import time
import jams
import re
import yaml
import os
import logging
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
        pattern_info_kg_data = self.__read_file(
           self.config['directories']['pickle_pattern_information'])

        self.pickle_pattern_information = pd.DataFrame.from_records(
            [x for x in pattern_info_kg_data],
            columns=KG_Data._fields
        )

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
                data = pd.read_csv(fileName, encoding='utf-8')
            return data
        except KeyError:
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
        feature_sequence_data = str(tuneRow['feature_sequence_data'])

        tuneJAMSFile.file_metadata.identifiers = {
            "tune-corpus": corpus,
            "url": self.config['jams_annotations']['tune_base_url']+tuneRow["id_number"]
        }
        tuneJAMSFile.file_metadata.title = tuneRow['tune_title']
        tuneJAMSFile.file_metadata.release = "n-grams patterns-kg 1.0"
        tuneJAMSFile.file_metadata.duration = float(tuneRow['duration_beats'])

        if (len(self.tunes_metadata) > 1):
            metadata_row = self.tunes_metadata.loc[self.tunes_metadata['X'] == int(tuneRow["id_number"])]
            if len(metadata_row) >= 1:
                tuneJAMSFile.sandbox.content = metadata_row.iloc[0]["score"]
                tuneJAMSFile.sandbox.feature_data = feature_sequence_data
                tuneJAMSFile.sandbox.transcriber = metadata_row.iloc[0]["Z"]
                tuneJAMSFile.sandbox.tunetype = metadata_row.iloc[0]["R"]
                tuneJAMSFile.sandbox.tunefamily = str(tuneRow['tune_family'])
                tuneJAMSFile.sandbox.key = metadata_row.iloc[0]["K"]
                tuneJAMSFile.sandbox.timesig = metadata_row.iloc[0]["M"]
                tuneJAMSFile.sandbox.tuneid = str(tuneRow["id_number"])
                title = re.sub(r'\d+', '', metadata_row.iloc[0]["Formatted_title"]).strip()
                tuneJAMSFile.sandbox.formatted_title = title
                tuneJAMSFile.file_metadata.title = title

        tuneJAMSFile.sandbox.type = "score"
        tuneJAMSFile.sandbox.expanded = "true"
        tuneJAMSFile.sandbox.composers = []
        return tuneJAMSFile

    def __createJAMSAnnotation(self, name_space):
        pattern_annotation = jams.Annotation(namespace=name_space)
        pattern_annotation.annotation_metadata.annotator.name = self.config['jams_annotations']['annotator_name']
        pattern_annotation.annotation_metadata.data_source = self.config['jams_annotations']['data_source']
        pattern_annotation.annotation_metadata.corpus = self.config['jams_annotations']['corpus']
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
        for index, tuneRow in self.pattern_locations_in_tunes.iterrows():
            print(counter, tuneRow['id_number'], tuneRow['tune_title'])
            if(len(tuneRow['tune_title']) == 0):
                blank_count = blank_count + 1
                continue
            file_exists = os.path.exists(self.config['directories']['JAMS_files_dir'] + tuneRow['id_number']+"-"+tuneRow['tune_title'] + ".jams")
            if file_exists:
                counter = counter + 1
                continue
            tuneJAMSFile = self.__setCurrentTuneJamsMetadata(tuneRow)
            pattern_annotation = self.__createJAMSAnnotation(self.config['jams_annotations']['schema_name'])
            pattern_details =  tuneRow['locations']

            for pattern, pattern_locations in pattern_details.items():
                for location in pattern_locations:
                    pattern_dict = {
                        "pattern_id": str(tuneRow['id_number']) + ":" + tuneRow['tune_title'],
                        "pattern_content": str(pattern).strip("()"),
                        "pattern_type": "pitch-class-values",
                        "pattern_frequency": len(pattern_locations),
                        "pattern_complexity": round(len(set(pattern)) / len(pattern), 2),
                        "pattern_length": len(pattern),
                    }
                    pattern_annotation.append(time=location, duration=0.0, value=pattern_dict, confidence=1)

            counter = counter + 1
            tuneJAMSFile.annotations.append(pattern_annotation)
            tuneJAMSFile.save(self.config['directories']['JAMS_files_dir'] + tuneRow['id_number']+"-"+ tuneRow['tune_title'] + ".jams", strict=False)

    # Deprecated function
    def createJAMSFiles(self):
        self.jams_files_completions_status = 0
        counter = 1
        for tuneName in self.listOfTunes:
            file_exists = os.path.exists(self.config['directories']['JAMS_files_dir']+ tuneName+".jams")
            if file_exists:
                counter = counter + 1
                #continue
            #print(tuneName)
            rslt_df = self.filtered_df.loc[self.filtered_df[tuneName].notnull() == True, [tuneName, "index"]]
            #tune_feature_data = self.pattern_locations_in_tunes[tuneName].get(tune_feature_data)
            tune_id = self.getTuneId(tuneName)
            m_tune_id = self.getMorphedTuneId(tuneName)
            pattern_details_row = self.pattern_locations_in_tunes.loc[(self.pattern_locations_in_tunes['id_number'] == m_tune_id)]

            print(f"tune id: {tune_id}, m_tune_id: {m_tune_id}, tunename: {tuneName}, pattern_location: {len(pattern_details_row)}, pattern_freq: {len(rslt_df)}")
            #continue

            tuneJAMSFile = self.__setCurrentTuneJamsMetadata(tuneName)
            pattern_annotation = self.__createJAMSAnnotation(self.config['jams_annotations']['schema_name'])
            for index, row in rslt_df.iterrows():
                pattern_content = tuple(row['index']) #.strip("[]")
                # get locations
                # 40152 files are there in pattern file while in location file there are
                # 40148 record
                if(len(pattern_details_row) >= 1):
                    pattern_locations_dict = pattern_details_row.iloc[0]['locations']
                    if(pattern_content in pattern_locations_dict):
                        locations = pattern_locations_dict[pattern_content]
                        my_list = locations
                    else:
                        #print(f'{pattern_content} was not found in  {tuneName}')
                        logging.warning(f'{pattern_content} was not found in  {tuneName}')
                        my_list = []
                else:
                    logging.warning(f'Mismatch: {tuneName} was not found in pattern location pickel file ')
                    my_list = []

                for location in my_list:
                    #print(my_list, len(set(pattern_content)), len(v))
                    pattern_dict = {
                        "pattern_id": str(tune_id) + ":" + tuneName,
                        "pattern_content": str(pattern_content).strip("()"),
                        "pattern_type": "pitch-class-values",
                        "pattern_frequency": len(my_list),
                        "pattern_complexity": round(len(set(pattern_content)) / len(pattern_content), 2),
                        "pattern_length": len(pattern_content),
                    }
                    pattern_annotation.append(time=location, duration=0.0, value=pattern_dict, confidence=1)

            tuneJAMSFile.annotations.append(pattern_annotation)
            tuneJAMSFile.save(self.config['directories']['JAMS_files_dir']+ tuneName+".jams", strict=False)
            counter += 1

        # this will be used by rdf generator
        self.jams_files_completions_status = 0

if __name__ == "__main__":
    config = yaml.safe_load(open("config/config.yml"))
    genJAMSFiles = GenerateTunesJamsFile(config)
    genJAMSFiles.createJAMSFilesUsingNewPickleFile()
