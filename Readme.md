# Run
>If capture_output is true, stdout and stderr will be captured. When used, the internal Popen object is automatically created with stdout=PIPE and stderr=PIPE. The stdout and stderr arguments may not be supplied at the same time as capture_output. If you wish to capture and combine both streams into one, use stdout=PIPE and stderr=STDOUT instead of capture_output.

当`capture_output=True`时，run（）会将执行命令的输出重定向到PIPE，当运行那种持续性输出的命令时，不要用
If you wish to capture and combine both streams into one, use stdout=PIPE and stderr=STDOUT instead of capture_output.
所以，可以`stdout=fd and stderr=STDOUT` `fd file-like object`将结果保存到文件

# Popen
Popen是非堵塞型的
```python
 class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=None, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, encoding=None, errors=None, text=None)
 ```

Popen 对象支持通过 with 语句作为上下文管理器，在退出时关闭文件描述符并等待进程:
```python
with Popen(["ifconfig"], stdout=PIPE) as proc:
    log.write(proc.stdout.read())
```

## 参数说明：
### args
>注解

shlex.split() 在确定正确 args 的正确标记化时非常有用，尤其是在复杂情况下:
```python
>>> import shlex, subprocess
>>> command_line = input()
/bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
>>> args = shlex.split(command_line)
>>> print(args)
['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
>>> p = subprocess.Popen(args) # Success!
```
>特别注意

由 shell 中的空格分隔的选项（例如 -input）和参数（例如 eggs.txt ）位于分开的列表元素中，而在需要时使用引号或反斜杠转义的参数在 shell （例如包含空格的文件名或上面显示的 echo 命令）是单独的列表元素。

### shell
参数 shell （默认为 False）指定是否使用 shell 执行程序。

如果 shell 为 True，更推荐将 args 作为**字符串**传递而非序列。
```python
p = subprocess.Popen('ls -l', shell=True)
p = subprocess.Popen(['ls','-l'], shell=False)  # 推荐使用
```
> 在 POSIX，当 shell=True， shell 默认为 /bin/sh。

>如果 args 是一个**字符串**

此字符串指定将通过 shell 执行的命令。

这意味着字符串的格式必须和在命令提示符中所输入的完全相同。这包括，例如，引号和反斜杠转义包含空格的文件名。

>如果 args 是一个序列

第一项指定了**命令**，另外的项目将作为传递给 shell （而非命令） 的**参数**对待。也就是说， Popen 等同于:
```python
Popen(['/bin/sh', '-c', args[0], args[1], ...])
# [命令， 参赛0， 参赛1，...] 不用进行转义，更好用！！
```
> 在 Windows，使用 shell=True，环境变量 COMSPEC 指定了默认 shell。

>Note:

实际上，在 Windows 你唯一需要指定 shell=True 的情况是你想要执行内置在 shell 中的命令（例如 dir 或者 copy）。

在运行一个批处理文件或者基于控制台的可执行文件时，不需要 shell=True。

### bufsize
bufsize 将在 open() 函数创建了 stdin/stdout/stderr 管道文件对象时作为对应的参数供应:

0. 表示不使用缓冲区 （读取与写入是一个系统调用并且可以返回短内容）
1. 表示**行缓冲**（只有 universal_newlines=True 时才有用，例如，在文本模式中）
    > 3.7 新版功能: 添加了 text 形参作为 universal_newlines 的别名

    >当 universal_newline 被设为 True，则类使用 locale.getpreferredencoding(False) 编码来代替 locale.getpreferredencoding()。
    不同平台换行符不同，如window '\r\n';linux '\n'。
2. 任何其他正值表示使用一个约为对应大小的缓冲区
    负的 bufsize （默认）表示使用系统默认的 io.DEFAULT_BUFFER_SIZE。

在 3.3.1 版更改: bufsize 现在默认为 -1 来启用缓冲，以符合大多数代码所期望的行为。在 Python 3.2.4 和 3.3.1 之前的版本中，它错误地将默认值设为了为 0，这是无缓冲的并且允许短读取。这是无意的，并且与大多数代码所期望的 Python 2 的行为不一致。

### Popen堵塞导致死锁
>问题描述：

简单说就是，使用 subprocess 模块的 Popen 调用外部程序，如果 stdout 或 stderr 参数是 pipe，并且程序输出超过操作系统的 pipe size时，如果使用 Popen.wait() 方式等待程序结束获取返回值，会导致死锁，程序卡在 wait() 调用上。

>那死锁问题如何避免呢？

官方文档里推荐使用 Popen.communicate()。这个方法会把输出放在**内存**，而不是管道里，所以这时候上限就和内存大小有关了，一般不会有问题。而且如果要获得程序返回值，可以在调用 Popen.communicate() 之后取 Popen.returncode 的值。

>结论：

如果使用 subprocess.Popen，就不使用 Popen.wait()，而使用 Popen.communicate() 来等待外部程序执行结束。

> 典型用法：

处理模型程序输出的结果时，可以使用

> 特别注意：

内存里数据读取是缓冲的，所以如果数据尺寸过大或无限，不要使用Popen.communicate()。

