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
    drop_a_view("v_success_view_counts_bydate")
    drop_a_view("v_view_counts_bydate")


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
                    left join log l on l.path = '/article/' || a.slug \
                    group by a.title order by views desc;")
        db.commit()
        db.close()

    # Make sure the v_view_counts_bydate doesn't already exist
    if check_view_exists("v_view_counts_bydate") is True:
        print("found v_view_counts_bydate")
    else:
        db = psycopg2.connect("dbname={}".format(DBNAME))
        c = db.cursor()

        # Build the view
        c.execute("create view v_view_counts_bydate as select count(*), date(time) \
                  from log group by date;")
        db.commit()
        db.close()

    # Make sure the v_success_view_counts_bydate doesn't already exist
    if check_view_exists("v_success_view_counts_bydate") is True:
        print("found v_success_view_counts_bydate")
    else:
        db = psycopg2.connect("dbname={}".format(DBNAME))
        c = db.cursor()

        # Build the view
        c.execute("create view v_success_view_counts_bydate as \
                  select count(*), date(time) from log \
                  where status = '200 OK' \
                  group by date(time);")
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
    c.execute("select * from v_most_viewed_article limit 3;")
    rows = c.fetchall()
    db.close()
    return(rows)


def report_http_errors():
    """report on dates with more than 1% of requests returning errors"""

    db = psycopg2.connect("dbname={}".format(DBNAME))
    c = db.cursor()
    c.execute("select *  \
              from (select to_char(a.date,'Mon DD, YYYY') as friendly_date, \
              ROUND((1.0-((s.count+0.0)/(a.count))) * 100,2) \
              as percent_of_error from \
              v_success_view_counts_bydate s \
              right join v_view_counts_bydate a on a.date = s.date) as tbl \
              where tbl.percent_of_error > 1;")
    rows = c.fetchall()
    db.close()
    return(rows)


def print_report_summary(rows_to_print):
    """Print summary showing all reports, up to a line limit 'rows_to_print'"""

    # Header
    print("")
    print("Here's your report summary")
    print("<><><><><><><><><><><><><>")
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
        print(str(rows[i][-2]) + " - " + str(rows[i][-1]) + "%")
        i += 1
