#!/usr/bin/python3

import argparse
import reportdb


PARSER = argparse.ArgumentParser()
PARSER.add_argument("-c", "--createviews",
                    help="if the views haven't been created, \
                    this flag will attempt to build them",
                    action="store_true")
PARSER.add_argument("-d", "--dropviews",
                    help="drop views and exit",
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

    if ARGS.dropviews:
        # Drop views and exit
        print("Attempting to drop views and exit the program")
        reportdb.drop_all_views()
        return 0

    if ARGS.createviews:
        print("Attempting to create and/or test the views. \
              You should see a list of author names if successful.")

        # Test a call to the db
        try:
            reportdb.create_views()
            print_10_rows("v_author_article")
            print("Views created and tested")
        except Exception as e:
            print("There was a problem connecting \
                  to the 'v_author_article' view. \
                  there may be a problem with \
                  the database or views didn't build correctly. \
                  An error message should follow with technical details")
            print(e.args[0])
        return
    else:
        try:
            if reportdb.check_view_exists("v_author_article") is False:
                print("Something went wrong. Perhaps try to build the views by running with the --createviews flag")
                return 1
        except:
            print("Something went wrong. Make sure the reportdb.py exists in the same directory as report.py")

    reportdb.print_report_summary(100)

if __name__ == '__main__':
    main()
