#!/bin/sh
# Seeds trains.db with the exact dataset used in Session 6.
# Run once, from your project's root folder (next to actions.py):
#
#   sh seed_trains_db.sh
#
# Safe to re-run: it drops and recreates the table each time.

sqlite3 trains.db "DROP TABLE IF EXISTS routes;"
sqlite3 trains.db "CREATE TABLE routes (origin TEXT, destination TEXT, direct INTEGER);"
sqlite3 trains.db "INSERT INTO routes VALUES
  ('Berlin','Munich',1), ('Berlin','Hamburg',1),
  ('Berlin','Freiburg',0), ('Munich','Freiburg',1);"

echo "trains.db seeded. Expected results:"
echo "  Berlin -> Munich:   direct"
echo "  Berlin -> Hamburg:  direct"
echo "  Berlin -> Freiburg: indirect"
echo "  Munich -> Freiburg: direct"
echo "  anything else (e.g. Berlin -> Paris): not_found"
