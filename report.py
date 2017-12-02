import psycopg2
import inspect
import reportdb

DEBUG=1

def debugger():
    print("called {}".format(inspect.stack()[1][3]))
    print("called from {}".format(inspect.stack()[2][3]))

def test_function():
    if (DEBUG==1):
        debugger()

def main():
    if (DEBUG==1):
        debugger()
        test_function()
    '''Main program to run automatically when this module is called directly'''
    rows = reportdb.get_data("log")
    i = 0
    while i < 10:
        print(rows[i][3]) # testing TODO: remove this. It shows that I can access column 4 from a resulting table
        i+=1


if __name__ == '__main__':
    main()
