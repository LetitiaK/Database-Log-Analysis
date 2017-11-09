# What are the most popular three articles of all time?
# Who are the most popular article authors of all time?
# On which days did more than 1% of requests lead to errors?

import psycopg2

# Connect to the database
conn = psycopg2.connect("dbname=news")
cur = conn.cursor()
cur.execute("SELECT * FROM article_views LIMIT 3;")
results = cur.fetchall()
print(results)
cur.close()
conn.close()

# What are the most popular three articles of all time?

# CREATE VIEW article_views AS
# SELECT title, count(*) as views
# FROM (SELECT path, title FROM articles JOIN log ON
# path LIKE '%' || slug || '%') AS sub
# GROUP BY title
# ORDER BY views DESC;

# SELECT *
# FROM article_views;

# Who are the most popular article authors of all time?

# CREATE VIEW name_title AS
# SELECT name, title
# FROM articles, authors
# WHERE author = authors.id

# SELECT name, sum(views) as views
# FROM article_views, name_title
# WHERE article_views.title = name_title.title
# GROUP BY name
# ORDER BY views DESC;

# On which days did more than 1% of requests lead to errors?

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

# SELECT day, percent
# FROM (SELECT day, errors/cast(ok as float)*100 AS percent FROM status) AS sub
# WHERE percent > 1;
