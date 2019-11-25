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
import re

import sqlite3


def ingest_pokemon():
    """Ingests the Pokemon model from the Pokemon API into SQLite table
    'pokemon'.

    NOTE: Problem statement explicitly discusses queries are bounded to the
    "first 15" of Pokemon. Assume that by the "first 15", sort by is on
    attribute "id" only, in ascending order (least to greatest).
    """
    def pokemon_table_schema_is_valid():
        """Validates SQLite table 'pokemon' and panics if result table schema
        does not match the expected table schema.

        Since method call is highly dependent on what the SQLite table schema
        is, ensure alignment between stateful db table generation, and stateful
        ingestion from third-party API, and checkpoint the data pipeline to
        diagnose any failures.
        """
        # Check that the database file exists. #
        expected_table_schema = ''
        expected_db_name = 'pokemon.db'
        expected_db_abspath = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            expected_db_name
        ))
        if not os.path.exists(expected_db_abspath):
            return False

        sqlite3_conn = sqlite3.connect(expected_db_name)
        sqlite3_cursor = sqlite3_conn.cursor()

        # Check that the table 'pokemon' exists. #
        existence_pokemon_sql = '''
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='pokemon';
        '''
        sqlite3_cursor.execute(existence_pokemon_sql)
        result = sqlite3_cursor.fetchone()[0]

        if result != 'pokemon':
            return False

        # Check that the table 'pokemon' has the expected schema. #
        describe_pokemon_sql = '''
        SELECT sql
        FROM sqlite_master
        WHERE name = 'pokemon';
        '''
        sqlite3_cursor.execute(describe_pokemon_sql)
        result = sqlite3_cursor.fetchone()[0]
        result = re.sub('[^0-9a-zA-Z\(\)]', ' ', result)
        result = ' '.join(result.split())

        expected = '''
        CREATE TABLE pokemon
            (
                id INTEGER PRIMARY KEY NOT NULL,
                name NVARCHAR(256) NOT NULL,
                type NVARCHAR(256) NOT NULL,
                weight INTEGER NOT NULL
            )
        '''
        expected = re.sub('[^0-9a-zA-Z\(\)]', ' ', expected)
        expected = ' '.join(expected.split())

        if expected != result:
            return False

        sqlite3_cursor.close()
        sqlite3_conn.close()

        return True

    if not pokemon_table_schema_is_valid():
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
