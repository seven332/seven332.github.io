Title: Activity.isFinishing()
Date: 2016-09-22 01:35
Category: Android

`Activity.isFinishing()` 挺有用的，可以在 `onDestroy()` 里来判断 Activity 是真的要关闭还是只是要重新创建，方便资源释放。之前没想到这个，用了麻烦的方法来实现功能，翻源码才想起了这个。
