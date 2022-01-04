# Redis配置参数


```shell
# 启动自动内存碎片清理
config set activedefrag yes

# ：表示内存碎片的字节数达到 100MB 时，开始清理
active-defrag-ignore-bytes 100mb
# ：表示内存碎片空间占操作系统分配给 Redis 的总空间比例达到 10% 时，开始清理。
active-defrag-threshold-lower 10

# ： 表示自动清理过程所用 CPU 时间的比例不低于 25%，保证清理能正常开展；
active-defrag-cycle-min 25
# ：表示自动清理过程所用 CPU 时间的比例不高于 75%，一旦超过，就停止清理，从而避免在清理时，大量的内存拷贝阻塞 Redis，导致响应延迟升高。
active-defrag-cycle-max 75
```


```shell
# 查看服务器和客户端对输入缓冲区的使用情况
CLIENT LIST
id=5 addr=127.0.0.1:50487 fd=9 name= age=4 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=26 qbuf-free=32742 obl=0 oll=0 omem=0 events=r cmd=client
```
> addr：ip和端口
> cmd：表示客户端最近执行的命令
> qbug：表示输入缓冲区已经使用了的大小
> qbug-free：表示输入缓冲区还没使用了的大小


```shell
# 设置输出缓冲区的大小
client-output-buffer-limit
# eg
client-output-buffer-limit normal 0 0 0
# normal 表示当前设置的是普通客户端，第 1 个 0 设置的是缓冲区大小限制，第 2 个 0 和第 3 个 0 分别表示缓冲区持续写入量限制和持续写入时间限制。
```


```shell
# 设置复制缓冲区大小
config set client-output-buffer-limit slave 512mb 128mb 60
# slave 参数表明该配置项是针对复制缓冲区的。512mb 代表将缓冲区大小的上限设置为 512MB；128mb 和 60 代表的设置是，如果连续 60 秒内的写入量超过 128MB 的话，也会触发缓冲区溢出。
```