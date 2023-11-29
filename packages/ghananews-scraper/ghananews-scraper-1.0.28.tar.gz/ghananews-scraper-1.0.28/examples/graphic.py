from graphiconline.scraper import GraphicOnline

urls = [
    "https://www.graphic.com.gh/news.html"
]

if __name__ == '__main__':

    for url in urls:
        print(f"Downloading data from: {url}")
        graphic = GraphicOnline(url=url)
        graphic.download()
