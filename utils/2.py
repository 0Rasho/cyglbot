import requests
import sys
import os

offset=0
gif_list=[]

file1 = open('cache', 'r')
file1.seek(0, os.SEEK_SET)
elist=[]
for quote in file1:
    quote=quote.strip('\n')
    quote=quote.strip()
    elist.append(quote)
file1.close()

file1 = open('cache', 'a')
def get_gif_list(last_offset, key):
    params = {'q': (key)}
    params['api_key'] = "dc6zaTOxFJmzC"
    params['limit'] = 25
    params['offset'] = last_offset
    resp = requests.get("http://api.giphy.com/v1/gifs/search", params=params)
    k=(resp.json())
    try:
        k= k['data']
    except:
        pass
    i=0
    while i < len(k):
        try:
            url=str(k[i]['images']['fixed_width']['url'].split('?')[0])
            if url not in elist:
                gif_list.append(url)
                file1.write(url)
                file1.write("\n")
        except:
            pass
        i=i+1

c = sys.argv[1]
get_gif_list(0, c)
get_gif_list(25, c)
get_gif_list(50, c)
get_gif_list(75, c)