### 安全考量
不像一些其他的 popen 功能，此实现绝不会**隐式调用一个系统 shell**。

这意味着任何字符，包括 shell 元字符，可以安全地被传递给子进程。如果 shell 被明确地调用，通过 shell=True 设置，则确保所有空白字符和元字符被恰当地包裹在引号内以避免 shell 注入 漏洞就由应用程序负责了。

当使用 shell=True， shlex.quote() 函数可以作为在将被用于构造 shell 指令的字符串中转义空白字符以及 shell 元字符的方案。

## Popen 方法

>Popen.poll()

    检查子进程是否已被终止。设置并返回 returncode 属性。否则返回 None。

>Popen.wait(timeout=None)

    等待子进程被终止。设置并返回 returncode 属性。

    如果进程在 timeout 秒后未中断，抛出一个 TimeoutExpired 异常，可以安全地捕获此异常并重新等待。

    注解

    当 stdout=PIPE 或者 stderr=PIPE 并且子进程产生了足以阻塞 OS 管道缓冲区接收更多数据的输出到管道时，将会发生死锁。当使用管道时用 Popen.communicate() 来规避它。

    注解

    此函数使用了一个 busy loop （非阻塞调用以及短睡眠） 实现。使用 asyncio 模块进行异步等待： 参阅 asyncio.create_subprocess_exec。

    在 3.3 版更改: timeout 被添加

>Popen.communicate(input=None, timeout=None)

    与进程交互：向 stdin 传输数据。从 stdout 和 stderr 读取数据，直到文件结束符。等待进程终止。可选的 input 参数应当未被传输给子进程的数据，如果没有数据应被传输给子进程则为 None。如果流以文本模式打开， input 必须为字符串。否则，它必须为字节。

    communicate() 返回一个 (stdout_data, stderr_data) 元组。如果文件以文本模式打开则为字符串；否则字节。

    注意如果你想要向进程的 stdin 传输数据，你需要通过 stdin=PIPE 创建此 Popen 对象。类似的，要从结果元组获取任何非 None 值，你同样需要设置 stdout=PIPE 或者 stderr=PIPE。

    如果进程在 timeout 秒后未终止，一个 TimeoutExpired 异常将被抛出。捕获此异常并重新等待将不会丢失任何输出。

    如果超时到期，子进程不会被杀死，所以为了正确清理一个行为良好的应用程序应该杀死子进程并完成通讯。

    proc = subprocess.Popen(...)
    try:
        outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()

    注解

    内存里数据读取是缓冲的，所以如果数据尺寸过大或无限，不要使用此方法。

    在 3.3 版更改: timeout 被添加

>Popen.send_signal(signal)

    将信号 signal 发送给子进程。

    注解

    在 Windows， SIGTERM 是一个 terminate() 的别名。 CTRL_C_EVENT 和 CTRL_BREAK_EVENT 可以被发送给以包含 CREATE_NEW_PROCESS 的 creationflags 形参启动的进程。

>Popen.terminate()

    停止子进程。在 Posix 操作系统上，此方法发送 SIGTERM。在 Windows，调用 Win32 API 函数 TerminateProcess() 来停止子进程。

>Popen.kill()

    杀死子进程。在 Posix 操作系统上，此函数给子进程发送 SIGKILL 信号。在 Windows 上， kill() 是 terminate() 的别名。

以下属性也是可用的：

>Popen.args

    args 参数传递给 Popen -- 一个程序参数的序列或者一个简单字符串。

    3.3 新版功能.

>Popen.stdin

    如果 stdin 参数为 PIPE，此属性是一个类似 open() 返回的可写的流对象。如果 encoding 或 errors 参数被指定或者 universal_newlines 参数为 True，则此流是一个文本流，否则是字节流。如果 stdin 参数非 PIPE， 此属性为 None。

>Popen.stdout

    如果 stdout 参数是 PIPE，此属性是一个类似 open() 返回的可读流。从流中读取子进程提供的输出。如果 encoding 或 errors 参数被指定或者 universal_newlines 参数为 True，此流为文本流，否则为字节流。如果 stdout 参数非 PIPE，此属性为 None。

>Popen.stderr

    如果 stderr 参数是 PIPE，此属性是一个类似 open() 返回的可读流。从流中读取子进程提供的输出。如果 encoding 或 errors 参数被指定或者 universal_newlines 参数为 True，此流为文本流，否则为字节流。如果 stderr 参数非 PIPE，此属性为 None。
```python
for line in proc.stdout:
    print(line)
# 用了with上下文管理后，不用显式调用proc.stdout.close()，会默认调用，我们只管用就行
```

>警告

当处理有限输出时，使用 communicate() 而非 .stdin.write， .stdout.read 或者 .stderr.read 来避免由于任意其他 OS 管道缓冲区被子进程填满阻塞而导致的死锁。

>Popen.pid

    子进程的进程号。

    注意如果你设置了 shell 参数为 True，则这是生成的子 shell 的进程号。

>Popen.returncode

    此进程的退出码，由 poll() 和 wait() 设置（以及直接由 communicate() 设置）。一个 None 值 表示此进程仍未结束。

    一个负值 -N 表示子进程被信号 N 中断 (仅 POSIX).
