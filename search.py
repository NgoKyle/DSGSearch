import requests
import time
import discord
import multiprocessing
from discord_webhook import DiscordWebhook
from bs4 import BeautifulSoup

zipcode = []
with open('zipcode.txt','r') as f:
    zipList = f.read().splitlines()

#get SKUs, Products name from URL
links = []
names = []
skus = []
with open('links.txt','r') as f:
    for line in f:
        try:
            link = line.strip()

            r = requests.get(link)
            bsObj = BeautifulSoup(r.text, 'html.parser')

            name = bsObj.find("h1", {'itemprop':'name'}).text

            sku = bsObj.find("ul", {"class":"product-numbers"}).findAll("li")[1].find("span").text

            names.append(name)
            links.append(link)
            skus.append(sku)

            #print(name, sku, link)
        except:
            continue

    links.append("https://www.dickssportinggoods.com/p/bowflex-selecttech-552-dumbbells-16bfxuslcttchdmbbslc/16bfxuslcttchdmbbslc")
    names.append("Bowflex selecttech 552")
    skus.append("11465449")

def parseLocation(sets, name, link, sku, result, zip):
    qty = result['skus'][0]['qty']
    ats = qty['ats']

    if(int(ats) > 0):
        zipcode = result['store']['zip']
        street = result['store']['street1']
        city = result['store']['city']
        state = result['store']['state']
        loc = result['store']['location']

        key = street + sku + ats
        #print("key: " + key)
        if key in sets:
            #print("key in set")
            return
        sets.add(key)

        backdoor = """
        fetch("https://www.dickssportinggoods.com/AjaxRESTOrderItemAdd", {
            "headers": {
                "accept": "/",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/x-www-form-urlencoded",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-auth-cookie-required": "true"
            },
            "referrer": "https://www.dickssportinggoods.com/p/bowflex-selecttech-552-dumbbells-16bfxuslcttchdmbbslc/16bfxuslcttchdmbbslc",
            "referrerPolicy": "no-referrer-when-downgrade",
            "body": "storeId=15108&catalogId=12301&langId=-1&orderId=.&addtocart=Y&calculateOrder=0&catEntryId=1294213&quantity=1&warCatEntry=false&partNumber=11465449&requesttype=ajax&inventoryValidation=false&bopisStLocId="""+loc+"""&bopisItem=Y",
            "method": "POST",
            "mode": "cors",
            "credentials": "include"
        });
        """
        message = time.strftime('%a %H:%M:%S') + "\t{}{}\nStreet: {}\nLocation: {}, {} \t zipcode: {}\t bopisStLocId: {}\n{}".format(name, str(qty), street, city, state, zipcode, loc, link)
        print(message)

        if skus[i] in '11465449':
            discord.sendDiscord(message, 'curbside', skus[i], 'bowflex')
        else:
            discord.sendDiscord(message, 'curbside', skus[i], 'everywhere')

def worker(i):
    sets = set()
    while True:
        for zip in zipList:
            sku = skus[i]
            name = names[i]
            link = links[i]

            #for sku, name in skus.items():
            url = 'https://availability.dickssportinggoods.com/ws/v2/omni/stores?addr={}&radius=100&uom=imperial&lob=dsg&sku={}&res=locatorsearch&qty=1'.format(zip, sku)
            getheaders = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0', 'if-modified-since': 'Fri, 05 Jan 2018 11',
                'if-none-match': '"42f-562062e8ef580-gzip"', 'upgrade-insecure-requests': '1',
                'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
            }

            proxy = {
              "http": "http://108.59.14.203:13010",
              "https": "http://108.59.14.203:13010",
            }

            try:
                r = requests.get(url, timeout=7, proxies=proxy, headers=getheaders).json()
                print(zip, r)
            except:
                continue

            if 'data' not in r:
                continue
            if(len(r['data']['results']) == 0):
                continue

            result = r['data']['results']
            for j in range(len(result)):
                parseLocation(sets, name, link, sku, result[j], zip)


for i in range(len(links)):
    p1 = multiprocessing.Process(target=worker, args=(i,))
    p1.start()
