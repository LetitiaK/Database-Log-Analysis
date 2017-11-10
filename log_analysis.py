#!/usr/bin/env python

# This Python code uses the news database and psycopg2 to answer the
# following three questions:
# What are the most popular three articles of all time?
# Who are the most popular article authors of all time?
# On which days did more than 1% of requests lead to errors?

import psycopg2


# Connect to database
def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cur = db.cursor()
        return db, cur
    except BaseException:
        print("Unable to connect to database")


# Perform SQL query
def sql_query(headline, query, result_file, category):
    db, cur = connect()
    result_file.write(headline)
    cur.execute(query)
    results = cur.fetchall()
    write_results(results, category)
    cur.close()
    db.close()


# Format output correctly depending on query
def write_results(results, category):
    for item in results:
        if category == "article":
            result_file.write("* \"%s views \n" % "\" -- ".
                              join(map(str, item)))
        elif category == "author":
            result_file.write("* %s views \n" % " -- ".join(map(str, item)))
        elif category == "percent":
            result_file.write("* %s%% errors \n" % " -- ".join(map(str, item)))


# Create output file
result_file = open("results.txt", "w")
sql_query("\n The three most popular articles of all time: \n",
          "SELECT * FROM article_views LIMIT 3;", result_file, "article")
sql_query("\n The most popular authors of all time: \n",
          """SELECT name, sum(views) as views FROM article_views, name_title
          WHERE article_views.title=name_title.title GROUP BY name
          ORDER BY views DESC;""", result_file, "author")
sql_query("\n Days with more than 1% error rate: \n",
    	     """SELECT day, percent FROM (SELECT day,
             ROUND(CAST(errors/CAST(ok + errors AS FLOAT)*100 AS NUMERIC),2)
             AS percent FROM status) AS sub
             WHERE percent > 1;""", result_file, "percent")
