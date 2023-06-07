import os
import sys
import yaml
from subprocess import check_output, CalledProcessError
import glob, os
import os.path
from rdflib import Graph, URIRef

class JAMS2RDF:
    query_test = namespace= rdf_directory= jams_files_dirctory = ""
    config = []
    jams2rdf_obj = None
    # constructor of the class for initialiazing various class level variables
    def __init__(self, config, jams_files_dirctory, jams2rdf_obj):
        self.sparql_query_file = config['directories']['sparql_query_file']
        self.rdf_directory = config['directories']['rdf_directory']
        if not os.path.isdir(self.rdf_directory):
            os.makedirs(self.rdf_directory)
        self.jams_files_dirctory = jams_files_dirctory
        self.config = config
        self.jams2rdf_obj = jams2rdf_obj
    # jams2rdf is the main function for converting a JAMS file into RDF, according to jams
    # ontology and by using the SPARQL Anything software.
    # In particular, this code calls the SPARQL Anything code, written in Java
    # and runs it against a SPARQL Anything query, specifically developed for
    # converting JAMS files.
    def jams2rdf(self, input_file: str, output=None, output_format: str = 'ttl'):
        input_filename_with_ext = os.path.basename(input_file)
        jams_file, ext = os.path.splitext(input_filename_with_ext)
        input_file_dir_name = os.path.dirname(input_file)
        # input_file = input_file_dir_name +"/"+ input_filename_with_ext
        print(input_filename_with_ext, output)
        # change here: no need to have a template query and replace the filename.
        # instead, hard-code the filename as tmp.jams, and copy the input .jams file there
        check_output(['cp', input_file, './sparql_anything/tmp.jams'])        
        g = Graph()
        os.chdir(self.config["directories"]["query_dir"])
        try:
            out = check_output(["java", "-jar",
                                self.config["directories"]["sparql_anything_jar_file"],
                                "-q",
                                self.config["directories"]["sparql_query_file"],
                                "-o",
                                output
                                ])
            # print(out)
            # g.parse(out)
        except CalledProcessError as e:
            print(e)
            print("Output graph is empty for {}".format(input_file))
        os.chdir("..")

        # previous method was to parse the output to a Graph and serialise
        # but for now, we are just going to write the output straight to disk
        # I'm keeping this code in case we revert later.
        # if output:
        #     with open(output, 'w', encoding='utf-8') as wo:
        #         wo.write(g.serialize(format=output_format))


    # this function will iterate over JAMS directory
    def iterateThroughDirectory(self):
            print("The second step of JAMS pipeline - Iterating JAMS directory for converting JAMS to RDF")
            #while self.jams2rdf_obj.get_jams_files_completions_status() :
            counter = 1
            for filename in glob.iglob(self.jams_files_dirctory+ "*.jams", recursive=True):
                if os.path.isfile(filename):  # filter dirs
                    #print(counter, filename)
                    filenamewithext = os.path.basename(filename)
                    jams_file, ext = os.path.splitext(filenamewithext)
                    outfilePath = self.rdf_directory + "/" + jams_file + ".ttl"
                    file_exists = os.path.exists(outfilePath)
                    if not file_exists:
                        print(counter, filename)
                        counter = counter + 1
                        self.jams2rdf(filename, outfilePath)
            print("Process end: conversion completed (no more files available for conversion)")
if __name__ == "__main__":
    config = yaml.safe_load(open("config/jams2rdf_config.yml"))
    jams2rdf = JAMS2RDF(config)
    jams2rdf.iterateThroughDirectory()
