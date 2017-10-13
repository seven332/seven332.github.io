---
layout: post
title: "Android DateFormat 关于小时的解析"
date: 2015-09-29 15:00
categories: Android
comments: true
---

这是以前写的文章。

这是以前遇到的问题，具体可以在[这里](https://github.com/seven332/EhViewer/issues/16)看到。今天不想做别的事所以又研究了下。我本来是想弄个显示时间的控件，记得 Android 本身就有个 TextClock 就直接拿过来用了。结果这个是 JELLY_BEAN_MR1（API 17） 的时候加入的。为了兼容旧的 Android 本版，我直接把 TextClock 的代码拷贝了一份修改了下就能用了。后来有看到别人发的截图，时间显示的是 HH:什么什么。我当时没有注意。后来有人发个了 issue，我才开始注意这个问题。

JELLY_BEAN_MR1（API 17） TextClock 默认解析格式是

```java
public static final CharSequence DEFAULT_FORMAT_12_HOUR = "h:mm aa";
public static final CharSequence DEFAULT_FORMAT_24_HOUR = "k:mm";
```

JELLY_BEAN_MR2（API 18） TextClock 默认解析格式是

```java
public static final CharSequence DEFAULT_FORMAT_12_HOUR = "h:mm a";
public static final CharSequence DEFAULT_FORMAT_24_HOUR = "H:mm";
```

可以看出来问题是出在 k 与 H 之间，低版本无法解析 H。

具体的解析工作是由 `android.text.format.DateFormat` 完成的。主要函数为 `public static CharSequence format(CharSequence inFormat, Calendar inDate)`。

JELLY_BEAN_MR1（API 17） 相关片段（注释是我自己加的）
```java
case HOUR: // 'h'
    temp = inDate.get(Calendar.HOUR);

    if (0 == temp)
        temp = 12;

    replacement = zeroPad(temp, count);
    break;

case HOUR_OF_DAY: // 'k'
    replacement = zeroPad(inDate.get(Calendar.HOUR_OF_DAY), count);
    break;
```

JELLY_BEAN_MR2（API 18） 相关片段

```java
case 'K': // hour in am/pm (0-11)
case 'h': // hour in am/pm (1-12)
    {
        int hour = inDate.get(Calendar.HOUR);
        if (c == 'h' && hour == 0) {
            hour = 12;
        }
        replacement = zeroPad(hour, count);
    }
    break;
case 'H': // hour in day (0-23)
case 'k': // hour in day (1-24) [but see note below]
    {
        int hour = inDate.get(Calendar.HOUR_OF_DAY);
        // Historically on Android 'k' was interpreted as 'H', which wasn't
        // implemented, so pretty much all callers that want to format 24-hour
        // times are abusing 'k'. http://b/8359981.
        if (false && c == 'k' && hour == 0) {
            hour = 24;
        }
        replacement = zeroPad(hour, count);
    }
    break;
```

由此可见关于小时 JELLY_BEAN_MR2（API 18） 以前是只能解析 h 与 k，其中

    h : 1-12
    k : 0-23

对于 JELLY_BEAN_MR2（API 18） 及以后的本版可以解析h，H，k，K，其中

    h : 1-12
    H : 0-23
    k : 1-24
    K : 0-11

为啥要改成这个样子呢？大概是因为 `java.text.SimpleDateFormat` 也是这个样子吧，具体可以看[这里](http://docs.oracle.com/javase/6/docs/api/java/text/SimpleDateFormat.html)。unicode 也有一样的[标准](http://www.unicode.org/reports/tr35/tr35-dates.html#Date_Format_Patterns)。
