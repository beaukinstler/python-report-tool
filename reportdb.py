#!/usr/bin/python3

# "Database code" for the report.
import psycopg2


DBNAME = "news"


def drop_a_view(table):
    """Drop a view"""
    db = psycopg2.connect("dbname={}".format(DBNAME))
    db.set_isolation_level(0)
    c = db.cursor()

    query = "drop view public.{};".format(table)
    try:
        c.execute(query)
    except:
        print("{} not found, nothing deleted".format(table))
    db.close()

def drop_all_views():
    drop_a_view("v_author_article")
    drop_a_view("v_most_viewed_article")
    drop_a_view("v_report_errors")

def get_data(table):
    """Return all from the 'database', most recent first."""
    db = psycopg2.connect("dbname={}".format(DBNAME))
    c = db.cursor()
    query = "select * from {}".format(table)
    c.execute(query)
    rows = c.fetchall()
    db.close()
    return rows


def check_view_exists(view_name):
    db = psycopg2.connect("dbname={}".format(DBNAME))
    c = db.cursor()
    c.execute("select * from information_schema.views    \
              where table_name = '{}';".format(view_name))

    rows = c.fetchall()
    db.close()

    if len(rows) > 0:
        return True
    else:
        return False


def create_views():
    """Build the views used for reports"""

    # Make sure the v_author_article doesn't already exist
    if check_view_exists("v_author_article") is True:
        print("found v_author_article")
    else:
        db = psycopg2.connect("dbname={}".format(DBNAME))
        c = db.cursor()

        # Build the view
        c.execute("create view v_author_article as select ath.name, \
                  count(l.path) from log l \
                  join articles a on '/article/' || a.slug = l.path \
                  join authors ath on ath.id = a.author group by \
                  ath.name order by count desc;")
        db.commit()
        db.close()

    # Make sure the v_most_viewed_article doesn't already exist
    if check_view_exists("v_most_viewed_article") is True:
        print("found v_most_viewed_article")
    else:
        db = psycopg2.connect("dbname={}".format(DBNAME))
        c = db.cursor()

        # Build the view
        c.execute("create view v_most_viewed_article as select a.title, \
                    count(l.time) as views from articles a \
                    left join log l on substr(l.path,10) = a.slug \
                    group by a.title order by views desc;")
        db.commit()
        db.close()

    # Make sure the v_report_errors doesn't already exist
    if check_view_exists("v_report_errors") is True:
        print("found v_report_errors")
    else:
        db = psycopg2.connect("dbname={}".format(DBNAME))
        c = db.cursor()

        # Build the view
        c.execute("create view v_report_errors as select *, \
                  to_char(date,'Mon DD, YYYY') as friendly_date \
                  from (select date, round((err+0.0)/ok,4)*100 as percent \
                  from (select date(log.time),count(ok.id) as ok \
                  , count(notok.id) as err  from log \
                  left join log ok on ok.status = '200 OK' and ok.id = log.id \
                  left join log notok on notok.status <> '200 OK' and \
                  notok.id = log.id group by date(log.time)) as tbl) \
                  as tbl2 where percent > 1;")
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


def report_articles_most_viewied():
    """get the Authors' article counts"""
    db = psycopg2.connect("dbname={}".format(DBNAME))
    c = db.cursor()
    c.execute("select * from v_most_viewed_article;")
    rows = c.fetchall()
    db.close()
    return(rows)


def report_http_errors():
    """report on dates with more than 1% of requests returning errors"""
    db = psycopg2.connect("dbname={}".format(DBNAME))
    c = db.cursor()
    c.execute("select friendly_date, cast(round(percent,2) as text) \
              ||'%' as error from v_report_errors;")
    rows = c.fetchall()
    db.close()
    return(rows)


def print_report_summary(rows_to_print):
    """Print summary showing all reports, up to a line limit 'rows_to_print'"""

    # Header
    print("")
    print("Here's your report summary")
    print("||||||||||||||||||||||||||||")
    print("")

    # Report 1
    print("Number of articles by author")
    print("============================")
    rows = report_authors_article_count()
    i = 0
    while i < rows_to_print and i < len(rows):
        print(str(rows[i][-2]) + " - " + str(rows[i][-1]))
        i += 1
    print("")

    # Report 2
    print("Number of views by article")
    print("==========================")
    rows = report_articles_most_viewied()
    i = 0

    while i < rows_to_print and i < len(rows):
        print('"' + str(rows[i][-2]) + '"' + " - " + str(rows[i][-1]))
        i += 1
    print("")

    # Report 3
    print("Dates with errors on over 1% of HTTP requests")
    print("=============================================")
    rows = report_http_errors()
    i = 0

    while i < len(rows):
        print(str(rows[i][-2]) + " - " + str(rows[i][-1]))
        i += 1
