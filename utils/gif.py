import requests
import sys
import os

gif_list=[]

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
            print url
        except:
            pass
        i=i+1

c = sys.argv[1]
get_gif_list(0, c)
