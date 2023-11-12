# process metadata and pickle files to jams files to ttl files to single ttl file

# the config file is specified on the command-line: read it. it specifies
# directories

# input: directory containing both data and metadata (one line per tune)
# also contains relevant metadata, eg transcriber, corpus name in another csv

# open multiple pickles and open metadata x2

# for line in metadata
# assemble metadata to a jams file
# get all relevant pickle data for that line
# assemble into a list of observations
# each observation is of a pattern
# observations have locations in file
# patterns have other data - contents, length, type
# write a single jams file for this line, call it tmp.jams

# sparql query: read that tmp.jams, save in a list of outputs

# cat all the outputs, but omit the prefixes



