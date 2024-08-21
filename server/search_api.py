from database import connect_to_local_database
from weaviate.classes.query import MetadataQuery

with connect_to_local_database() as client:
    articles = client.collections.get("Article")

    response = articles.query.near_text(
        query="food crisis",
        distance=0.6,
        return_metadata=MetadataQuery(distance=True),
    )

    for o in response.objects:
        print(o.properties)
        print(o.metadata.distance)
