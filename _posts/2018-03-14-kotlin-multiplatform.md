---
layout: post
title: "尝试 Kotlin Multiplatform Projects"
date: 2018-03-14 12:48
categories: Kotlin
comments: true
---

Kotlin 的 Multiplatform Projects 看起来是个挺不错的跨平台技术。能 JVM 能 JS 还能 Native。不过真正要弄起来还是会遇到些问题的。

介绍在[这里](https://kotlinlang.org/docs/reference/multiplatform.html)，照着写一遍也不会遇到什么问题。简单来说就是 common 模块里出现 expect 关键字的声明，都要在所有的 platform 模块里实现并加上 actual 关键字。

遇到的第一个问题是 coroutines 在 Kotlin/JS 上的测试。目前 kotlin coroutines 的教程上讲的都是用`runBlocking`来包住测试代码块。

```kotlin
@Test
fun test() = runBlocking<Unit> {
    // ...
}
```

但是 Kotlin/JS 现在没有`runBlocking`了。有篇[博客](https://blog.kotlin-academy.com/testing-common-modules-66b39d641617)介绍了一种方法，用`promise`来包住测试代码块。

```kotlin
@Test
fun test() = promise {
    // ...
}
```

不过这个解决方法还是有些局限性的。若是需要`onBefore`或者`onAfter`的话，还要自行加入锁机制，保证运行顺序。

另外一个问题就是如何在浏览器上测试生成的 js 代码。官方给出的[示例](https://github.com/JetBrains/kotlin-examples/tree/master/gradle/js-tests)是 node.js 来测试的。在浏览器测试的话就应该用 headless browser 了。搜索了一番发现 mocha-headless-chrome 可以用。那么解决方法就是生成测试入口 html，再调用 mocha-headless-chrome 来载入这个 html。

所用的代码都可以再[这里](https://github.com/ehviewer-team/ehviewer-core)找到。
