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


# Perform SQL query for top 3 article_views
def getTopArticles(file_name):
    db, cur = connect()
    query = "SELECT * FROM article_views LIMIT 3;"
    cur.execute(query)
    result = cur.fetchall()
    writeResults(file_name, result, "article")
    cur.close()
    db.close()


# Perform SQL query for top 3 authors
def getTopAuthors(file_name):
    db, cur = connect()
    query = """SELECT name, sum(views) as views FROM article_views, name_title
    WHERE article_views.title=name_title.title GROUP BY name
    ORDER BY views DESC;"""
    cur.execute(query)
    result = cur.fetchall()
    writeResults(file_name, result, "author")
    cur.close()
    db.close()


# Perform SQL query for dates with error rate > 1%
def getErrorDates(file_name):
    db, cur = connect()
    query = """SELECT day, percent FROM (SELECT day,
    ROUND(CAST(errors/CAST(ok + errors AS FLOAT)*100 AS NUMERIC),2)
    AS percent FROM status) AS sub
    WHERE percent > 1;"""
    cur.execute(query)
    result = cur.fetchall()
    writeResults(file_name, result, "error")
    cur.close()
    db.close()


# Format output correctly depending on query
def writeResults(result_file, results, category):
    # result_file = open(file_name, "w")
    if category == "article":
        result_file.write("\n The three most popular articles of all time: \n")
    elif category == "author":
        result_file.write("\n The most popular authors of all time: \n")
    elif category == "error":
        result_file.write("\n Days with more than 1% error rate: \n")
    for item in results:
        if category == "article":
            result_file.write("* \"%s views \n" % "\" -- ".join(map(str, item)))  # NOQA
        elif category == "author":
            result_file.write("* %s views \n" % " -- ".join(map(str, item)))
        elif category == "error":
            result_file.write("* %s%% errors \n" % " -- ".join(map(str, item)))


# Create output file
def writeReport(file_name):
    with open(file_name, "w") as result_file:
        getTopArticles(result_file)
        getTopAuthors(result_file)
        getErrorDates(result_file)


writeReport("results.txt")
