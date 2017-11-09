# What are the most popular three articles of all time?
# Who are the most popular article authors of all time?
# On which days did more than 1% of requests lead to errors?

import psycopg2

# Connect to database
conn = psycopg2.connect("dbname=news")
cur = conn.cursor()

# Create output file
result_file = open("results.txt", "w")

# What are the most popular three articles of all time?
result_file.write("\n The three most popular articles of all time: \n")
cur.execute("SELECT * FROM article_views LIMIT 3;")
results1 = cur.fetchall()
for item in results1:
    result_file.write("%s \n" % str(item))

# Who are the most popular article authors of all time?
result_file.write("\n The most popular authors of all time: \n")
cur.execute("""SELECT name, sum(views) as views FROM article_views, name_title
            WHERE article_views.title=name_title.title GROUP BY name
            ORDER BY views DESC;""")
results2 = cur.fetchall()
for item in results2:
    result_file.write("%s \n" % str(item))

# On which days did more than 1% of requests lead to errors?
result_file.write("\n Days with more than 1% error rate: \n")
cur.execute("""SELECT day, percent
            FROM (SELECT day, errors/cast(ok as float)*100
            AS percent FROM status) AS sub
            WHERE percent > 1;""")
results3 = cur.fetchall()
for item in results3:
    result_file.write("%s \n" % str(item))

# Close connection to database
cur.close()
conn.close()

# VIEW for the most popular three articles

# CREATE VIEW article_views AS
# SELECT title, count(*) as views
# FROM (SELECT path, title FROM articles JOIN log ON
# path LIKE '%' || slug || '%') AS sub
# GROUP BY title
# ORDER BY views DESC;

# VIEW for the most popular authors

# CREATE VIEW name_title AS
# SELECT name, title
# FROM articles, authors
# WHERE author = authors.id

# VIEWS for the error rates

# CREATE VIEW errors AS
# SELECT date_trunc('day', time) AS day, count(*) as errors
# FROM log
# WHERE status != '200 OK'
# GROUP BY day;

# CREATE VIEW ok AS
# SELECT date_trunc('day', time) AS day, count(*) as ok
# FROM log
# WHERE status = '200 OK'
# GROUP BY day;

# CREATE VIEW status AS
# SELECT ok.day, ok, errors
# FROM errors, ok
# WHERE ok.day = errors.day;
