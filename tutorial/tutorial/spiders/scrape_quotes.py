import scrapy


class ScrapeQuotesSpider(scrapy.Spider):
    name = 'scrape_quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        # total_quotes_in_page = len(response.xpath('//span[contains(@class, "text")]/text()'))

        for quote in response.xpath('//div[contains(@class, "quote")]'):
            yield {
                'quote':  response.xpath('span[contains(@class, "text")]/text()').get(),
                'author': response.xpath('small[contains(@class, "author")]/text()').get()
            }

        next_page = response.xpath('//a[contains(text(), "Next")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    custom_settings = {
        'FEED_URI': 'quotes.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {
            'csv': 'scrapy.exporters.CsvItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }


