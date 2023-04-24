import os
import re
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()
app = Flask(__name__)


def main(URL):
    LINK = URL
    SUBREDDIT = re.search("r/(\w+?)/", LINK).group(1)
    ID36 = re.search("comments/(\w+?)/", LINK).group(1)

    CLIENT_ID = os.environ.get("CLIENT_ID")
    SECRET_TOKEN = os.environ.get("SECRET_TOKEN")
    USER = os.environ.get("USER")
    PASSWORD = os.environ.get("PASSWORD")

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

    # here we pass our login method (password), username, and password
    data = {
        "grant_type": "password",
        "username": USER,
        "password": PASSWORD,
    }

    # The purpose of this code is to retrieve comments of a Reddit post, extract the text of the parent comments,
    # and save them in a txt file.

    # Setup the header information which includes the description of our app.
    headers = {"User-Agent": "MyBot/0.0.1"}

    # Send the request for an OAuth token.
    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )
    # Convert the response to JSON and extract the access_token value.
    TOKEN = res.json()["access_token"]

    # Add authorization to the headers dictionary.
    headers = {**headers, **{"Authorization": f"bearer {TOKEN}"}}

    # Use headers=headers to make requests while the token is valid (around 2 hours).

    # Send the GET request to retrieve comments from the specified subreddit and article.
    response = requests.get(
        f"https://oauth.reddit.com/r/{SUBREDDIT}/comments/{ID36}?limit=200",
        headers=headers,
    )

    # Convert the response to JSON format.
    response = response.json()

    # Extract subreddit title
    subreddit_title = response[0]["data"]["children"][0]["data"]["subreddit"]

    # Extract post title
    post_title = response[0]["data"]["children"][0]["data"]["title"]

    # Get the data of parent comments.
    parent_comments = response[1]["data"]["children"]

    # Create an empty list to store the extracted comment text.
    comment_list = []

    # Extract the text of parent comments.
    for comment in parent_comments:
        try:
            if not comment["data"]["body"]:
                continue
        except KeyError:
            continue
        comment_list.append(comment["data"]["body"])

    # Write the comment text into a txt file.
    with open("comments.txt", "w", encoding="utf-8") as file:
        file.write(f"Subreddit Title: {subreddit_title}\n\n")
        file.write(f"Post Title: {post_title}\n\n")
        file.write(f"Comments Below:\n\n")
        for item in comment_list:
            file.write(f"{str(item)}\n")
            file.write(f"----------\n")

    # comments_dict = {
    #     "Subreddit Title": subreddit_title,
    #     "Post Title": post_title,
    #     "Comments": comment_list,
    # }

    return comments_dict


def run(URL):
    # Call your Python module here and get the result
    result = main(URL)
    # Return the result as a JSON object
    return result


print(
    run(
        "https://www.reddit.com/r/soccer/comments/12t6oqg/giovanni_albanese_the_sentence_on_the_fifteen/"
    )
)
