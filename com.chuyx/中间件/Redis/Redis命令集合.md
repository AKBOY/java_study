# Redis中的其他命令

1. MULTI & EXEC：MULTI 命令：表示一系列原子性操作的开始。收到这个命令后，Redis 就知道，接下来再收到的命令需要放到一个内部队列中，后续一起执行，保证原子性。EXEC 命令：表示一系列原子性操作的结束。一旦 Redis 收到了这个命令，就表示所有要保证原子性的命令操作都已经发送完成了。此时，Redis 开始执行刚才放到内部队列中的所有命令操作。
```shell
127.0.0.1:6379> MULTI
OK
127.0.0.1:6379> HSET key 202008030911 26.8
QUEUED
127.0.0.1:6379> ZADD key 202008030911 26.8
QUEUED
127.0.0.1:6379> EXEC
1) (integer) 1
2) (integer) 1

```


2. 执行下面的命令，就把 Redis 实例绑在了 0 号核上，其中，“-c”选项用于设置要绑定的核编号。
```shell
taskset -c 0 ./redis-server
```

3. 查询Redis内存使用详情
INFO memory
# Memory
used_memory:1073741736      // used_memory 是 Redis 为了保存数据实际申请使用的空间
used_memory_human:1024.00
Mused_memory_rss:1997159792 // used_memory_rss 是操作系统实际分配给 Redis 的物理内存空间，里面就包含了碎片
used_memory_rss_human:1.86G
mem_fragmentation_ratio:1.86    // used_memory_rss/ used_memory

4. 设置Redis缓存最大容量
CONFIG SET maxmemory 4G

5、查询Redis 切片集群Slot的分配情况
127.0.0.1:6379> cluster slots
1) 1) (integer) 0 
   1) (integer) 4095 
   2) 1) "192.168.10.3" 
      1) (integer) 6379
2) 1) (integer) 12288 
   1) (integer) 16383 
   2) 1) "192.168.10.5" 
      1) (integer) 6379
命令返回结果显示，Slot 0 到 Slot 4095 被分配到了实例 192.168.10.3 上，而 Slot 12288 到 Slot 16383 被分配到了实例 192.168.10.5 上。
