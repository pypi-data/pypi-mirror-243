import csv
import unicodedata
from dataclasses import asdict

import requests
from bs4 import BeautifulSoup
from .utils import SaveFile, HEADERS, Article
from datetime import datetime
import uuid
import os
from loguru import logger


class CitiBusiness:
    def __init__(self, author: str, limit_pages: int = None):
        self.file_name = str(uuid.uuid4().hex)
        self.author = author
        self.limit_pages = limit_pages

        self.url = f"https://citibusinessnews.com/author/{self.author}/"
        response = requests.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        self.last_page = int(soup.find("span", class_="page_info").text.split(" ")[-1])

        if self.limit_pages is not None:
            self.last_page = self.limit_pages
            logger.info(f"Scraping data from: {self.last_page} pages. Please wait...")
        else:
            logger.info(f"Scraping data from: {self.last_page} pages. Please wait...")

    def download(self, output_dir=None):
        try:
            logger.info("Saving results to CSV...")
            if output_dir is None:
                output_dir = os.getcwd()
                SaveFile.mkdir(output_dir)
            if not os.path.isdir(output_dir):
                raise ValueError(f"Invalid output directory: {output_dir} is not a directory")
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
                fieldnames = ["title",
                              "content",
                              "author",
                              "category",
                              "published_date",
                              "page_url"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                session = requests.Session()

                for page_num in range(1, self.last_page + 1):
                    if page_num == 1:
                        page_url = self.url
                    else:
                        page_url = f"{self.url}page/{page_num}/"

                    response_page = session.get(page_url, headers=HEADERS)
                    soup_page = BeautifulSoup(response_page.text, "html.parser")

                    urls = [url.a['href'] for url in soup_page.find_all("h3", class_="jeg_post_title")]

                    data_rows = []
                    for url in urls:
                        response_article = session.get(url, headers=HEADERS)
                        data_page = BeautifulSoup(response_article.text, "html.parser")

                        author = data_page.find("div", class_="jeg_meta_author coauthor")
                        if author is not None:
                            a_author = author.find("a")
                            if a_author is not None:
                                author_text = a_author.get_text(strip=True)
                            else:
                                logger.info("No <a> element found!")
                        # else:
                        #     logger.warning("No div element with class 'jeg_meta_author coauthor' found. Please wait...")

                        published_date = data_page.select_one("div.jeg_meta_date a")
                        published_date = published_date.text.strip() if published_date else ""

                        category = data_page.select_one("div.jeg_meta_category a")
                        category = category.text.strip() if category else ""

                        title = data_page.select_one("h1.jeg_post_title")
                        title = title.text.strip() if title else ""
                        title = unicodedata.normalize("NFKD", title).encode("ASCII", "ignore").decode("utf-8")

                        content = [content.text.strip() for content in
                                   data_page.select("div.content-inner p")]

                        article = Article(
                            title=title,
                            content=' '.join(content),
                            author=author_text,
                            category=category,
                            published_date=published_date,
                            page_url=url,
                        )

                        data_rows.append(asdict(article))

                    # write data
                    writer.writerows(data_rows)
            logger.info(f"All file(s) saved to: {output_dir} successfully!")
            logger.info("Done!")
        except Exception as err:
            logger.error(f"Error: {err}")


# if __name__ == "__main__":
#     three = CitiBusiness(author="citibusinessnews", limit_pages=4)
#     three.download()

# import csv
# import os
# import uuid
# from urllib.parse import unquote
# import requests
# from bs4 import BeautifulSoup
# from utils import SaveFile, HEADERS
# from datetime import datetime
#
#
# class ThreeNews:
#     def __init__(self, author: str):
#
#         self.file_name = str(uuid.uuid4().hex)
#         self.author = author
#         self.url = f"https://3news.com/author/{self.author}/"
#         data = requests.get(self.url)
#         soup = BeautifulSoup(data.content, "html.parser")
#
#         self.last_page = int(soup.find("a", class_="last").text.strip().replace(",", ""))
#
#     def download(self, output_dir=None):
#         """scrape data"""
#         try:
#             print("saving results to csv...")
#             if output_dir is None:
#                 output_dir = os.getcwd()
#                 SaveFile.mkdir(output_dir)
#             if not os.path.isdir(output_dir):
#                 raise ValueError(
#                     f"Invalid output directory: {output_dir} is not a directory"
#                 )
#             print(f"File will be saved to: {output_dir}")
#
#             stamp = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")
#             with open(
#                     os.path.join(output_dir, self.file_name + f"_{stamp}.csv"),
#                     mode="w",
#                     newline="",
#                     encoding="utf-8",
#             ) as csv_file:
#                 fieldnames = ["title", "content", "author", "category", "published_date", "page_url"]
#                 writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#                 writer.writeheader()
#
#                 for page_num in range(1, self.last_page + 1):
#                     url_link = f"{self.url}/page/{page_num}/"
#
#                     data = requests.get(url_link)
#                     soup_page = BeautifulSoup(data.content, "html.parser")
#
#                     # for each page number find all urls:
#                     url = soup_page.find("h3", class_="entry-title td-module-title").find("a")['href']
#
#                     response_page = requests.get(url)
#                     data_page = BeautifulSoup(response_page.text, 'html.parser')
#
#                     # find author
#                     author = data_page.find("div", class_="td-post-author-name").find("a").text.strip()
#                     # find published date
#                     published_date = data_page.find("time", class_="entry-date updated td-module-date").text.strip()
#                     # find entry category
#                     category = data_page.find("li", class_="entry-category").find("a").text.strip()
#                     # find title
#                     title = data_page.find("h1", class_="entry-title").text.strip()
#                     # find content
#                     content = [content.text.strip() for content in
#                                data_page.find("div", class_="td-post-content tagdiv-type").find_all("p")]
#
#                     writer.writerow(
#                         {
#                             "title": title,
#                             "content": content,
#                             "author": author,
#                             "category": category,
#                             "published_date": published_date,
#                             "page_url": url,
#                         }
#                     )
#                 print("Writing data to file...")
#         except Exception as err:
#             print(f"error: {err}")
#
#         print(f"All file(s) saved to: {output_dir} successfully!")
#         print("Done!")
#
#
# if __name__ == '__main__':
#     three = ThreeNews(author="laud-nartey")
#     three.download()
