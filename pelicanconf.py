#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Hippo'
SITENAME = u"Hippo's Blog"
SITEURL = 'http://seven332.github.io'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

DEFAULT_DATE_FORMAT = '%y-%m-%d %H %a'

DEFAULT_CATEGORY = u'无'

THEME = "./theme"

# Plugin
PLUGIN_PATHS = ('./plugins',)
PLUGINS = ('minify',)

# Comments
DISQUS_SITENAME = "seven332"

# Feed generation is usually not desired when developing
FEED_RSS = None
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = None
AUTHOR_FEED_RSS = None
TAG_FEED_RSS = None
TRANSLATION_FEED_RSS = None

FEED_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
TAG_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = ((u'无', '#'),)

# Social widget
SOCIAL = (('github', 'http://github.com/seven332'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
