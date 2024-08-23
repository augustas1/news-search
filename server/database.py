import asyncio
import os
from weaviate import use_async_with_local
from weaviate.classes.config import Property, DataType, Configure

cohere_key = os.getenv("COHERE_APIKEY")
headers = {
    "X-Cohere-Api-Key": cohere_key,
}


def connect_to_database():
    if os.getenv("LOCAL"):
        return use_async_with_local(headers=headers)
    else:
        return use_async_with_local(headers=headers, host="weaviate")


async def main():
    async with connect_to_database() as client:
        await client.collections.delete_all()

        await client.collections.create(
            "Article",
            vectorizer_config=[
                Configure.NamedVectors.text2vec_cohere(
                    name="title_vector",
                    source_properties=["title"],
                ),
                Configure.NamedVectors.text2vec_cohere(
                    name="description_vector",
                    source_properties=["description"],
                ),
            ],
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="pubDate", data_type=DataType.DATE),
                Property(name="guid", data_type=DataType.TEXT),
                Property(name="link", data_type=DataType.TEXT),
                Property(name="description", data_type=DataType.TEXT),
            ],
        )


if __name__ == "__main__":
    asyncio.run(main())
