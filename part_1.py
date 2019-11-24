"""Part 1 of the Compass data engineering challenge.

Problem: The Data Engineering team is trying to help the Pokemon services team
with creating an analytics database that they can answer some metrics
questions with. Pokemon services has a publicly available API located at
https://pokeapi.co/docs/v2.html/ that we will use to pull data from. We’ve
been tasked with designing a schema with tables that contain information to
answer the following questions about the first 15 Pokemon in their API.

Part 1: Using the API docs provided, design the tables with the columns you
will need to create in order to serve queries about the questions above. List
out all of the table names and columns in a text file to be submitted with the
homework. Additionally, create a SQLite database and create the schema/tables
that you designed in that database.
"""

from __future__ import absolute_import

import os

import sqlite3


def generate_sqlite_schema():
    """Generates the SQLite schema according to problem requirements.
    """
    # The problems involve keeping track of:
    # - Pokemon
    #   - Weight
    #   - Type
    #
    # - Moves
    #   - Type
    #   - Accuracy
    #
    # With a JOIN issued on type between the two tables.

    # Define variables to be used as part of the method.
    database = 'pokemon.db'

    # Delete the database if it already exists, in order to ensure idempotency
    # from stateful method call with side effects.
    database_abspath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        database
    ))
    if os.path.exists(database_abspath):
        os.remove(database_abspath)

    sqlite3_conn = sqlite3.connect(database)
    sqlite3_conn.commit()

    # Create SQL statements to be run.
    pokemon_create_table_sql = '''
    CREATE TABLE pokemon
    (
        id INTEGER PRIMARY KEY NOT NULL,
        name NVARCHAR(256) NOT NULL,
        type NVARCHAR(256) NOT NULL,
        weight INTEGER NOT NULL
    );
    '''
    sqlite3_conn.execute(pokemon_create_table_sql)
    sqlite3_conn.commit()

    moves_create_table_sql = '''
    CREATE TABLE moves
    (
        id INTEGER PRIMARY KEY NOT NULL,
        type NVARCHAR(256) NOT NULL,
        accuracy INTEGER NOT NULL
    );
    '''
    sqlite3_conn.execute(moves_create_table_sql)
    sqlite3_conn.commit()


def generate_txt_file_from_sqlite_schema():
    """Generates a .txt file from a SQLite schema.
    """
    pass

# Wrapping in order to avoid having to eagerly loading entire module at import
# time.
if __name__=='__main__':
    generate_sqlite_schema()
    generate_txt_file_from_sqlite_schema()
