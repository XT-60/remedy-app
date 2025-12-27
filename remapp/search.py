from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

client = MongoClient("mongodb+srv://myuser:mypassword123@pcluster.uytionn.mongodb.net/?appName=pcluster")
db = client["remedies"]
collection = db["remedies"]

model = SentenceTransformer("all-MiniLM-L6-v2")

def search_remedies(query, k=5):
    query_embedding = model.encode(query).tolist()

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": k
            }
        },
        {
            "$project": {
                "_id": 0,
                "condition": 1,
                "remedy_name": 1,
                "ingredients": 1,
                "steps": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    return list(collection.aggregate(pipeline))