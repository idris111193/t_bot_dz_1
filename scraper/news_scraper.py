import requests
from parsel import Selector


class NewsScraper:
    URL = "https://www.prnewswire.com/news-releases/news-releases-list/"
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0"
    }
    TITLE_XPATH = '//div[@class="col-sm-8 col-lg-9 pull-left card"]/h3/text()'
    IMG_XPATH = '//div[@class="img-ratio-element"]/img/@src'
    DESCRIPTION_XPATH = '//p[@class="remove-outline"]/text()'
    LINK_XPATH = '//a[@class="newsreleaseconsolidatelink display-outline w-100"]/@href'

    def scrape_data(self):
        response = requests.get(self.URL, headers=self.HEADERS)
        tree = Selector(text=response.text)
        titles = tree.xpath(self.TITLE_XPATH).getall()
        images = tree.xpath(self.IMG_XPATH).getall()
        descs = tree.xpath(self.DESCRIPTION_XPATH).getall()
        links = tree.xpath(self.LINK_XPATH).getall()

        for i in descs:
            print(i)
        return links[:5]


if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.scrape_data()