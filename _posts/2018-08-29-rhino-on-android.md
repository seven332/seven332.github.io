---
layout: post
title: "移植 Rhino 到 Android"
date: 2018-08-29 15:45
categories: Android
comments: true
---

最近我想在 Android 上跑个 JavaScript 的沙盒，效果就和 Node.js 一样，能执行脚本，环境就是在纯 JavaScript 的基础上提供一些的模块。

首先要有个 JavaScript engine。我第一个想到的就是 v8，但是 v8 太大了，而且占空间的是 so 文件，启用 proguard 也没用。

纯 Java 的 JavaScript engine 就是 Rhino 了。至于 Nashorn，是 JDK 的一部分，Android 里又没有，不方便用，所以就不考虑了。让我惊讶的是 Rhino 还一直有人维护，都 20 多年了。从 1.7.8 版开始 Rhino 只支持 Java 8 了，现在 Android API 24 以下的设备还很多，所以修改源码是必须的。

目的就是让 Rhino 的测试在 Android 上全通过，至少我要明白不能通过的原因。

第一个问题是测试文件的读取。Android Test 是远程测试，无法直接读取测试文件，要把所有测试文件打包传到 Android 设备中。所有读取文件的地方还要修改，要修改的地方相当多。

第二个问题是调用了 Java 8 的 API。还好没啥无法用 Java 6 替代的。Animal Sniffer 是个很好的工具，能够找出超纲的 API 调用。至于 Java 8 的 lambda 用的 invokedynamic，D8 会妥善处理的。

第三个问题是 class 的读取。Rhino 在非解释模式下会把 js 的流程逻辑那部分编译成 JVM bytecode，但 Android 不能直接执行 class 文件，要转成 dex 才行。已经有个[项目](https://github.com/F43nd1r/rhino-android)是解决这个问题的。不过我感觉可以直接生成 dex，而非再转换一遍，而且 dex 合并不适合所有项目。直接生成 dex 就麻烦很多了，目前先不考虑。其实性能要求不高的话，用解释模式就行了。

第四个问题是非解释模式下 exception 的 line number 有问题。原因是 bytecode 的生成存在问题，line number table 中有多个 start pc 对应同一个 line number 的问题。JVM 会使用最后一个，而在 class 至 dex 的转换中仅保留第一个。

第五个问题是 Android 中 Math 的行为与 Java 中的不统一。用 StrictMath 替换即可。

第六个问题是 `\u180E` 是否为 Space Separator 的认定。Java 8 支持 Unicode 6.2。那时 `\u180E` 还是 Space Separator。从 Unicode 6.3 开始，`\u180E` 就不是 Space Separator 了。

剩下的都是 E4X（ECMAScript for XML）的问题了。E4X 基本没谁用了，这里也没必要再写了。总之就是 org.apache.harmony.xml 的行为怪异。
