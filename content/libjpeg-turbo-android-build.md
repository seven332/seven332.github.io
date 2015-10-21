Title: Android 下编译 libjpeg-turbo
Date: 2015-10-21 23:47
Category: Android

以前就移植过 libjpeg-turbo，这次又下载了最新的源码重新移植了一遍，发现在以前移植过程中有不好的做法，同时也出现了新的问题。

源码可以在[这里](https://github.com/seven332/seven332.github.io)找到。

移植的过程基本就是把 Makefile 转为 Android.mk 的过程，当然其中会出现不少问题。同时所需要的只有解码部分，所以要把编码部分的源码剔除。

libjpeg-turbo 与 libjpeg 最大的区别在于 libjpeg-turbo 有不少汇编代码。Android 也是有多个硬件平台，可以与其汇编代码对应起来。具体各个平台需要哪些源码直接看[这里](https://github.com/seven332/libjpeg-turbo/blob/master/Android.mk)好了，值得注意的是并不所有的 Android 硬件平台 libjpeg-turbo 都提供了汇编代码，对于那些没有被照顾到的硬件平台就添加 jsimd_none.c 文件。

接下来是遇到的问题，x86_64 编译会出现问题

    ***/jni/libjpeg-turbo/simd/jccolext-sse2-64.asm:50: error: redefinition of `collect_args'
    ***/jni/libjpeg-turbo/simd/jccolext-sse2-64.asm:50: error: `collect_args' previously defined here
    ***/jni/libjpeg-turbo/simd/jccolext-sse2-64.asm:74: error: redefinition of `collect_args.rowloop'
    ***/jni/libjpeg-turbo/simd/jccolext-sse2-64.asm:74: error: `collect_args.rowloop' previously defined here
    ***/jni/libjpeg-turbo/simd/jccolext-sse2-64.asm:91: error: redefinition of `collect_args.column_ld1'
    ***/jni/libjpeg-turbo/simd/jccolext-sse2-64.asm:91: error: `collect_args.column_ld1' previously defined here
    ...
    make.exe: *** [E:/JetBrains/Projects/CLionProjects/Image/libimage/obj/local/x86_64/objs-debug/jpeg-turbo/simd/jccolor-sse2-64.o] Error 1

中间省略了一些，反正是类似的错误。印象中上次移植并没有遇到这个问题，难道是作者更新了源码导致的错误？上次移植用的是 Android NDK r10d，x86_64 还不能自动识别 asm，我只好修改了下 build-binary.mk。我把以前修改 build-binary.mk 的[记录](https://github.com/seven332/EhViewer/blob/dev/README.md)翻了出来。与默认的编译命令相比多了 `-m amd64 -DELF -D__x86_64__ -DPIC`，想必是这些参数使得编译成功。到底是哪个呢，一个个试就知道了。结果是 -D__x86_64__。在 jsimdext.inc 中也可以看到。

然后就是链接问题了

    ***/jni/libjpeg-turbo/simd/jsimd_x86_64.c:43: error: undefined reference to 'jconst_rgb_ycc_convert_sse2'
    ***/jni/libjpeg-turbo/simd/jsimd_x86_64.c:60: error: undefined reference to 'jconst_rgb_gray_convert_sse2'
    ***/jni/libjpeg-turbo/simd/jsimd_x86_64.c:77: error: undefined reference to 'jconst_ycc_rgb_convert_sse2'
    ***/jni/libjpeg-turbo/simd/jsimd_x86_64.c:98: error: undefined reference to 'jsimd_extrgb_ycc_convert_sse2'
    ...
    collect2.exe: error: ld returned 1 exit status
    make.exe: *** [E:/JetBrains/Projects/CLionProjects/Image/libimage/obj/local/x86_64/libjpeg-turbo.so] Error 1

这个问题上次就出现过，我直接把 `%define EXTN(name)   _ %+ name` 改成了 `%define EXTN(name)  name`，然而这并不是一个好办法。通过看 jsimdext.inc 的源码可以知道，分明缺的是 ELF 这个宏，所以加上 `-DELF` 就好了。

然后就顺利编译完成了。可是在手机里显示的图像却是错误的。这令我颇不愉快。莫非我的代码写得有问题？我又把代码放到 Windows 上跑一遍，没有问题。那么应该就是 arm 上的汇编代码写得有问题，我又取消了 simd 重新编译，可是在手机上跑还是解码有问题。那么可能是版本问题，我把版本号降到了之前编译的版本 1.4.0，再编译一遍，可以正常解码。换到 1.4.1，解码错误。为何会这样呢？作者没发现这个问题，还是我在移植过程中出了什么错误呢？直接看看 1.4.1 都有啥变动吧。

    git diff 1.4.0 1.4.1

有这么两行

    -#if __WORDSIZE == 64 || defined(_WIN64)
    +#if SIZEOF_SIZE_T==8 || defined(_WIN64)

SIZEOF_SIZE_T 这是个宏，是 jconfig.h 里的，`#define SIZEOF_SIZE_T 8`。jconfig.h 是直接 `./configure` 跑出来的，PC 系统是 64 位，size_t 大小是 8，而手机系统是 32 位，size_t 大小是 4，所以很可能是这里除了问题。怎么办呢？又不能直接换成 `sizeof(size_t)`。还是通过判断是 64 位还是 32 位来决定吧，虽然不能保证一定是正确的。看看 gcc 有没有什么特殊的预设宏。查看的方法在[这里](http://nadeausoftware.com/articles/2011/12/c_c_tip_how_list_compiler_predefined_macros)，需要注意的是 Windows 下没有 `/dev/null`，直接换成随便一个文件名。预设宏很多啊，突然看到原来就有 `__SIZEOF_SIZE_T__` 这个宏。直接就可以改成 `#define SIZEOF_SIZE_T __SIZEOF_SIZE_T__`。

如此一来算是完成了 libjpeg-turbo 到 Android 的移植。不过还可以做些修改让 libjpeg-turbo 在 Android 上运行的更好。

首先是 arm 上 neon 的判断，可以直接调用 cpufeatures，具体可参照[这里](https://github.com/seven332/libjpeg-turbo/commit/b1bef0d986397a1ee1019e610f5e9d4c28a316c2)。

Android L 引入了新的文件机制，有时需要通过这种文件机制来读取图片。而 libjpeg-turbo 仅提供了 FILE\* 读取和内存读取两种方法。想要通过 Android 新的文件机制来读取就只能先完全把图片文件读取到内存里。这似乎并不是个好主意，这有些浪费内存的感觉。好的解决方法是添加一种自定义的读取方式，就像 libpng 和 giflib 那样。修改起来也很简单，基本就是在 FILE* 读取方法上稍作修改就好了。具体可参照[这里](https://github.com/seven332/libjpeg-turbo/commit/efa06eed172cf6ae2c394d51e2ea119a329e4d92)。
