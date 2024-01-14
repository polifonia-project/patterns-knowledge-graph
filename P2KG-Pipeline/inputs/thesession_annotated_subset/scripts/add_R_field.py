import pandas as pd

fname = "../metadata/thesession_subset_metadata.csv"
outfname = "../metadata/thesession_subset_metadata_with_R.csv"
import pandas as pd
df = pd.read_csv(fname)

def getRhythm(s):
    start = s.find("R:")
    end = s[start+2:].index(" ")
    return s[start+2:start+2+end].strip()

rhythms = [getRhythm(s) for s in df['abc_score']]

df['R'] = rhythms

df.to_csv(outfname)