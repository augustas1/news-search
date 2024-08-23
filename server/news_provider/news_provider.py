import asyncio
import csv
from datetime import datetime
from zoneinfo import ZoneInfo
from server.news_worker.article_queue import Article
from server.sqs import get_sqs
from itertools import batched
from types_aiobotocore_sqs.service_resource import Queue


async def main():
    with open("server/news_provider/bbc_news.csv") as csv_file:
        news_reader = csv.reader(csv_file)

        # skip the header
        next(news_reader)

        async with get_sqs() as sqs:
            queue = await sqs.get_queue_by_name(QueueName="article")
            batches = batched(enumerate(news_reader), 10)
            async_batches = batched(batches, 10)

            for parallel_batch in async_batches:
                await asyncio.gather(
                    *[send_message_batch(batch, queue) for batch in parallel_batch]
                )


async def send_message_batch(batch: tuple[tuple[int, list[str]]], queue: Queue):
    article_batch = []

    for index, article_properties in batch:
        article = Article(
            title=article_properties[0],
            pubDate=parse_date_string(article_properties[1]),
            guid=article_properties[2],
            link=article_properties[3],
            description=article_properties[4],
        )

        article_batch.append(
            {"Id": str(index), "MessageBody": article.model_dump_json()}
        )

    await queue.send_messages(Entries=article_batch)
    print(f"{datetime.now()} Sent {len(article_batch)} articles to the SQS queue.")


def parse_date_string(date_string: str):
    return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z").replace(
        tzinfo=ZoneInfo(date_string[-3:])
    )


if __name__ == "__main__":
    asyncio.run(main())
