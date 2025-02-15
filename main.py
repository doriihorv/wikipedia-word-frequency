from fastapi import FastAPI
from pydantic import BaseModel
from wikipedia_scraper import collect_article_texts, count_words

app = FastAPI()

class KeywordsRequest(BaseModel):
    article: str
    depth: int
    ignore_list: list[str]
    percentile: int

@app.get("/word-frequency")
def word_frequency(article: str, depth:int):
    print(f"called word_frequency with {article} and depth: {depth}")
    collected_article_texts = collect_article_texts(article, depth)
    return count_words(collected_article_texts)


@app.post("/keywords")
def keyword_frequency(request: KeywordsRequest):
    collected_article_texts = collect_article_texts(request.article, request.depth)
    article_words_dict = count_words(collected_article_texts, request.ignore_list)
    result = {key: value for key, value in article_words_dict.items() if value[1] > request.percentile}
    return result