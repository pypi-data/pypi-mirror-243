# Option 1.
from myjoyonline.scrapy import MyJoyOnlineNews

if __name__ == '__main__':
    url = 'https://myjoyonline.com/politics'
    print(f"Downloading data from: {url}")
    joy = MyJoyOnlineNews(url=url)
    joy.download()
