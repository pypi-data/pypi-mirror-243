from citionline.scraper import CitiBusinessOnline

urls = [
    "https://citibusinessnews.com/ghanabusinessnews/features/",
    "https://citibusinessnews.com/ghanabusinessnews/telecoms-technology/",
    "https://citibusinessnews.com/ghanabusinessnews/international/",
    "https://citibusinessnews.com/ghanabusinessnews/news/government/",
    "https://citibusinessnews.com/ghanabusinessnews/news/",
    "https://citibusinessnews.com/ghanabusinessnews/business/",
    "https://citibusinessnews.com/ghanabusinessnews/news/economy/",
    "https://citibusinessnews.com/ghanabusinessnews/news/general/",
    "https://citibusinessnews.com/ghanabusinessnews/news/top-stories/",
    "https://citibusinessnews.com/ghanabusinessnews/business/tourism/"
]

if __name__ == '__main__':

    for url in urls:
        print(f"Downloading data from: {url}")
        citi = CitiBusinessOnline(url=url)
        citi.download()
