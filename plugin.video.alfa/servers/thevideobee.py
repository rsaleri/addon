# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Conector thevideobee By Alfa development Group
# --------------------------------------------------------

from core import httptools
from core import scrapertools
from platformcode import logger


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data
    if "no longer exists" in data or "to copyright issues" in data:
        return False, "[thevideobee] El video ha sido borrado"
    return True, ""


def get_video_url(page_url, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data
    video_urls = []
    videourl = scrapertools.find_single_match(data, 'src: "([^"]+)')
    video_urls.append([".MP4 [thevideobee]", videourl])

    return video_urls
