from ..database import connect_to_database
from weaviate.classes.query import TargetVectors, MetadataQuery
from fastapi import FastAPI

app = FastAPI()


@app.get("/api/articles")
async def get_articles(query: str, limit: int, offset: int):
    async with connect_to_database() as client:
        articles = client.collections.get("Article")

        response = await articles.query.near_text(
            query=query,
            limit=limit,
            offset=offset,
            distance=0.6,
            target_vector=TargetVectors.manual_weights(
                {"title_vector": 0.7, "description_vector": 0.3}
            ),
            return_metadata=MetadataQuery(distance=True),
        )

        return [
            {**article.properties, "distance": article.metadata.distance}
            for article in response.objects
        ]
