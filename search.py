import requests

s = requests.Session()
s.get("https://www.dickssportinggoods.com/")

zipcode = []

with open('zipcode.txt','r') as f:
    zipList = f.read().splitlines()

for zip in zipList:
    sku = '10836482'
    url = 'https://availability.dickssportinggoods.com/ws/v2/omni/stores?addr={}&radius=100&uom=imperial&lob=dsg&sku={}&res=locatorsearch&qty=1'.format(zip, sku)
    getheaders = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0', 'if-modified-since': 'Fri, 05 Jan 2018 11',
        'if-none-match': '"42f-562062e8ef580-gzip"', 'upgrade-insecure-requests': '1',
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    r = s.get(url, timeout=6, headers=getheaders).json()

    if 'data' not in r:
        continue
    if(len(r['data']['results']) == 0):
        continue

    result = r['data']['results'][0]
    location = result['store']['zip']
    sku = result['skus'][0]
    print("zipcode: " + location, sku)
