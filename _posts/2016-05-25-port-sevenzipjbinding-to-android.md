---
layout: post
title: "移植 7-Zip-JBinding 到 Android"
date: 2016-05-25 19:04
categories: Android
comments: true
---

近期一直在做 7-Zip-JBinding 到 Android 的移植，目前算是完成了。7-Zip-JBinding 对 7-Zip 的封装完成度很高。不过在移植过程中还是遇到过一些问题。

首先是创建 7z 格式压缩文件的时候会出现 native crash。

    JNI DETECTED ERROR IN APPLICATION: use of invalid jobject 0x7f49b9dd

一般来说，`invalid jobject` 是 0x00000000，也就是 `NULL`，不过这里不是，那么就是别的问题。调了下发现是在别的线程里出现的这个问题，那么就应该是没有创建 global references 的问题。加上后就好了。

修改后依然有 native crash，调了下发现是有个 `jclass` 为 `NULL`。为啥 `env->FindClass` 会返回 `NULL` 呢？明明这个 class 是存在的。查了下发现，在非 java 代码里创建的线程通过 `env->FindClass` 只能找到系统自带的 class，因为只用系统的 class loader。那么我就在 java 那边加了 FindClass 的静态函数，使用应用的 class loader 来 `loadClass`，在要调用 `env->FindClass` 的时候就换成调用自己加的 FindClass。这样问题就解决了。

现在基本的压缩和解压都能用了。为了稳妥还是移植下 7-Zip-JBinding 里的 test。遇到的第一个问题就是测试文件的读取。要在 Android 平台上测试就要把测试文件放到 Android 的文件系统里，而 Android API 23 加了个动态权限申请，测试的时候又没办法手动点确定。所以需要把测试文件放到无需申请权限的空间。比较好的方法是把测试文件放到 assets 里，在跑测试前把 assets 里的测试文件拷贝出来。这个时候让人很不愉快的事情发生了，aapt 会自动解压 gz 文件。**我还没测试你就解压，我还个测试什么呢？**只好把所有测试文件打个包，到时候再解压。然后改下测试文件的路径就好了。

测试开始跑了，不一会儿就出现问题了。

    JNI ERROR (app bug): local reference table overflow (max=512)

正如错误本身所说，本地引用表溢出了，想必是缺 `DeleteLocalRef` 了，那么就加上些吧。该加的地方还不少，顺便还发现了些缺 `ReleaseStringUTFChars` 的地方。

还有个问题着实然后头疼了一阵，就是这个。

    JNI DETECTED ERROR IN APPLICATION: the return type of CallObjectMethodV does not match net.sf.sevenzipjbinding.IOutItemBase net.sf.sevenzipjbinding.IOutCreateCallback.getItemInformation(int, net.sf.sevenzipjbinding.impl.OutItemFactory)

这个错误是自相矛盾啊，返回值类型没问题呀。仔细看了下 java 那边的代码，感觉是 `java.reflect.Proxy` 有问题，取消掉后就好了。猜测不能再 jni 里调用 `java.reflect.Proxy`。

遇到的有价值的问题大概就这些。

* [https://developer.android.com/training/articles/perf-jni.html](https://developer.android.com/training/articles/perf-jni.html)
* [http://android-developers.blogspot.com/2011/11/jni-local-reference-changes-in-ics.html](http://android-developers.blogspot.com/2011/11/jni-local-reference-changes-in-ics.html)
