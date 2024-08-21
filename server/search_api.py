from database import connect_to_local_database
from weaviate.classes.query import MetadataQuery
from fastapi import FastAPI

app = FastAPI()


@app.get("/api/articles")
def get_articles(query: str):
    with connect_to_local_database() as client:
        articles = client.collections.get("Article")

        response = articles.query.near_text(
            query=query,
            distance=0.6,
            return_metadata=MetadataQuery(distance=True),
        )

        return [
            {**article.properties, "distance": article.metadata.distance}
            for article in response.objects
        ]
