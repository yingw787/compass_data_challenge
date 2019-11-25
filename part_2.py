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

import os
import requests

import sqlite3

import utils


def ingest_data():
    """Ingests the Pokemon model from the Pokemon API into SQLite table
    'pokemon'.

    NOTE: Problem statement explicitly discusses queries are bounded to the
    "first 15" of Pokemon. Assume that by the "first 15", sort by is on
    attribute "id" only, in ascending order (least to greatest).

    NOTE: Due to the prior limitation, and the fact that the REST API has
    limited separation of concerns w.r.t. model relations / associations, it may
    be best to re-use state within one method, rather than have multiple methods
    to retrieve data by data model.
    """
    def validate_execution_context():
        """Validates execution context to checkpoint progress in data pipeline.
        """
        expected_db_name = 'pokemon.db'
        expected_db_abspath = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            expected_db_name
        ))
        if not utils.database_exists():
            error_message = (
                'Database file \"{expected_db_abspath}\" does not exist.'
            )
            raise ValueError(error_message)

        sqlite3_conn = sqlite3.connect(expected_db_name)
        sqlite3_cursor = sqlite3_conn.cursor()

        if not utils.pokemon_table_schema_is_valid(
            sqlite3_conn,
            sqlite3_cursor
        ):
            error_message = (
                "SQLite table 'pokemon' is not valid. Re-run file " +
                "'$(pwd)/part_1.py' to regenerate persistent state."
            )
            raise ValueError(error_message)

        if not utils.moves_table_schema_is_valid(
            sqlite3_conn,
            sqlite3_cursor
        ):
            error_message = (
                "SQLite table 'moves' is not valid. Re-run file " +
                "'$(pwd)/part_1.py' to regenerate persistent state."
            )
            raise ValueError(error_message)


if __name__=='__main__':
    ingest_data()
