
# [ Edited On 16.2.2016 ] 
# On that date this program was working. 

#Warning: For original Bucky's typed lines of code, take a look at the file 27_python.py .

#Description:
#This file is alternative solution for web crowler. 
# Mayor reason for this is that website BuckysRoom.com is down, so original code doesnot work anymore. 
# Solution description (what this program does):
#This program goes on website https://www.thenewboston.com/search.php?type=0&sort=reputation ,
#and goes on every user's profile, and on that profile, 
#it prints the first few (approx. 20) links of latest photos. To view photos, click on url or copy in web broser.


# But history is changing and sooner or later this file or program will not work!. 
# On day of the creation this program was working. 





import requests
from bs4 import BeautifulSoup


def trade_spider(max_pages):
    page = 1
    while page <= max_pages:
        url = 'https://www.walmart.com/search/?page='+str(page)+'&ps=40&query=laptop+hp'
        source_code = requests.get(url, allow_redirects=False)
        # just get the code, no headers or anything
        plain_text = source_code.text.encode('ascii', 'replace')
        # BeautifulSoup objects can be sorted through easy
        soup = BeautifulSoup(plain_text,'html.parser')
        for link in soup.findAll('a', {'class': 'product-title-link line-clamp line-clamp-2'}):
            href = "https://www.walmart.com"+link.get('href')
            #title = link.string  # just the text, not the HTML
            print(href)
            #print(title)
            get_single_item_data(href)
        page += 1


def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,"lxml")#
    # if you want to gather photos from that user
    for item_name in soup.findAll('h1', {'class': 'prod-ProductTitle font-normal'}): # all photos of the user
        title=item_name.string
        print(title)
    for brand_name in soup.findAll('a',{'class':'prod-brandName'}):
        brand=brand_name.string
        print(brand)
    for ratings in soup.findAll('span',{'itemprop':'ratingValue'}):
        rating=ratings.string
        print(rating)
    for p1 in soup.findAll('span',{'class':'price-currency'}):
        p11=p1.string
    for p2 in soup.findAll('span',{'class':'price-characteristic'}):
        p22=p2.string
    for p3 in soup.findAll('span',{'class':'price-mark'}):
        p33=p3.string
    for p4 in soup.findAll('span',{'class':'price-mantissa'}):
        p44=p4.string
    price=p11+p22+p33+p44
    print(price)

    
'''
    for spec in soup.findAll('table',{'class':'table table-striped-odd specification'}):
        specification=spec.string
        print(specification)    
        
    # if you want to gather links for a web crawler
    for link in soup.findAll('a'):
        href = link.get('href')
        print(href)
    for title in soup.findAll('h1',{'class':'prod-ProductTitle font-normal'}):
        name=title.string
        print(name)
'''

trade_spider(2)




