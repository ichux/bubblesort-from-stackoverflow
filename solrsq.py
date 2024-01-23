import warnings

import sqlalchemy
from sqlalchemy import text

ENGINE = sqlalchemy.create_engine("solr://127.0.0.1:8983/solr/timestamps/sql")

SQL = "SELECT cat, name, price, inStock, author, series_t, sequence_i, genre_s FROM books LIMIT 10"
SQL2 = "SELECT series_t, count(*) FROM books GROUP BY series_t ORDER BY count(*) desc LIMIT 10"
SQL3 = "SELECT id, uptime, disk_percentage, added_on FROM timestamps LIMIT 3"


with ENGINE.connect() as conn:
    for query in [SQL3]:
        print(f"{query}\n")
        for _ in conn.execute(text(query)).all():
            print(_)

        print("\n")
