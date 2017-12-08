import argparse
import reportdb


PARSER = argparse.ArgumentParser()
PARSER.add_argument("-c", "--createviews",
                    help="if the views haven't been created, \
                    this flag will attempt to build them",
                    action="store_true")
ARGS = PARSER.parse_args()


def print_10_rows(table):
    """utility to print first 10 rows from a table"""

    rows = reportdb.get_data(table)
    i = 0
    while i < 10 and i < len(rows):
        print(rows[i][0])
        i += 1


def main():
    """main program"""

    if ARGS.createviews:
        reportdb.create_views()

        # Test a call to the db
        try:
            print_10_rows("v_author_article")
            print("Views created and tested")
        except Exception as e:
            print("There was a problem connecting \
                  to the 'v_author_article' view. \
                  there may be a problem with \
                  the database or views didn't build correctly.")
            print(e.args[0])
        return

    reportdb.print_report_summary(100)

if __name__ == '__main__':
    main()
