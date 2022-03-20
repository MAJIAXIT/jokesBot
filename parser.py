import requests
from bs4 import BeautifulSoup
import re
from joke import Joke
import json
import psycopg2
from psycopg2 import sql
from config import dbname, user, password, host


def main():
    push_to_db()


def parse_html_data():
    """Parse html on the url"""

    url = "http://bashorg.org/random"
    r = requests.get(url=url)

    soup = BeautifulSoup(r.text, 'lxml')

    data = []

    for tag in soup.find_all("div", class_="q"):
        jokeId = "".join(re.findall(r"#([0-9]+)", tag.text))
        jokeText = tag.find("div", class_="quote").getText(separator="\n")

        joke = Joke(jokeId, jokeText)
        data.append(joke.__dict__)
    return data


def push_to_db():
    """Push data to database"""

    data = list(parse_html_data())

    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)

    cursor = conn.cursor()
    cursor.execute("TRUNCATE ONLY jokes RESTART IDENTITY")

    for joke in data:
        cursor.execute("INSERT INTO jokes (text) VALUES (%s)",
                       (str(joke["text"]),))
        conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
