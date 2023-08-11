from setuptools import find_packages, setup

setup(
    name='EstPriceScraper',
    packages=find_packages(where="./src"),
    version='0.1.0',
    description='Python library for scraping Estonian grocery store prices',
    license='GPLv3',
    url='https://github.com/Rig14/price-scraper-est'
)
