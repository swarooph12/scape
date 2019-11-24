import scrapy
import requests
from ..items import Mobile

class AmazonScraper(scrapy.Spider):
    name = "amazon_scraper"

    def __init__(self, category='', **kwargs):
        self.start_urls = [f'https://www.amazon.com/s?k={category}&ref=nb_sb_noss']  # py36
        super().__init__(**kwargs)

    # How many pages you want to scrape
    no_of_pages = 1

    # Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser ;)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36'}

    def start_requests(self):
        # starting urls for scraping
        urls = self.start_urls

        for url in urls: yield scrapy.Request(url = url, callback = self.parse, headers = self.headers)
    def check_response(response):
        if response.body != '':
            return response
        else:
            return Request(copy_of_response.request,callback=check_response,dont_filter=True)    

    def parse(self, response):

        self.no_of_pages -= 1
        

        print(response.text)

        
        mobiles=response.xpath("//a[@class='a-link-normal a-text-normal']").xpath("@href").getall()
        # print(len(mobiles))

        for mobile in mobiles:
            try:
                final_url = response.urljoin(mobile)
            except AttributeError:
                
                yield scrapy.Request(url=final_url, callback = self.parse_mobile, headers = self.headers,)
            # break
            # print(final_url)

        # print(response.body)
        # title = response.xpath("//span[@class='a-size-medium a-color-base a-text-normal']//text()").getall()
        # title = response.css('span').getall()
        # print(title)
        
        if(self.no_of_pages > 0):
            next_page_url = response.xpath("//ul[@class='a-pagination']/li[@class='a-last']/a").xpath("@href").get()
            final_url = response.urljoin(next_page_url)
            yield scrapy.Request(url = final_url, callback = self.parse, headers = self.headers)

    def parse_mobile(self, response):
        title = response.xpath("//span[@id='productTitle']//text()").get() or response.xpath("//h1[@id='title']//text()").get()
        brand = response.xpath("//a[@id='bylineInfo']//text()").get() or "not specified"
        rating = response.xpath("//div[@id='averageCustomerReviews_feature_div']").xpath("//span[@class='a-icon-alt']//text()").get()

        price = response.xpath("//span[@id='priceblock_ourprice']//text()") or response.xpath("//span[@id='priceblock_dealprice']//text()")
        print(price)
        if len(price) > 1: price = price[1].get()
        elif len(price) == 1: price = price[0].get()
        else : price = price.get()

        colour = response.xpath("//div[@id='variation_color_name']/div/span[@class='selection']//text()").get() or "not defined"
        instock = response.xpath("//div[@id='availability']").xpath("//span[@class='a-size-medium a-color-success']//text()").get() or "Out Stock"
        instock = instock.strip() == "In stock."
        reviews = response.xpath("//div[@class='a-expander-content reviewText review-text-content a-expander-partial-collapse-content']/span//text()").getall()
        description_raw = response.xpath("//div[@id='featurebullets_feature_div']//span[@class='a-list-item']//text()").getall()

        img_url = response.xpath("//img[@id='landingImage']/@data-old-hires").get() or response.xpath("//img[@id='imgBlkFront']/@src").get()

        description = []
        for description_temp in description_raw:
            description.append(description_temp.strip())

        print(title, brand, rating, price, colour, instock, img_url)
        # print(final_review)
        # print(reviews)
        # print(description)

        yield Mobile(title = title.strip(), brand = brand.strip(), rating = rating.strip(), price = price.strip(), colour = colour.strip(), instock = instock, reviews = reviews, description = description, image_urls = [img_url])