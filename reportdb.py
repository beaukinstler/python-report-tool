# "Database code" for the report.

import datetime
import psycopg2


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


def create_view_author_article_count():
  """Build the view of author ariticle counts"""
  db = psycopg2.connect("dbname={}".format(DBNAME))
  c = db.cursor()
  c.execute("create view v_author_article as select authors.name, count(articles.author) as num_of_articles \
                from authors \
                left outer join articles on authors.id = articles.author \
                group by authors.name order by num_of_articles desc;")
  db.commit()
  db.close()

def report_authors_article_count():
  """get the Authors' article counts"""
  db = psycopg2.connect("dbname={}".format(DBNAME))
  c = db.cursor()
  c.execute("select * from v_author_article;")
  rows = c.fetchall()
  db.close()
  return(rows)
