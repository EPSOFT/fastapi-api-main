# import asyncio

import nltk
from newspaper import Article

from app.models.tortoise import TextSummary
from app.sentiment import BertClassifier


async def generate_summary(summary_id: int, url: str) -> None:
    """ """

    # article summary
    article = Article(url)
    article.download()
    article.parse()

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")
    finally:
        article.nlp()

    summary = article.summary

    # sentiment analysis
    sentiment, positive_score, neutral_score, negative_score = BertClassifier(
        summary
    ).return_list()

    # summary model
    await TextSummary.filter(id=summary_id).update(
        summary=summary,
        sentiment=sentiment,
        positive_score=positive_score,
        neutral_score=neutral_score,
        negative_score=negative_score,
    )
