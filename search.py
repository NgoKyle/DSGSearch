import requests
from discord_webhook import DiscordWebhook
from bs4 import BeautifulSoup

s = requests.Session()
s.get("https://www.dickssportinggoods.com/")

proxies = {
  "http": "http://108.59.14.208:13080",
  "https": "http://108.59.14.208:13080"
}

zipcode = []
with open('zipcode.txt','r') as f:
    zipList = f.read().splitlines()

#get SKUs, Products name from URL
links = []
names = []
skus = []
with open('links.txt','r') as f:
    for line in f:
        link = line.strip()
        links.append(link)

        r = requests.get(link)
        bsObj = BeautifulSoup(r.text, 'html.parser')

        name = bsObj.find("h1", {'itemprop':'name'}).text
        names.append(name)

        sku = bsObj.find("ul", {"class":"product-numbers"}).findAll("li")[1].find("span").text
        skus.append(sku)

        print(name, sku, links)

"""
zipList = [
    '97236',
    '98501',
    '97401',
    '99201',
]
"""

while True:
    for zip in zipList:
        for i in range(len(links)):
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
            try:
                r = s.get(url, timeout=7, proxies=proxies, headers=getheaders).json()
                print(r)
            except:
                continue

            print(r)

            if 'data' not in r:
                continue
            if(len(r['data']['results']) == 0):
                continue

            result = r['data']['results'][0]
            location = result['store']['zip']
            addy = r['data']['origin']['geocoded_address']
            sku = result['skus'][0]
            message = "{} \t  zipcode: {}\n{}".format(name, addy, link)
            print(message)
            webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/697209785308807200/N43rRgJLgO-BgXhue9WY3Bs5tFlJTE-m6SXnqjRJRHJ0Qp_xoC0l6h0H5enu3WkaY5rA',
            content=message)
            response = webhook.execute()
