# we have to have this type available at the global scope. 
# but it's used by multiple other files, so we keep it here
# in its own file and import it elsewhere.
from typing import NamedTuple
KG_Data = NamedTuple('KG_Data', [
    ('identifiers', str),
    ('title', str),
    # ('tune_family', str), # not used in MTC
    ('feature', str),
    ('level', str),
    ('n_vals', tuple),
    ('duration', int), # was 'duration_beats'
    ('pattern_locations', dict),
    ('data', list)
])

