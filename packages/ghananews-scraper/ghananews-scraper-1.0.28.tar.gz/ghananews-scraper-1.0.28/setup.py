from setuptools import setup, find_packages

with open("README.md") as f:
    README = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name="ghananews-scraper",
    py_modules=[
        "ghanaweb",
        "myjoyonline",
        "graphiconline",
        "yen",
        "citionline",
        "mynewsgh",
        "threenews",
        "pulsegh",
    ],
    version="1.0.28",
    packages=find_packages(exclude=["docs", "tests", "tests.*"]),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/donwany/ghananews-scraper",
    license="MIT License",
    author="Theophilus Siameh",
    author_email="theodondre@gmail.com",
    install_requires=install_requires,
    description="A python package to scrape data from Ghana News Portals",
    classifiers=[
        # See https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
    keywords="Scraper, Data, GhanaNews, GhanaWeb, JoyNews, MyJoyOnline, News, Yen, MyNewsGh, ThreeNews, Web Scraper, Ghana Scraper",
    platforms=["any"],
    python_requires=">=3.7",
)
