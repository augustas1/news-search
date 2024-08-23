import asyncio
from datetime import datetime
from pydantic import BaseModel
from server.sqs import get_sqs


class Article(BaseModel):
    title: str
    pubDate: datetime
    guid: str
    link: str
    description: str


async def main():
    async with get_sqs() as sqs:
        await sqs.create_queue(QueueName="article")


if __name__ == "__main__":
    asyncio.run(main())
