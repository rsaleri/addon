# -*- coding: utf-8 -*-

import re
import urlparse

from core import httptools
from core import servertools
from core import scrapertools
from core.item import Item
from platformcode import logger
import base64

server = {'1': 'https://www.mangovideo.pw/contents/videos/', '7' : 'https://server9.mangovideo.pw/contents/videos/',
          '8' : 'https://s10.mangovideo.pw/contents/videos/', '9' : 'https://server2.mangovideo.pw/contents/videos/',
          '10' : 'https://server217.mangovideo.pw/contents/videos/', '11' : 'https://234.mangovideo.pw/contents/videos/',
          '12' : 'https://98.mangovideo.pw/contents/videos/'
         }


host = "https://watchfreexxx.net/"

def mainlist(item):
    itemlist = []

    itemlist.append(Item(channel=item.channel, title="Peliculas", action="lista",
                         url = urlparse.urljoin(host, "category/porn-movies/")))

    itemlist.append(Item(channel=item.channel, title="Escenas", action="lista",
                         url = urlparse.urljoin(host, "category/xxx-scenes/")))

    itemlist.append(Item(channel=item.channel, title="Buscar", action="search", url=host+'?s=',
                         thumbnail='https://s30.postimg.cc/pei7txpa9/buscar.png',
                         fanart='https://s30.postimg.cc/pei7txpa9/buscar.png'))

    return itemlist


def search(item, texto):
    logger.info()
    texto = texto.replace(" ", "+")
    item.url = item.url + texto
    try:
        if texto != '':
            item.extra = 'Buscar'
            return lista(item)
        else:
            return []
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def lista(item):
    logger.info()
    itemlist = []
    if item.url == '': item.url = host
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    patron = '<article id=.*?<a href="([^"]+)".*?<img data-src="([^"]+)" alt="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for data_1, data_2, data_3 in matches:
        url = data_1
        thumbnail = data_2
        title = data_3
        itemlist.append(Item(channel=item.channel, action='findvideos', title=title, url=url, thumbnail=thumbnail))
    #Paginacion
    if itemlist != []:
        actual_page_url = item.url
        next_page = scrapertools.find_single_match(data, '<a href="([^"]+)">Next</a>')
        if next_page != '':
            itemlist.append(Item(channel=item.channel, action="lista", title='Siguiente >>>', url=next_page,
                                 thumbnail='https://s16.postimg.cc/9okdu7hhx/siguiente.png', extra=item.extra))
    return itemlist


def findvideos(item):
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|amp;|\s{2}|&nbsp;", "", data)
    patron = '- on ([^"]+)" href="([^"]+)"'
    matches = scrapertools.find_multiple_matches(data, patron)
    for scrapedtitle,url in matches:
        if "tk/goto/" in url:
            n = 3
            while n > 0:
                url= url.replace("https://vshares.tk/goto/", "").replace("https://waaws.tk/goto/", "").replace("https://openloads.tk/goto/", "")
                url = base64.b64decode(url)
                n -= 1
        itemlist.append(item.clone(action="play", title ="%s", fulltitle=item.title, url=url ))
    itemlist = servertools.get_servers_itemlist(itemlist, lambda i: i.title % i.server.capitalize())
    return itemlist


