from ghanaweb.scraper import GhanaWeb


urls = ['https://www.ghanaweb.com/GhanaHomePage/politics/',
        'https://www.ghanaweb.com/GhanaHomePage/health/',
        'https://www.ghanaweb.com/GhanaHomePage/crime/',
        'https://www.ghanaweb.com/GhanaHomePage/regional/',
        'https://www.ghanaweb.com/GhanaHomePage/year-in-review/'
    ]

if __name__ == '__main__':
    for url in urls:
        print(f"Downloading data from: {url}")
        web = GhanaWeb(url=url)
        web.download()
