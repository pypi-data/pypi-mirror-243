import csv
import os
import uuid
from datetime import datetime
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

from .utils import HEADERS, SaveFile

BASE_PAGE = 'https://www.modernghana.com/archive/20230623/'


class ModernGhana:
    def __init__(self, url, by_date: str):
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL: must start with 'http://' or 'https://'")
        self.url = url
        self.file_name = str(uuid.uuid4().hex)

    def download(self, output_dir=None):
        """scrape data"""
        with requests.Session() as session:
            response = session.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        lst_pages = [
            BASE_PAGE + page.a["href"] for page in soup.find_all('td', class_='list-title')
        ]

        try:
            print("saving results to csv...")
            if output_dir is None:
                output_dir = os.getcwd()
                SaveFile.mkdir(output_dir)
            if not os.path.isdir(output_dir):
                raise ValueError(
                    f"Invalid output directory: {output_dir} is not a directory"
                )
            print(f"File will be saved to: {output_dir}")

            stamp = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")
            with open(
                    os.path.join(output_dir, self.file_name + f"_{stamp}.csv"),
                    mode="w",
                    newline="",
                    encoding="utf-8",
            ) as csv_file:
                fieldnames = ["title", "content", "published_date", "page_url"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                for page_url in lst_pages:
                    with requests.Session() as session:
                        response_page = session.get(page_url, headers=HEADERS)
                        soup_page = BeautifulSoup(response_page.text, "html.parser")

                        title = soup_page.find("div", class_="article-header")
                        title = title.text.strip() if title else ""

                        content_main = None
                        content = soup_page.find("div", {"class": "article-details"}).select("div p")
                        for tag in content:
                            content_main = tag.get_text().strip() if tag else ""

                        published_date = soup_page.find("div", {"class": "article-info"}).find("span", class_="published")
                        published_date = published_date.text.strip() if published_date else ""

                        writer.writerow(
                            {
                                "title": title,
                                "content": content_main,
                                "published_date": published_date,
                                "page_url": page_url,
                            }
                        )
                print("Writing data to file...")
        except Exception as err:
            print(f"error: {err}")

        print(f"All file(s) saved to: {output_dir} successfully!")
        print("Done!")
