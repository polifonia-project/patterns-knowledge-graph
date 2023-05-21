# we have to have this type available at the global scope. 
# but it's used by multiple other files, so we keep it here
# in its own file and import it elsewhere.
KG_Data = NamedTuple('KG_Data', [
    ('id_number', str),
    ('tune_title', str),
    # ('tune_family', str), # not used in MTC
    ('feature', str),
    ('level', str),
    ('n_vals', tuple),
    ('duration', int), # was 'duration_beats'
    ('locations', dict),
    ('feature_sequence_data', list)
])

