"""Part 2 of the Compass data engineering challenge.

Part 2: Using the API and your language of choice, write a function that pulls
the data and loads it into the SQLite database.

__________

NOTE: Assumption is that file './part_1.py' has already been run using command
`$(which python3.7 dirname/part_1.py)` or similar. This is not re-run here,
although script is idempotent, due to possible side effects (e.g. possible
reprinted log statements).
"""

from __future__ import absolute_import

import utils


def ingest_pokemon():
    """Ingests the Pokemon model from the Pokemon API into SQLite table
    'pokemon'.

    NOTE: Problem statement explicitly discusses queries are bounded to the
    "first 15" of Pokemon. Assume that by the "first 15", sort by is on
    attribute "id" only, in ascending order (least to greatest).
    """
    if not utils.pokemon_table_schema_is_valid():
        error_message = (
            "SQLite table 'pokemon' is not valid. Re-run file " +
            "'$(pwd)/part_1.py' to reset persistent state."
        )
        raise ValueError(error_message)


def ingest_moves():
    """Ingests the Moves model from the Pokemon API into SQLite table 'moves'.
    """
    pass


if __name__=='__main__':
    ingest_pokemon()
    ingest_moves()
