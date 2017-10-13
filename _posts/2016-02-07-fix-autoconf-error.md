---
layout: post
title: "修正 autoconf 中出现的错误"
date: 2016-02-07 23:34
categories: C/C++
comments: true
---

有时跑 autoconf 会出现类似`error: possibly undefined macro: XXX`的问题。我在[这里](https://bbs.archlinux.org/viewtopic.php?id=161452)看到了解决方法。

    $ libtoolize --force
    $ aclocal
    $ autoheader
    $ automake --force-missing --add-missing
    $ autoconf

这样就好了。
