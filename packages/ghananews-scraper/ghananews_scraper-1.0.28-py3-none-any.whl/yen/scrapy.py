import csv
import os
import sys
import unicodedata
import uuid
from dataclasses import asdict
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from loguru import logger

from .utils import HEADERS, SaveFile, Article, Link

link1 = Link(url="https://yen.com.gh/politics/", category="politics", page_number=257)
link2 = Link(
    url="https://yen.com.gh/world/europe/", category="world/europe", page_number=14
)
link3 = Link(url="https://yen.com.gh/education/", category="education", page_number=90)
link4 = Link(url="https://yen.com.gh/ghana/", category="ghana", page_number=650)
link5 = Link(url="https://yen.com.gh/people/", category="people", page_number=1070)
link6 = Link(
    url="https://www.yen.com.gh", category="https://www.yen.com.gh", page_number=1
)
link7 = Link(
    url="https://yen.com.gh/world/africa/", category="world/africa", page_number=125
)
link8 = Link(url="https://yen.com.gh/world/asia/", category="world/asia", page_number=4)
link9 = Link(
    url="https://yen.com.gh/entertainment/", category="entertainment", page_number=1
)
link10 = Link(
    url="https://yen.com.gh/business-economy/",
    category="business-economy",
    page_number=1,
)
link11 = Link(
    url="https://yen.com.gh/business-economy/money/",
    category="business-economy/money",
    page_number=4,
)
link12 = Link(
    url="https://yen.com.gh/business-economy/technology/",
    category="business-economy/technology",
    page_number=7,
)


class YenNews:
    def __init__(self, url: str):
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL: must start with 'http://' or 'https://'")
        self.url = url
        self.file_name = str(uuid.uuid4().hex)

    def download(self, output_dir=None):
        """scrape data"""
        with requests.Session() as session:
            response = session.get(self.url, headers=HEADERS)
            if response.status_code != 200:
                logger.error(f"Request: {requests}; status code:{response.status_code}")
                response.raise_for_status()
                sys.exit(1)

        try:
            logger.info("Saving results to csv...")
            if output_dir is None:
                output_dir = os.getcwd()
                SaveFile.mkdir(output_dir)
            if not os.path.isdir(output_dir):
                raise ValueError(
                    f"Invalid output directory: {output_dir} is not a directory"
                )
            logger.info(f"File will be saved to: {output_dir}")
            stamp = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")
            file_path = os.path.join(output_dir, self.file_name + f"_{stamp}.csv")
            logger.info(f"Saving file as: {file_path}")
            with open(
                    file_path,
                    mode="w",
                    newline="",
                    encoding="utf-8",
            ) as csv_file:
                fieldnames = [
                    "title",
                    "content",
                    "author",
                    "category",
                    "published_date",
                    "page_url",
                ]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                links = [
                    (link1.url, link1.page_number, link1.category),
                    (link2.url, link2.page_number, link2.category),
                    (link3.url, link3.page_number, link3.category),
                    (link4.url, link4.page_number, link4.category),
                    (link5.url, link5.page_number, link5.category),
                    (link6.url, link6.page_number, link6.category),
                    (link7.url, link7.page_number, link7.category),
                    (link8.url, link8.page_number, link8.category),
                    (link9.url, link9.page_number, link9.category),
                    (link10.url, link10.page_number, link10.category),
                    (link11.url, link11.page_number, link11.category),
                    (link12.url, link12.page_number, link12.category),
                ]

                for url, num_pages, category in links:
                    if category in self.url:
                        page_numbers = num_pages
                        for page_num in range(1, page_numbers + 1):
                            page_url = url + f"?page={page_num}"
                            response_page = session.get(page_url, headers=HEADERS)
                            soup_page = BeautifulSoup(response_page.text, "html.parser")

                            pages = soup_page.find_all(
                                "a",
                                {
                                    "class": [
                                        "c-article-card-with-badges__headline",
                                        "c-article-card__headline",
                                        "c-article-card-main__headline",
                                        "c-article-card-horizontal__headline",
                                        "c-article-card-featured__headline",
                                    ]
                                },
                            )

                            links = [page["href"] for page in pages]

                            for link in links:
                                if link:
                                    with requests.Session() as session:
                                        response_page = session.get(
                                            link, headers=HEADERS, timeout=600
                                        )
                                    soup_page = BeautifulSoup(
                                        response_page.text, "html.parser"
                                    )

                                    title = soup_page.find(
                                        "h1", class_="c-main-headline"
                                    )
                                    title_main = title.text.strip() if title else ""
                                    title_main = (
                                        unicodedata.normalize("NFKD", title_main)
                                        .encode("ASCII", "ignore")
                                        .decode("utf-8")
                                    )

                                    content_main = ""
                                    content_div = [
                                        item
                                        for item in soup_page.find(
                                            "div", {"class": "post__content"}
                                        ).select("ul li strong")
                                    ]

                                    for tag in content_div:
                                        content_main = (
                                            content_main + tag.get_text().strip()
                                            if tag
                                            else ""
                                        )

                                    meta_date = soup_page.find(
                                        "div", {"class": "c-article-info post__info"}
                                    )
                                    published_date = (
                                        meta_date.text.strip() if meta_date else ""
                                    )

                                    author = soup_page.find(
                                        "span", {"class": "c-article-info__author"}
                                    )
                                    author_name = author.text.split("by", 1)[-1].strip() if author else None

                                    category = soup_page.find(
                                        "a", class_="c-label-item"
                                    )
                                    category = category.text.strip() if category else ""

                                    article = Article(
                                        title=title_main,
                                        content=content_main,
                                        author=author_name,
                                        category=category,
                                        published_date=published_date,
                                        page_url=link,
                                    )
                                    # write data
                                    writer.writerow(asdict(article))
                        break  # Stop looping if a matching category is found

                logger.info("Writing data to file...")
        except Exception as err:
            logger.error(f"error: {err}")

        logger.info(f"All file(s) saved to: {output_dir} successfully!")
        logger.info("Done!")


# if __name__ == "__main__":
#     urls = [
#         "https://yen.com.gh/people/",
#         "https://yen.com.gh/ghana/",
#         "https://yen.com.gh/education/",
#         "https://yen.com.gh/entertainment/",
#         "https://yen.com.gh/business-economy/",
#         "https://www.yen.com.gh/politics/",
#         "https://www.yen.com.gh/world/",
#         "https://www.yen.com.gh/world/europe/",
#         "https://www.yen.com.gh/world/asia/",
#         "https://www.yen.com.gh/world/africa/",
#         'https://yen.com.gh/business-economy/money/',
#         'https://yen.com.gh/business-economy/technology/'
#     ]
#
#     for url in urls:
#         print(f"Downloading data from: {url}")
#         yen = YenNews(url=url)
#         yen.download()
