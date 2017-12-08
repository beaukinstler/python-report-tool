Python Reporting Tool
================

This is a sample project for Udacity's "Programming Foundations" course, and the Full Stack Web Dev nano-degree.

In this project, I'm making a tool to report basic stats via text output.  The stats in this case, will be based on a postgresql database that has website logs.

Getting Started
---------------

You'll need to have Python installed on your computer. Python 3 is the version this application is developed on. Python 2.7 may work, but isn't the tested version.

You may also need to install some modules via pip

- psycopg2
- argparser

This tool also requires Postgresql. Tested on version 9.5.10. The database named `news` must be created, and the user running the code must have rights to write, read, and create views.

Finally, this requires a specific data and logs formated based on Udacity's sample blog app, and there should be data in those tables.

Documentation and Support
-------------------------

This is a demo project, and there is planned support. However, you may find support on the [Udacity forums](https://discussions.udacity.com/).

Usage
-----

1. Download and unzip the files in this [zip file](https://github.com/beaukinstler/python-report-tool/archive/master.zip), 
or clone with `$ git@github.com:beaukinstler/python-report-tool.git`
1. `cd` into the 'python-report-tool' folder.
1. Build the views
    - run `python3 report.py --createviews` or `python3 report.py -c`
1. With the views create, and data in the tables, run `python3 report.py`.


Issues
------

Contributing
------------

This is a demo project and will not be actively maintained. Your talents will be far more useful elsewhere.

Credits
-------

Beau Kinstler - Developer

Udacity and all it's contributors

License
-------

[MIT License](https://opensource.org/licenses/mit-license)
