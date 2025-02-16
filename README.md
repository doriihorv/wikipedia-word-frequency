## WIKIPEDIA WORD FREQUENCY ##
Python server application that takes an article and a depth parameter as input, and
generates a word-frequency dictionary by traversing Wikipedia articles up to the specified depth.


### GET/word-frequency ###
Parameters:
article (string): The title of the Wikipedia article to start from.
depth (int): The depth of traversal within Wikipedia articles.

Response: 
A word-frequency dictionary that includes the count and percentage frequency of 
each word found in the traversed articles.

Example usage:
(given the uvicorn is running on local host and port 8000)
http://127.0.0.1:8000/word-frequency?article=Miss%20Meyers&depth=0


### POST /keywords ###
Request Body:
article (string): The title of the Wikipedia article.
depth (int): The depth of traversal.
ignore_list (array[string]): A list of words to ignore.
percentile (int): The percentile threshold for word frequency.

Response: 
A dictionary similar to the one returned by /word-frequency, but excluding words 
in the ignore list and filtered by the specified percentile.

Example usage (e.g. with postman)
url: http://127.0.0.1:8000/keywords
post data (json format): {"article":"Miss Meyers", "depth":0, "ignore_list":["and"], "percentile":"2"}


## Run the application ##
run the application with the following command:
uvicorn main:app --reload
