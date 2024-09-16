import urllib.request
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import re

load_dotenv()
client = OpenAI() #auto gets API key from env
news_apikey = os.getenv("NEWS_API_KEY")


def get_news(category):
    # categories : general, world, nation, business, technology, entertainment, sports, science, health
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=uk&max=1&apikey={news_apikey}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

        for i in range(len(articles)):
            # articles[i].title
            print(f"Title: {articles[i]['title']}")
            # articles[i].description
            print(f"Description: {articles[i]['description']}")
            # You can replace {property} below with any of the article properties returned by the API.
            # articles[i].{property}
            # print(f"{articles[i]['{property}']}")
            return articles[i]['title'], articles[i]['description'], "uk"

def get_fact(title, description, country): # asks gpt to select a colour depending on weather factors
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an interesting fact generator, you will be given the title, description of a current news headline and you must generate a relevant unique and rare fact relating to this. Only state the fact with nothing additional."},
        {"role": "user", "content": f"The title is {title}. The description is {description}."}
    ]
    )
    return completion.choices[0].message.content

print("---------- NEWS -----------")
news_title, news_description, news_country = get_news("science")
print("\n---------- FACT -----------")
print(get_fact(news_title, news_description, news_country))

