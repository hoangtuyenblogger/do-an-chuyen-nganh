import sqlite3
conn = sqlite3.connect("data.db")
max_id = 0
sum_id = conn.execute("SELECT count(*) FROM links_news").fetchall()

for i in sum_id:
    for item in i:
        max_id = item
        pass
print(max_id)
