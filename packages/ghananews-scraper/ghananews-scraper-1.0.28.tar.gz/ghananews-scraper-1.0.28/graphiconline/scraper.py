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

from .utils import HEADERS, SaveFile, Article


class GraphicOnline:
    def __init__(self, url: str):
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL: must start with 'http://' or 'https://'")
        self.url = url
        self.file_name = str(uuid.uuid4().hex)
        self.BASE_PAGE = 'https://www.graphic.com.gh'

    def download(self, output_dir=None):
        """scrape data"""
        with requests.Session() as session:
            response = session.get(self.url, headers=HEADERS)

        if response.status_code != 200:
            logger.error(f"Request: {requests}; status code:{response.status_code}")
            response.raise_for_status()
            sys.exit(1)
        soup = BeautifulSoup(response.text, "html.parser")

        lst_pages = [
            self.BASE_PAGE + page.a["href"] for page in soup.find_all('td', class_='list-title')
        ]

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
                fieldnames = ["title", "content", "author", "category", "published_date", "page_url"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                for page_url in lst_pages:
                    with requests.Session() as session:
                        response_page = session.get(page_url, headers=HEADERS)
                        soup_page = BeautifulSoup(response_page.text, "html.parser")

                        title = soup_page.find("div", class_="article-header")
                        title = title.text.strip() if title else ""
                        title = unicodedata.normalize("NFKD", title).encode("ASCII", "ignore").decode("utf-8")

                        content_main = None
                        content = soup_page.find("div", {"class": "article-details"}).select("div p")
                        for tag in content:
                            content_main = tag.get_text().strip() if tag else ""

                        published_date = soup_page.find("div", {"class": "article-info"}).find("span",
                                                                                               class_="published")
                        published_date = published_date.text.strip() if published_date else ""

                        author = soup_page.find("div", {"class": "article-info"}).find("span", class_="createdby")
                        author = author.text.strip() if author else ""

                        # category
                        category = soup_page.find("div", {"class": "article-info"}).find("span", class_="category-name")
                        category = category.text.strip() if category else ""

                        article = Article(
                            title=title,
                            content=content_main,
                            author=author,
                            category=category,
                            published_date=published_date,
                            page_url=page_url,
                        )
                        # write data
                        writer.writerow(asdict(article))

                logger.info("Writing data to file...")
        except Exception as err:
            logger.error(f"error: {err}")

        logger.info(f"All file(s) saved to: {output_dir} successfully!")
        logger.info("Done!")


# if __name__ == '__main__':
#     graphic = GraphicOnline(url="https://www.graphic.com.gh/news/politics.html")
#     graphic.download()
