Title: UnsatisfiedLinkError: dlopen failed: has text relocations
Date: 2016-03-08 22:21
Category: Android

有人说 Nimingban 在 Android 6.0 下闪退，我感觉很奇怪，因为我用的就是 Android 6.0，而且使用正常。于是我在 Android 6.0 x86 的虚拟机上跑了下，果然闪退了。错误是这样的

    java.lang.UnsatisfiedLinkError: dlopen failed: xxx.so: has text relocations

搜索了下发现了[这个](http://slowbutdeadly.blogspot.jp/2015/09/javalangunsatisfiedlinkerror-dlopen.html)。根据他的描述，使用最新的 NDK 就可以解决这个问题，而我使用就是最新的 NDK，结果还是在 x86 上出了问题。那么应该是平台问题了。

看看这个问题，说的是 has text relocations，这个问题似乎在以前的 Android 版本中就存在的，不过之前是警告，只有可执行程序在 Android 4.x 之后是视为错误的。以前我也遇到过这个问题，加入 -fPIC 即可。既然说是新版的 NDK 可以自动解决这个问题，-fPIC 应该是成了默认参数。

为何 x86 下还是有这个问题呢？原来是因为 x86 下用了 yasm 编译汇编代码，我用 libjpeg-turbo 解码图片，而 libjpeg-turbo 使用了汇编代码。yasm 怎么启用 PIC 呢？加入 -fPIC 参数会报错。搜索了下发现[这里](http://ffmpeg.org/pipermail/ffmpeg-devel/2009-November/076635.html)有提到 -DPIC，加入后果然好使了。不过 -D 在 yasm 中只不过是加入一个宏，汇编代码中应该会有对应了处理的。粗略看上去似乎是这样的。
