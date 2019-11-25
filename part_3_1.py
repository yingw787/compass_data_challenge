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
