import requests
from flask import json
from bs4 import BeautifulSoup
from urllib import parse
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


class SteamSearch(Resource):
    def put(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('query', required=True,
                            help='A search term needs to be provided')
        parser.add_argument('brand', required=True,
                            help='A search term needs to be provided')                    
        
        args = parser.parse_args()

        product = parse.urlencode({'query': args.query})
        brand=(parse.urlencode({'brand':args.brand})).split("=")[1]
        find=product+'+'+brand
        print(find)
        

        
           
        r = requests.get(f'https://www.walmart.com/search/?{find}')
        
        
        
        results = []
        # just get the code, no headers or anything
        plain_text = r.text.encode('ascii', 'replace')
        # BeautifulSoup objects can be sorted through easy
        soup = BeautifulSoup(plain_text,'html.parser')
        for link in soup.findAll('a', {'class': 'product-title-link line-clamp line-clamp-2'}):
            href =[]
            href.append("https://www.walmart.com"+link.get('href'))
            print(href)
       
            
            for url in href:
                
                source_code = requests.get(url)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text,"lxml")
                for item_name in soup.findAll('h1', {'class': 'prod-ProductTitle font-normal'}):
                                     title=item_name.string
                for brand_name in soup.findAll('a',{'class':'prod-brandName'}):
                                     brand=brand_name.string
                for ratings in soup.findAll('span',{'itemprop':'ratingValue'}):
                                     rating=ratings.string
                for p1 in soup.findAll('span',{'class':'price-currency'}):
                                    p11=p1.string
                for p2 in soup.findAll('span',{'class':'price-characteristic'}):
                                    p22=p2.string
                for p3 in soup.findAll('span',{'class':'price-mark'}):
                                     p33=p3.string
                for p4 in soup.findAll('span',{'class':'price-mantissa'}):
                                     
                                     p44=p4.string
                price=p11+p22+p33+p44
                for desc in soup.findAll('div',{'class':'about-desc'}):
                    description=[]

                    description.append(desc.find('ul').findAll('li').text)

                print(title,price,brand,rating)                     
            results.append({'title':title,
                           'brand':brand,
                           'rating':rating,
                          'price':price,
                          'description':description})
        return results
    

       
       
    
        
          


api.add_resource(SteamSearch, '/query')

if __name__ == '__main__':
    app.run(debug=True)
