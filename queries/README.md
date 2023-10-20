# SPARQL queries for the Patterns Knowledge Graph

Reminder: the Patterns KG is hosted and publicly available here: https://polifonia.disi.unibo.it/fonn/sparql

The `.sparql` files in this directory are SPARQL queries which can be run against that endpoint.

The following are intended to be useful in the Polifonia Web Portal:

* Complete list of tunes, giving tune title and URI: `get_tune_titles.sparql`
* Given a tune:
  * Find metadata such as title, duration in beats, key, meter (4/4, 6/8, etc): `find_metadata_given_tune.sparql`
  * Find which corpus it is from - with link to corpus: `find_corpus_given_tune.sparql`
  * Find the tune family and members: `find_members_same_family.sparql`
  * Find what patterns are present and how frequent they are: `get_patterns_frequences_given_tune.sparql`
  * Find similar tunes via similar patterns: `find_tunes_by_common_patterns.sparql`
  * In particular, find similar tunes **in a different corpus** via similar patterns: `TODO`
  * Find similar tunes via pre-calculated similarity values: **not implemented here, see TUNES**
* Given a tune family:
  * Find what patterns are present across the family and how frequent they are: `TODO`
  * Find a similar tune family via similar patterns **in a different corpus**: `TODO`
