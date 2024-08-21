import csv
from datetime import datetime
from zoneinfo import ZoneInfo

from database import connect_to_local_database


def parse_date_string(date_string: str):
    return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z").replace(
        tzinfo=ZoneInfo(date_string[-3:])
    )


with open("bbc_news.csv") as csv_file:
    news_reader = csv.reader(csv_file)

    # skip the header
    next(news_reader)

    with connect_to_local_database() as client:
        articles = client.collections.get("Article")

        for i, article in enumerate(news_reader):
            articles.data.insert(
                {
                    "title": article[0],
                    "pubDate": parse_date_string(article[1]),
                    "guid": article[2],
                    "link": article[3],
                    "description": article[4],
                }
            )

            if i == 5:
                break
