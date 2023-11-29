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


class PulseGh:
    def __init__(self, url: str, total_pages: int = None, limit_pages: int = None):
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL: must start with 'http://' or 'https://'")
        self.BASE_URL = url
        self.file_name = str(uuid.uuid4().hex)
        self.limit_pages = limit_pages
        self.total_pages = total_pages
        # self.BASE_URL = f"https://www.pulse.com.gh/{self.url_name}"
        # self.page_url_list = None
        # self.final_results = []
        self.session = requests.Session()

        if self.limit_pages is not None:
            if self.total_pages is None or self.total_pages > self.limit_pages:
                self.total_pages = self.limit_pages
            logger.info(f"Scraping from: {self.total_pages} pages. Please wait...")
        elif self.total_pages is not None:
            logger.info(f"Scraping from: {self.total_pages} pages. Please wait...")
        else:
            logger.error("Invalid configuration: No limit or total pages specified.")
            sys.exit(1)

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
        try:
            logger.info("saving results to csv...")
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
                    # scraping subsequent pages
                    for page_num in range(0, self.total_pages + 1):
                        if page_num == 0:
                            url = "https://www.pulse.com.gh"
                        elif page_num == 1:
                            # Scraping the base URL
                            url = self.BASE_URL
                        else:
                            url = f"{self.BASE_URL}?page={page_num}"

                        # Send a GET request to the URL
                        response = session.get(url, headers=HEADERS)

                        # Create a BeautifulSoup object with the response text and specify the parser
                        soup = BeautifulSoup(response.content, "html.parser")

                        # article_titles = soup.find("ul", class_="article-list-items list row")
                        # if not article_titles:
                        #     logger.warning(f"No article titles found on page {page_num}. Skipping...")
                        #     continue

                        links = soup.find_all("div", class_="gradient-overlay")

                        page_urls = [link.a["href"] for link in links]

                        for page in page_urls:
                            data = session.get(page, headers=HEADERS)
                            response_page = BeautifulSoup(data.content, "html.parser")
                            # title
                            title = response_page.find(
                                "h1", class_="article-headline"
                            ).find("span")
                            title = title.text.strip() if title else ""
                            title = unicodedata.normalize("NFKD", title).encode("ASCII", "ignore").decode("utf-8")

                            # author
                            author = response_page.find("span", class_="author-name")
                            author = author.text.strip() if author else ""

                            # category
                            category = response_page.find_all("a", class_="breadcrumbs-link")[-2]
                            category = category.text.strip() if category else ""

                            # published date
                            published_date = response_page.find(
                                "time",
                                class_="detail-article-date date-type-publicationDate",
                            )
                            published_date = (
                                published_date.text.strip() if published_date else ""
                            )
                            # content
                            content = response_page.find_all(
                                "div", class_="article-body-text"
                            )
                            all_text = "".join(
                                paragraph.get_text()
                                .strip()
                                .replace("ADVERTISEMENT", "")
                                for paragraph in content
                            )

                            article = Article(
                                title=title,
                                content=all_text,
                                author=author,
                                category=category,
                                published_date=published_date,
                                page_url=page,
                            )
                            # write data
                            writer.writerow(asdict(article))

                logger.info("Writing data to file...")
        except Exception as err:
            logger.error(f"Error: {err}")

        logger.info(f"All file(s) saved to: {output_dir} successfully!")
        logger.info("Done!")

# if __name__ == '__main__':
#     news = PulseGh(url="https://www.pulse.com.gh/news", total_pages=5, limit_pages=None)
#     news.download()
