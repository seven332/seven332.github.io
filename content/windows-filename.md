Title: Windows 文件名限制
Date: 2017-10-10 10:47
Category: Windows

如果要在 Windows 下创建文件，或者可能将在其他操作系统下创建的文件拷贝至 Windows，就需要考虑 Windows 的文件名限制。否则程序会出错，用户会不高兴。

# 文件夹与文件

文件夹就是文件，所以两者的限制是一样的。

# 限制

1. 保留字符

    1. \< （小于）
    2. \> （大于）
    3. \: （冒号）
    4. \" （引号）
    5. \/ （斜杠）
    6. \\ （反斜杠）
    7. \| （束杠）
    8. \? （问号）
    9. \* （星号）

2. 值为 0~31 的字符不可出现。似乎某些字符是允许出现的，不过目前我无法确实有哪些，并且是否在所有流行的 Windows 版本中都适用。谨慎些的话，可以把这些都排除了。

3. `CON`，`PRN`，`AUX`，`NUL`，`COM1`，`COM2`，`COM3`，`COM4`，`COM5`，`COM6`，`COM7`，`COM8`，`COM9`，`LPT1`，`LPT2`，`LPT3`，`LPT4`，`LPT5`，`LPT6`，`LPT7`，`LPT8`和`LPT9`都不可作为文件的名称。文件名一般会被最后一个`.`分为名称与扩展名两个部分。可见`NUL.txt`和`NUL`都是非法文件名，而`txt.NUL`和`.NUL`都是合法文件名。

4. 不可以<code> </code>（空格）和`.`（句号）结尾，但可以其开头。可见<code>note.txt  </code>和`note.`是非法文件名，而<code>  note.txt</code>和`.note.txt`是合法文件名。

所有的限制都在参考内容里有描述。

# 文件名最大长度

很难确定文件名到底能有多长，不同的 Windows 版本的限制不一样，而且还要配合路径的最大长度限制。那么可以使用`128`这个数来作为最大长度限制。所谓的限制指的是字符个数而非编码后的字节个数。

# 参考
[https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247%28v=vs.85%29.aspx#naming_conventions](https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247%28v=vs.85%29.aspx#naming_conventions)  
[https://blog.codinghorror.com/filesystem-paths-how-long-is-too-long/](https://blog.codinghorror.com/filesystem-paths-how-long-is-too-long/)
