import urllib.request
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from plyer import notification
import time

load_dotenv()
client = OpenAI() #auto gets API key from env
news_apikey = os.getenv("NEWS_API_KEY")

categories = ["general", "world", "nation", "business", "technology", "entertainment", "sports", "science", "health"]

def get_news(category):
    # categories : general, world, nation, business, technology, entertainment, sports, science, health
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=uk&max=1&apikey={news_apikey}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

        for i in range(len(articles)):

            # print(f"Title: {articles[i]['title']}")
            # print(f"Description: {articles[i]['description']}")

            return articles[i]['title'], articles[i]['description'], "uk"

def get_fact(title, description, country): # asks gpt to select a colour depending on weather factors
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an interesting fact generator, you will be given the title, description of a current news headline and you must generate a relevant unique and rare fact relating to this. Only state the fact with nothing additional. It must be a maximum of 64 characters"},
        {"role": "user", "content": f"The title is {title}. The description is {description}."}
    ]
    )
    return completion.choices[0].message.content

def shorten_title(title, description):
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Given the title and description of a news headline. please shorten the title to be less than 59 characters and make it suitable for a title of a fact. Only return the shortened title"},
        {"role": "user", "content": f"The title is {title}. The description is {description}."}
    ]
    )
    return completion.choices[0].message.content


def notify(title, fact):
    notification.notify(
        title=f"NEWS: {title}",
        message=fact,
        app_name='News Fact App',
        timeout=10
    )


def main():
    while True:
        for category in categories:
            news_title, news_description, news_country = get_news(category)
            # print(f"{category.upper()} NEWS:\n {news_title} - {news_description[:150]}...\n")
            shortened = shorten_title(news_title, news_description)
            fact = get_fact(news_title, news_description, news_country)
            # print(f"{shortened.upper()} FACT:\n {fact}\n")
            notify(shortened, fact)
            time.sleep(60*60*2) # sleeps for 2 hrs

if __name__ == "__main__":
    main()