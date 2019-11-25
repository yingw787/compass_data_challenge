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

__________

NOTE: Script should guarantee idempotency w.r.t. side effects on mainline
execution flow.

NOTE: Python module `sqlite3` connection and cursor objects do not implement
method `__enter__`, which means that they cannot be used as part of a context
manager. This may embrittle the process of closing connections in the event of
OS interrupts to Python process. However, since SQLite is a file and not
necessarily a separate daemon, this possibility may be mitigated or different
entirely from e.g. PostgreSQL.
"""

from __future__ import absolute_import

import contextlib
import os

import sqlite3


def generate_sqlite_schema():
    """Generates the SQLite schema according to problem requirements.
    """
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
    sqlite3_cursor = sqlite3_conn.cursor()

    sqlite3_conn.commit()

    # Create SQL statements to be run.
    pokemon_create_table_sql = '''
    CREATE TABLE pokemon
    (
        pokemon_id INTEGER NOT NULL,
        name NVARCHAR(256) NOT NULL,
        type NVARCHAR(256) NOT NULL,
        weight INTEGER NOT NULL,
        num_moves INTEGER NOT NULL
    );
    '''
    sqlite3_cursor.execute(pokemon_create_table_sql)
    sqlite3_conn.commit()

    # column 'accuracy' is nullable because some values can be null:
    # https://pokeapi.co/api/v2/move/14
    moves_create_table_sql = '''
    CREATE TABLE moves
    (
        move_id INTEGER PRIMARY KEY NOT NULL,
        name NVARCHAR(256) NOT NULL,
        type NVARCHAR(256) NOT NULL,
        accuracy INTEGER
    );
    '''
    sqlite3_cursor.execute(moves_create_table_sql)
    sqlite3_conn.commit()

    sqlite3_cursor.close()
    sqlite3_conn.close()


def generate_txt_file_from_sqlite_schema():
    """Generates a .txt file from a SQLite schema.

    Using a method to derive the answer from the created SQLite schemas in order
    to guarantee consistency between actual/stated schema.
    """
    txt_filename = 'schemas.txt'
    txt_abspath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        txt_filename
    ))
    if os.path.exists(txt_abspath):
        os.remove(txt_abspath)

    database = 'pokemon.db'
    sqlite3_conn = sqlite3.connect(database)
    sqlite3_cursor = sqlite3_conn.cursor()

    file_descriptor = open(txt_abspath, 'w')

    file_descriptor_intro = '''
    This file describes the schemas of tables used as part of the Compass data
    engineering challenge.

    Database is "pokemon.db".

    Tables as follows:
    '''
    file_descriptor.write(file_descriptor_intro)
    file_descriptor.flush()

    describe_pokemon_sql = '''
    SELECT sql
    FROM sqlite_master
    WHERE name = 'pokemon';
    '''
    sqlite3_cursor.execute(describe_pokemon_sql)
    result = sqlite3_cursor.fetchone()[0]
    file_descriptor.write('\n')
    file_descriptor.write(result)
    file_descriptor.write('\n')
    file_descriptor.flush()

    describe_moves_sql = '''
    SELECT sql
    FROM sqlite_master
    WHERE name = 'moves';
    '''
    sqlite3_cursor.execute(describe_moves_sql)
    result = sqlite3_cursor.fetchone()[0]
    file_descriptor.write('\n')
    file_descriptor.write(result)
    file_descriptor.write('\n')
    file_descriptor.flush()

    sqlite3_cursor.close()
    sqlite3_conn.close()
    file_descriptor.close()


# Wrapping in order to avoid having to eagerly loading entire module at import
# time.
if __name__=='__main__':
    generate_sqlite_schema()
    generate_txt_file_from_sqlite_schema()
