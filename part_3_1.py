"""Part 3.1 of the Compass data engineering challenge.

Part 3: Write a function to pull the correct data from the SQLite DB for each
question that the Pokemon services team wants answered.

- List the highest accuracy move by Pokemon type

__________

There appears to be a property-based guarantee on a one-to-one association
between a "move" and a "type". Each move as an attribute of type "dict" and name
"type", with a key in the dict being "name". I believe names of types are
distinct, hence the one-to-one association.

Therefore, a simple aggregate group by query directly on the "moves" table
should suffice in answering this question, since each move is distinct,

NOTE: I wasn't sure whether "all moves" was all moves available through the API,
or whether it is set of moves available to the first 15 pokemon. I am assuming
that "all moves" is the set of moves available to the first 15 pokemon. From
manual testing of the API, I believe there are 728 distinct moves, and the move
with highest accuracy may vary drastically depending which assumption I went
with, and since the constraint is available, it should not be ignored. In a
production setting, due to changing requirements, the best solution may be to
download all moves into the table, and execute a filter by based on the
aggregate set of distinct moves from the 'pokemon' table.
"""

from __future__ import absolute_import

import csv
import os

import sqlite3


def problem_3_1():
    """Solution to Problem 3.1.
    """
    database_name = 'pokemon.db'
    sqlite3_conn = sqlite3.connect(database_name)
    sqlite3_cursor = sqlite3_conn.cursor()

    sql_query = (
        'SELECT type, max(accuracy) ' +
        'FROM moves ' +
        'GROUP BY type ' +
        'ORDER BY type;'
    )
    print('SQL statement: ', sql_query)
    sqlite3_cursor.execute(sql_query)
    result = sqlite3_cursor.fetchall()

    result_filename = 'problem_3_1.csv'
    result_abspath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        result_filename
    ))
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
    problem_3_1()
