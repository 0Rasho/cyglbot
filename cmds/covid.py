import requests
import json

def get_count(field):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.arcgis.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.arcgis.com/',
        'TE': 'Trailers',
    }

    params = (
        ('f', 'json'),
        ('where', '1=1'),
        ('returnGeometry', 'false'),
        ('spatialRel', 'esriSpatialRelIntersects'),
        ('outFields', '*'),
        ('outStatistics', '[{"statisticType":"sum","onStatisticField":"'+(field)+'","outStatisticFieldName":"value"}]'),
        ('cacheHint', 'true'),
    )
    response = requests.get('https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/1/query', headers=headers, params=params)
    a=json.loads(response.text)
    count=a['features'][0]['attributes']['value']
    return count
class covid(object):
    def _cmd_covid(self, cirno, username, args):
        c=get_count("Confirmed")
        a=get_count("Active")
        d=get_count("Deaths")
        r=get_count("Recovered")
        buf="COVID-19 <-> Confirmed = "+str(c)+" Active = "+str(a)+" Deaths = "+str(d)+" Recovered = "+str(r)
        cirno.sendmsg(buf)

def setup():
    return covid()


