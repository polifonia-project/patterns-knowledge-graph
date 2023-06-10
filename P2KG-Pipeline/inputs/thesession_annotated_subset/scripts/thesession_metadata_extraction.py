"""
thesession_metadata_extraction.py contains tools to extract metadata and musical score content from ABC Notation corpora
and write output to csv.
"""

import os
import pandas as pd


class AbcTransform:
    """Transform ABC Notation corpus from flat textfile to csv file

    Attributes:
        input_dir -- path to directory containing ABC Notation corpus file(s)
        abc_tunes -- concatenated list of all individual ABC Notation documents extracted from corpus file(s)
        abc_metadata -- dictionary containing restructured content from each item in abc_tunes for output to csv"""

    def __init__(self, input_dir):
        """initialize class object
        Args:
            input_dir -- see AbcTransform class docstring above"""
        self.input_dir = input_dir
        self.abc_tunes = []
        self.abc_metadata = dict()

    def read_abc(self):
        """Open, read and split content of ABC Notation corpus file(s) stored in input_dir.
         Output as list to abc_tunes attr"""

        concatenated_abc_content = []
        # read all ABC files in input_dir, split each tune and concatenate in one list
        for filename in os.listdir(self.input_dir):
            if filename.endswith(".abc"):
                with open(self.input_dir + "/" + filename, "r") as abc_file:
                    content = abc_file.read().split('\n\n')
                    concatenated_abc_content.append(content)

        for file_content in concatenated_abc_content:
            print(file_content)
            for line in file_content:
                    if not line.startswith("%"):
                        self.abc_tunes.append(f"\n{line}\n")

        return self.abc_tunes

    def extract_abc_metadata(self):

        """
        Extract content from abcstandard:v2.1 ABC metadata fields for all tunes in ABCTransform.abc_tunes
        and restructure to csv-ready dict
        """

        # relevant content field identifiers from ABC Notation
        abc_metadata_identifiers = ('identifiers', 'title', 'M', 'N', 'L', 'K', 'abc_score')
        for i in abc_metadata_identifiers:
            self.abc_metadata[i] = []

        # extract content from each field defined above
        for tune in self.abc_tunes:
            tune_lines = tune.split('\n')
            notes, titles, composer, identifier, key_signature, meter, tempo = [], [], [], [], [], [], []
            # 'N': notes
            for line in tune_lines:
                if line.startswith("N:"):
                    notes.append(line[2:])
            notes_str = ' / '.join(notes)
            self.abc_metadata["N"].append(notes_str)
            # 'T': tune title
            for line in tune_lines:
                if line.startswith("T:"):
                    # remove id number suffix
                    title_lst = line[2:].split(' ')[:-1]
                    formatted_title = ' '.join(title_lst)
                    titles.append(formatted_title)
            titles_str = ' '.join(titles)
            self.abc_metadata["title"].append(titles_str)
            # 'X': reference number
            for line in tune_lines:
                if line.startswith("X:"):
                    identifier.append(line[2:])
            id_str = ' '.join(identifier)
            self.abc_metadata["identifiers"].append(id_str)
            # 'K': key
            for line in tune_lines:
                if line.startswith("K:"):
                    key_signature.append(line[2:])
            key_str = ' '.join(key_signature)
            self.abc_metadata["K"].append(key_str)
            # 'M': meter
            for line in tune_lines:
                if line.startswith("M:"):
                    meter.append(line[2:])
            meter_str = ' '.join(meter)
            self.abc_metadata["M"].append(meter_str)
            # 'L': unit note length
            for line in tune_lines:
                if line.startswith("L:"):
                    tempo.append(line[2:])
            tempo_str = ' '.join(tempo)
            self.abc_metadata["L"].append(tempo_str)
            # music score content
            score = [line for line in tune_lines if not (line.startswith(abc_metadata_identifiers))]
            transcr_str = ' '.join(score)
            self.abc_metadata["abc_score"].append(transcr_str)

        return self.abc_metadata

    def write_output(self, out_path):
        """Write output to pandas DataFrame"""

        abc_metadata = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in self.abc_metadata.items()]))
        # drop empty rows
        rows_to_drop = abc_metadata[abc_metadata['identifiers'] == ''].index
        abc_metadata.drop(rows_to_drop, inplace=True)
        abc_metadata.to_csv(out_path, encoding='utf-8')


def main():
    """Apply metadata extraction process to ground-truth annotated subset of The Session corpus."""
    in_dir = "annotated_subset/families" # assumes user has stored abc files here
    out_path = "metadata/thesession_subset_metadata.csv"
    metadata = AbcTransform(in_dir)
    metadata.read_abc()
    metadata.extract_abc_metadata()
    metadata.write_output(out_path)


if __name__ == '__main__':
    main()
