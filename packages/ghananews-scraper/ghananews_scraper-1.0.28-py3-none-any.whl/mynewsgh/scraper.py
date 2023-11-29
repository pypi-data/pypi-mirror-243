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


class MyNewsGh:
    def __init__(self, url: str, limit_pages: int = None):
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL: must start with 'http://' or 'https://'")
        self.url = url
        self.file_name = str(uuid.uuid4().hex)
        self.limit_pages = limit_pages
        # self.page_url_list = None
        # self.final_results = []
        self.session = requests.Session()
        response_page = self.session.get(self.url, headers=HEADERS)

        soup = BeautifulSoup(response_page.text, "html.parser")
        self.pages = soup.find_all(
            "li", class_="mvp-blog-story-wrap left relative infinite-post"
        )

        if self.limit_pages is not None:
            logger.info(f"Scraping from: {self.limit_pages} pages. Please wait...")
            self.page_url_list = [
                self.url + f"page/{page}/"
                for page in range(1, int(self.limit_pages) + 1)
            ]
        else:
            total_pages = soup.find("div", class_="pagination").span.text.split(" ")[-1]
            logger.info(f"Scraping from: {int(total_pages)} pages. Please wait...")
            self.page_url_list = [
                self.url + f"page/{page}/" for page in range(1, int(total_pages) + 1)
            ]

    # def get_tasks(self, session):
    #     tasks = []
    #     for url in self.page_url_list:
    #         tasks.append(asyncio.create_task(session.get(url)))
    #     return tasks
    #
    # async def get_data(self):
    #     async with aiohttp.ClientSession() as session:
    #         tasks = self.get_tasks(session)
    #
    #         responses = await asyncio.gather(*tasks)
    #         for response in responses:
    #             self.final_results.append(await response.text())

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
            with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
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

                with requests.Session() as session:
                    for page_url in self.page_url_list:
                        response_page = session.get(page_url, headers=HEADERS)
                        soup = BeautifulSoup(response_page.text, "html.parser")

                        pages = soup.find_all(
                            "li",
                            class_="mvp-blog-story-wrap left relative infinite-post",
                        )
                        articles = [page.a["href"] for page in pages]

                        for url in articles:
                            response_page = session.get(url, headers=HEADERS)
                            soup_page = BeautifulSoup(response_page.text, "html.parser")

                            # title
                            title = soup_page.find(
                                "h1", class_="mvp-post-title left entry-title"
                            )
                            title = title.text.strip() if title else ""
                            title = unicodedata.normalize("NFKD", title).encode("ASCII", "ignore").decode("utf-8")

                            # published data
                            published_date = soup_page.find(
                                "time", class_="post-date updated"
                            )
                            published_date = (
                                published_date.text.strip() if published_date else ""
                            )

                            # author
                            author = soup_page.find(
                                "span", class_="author-name vcard fn author"
                            ).find("a")
                            author = author.text.strip() if author else ""

                            # category
                            category = soup_page.find("span", class_="mvp-post-cat left")
                            category = category.text.strip() if category else ""
                            # print(category)

                            # content
                            content = [
                                content.text.strip()
                                for content in soup_page.find(
                                    "div", {"id": "mvp-content-main"}
                                ).find_all("p")
                            ]

                            article = Article(
                                title=title,
                                content=" ".join(content),
                                author=author,
                                category=category,
                                published_date=published_date,
                                page_url=url,
                            )
                            # write data
                            writer.writerow(asdict(article))

                logger.info("Writing data to file...")
        except Exception as err:
            logger.error(f"Error: {err}")

        logger.info(f"All file(s) saved to: {output_dir} successfully!")
        logger.info("Done!")


# if __name__ == '__main__':
#     news = MyNewsGh(url="https://www.mynewsgh.com/category/entertainment/", limit_pages=5)
#     news.download()

# def main():
#     news = MyNewsGh(url="https://www.mynewsgh.com/category/entertainment/", limit_pages=None)
#     asyncio.run(news.get_data())
#     news.download()
#
#
# if __name__ == '__main__':
#     main()
