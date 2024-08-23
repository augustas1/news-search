import asyncio
from datetime import datetime
from weaviate import WeaviateAsyncClient
from server.database import connect_to_database
from .article_queue import Article
from server.sqs import get_sqs
from types_aiobotocore_sqs.service_resource import Message, Queue


async def main():
    async with get_sqs() as sqs:
        queue = await sqs.get_queue_by_name(QueueName="article")

        async with connect_to_database() as database_client:
            while True:
                await asyncio.gather(
                    *[process_messages(queue, database_client) for index in range(20)]
                )
                print(f"{datetime.now()} Processed async batch.")


async def process_messages(queue: Queue, database_client: WeaviateAsyncClient):
    messages = await queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=2)

    if messages:
        await save_articles_to_database(database_client, messages)
        await delete_messages_from_queue(queue, messages)
        print(f"{datetime.now()} Processed {len(messages)} articles from SQS queue.")
    else:
        print(f"{datetime.now()} No messages in queue.")


async def save_articles_to_database(
    database_client: WeaviateAsyncClient, messages: list[Message]
):
    articles = database_client.collections.get("Article")

    extracted_articles = [
        Article.model_validate_json(await message.body).model_dump()
        for message in messages
    ]

    await articles.data.insert_many(extracted_articles)


async def delete_messages_from_queue(queue: Queue, messages: list[Message]):
    await queue.delete_messages(
        Entries=[
            {
                "Id": str(index),
                "ReceiptHandle": message.receipt_handle,
            }
            for index, message in enumerate(messages)
        ]
    )


if __name__ == "__main__":
    asyncio.run(main())
