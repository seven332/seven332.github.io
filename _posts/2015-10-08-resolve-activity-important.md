---
layout: post
title: "resolveActivity 的重要性"
date: 2015-10-08 21:18
categories: Android
comments: true
---

在 Android Developers 发的视频 [Protecting Implicit Intents with Runtime Checks (Android Development Patterns Ep 1)](https://www.youtube.com/watch?v=HGElAW224dE) 中看到了自己以前犯过的一个错误，就是没有处理 Implicit Intents 导致的 ActivityNotFoundException 异常。

每当需要用 Implicit Intents 的时候我就会想，用户不可能连这个都没装吧，这是 Android L 的新特性，有系统应用支持肯定不会有问题的。结果都出问题了。可能是用户真的没有安装这类应用，譬如用户用的是模拟器什么类的特殊平台，或者有什么权限的限制。看到错误日志之后，我就直接获取 ActivityNotFoundException，然后忽略。但这并不是一个好的处理方式，因为 ActivityNotFoundException 继承的是 RuntimeException。没有人会不做边界检查直接捕获 IndexOutOfBoundsException。这时候 [resolveActivity](http://developer.android.com/reference/android/content/pm/PackageManager.html#resolveActivity(android.content.Intent, int)) 的重要性就体出来了。只需要调用再看看返回值是否为 null 就行了。
