"""Part 3.2 of the Compass data engineering challenge.

Part 3: Write a function to pull the correct data from the SQLite DB for each
question that the Pokemon services team wants answered.

- What is the average weight of the pokemon by Pokemon type?

__________

This problem was tricky because each Pokemon can have multiple types
(one-to-many association). For example, 'bulbasaur'
(https://pokeapi.co/api/v2/pokemon/1) has two types: 'grass' and 'poison'.

I interpreted this query as an aggregate group by over a table join between a
table of types and a table of pokemon. However, I did not understand how to
create the optimal data model given that, among other things, `sqlite3` has no
array type. I did find this answer on Stack Overflow w.r.t. creating one-to-many
relations in SQLite (https://stackoverflow.com/a/13262880), but I didn't
understand it fully, I don't know how extensible this would be in production,
and it seems overkill for a coding challenge.

Therefore, I munged my data model to duplicate records and flatten out the
'types' attribute directly within the 'pokemon' table so that I can execute an
aggregate group by query directly.
"""

from __future__ import absolute_import

import csv
import os

import sqlite3


def problem_3_2():
    """Solution to Problem 3.2.
    """
    database_name = 'pokemon.db'
    sqlite3_conn = sqlite3.connect(database_name)
    sqlite3_cursor = sqlite3_conn.cursor()

    sql_query = (
        'SELECT type, round(avg(weight), 2) ' +
        'FROM pokemon ' +
        'GROUP BY type ' +
        'ORDER BY type;'
    )
    print('SQL statement: ', sql_query)
    sqlite3_cursor.execute(sql_query)
    result = sqlite3_cursor.fetchall()

    result_filename = 'problem_3_2.csv'
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
    problem_3_2()
