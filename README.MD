# Log Analysis

This is the third project of the [Udacity](www.udacity.com) Nanodegree Program "Full Stack Web Developer". This code is a reporting tool that summarizes data from a large newspaper website database (which was provided by [Udacity](www.udacity.com)) using Python and PostgreSQL. In particular, the following three questions are answered:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Content

+ **log_analysis.py**: This file contains the python source code
+ **results.txt**: This is the output that is created by log_analysis.py

## The database
The database was provided by [Udacity](www.udacity.com) and was meant to represent the database of a newspaper website. It was structured as follows:

Table: **articles** -- 6 columns, 8 rows

| author     | title   | slug | lead | body | time | id|
| :----------| :-------|
| integer    | text    | text | text | text | timestamp with timezone | integer

Table: **authors** -- 3 columns, 4 rows

| name    | bio     | id |
| :-------| :-------|
| text    | text    | integer

Table: **log** -- 6 columns, 1,677,735 rows

| path   | ip    | method | status | time | id |
| :------| :-----|
| text   | inet  | text   | text   | timestamp with timezone | integer


## Getting started
*Please note: This code requires a working Python installation as well as a working PostgreSQL installation. The Python version used for this project is 2.7.12, which can be found [here](https://www.python.org/downloads/) and the PostgreSQL version used for this project is 9.5.9, which can be found [here](https://www.postgresql.org/download/).*

1. Download all files and save them within the same folder
2. Create the views for the database (see below!)
3. Chose one of the two possibilities described below to run the code

### Command line

1. Open a terminal
2. Change the directory (using cd) to access the folder, in which you saved the files
3. Type `python log_analysis.py`

### Python IDLE (Python GUI)

1. Open Python IDLE (it is automatically installed with the Python installation)
2. Open the file log_analysis.py
3. Run the code by pressing F5

## Views
In this project several views were created in order to solve the questions. In the following paragraphs, all views are presented in detail.

*! Note that you have to create these views in order to run the code !*

1. Open a terminal
2. Connect to your database by typing `psql -d news`
3. Copy and paste the following SQL queries and run them in your database.

### View for the most popular three articles
```
CREATE VIEW article_views AS
SELECT title, count(*) as views
FROM (SELECT path, title FROM articles JOIN log ON
path LIKE '%' || slug || '%') AS sub
GROUP BY title
ORDER BY views DESC;
```

### View for the most popular authors
```
CREATE VIEW name_title AS
SELECT name, title
FROM articles, authors
WHERE author = authors.id
```
### Views for the error rates
```
CREATE VIEW errors AS
SELECT date_trunc('day', time) AS day, count(*) as errors
FROM log
WHERE status != '200 OK'
GROUP BY day;
```
```
CREATE VIEW ok AS
SELECT date_trunc('day', time) AS day, count(*) as ok
FROM log
WHERE status = '200 OK'
GROUP BY day;
```
```
CREATE VIEW status AS
SELECT ok.day, ok, errors
FROM errors, ok
WHERE ok.day = errors.day;
```
## Troubleshooting
If running the code in the terminal throws an error, reinstall Python and make sure to select *Add python.exe* to Path during installation.

If the results are not shown correctly, make sure that you have created *ALL* views as desribed above.
