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
