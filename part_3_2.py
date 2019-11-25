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
and it seems overkill for a coding challenge. Therefore, I munged my data model
to duplicate records and flatten out the 'types' attribute directly within the
'pokemon' table so that I can execute an aggregate group by query directly.
"""
