Title: ValueAnimator.pause() 内存泄漏
Date: 2016-01-18 12:04
Category: Android

ValueAnimator.pause() 在 API 19 引入，若不正确使用会导致严重内存泄漏。

以前有些使用 ValueAnimator.stop() 的地方在 API 19 及以后可以使用 ValueAnimator.pause() 替代来达到更好的效果。但是若在调用 ValueAnimator.pause() 之后就放弃了 ValueAnimator 实例的话，这个 ValueAnimator 实例会一直被 ValueAnimator.AnimationHandler 占有，从而导致内存泄漏。
