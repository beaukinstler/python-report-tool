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

Finally, this requires a specific data and logs based on Udacity's sample blog app, and there should be data in those tables. As of now, this data can be [downloaded here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

To import this data into an existing postgresql installation, you refer to Udacity's instructions.

> To load the data, cd into the ... directory (where your "newsdata.sql" file is) and use the command
> `psql -d news -f newsdata.sql`.
> Here's what this command does:
> 
>     psql — the PostgreSQL command line program
>     -d news — connect to the database named news which has been set up for you
>     -f newsdata.sql — run the SQL statements in the file newsdata.sql
> 
> Running this command will connect to your installed database server and execute the SQL commands in 
> the downloaded file, creating tables and populating them with data. 

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

View Code
---------

_Note: These views are also built by running the `report.py` script with a `-c` flag. See above._

        create view v_author_article as 
        select authors.name,
        count(articles.author) as num_of_articles
        from authors
        left outer join articles on authors.id = articles.author
        group by authors.name order by num_of_articles desc;

        create view v_most_viewed_article as 
        select a.title, 
        count(l.time) as views from articles a 
        left join log l on substr(l.path,10) = a.slug 
        group by a.title order by views desc;

        create view v_report_errors as 
        select *, to_char(date,'Mon DD, YYYY') as friendly_date 
        from (
            select date, round((err+0.0)/ok,4)*100 as percent 
            from (
                select date(log.time),count(ok.id) as ok,
                    count(notok.id) as err  
                from log 
                left join log ok on ok.status = '200 OK' and ok.id = log.id 
                left join log notok on notok.status <> '200 OK' and 
                    notok.id = log.id group by date(log.time)
                ) as tbl
            ) as tbl2 where percent > 1;


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
