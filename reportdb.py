# "Database code" for the report.

import datetime
import psycopg2

if (DBNAME == ""):
    DBNAME="news" # TODO: remove this after testing

def get_data(table):
  """Return all from the 'database', most recent first."""
  db = psycopg2.connect("dbname={}".format(DBNAME)) 
  c = db.cursor()
  query = "select * from {}".format(table)
  c.execute(query)
  rows = c.fetchall()
  return(rows)
  db.close()

def add_row(table,content):
  """Add a row."""
  db = psycopg2.connect("dbname={}".format(DBNAME))
  c = db.cursor()
  c.execute("insert into (%s) values (%s)", (table,) (content,))
  db.commit()
  db.close()


