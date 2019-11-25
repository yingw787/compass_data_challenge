"""Part 3.3 of the Compass data engineering challenge.

Part 3: Write a function to pull the correct data from the SQLite DB for each
question that the Pokemon services team wants answered.

- Count the number of moves by Pokemon and order from greatest to least

__________

- Pokemon are associated with moves, but moves do not appear to be associated
  with Pokemon. This may be because one move may be associated with multiple
  Pokemon. I'm not proficient enough to understand how a table join may or may
  not solve this problem, so instead store the aggregate sum of moves by Pokemon
  within table 'pokemon' and execute a SELECT ORDER BY query on the table
  directly.

NOTE: Due to answering problem 3.3, I munged my data model in order to have
duplicate records for pokemon by flattening out the types directly within the
'pokemon' table. In order to retrieve a result set of distinct records, I added
a DISTINCT keyword on column 'name' of table 'pokemon'.
"""

from __future__ import absolute_import

import csv
import os

import sqlite3


def problem_3_3():
    """Solution to Problem 3.3.
    """
    database_name = 'pokemon.db'
    sqlite3_conn = sqlite3.connect(database_name)
    sqlite3_cursor = sqlite3_conn.cursor()

    sql_query = (
        'SELECT DISTINCT name, num_moves ' +
        'FROM pokemon ' +
        'ORDER BY num_moves DESC;'
    )
    print('SQL statement: ', sql_query)
    sqlite3_cursor.execute(sql_query)
    result = sqlite3_cursor.fetchall()

    result_filename = 'problem_3_3.csv'
    result_abspath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        result_filename
    ))
    if os.path.exists(result_abspath):
        os.remove(result_abspath)

    _fp = open(result_abspath, 'w')
    writer = csv.writer(_fp)
    writer.writerows(result)
    _fp.flush()

    sqlite3_cursor.close()
    sqlite3_conn.close()

    write_successful = (
        'Writing result set has been successful. File located at: ' +
        f'\"{result_abspath}\".'
    )
    print(write_successful)


if __name__=='__main__':
    problem_3_3()
