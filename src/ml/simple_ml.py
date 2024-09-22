from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from typing import List
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from db.postgres import get_session_service
from models.posts import Posts
from sqlalchemy import select, insert
from schemas.posts import Posts as PostSchema


class SimpleML:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.texts = []
        self.text_vectors = None

    async def get_chunk(self, session):
        chunk_size = 50
        id_ = 0
        while True:
            stmnt = await session.execute(select(Posts).where(
                Posts.id > id_
            ).order_by(Posts.id).limit(chunk_size))
            posts = stmnt.fetchall()
            if posts:
                id_ = posts[-1][0].id
            yield [PostSchema(title=post[0].title, post_text=post[0].post_text) for post in posts]
            if len(posts) < chunk_size:
                break

    async def train_by_bd(self):
        session = await get_session_service()
        async for data in self.get_chunk(session):
            await self.train(data)

    async def train(self, data):
        texts = [f"{elem.title} {elem.post_text}" for elem in data]
        self.text_vectors = self.vectorizer.fit_transform(texts)
        joblib.dump(self.vectorizer, 'ml/vectorizer.pkl')
        joblib.dump(self.text_vectors, 'ml/text_vectors.pkl')
        joblib.dump(texts, 'ml/texts.pkl')

    async def predict(self, title):
        self.vectorizer = joblib.load('ml/vectorizer.pkl')
        self.text_vectors = joblib.load('ml/text_vectors.pkl')
        self.texts = joblib.load('ml/texts.pkl')
        title_vector = self.vectorizer.transform([title])
        similarities = cosine_similarity(title_vector, self.text_vectors)
        most_similar_index = np.argmax(similarities)
        return self.texts[most_similar_index]
