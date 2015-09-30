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
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ((u'无', '#'),)

# Social widget
SOCIAL = ((u'无', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
