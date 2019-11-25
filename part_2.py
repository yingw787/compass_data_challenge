"""Part 2 of the Compass data engineering challenge.

Part 2: Using the API and your language of choice, write a function that pulls
the data and loads it into the SQLite database.
"""

from __future__ import absolute_import

import os
import requests

import sqlite3

import part_1
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
    def validate_execution_context(
            sqlite3_conn,
            sqlite3_cursor
    ):
        """Validates execution context to checkpoint progress in data pipeline.

        Args:
            sqlite3_conn (sqlite3.Connection)
            sqlite3_cursor (sqlite3.Cursor)

        Raises:
            ValueError: Execution context does not match expectations.
        """
        if not utils.database_exists():
            error_message = (
                'Database file \"{expected_db_abspath}\" does not exist.'
            )
            raise ValueError(error_message)

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

    db_name = 'pokemon.db'
    sqlite3_conn = sqlite3.connect(db_name)
    sqlite3_cursor = sqlite3_conn.cursor()

    validate_execution_context(
        sqlite3_conn,
        sqlite3_cursor
    )

    # Fetch data and populate tables. #
    api_base_endpoint = 'https://pokeapi.co/api/v2/'

    pokemon_id_genexpr = (idx for idx in range(1, 16))
    _id = 1

    for pokemon_id in pokemon_id_genexpr:
        api_endpoint = api_base_endpoint + 'pokemon/' + str(pokemon_id)
        response = requests.get(api_endpoint)
        if response.status_code != 200:
            error_message = (
                f"Response status code is '{response.status_code}', " +
                "not expected HTTP 200 OK. Double check request URI and " +
                "headers."
            )
            raise ValueError(error_message)

        # NOTE: Not doing any kind of validation on response body, since it
        # would be tautological to failing fast when processing the response
        # body. If I did need to implement validation, I might store the
        # expected relevant JSON schema and walk along the response body,
        # comparing as I went.
        content = response.json()

        pokemon_name = content["name"]
        pokemon_num_moves = len(content["moves"])
        pokemon_weight = content["weight"]
        pokemon_types = content["types"]
        pokemon_moves = content["moves"]

        for pokemon_type in pokemon_types:
            _type = pokemon_type["type"]["name"]
            # Cannot overwrite an existing record by primary key if the primary
            # key column is declared. Instead, use ROWID:
            # https://stackoverflow.com/a/3676311
            sql_statement = (
                'INSERT INTO pokemon(rowid, pokemon_id, name, type, ' +
                'weight, num_moves) VALUES (' +
                f'{_id}, {pokemon_id}, \"{pokemon_name}\", \"{_type}\", ' +
                f'{pokemon_weight}, {pokemon_num_moves});'
            )
            print('SQL statement: ', sql_statement)

            sqlite3_cursor.execute(sql_statement)
            sqlite3_conn.commit()
            _id += 1

        for pokemon_move in pokemon_moves:
            pokemon_move_url = pokemon_move['move']['url']
            response = requests.get(pokemon_move_url)
            if response.status_code != 200:
                error_message = (
                    f"Response status code is '{response.status_code}', " +
                    "not expected HTTP 200 OK. Double check request URI and " +
                    "headers."
                )
                raise ValueError(error_message)

            content = response.json()

            move_id = content['id']
            move_name = content['name']
            move_type = content['type']['name']
            move_accuracy = content['accuracy']

            # NOTE: accuracy is nullable. Direct insertion into SQLite is not
            # possible. Must use string interpolation to make SQLite recognize
            # proper mapping of NoneType to SQLite null:
            # https://stackoverflow.com/a/51740434
            move_accuracy = (
                move_accuracy
                if move_accuracy is not None
                else ':null'
            )

            # Check whether the record already exists in the table before
            # attempting insertion, to avoid key confliction.
            sql_statement = (
                f'SELECT EXISTS(SELECT 1 FROM moves WHERE move_id={move_id});'
            )
            print('SQL statement: ', sql_statement)
            sqlite3_cursor.execute(sql_statement)
            result = sqlite3_cursor.fetchone()[0]

            if not result:
                sql_statement = (
                    'INSERT INTO moves(move_id, name, type, accuracy) ' +
                    f'VALUES ({move_id}, \"{move_name}\", \"{move_type}\", ' +
                    f'{move_accuracy});'
                )
                print('SQL statement: ', sql_statement)

                sqlite3_cursor.execute(sql_statement, {'null': None})
                sqlite3_conn.commit()


if __name__=='__main__':
    # NOTE: Overwriting a record by primary key gives error:
    # "sqlite3.IntegrityError: UNIQUE constraint failed". This behavior differs
    # from expected behavior of idempotent insert operation. Therefore, apply
    # idempotent Part 1 in order to ensure clean database state at time of
    # insertion.
    part_1.generate_sqlite_schema()
    part_1.generate_txt_file_from_sqlite_schema()
    ingest_data()
