---
layout: post
title: "Android Adaptive Icons"
date: 2018-03-21 16:42
categories: Android
comments: true
---

Android O 里有个新的图标格式，叫做 Adaptive Icons。这个 Adaptive Icons 很好得解决了图标形状不一的问题，同时也为一些动画效果提供了前提。

我手上没有 Android O 的机子，所以刚出的时候每太注意，现在弄起来，发现尺寸方面有些需要注意的地方。

[介绍](https://developer.android.com/guide/practices/ui_guidelines/icon_design_adaptive.html)上是这么写的：

In Android 7.1 (API level 25) and earlier, launcher icons were sized at 48 x 48 dp. You must now size your icon layers using the following guidelines:
- Both layers must be sized at 108 x 108 dp.
- The inner 72 x 72 dp of the icon appears within the masked viewport.
- The system reserves the outer 18 dp on each of the 4 sides to create interesting visual effects, such as parallax or pulsing.

开头一句和前两条比较重要。以前的图标是 48 x 48 的，现在前景和背景都要 108 x 108，中间的 72 x 72 是给人看的。其实说得还不够明白。现在 108 x 108 中间那一块 72 x 72 就对应以前的 48 x 48。直接线性变换就行了。至于多出来的那一部分是动画效果需要的。同时考虑到裁剪蒙版形状，72 x 72 的区域也不是完全显示，别都占满了。

不过 Adaptive Icons 是不考虑 padding 的，这与之前的设计标准完全不一样，所以还需要做一些修改。
