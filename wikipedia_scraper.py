import wikipediaapi
import re
from typing import Optional

class ArticleTitleNotFoundError(Exception):
    """
    Custom exception for when an Article Title is not found.
    """

    def __init__(self, article_title: str):
        super().__init__(f"Error: The article '{article_title}' does not exist on Wikipedia.")


def get_article_page(article_title:str) -> Optional[wikipediaapi.WikipediaPage]:
    """
    Fetches a Wikipedia page by its title.

    Args:
        article_title (str): The title of the Wikipedia article.

    Returns:
        Optional[wikipediaapi.WikipediaPage]: A WikipediaPage object if the article exists,
        otherwise None.
    """
    wikipedia = wikipediaapi.Wikipedia(user_agent='WikipediaWordFreqProject', language='en')
    page = wikipedia.page(article_title)

    if not page.exists():
        raise ArticleTitleNotFoundError(f"Error: The article '{article_title}' does not exist on Wikipedia.")
    
    return page

def collect_article_texts(root_article_title:str, depth:int) -> list[str]:
    """
    Recursively collects text content from a Wikipedia article and its linked articles up to a specified depth.

    Args:
        root_article_title (str): The title of the Wikipedia article to start from.
        depth (int): The depth of traversal for linked articles.

    Returns:
        list[str]: A list containing the text content of all visited Wikipedia articles.
    """
    articles_visited = set()
    articles_to_visit = {root_article_title}
    current_depth = 0
    article_texts = []

    while current_depth <= depth:
        new_articles_to_visit = set()
        for article in articles_to_visit:
            articles_visited.add(article)

            try:
                article_page = get_article_page(article)
            except ArticleTitleNotFoundError as e:
                print(e)
                continue

            article_content = article_page.text
            article_texts.append(article_content)

            article_links = article_page.links.keys()
            for article_link in article_links:
                if article_link not in articles_visited:
                    new_articles_to_visit.add(article_link)
        
        current_depth += 1
        articles_to_visit = new_articles_to_visit

        if len(new_articles_to_visit) == 0:
            break
        
    return article_texts

def count_words(articles:list[str], ignore_list:Optional[list[str]]=None) -> dict[str, tuple[int, float]]:
    """
    Counts the frequency of words in a list of articles.

    Args:
        articles (list[str]): A list of article texts.
        ignore_list (Optional[list[str]], optional): A list of words to ignore. Defaults to None.

    Returns:
        dict[str, tuple[int, float]]: A dictionary where keys are words and values are tuples 
        containing the count of occurrences and percentage frequency.
    """
    article_words_dict = {}
    word_counts = 0
    for article in articles:
        article_words = re.findall(r"\b\w+\b", article.lower())

        for article_word in article_words:
            if ignore_list and article_word in ignore_list:
                continue
            word_counts += 1
            if article_word not in article_words_dict:
                article_words_dict[article_word] = 1
            else:
                article_words_dict[article_word] += 1
        
    for article_word, count in article_words_dict.items():
        article_words_dict[article_word] = (count, round(count/word_counts*100,1))

    return article_words_dict
 
