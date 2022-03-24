import urllib
import random
import sys
mfc_url_pcs="https://www.myfreecams.com/mfc2/php/ParseChatStream.php?"
args=sys.argv[1]
e_http=mfc_url_pcs+"a0="+str(args)+"&"+"&"+str(random.random())
response=urllib.urlopen(e_http).read()
response=response.strip('[{')
response=response.strip('}]')
emote = dict(response.split(':"') for response in response.split(',"'))
url=str(emote['url"'])
url=url.replace('\\','').strip('"')
print url

