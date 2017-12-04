import psycopg2
import inspect
import reportdb

DEBUG=0

def debugger():
    print("called {}".format(inspect.stack()[1][3]))
    print("called from {}".format(inspect.stack()[2][3]))

def test_function():
    if (DEBUG==1):
        debugger()

def print_10_rows(table):
    """print first 10 rows from the table"""
    rows = reportdb.get_data(table)
    i = 0
    while (i < 10 and i < len(rows)):
        print(rows[i][-2]) # testing TODO: remove this. It shows that I can access column 4 from a resulting table
        i+=1

def main():
    reportdb.create_views()
    if (DEBUG==1):
        debugger()
        test_function()
    '''Main program to run automatically when this module is called directly'''
    #print_rows("log")
    # print_rows("articles")
    # print_rows("authors")
    reportdb.print_report_summary(100)
    


if __name__ == '__main__':
    main()
