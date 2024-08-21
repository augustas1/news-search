import os
from weaviate import connect_to_local
from weaviate.classes.config import Property, DataType, Configure

cohere_key = os.getenv("COHERE_APIKEY")
headers = {
    "X-Cohere-Api-Key": cohere_key,
}


def connect_to_local_database():
    return connect_to_local(headers=headers)


if __name__ == "__main__":
    with connect_to_local() as client:
        # client.collections.delete_all()

        client.collections.create(
            "Article",
            vectorizer_config=[
                Configure.NamedVectors.text2vec_cohere(
                    name="title_description_vector",
                    source_properties=[
                        "title",
                        "description",
                    ],
                )
            ],
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="pubDate", data_type=DataType.DATE),
                Property(name="guid", data_type=DataType.TEXT),
                Property(name="link", data_type=DataType.TEXT),
                Property(name="description", data_type=DataType.TEXT),
            ],
        )
