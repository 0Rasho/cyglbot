#!/usr/bin/env python
#
# Simple interface to urbandictionary.com
#
# Author: Roman Bogorodskiy <bogorodskiy@gmail.com>

import sys
import random
import requests

if sys.version < '3':
    from urllib import quote as urlquote
    from urllib2 import urlopen
    from HTMLParser import HTMLParser
else:
    from urllib.request import urlopen
    from urllib.parse import quote as urlquote
    from html.parser import HTMLParser


class TermType(object):
    pass


class TermTypeRandom(TermType):
    pass


class UrbanDictParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self._section = None
        self.translations = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag != "div":
            return

        div_class = attrs_dict.get('class')
        if div_class in ('def-header', 'meaning', 'example'):
            self._section = div_class
            if div_class == 'def-header':  # NOTE: assume 'word' is the first section
                self.translations.append(
                    {'word': '', 'def': '', 'example': ''})

    def handle_endtag(self, tag):
        if tag == 'div':
            #NOTE: assume there is no nested <div> in the known sections
            self._section = None

    def handle_data(self, data):
        if not self._section:
            return

        if self._section == 'meaning':
            self._section = 'def'
        elif self._section == 'def-header':
            data = data.strip()
            self._section = 'word'

        self.translations[-1][self._section] += normalize_newlines(data)



def normalize_newlines(text):
    return text.replace('\r\n', ' ').replace('\r', ' ')


def urban_define(term):
        defs=[]
        definition=None
        url = "https://api.urbandictionary.com/v0/define?term=%s" % \
                   urlquote(term)
        response = requests.get(url)
        r = response.json()
        udef = r['list']
        for i in range(len(udef)):
            define=udef[i]['definition']
            defs.append(define)

        if len(defs) > 0:
            random.shuffle(defs)
            definition= defs[random.randint(0, len(defs)-1)]
        return definition.replace('[', '').replace(']', '')

def urban_define_old(term):
        defs=[]
        definition=None
        url = "http://www.urbandictionary.com/define.php?term=%s" % \
                   urlquote(term)
        try:
                f = urlopen(url)
                data = f.read().decode('utf-8')
        except:
                return None

        urbanDictParser = UrbanDictParser()
        urbanDictParser.feed(data)
        
        no_def="There aren't any definitions for"
        for index in range(len(urbanDictParser.translations)):
                        define=urbanDictParser.translations[index]['def'].strip('\n')
                        #if len(define) > 160:
                        #       continue
                        if no_def not in define:
                            defs.append(define)
                        if len(defs) > 0:
                            random.shuffle(defs)
                            definition= defs[random.randint(0, len(defs)-1)]
        return definition
