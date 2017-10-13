---
layout: post
title: "自然排序"
date: 2017-09-25 11:30
categories: Algorithm
comments: true
---

# 怎么排序

有一个文件夹，里面有一堆图片，漫画浏览器需要知道哪个是第一张，哪个是第二张，对于压缩包也是这样。这就是个排序问题。

我用的方法就是直接`Arrays.sort(array)`或者`Collections.sort(list)`，也就是直接使用 String 中 char 的值来进行排序。

在图片命名即为规范的情况下，这是没有问题的。譬如：

    0001.jpg
    0002.jpg
    0003.jpg

然而在其他情况下就会出问题。譬如：

    nazo-no-kanojo-ekkusu-1.jpg
    nazo-no-kanojo-ekkusu-11.jpg
    nazo-no-kanojo-ekkusu-2.jpg

显然，`nazo-no-kanojo-ekkusu-2.jpg`应该排在`nazo-no-kanojo-ekkusu-11.jpg`前面的，而该排序算法做不到这点。问题出在了数字部分的比较。用户不可能按照理想情况，来对数字用零填充，使所有数字位数相同。那么需要对字符串中的数字部分单独处理。

# 自然排序

Windows Explorer 文件排序的默认效果符合我的期望。Microsoft 官方称其为 `Numerical Sorting`。然而网络中常见的称呼是 `Natural Sorting`，姑且称之为`自然排序`。其实现方法也很简介，首先将字符串切分，分为全数字字符串与其他，再各部分一一对应比较，若皆为全数字字符串，则比较其值，否则按字符比较。

# Java 实现

StackOverflow 上 wumpz 给出了一种[实现方法](https://stackoverflow.com/a/23249000)。这个实现方法相比之前的描述要丰富了许多，譬如加入了对`空格`与`.`的特殊处理。不过还是有几处值得优化的地方。

1. 切分字符串时还应排除空字符串
2. 切分字符串没必要一次性完成，而是可以边切分边比较
3. 切分字符串较为简单，不必使用正则表达式
4. 数字字符串的判断不要利用异常判断

将其优化之后的代码是这样的：

<script src="https://gist.github.com/seven332/eadc44f1b35f756e46c410a8487fcc1d.js"></script>

# 缺陷

在某些情况自然排序也会导致糟糕的排序，譬如文件名中有小数，或者十六进制数。

# 参考

[https://technet.microsoft.com/en-us/library/hh475812.aspx](https://technet.microsoft.com/en-us/library/hh475812.aspx)
[http://www.interact-sw.co.uk/iangblog/2007/12/13/natural-sorting](http://www.interact-sw.co.uk/iangblog/2007/12/13/natural-sorting)
[https://stackoverflow.com/questions/23205020/java-sort-strings-like-windows-explorer](https://stackoverflow.com/questions/23205020/java-sort-strings-like-windows-explorer)
