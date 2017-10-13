---
layout: post
title: "在静态函数中使用匿名类可避免内存泄漏"
date: 2017-05-14 16:27
categories: Java
comments: true
---

虽然 JLS 上说匿名类永远不是静态的，但放到静态函数中的话，他爹实例的引用就不存在了，效果和静态类一样，写起来也方便。
