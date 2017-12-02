import psycopg2
import inspect

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


if __name__ == '__main__':
    main()
