import csv
import os
import sys
import unicodedata
import uuid
from dataclasses import asdict
from datetime import datetime
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

from .utils import HEADERS, SaveFile, Article
from loguru import logger


class CitiBusinessOnline:
    def __init__(self, url: str):
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL: must start with 'http://' or 'https://'")
        self.url = url
        # self.file_name = unquote(
        #     url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
        # )
        self.file_name = str(uuid.uuid4().hex)

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
            page.a["href"] for page in soup.find_all("div", class_="jeg_thumb")
        ]

        try:
            logger.info(f"Saving results to csv...")
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

                        title = soup_page.find("h1", class_="jeg_post_title")
                        title = title.text.strip() if title else ""
                        title = unicodedata.normalize("NFKD", title).encode("ASCII", "ignore").decode("utf-8")

                        content = soup_page.find("div", class_="content-inner")
                        content = content.text.strip().replace("ADVERTISEMENT", "") if content else ""

                        published_date = soup_page.find("div", class_="jeg_meta_date")
                        published_date = published_date.text.strip() if published_date else ""

                        category = soup_page.find('div', class_='jeg_meta_category')
                        if category:
                            category_text = category.text.strip()
                            category = category_text.replace('in', '').strip()
                            split_categories = [category.strip() for category in category.split(',')[:-1]]
                            category = ", ".join(split_categories)
                        else:
                            print("Category element not found.")

                        author = soup_page.find("div", class_="jeg_meta_author coauthor")
                        if author is not None:
                            a_author = author.find("a")
                            if a_author is not None:
                                author_text = a_author.get_text(strip=True)
                            else:
                                logger.info("No <a> element found!")

                        article = Article(
                            title=title,
                            content=content,
                            author=author_text,
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


# if __name__ == "__main__":
#     three = CitiBusinessOnline(url="https://citibusinessnews.com/ghanabusinessnews/business/")
#     three.download()

# Dallas75080!
# pypi-AgEIcHlwaS5vcmcCJGFhMTcxZjE3LTEwY2UtNDFjOC1hOGMyLWIyM2YzZDY3NTg0ZAACHlsxLFsiYmFuay1vZi1naGFuYS1meC1yYXRlcyJdXQACLFsyLFsiZDRkOTQ4NjUtZWExMC00MTM0LTg3YzktYjViZmFjM2U5OTMxIl1dAAAGIPm42YhtdJp3W0vsY3zxFfd2IhbzycfHGRgawNSUk5Yl