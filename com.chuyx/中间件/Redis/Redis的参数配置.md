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




COPY来的配置文件解析：（Redis4版本）
> ### 所有配置都来自于redis.conf  一下为4.0version
> ./redis-server /path/to/redis.conf # redis启动方式
> include /path/to/local.conf # redis依赖文件，redis是按照从上往下读取配置的方式，如果include的内容需要覆盖原始模板则 放置在配置文件最后一行，否则放置在最前面，redis做集群的时候，会需要一个标准的模板配置然后增加一些个性的配置
> bind 192.168.1.100 127.0.0.1 ::1 # 绑定redis只接收哪些网卡的请求，比如192.168.1.100表示的是内网地址，那么就可以接收 来自内网的请求，如果是外网地址那么则表示可以接收外网地址。如果不配置，那么表示接收所有的网络请求。 redis默认仅接收来自本机的IPv4网络请求
> protected-mode yes # 是否开启保护模式，默认开启
> 如果开启保护模式，而且server未绑定ip(bind)，也未设置连接密码，那么server只接收IPv4、IPv6 和Unix Domain Sockets发过来的连接请求
> 如果开启保护模式，而server有绑定ip，那么会接收来自绑定ip的网络请求
> 如果开启保护模式，而server未绑定ip，但是有设置连接密码，那么客户端可以连接到redis服务器，但是提交请求的时候需要输入密码
> 如果需要接收其它ip的连接请求，那么可以选择关闭保护模式(并且不绑定任何ip)，或者绑定ip
> 总结，如果有绑定IP，那么以绑定IP为优先级，如果未绑定IP，那么再采取保护模式以确定可以接收哪些主机的连接请求
> port 6379 # 设置server监听的端口(如果设置为0，那么不会接收tcp请求，比如Unix Domain Sockets)
> tcp-backlog 511 # tcp全连接数量(还需要配置系统参数/proc/sys/net/core/somaxconn大小)
> unixsocket /tmp/redis.sock # unix domain socket 监听地址，默认关闭
> timeout 0 # 当客户端连接空闲N秒后，关闭连接，0表示禁止关闭，由客户端控制连接是否关闭
> tcp-keepalive 300 # tcp服务端发送监控给客户端的时间间隔，以检测客户端是否关闭或者继续保持连接
> daemonize no # 是否以daemon的方式启动服务，如果以daemon启动，则pid会写入到${piffile}，如果未指定则放置/var/run/redis.pid
> pidfile redis.pid # 如果redis以daemon方式启动，那么会将pid文件写入到指定位置
> loglevel notice # redis日志等级，包括(debug、verbose、notice、warning)
> logfile "" # 日志文件名称，默认为空，即写入到标准控制台，如果是以daemon方式则输入到/dev/null
> databases 16 # 设置数据库数量，默认是将数据存放在0数据库，如果用了redis cluster则不需要了 (如果需要将多个key存储到同一个节点，那么可以使用hash tag，比如：aaa{username}bbb，xxx{username}yyy， 这两个key可以按照username这个tag进行hash，然后放入到同一个节点)
> always-show-logo yes # redis启动时显示logo
> 数据持久化配置，可以组合多个配置
> save 900 1 # 如果900秒内，有超过1个key改变，则持久化
> save 300 10 # 如果300秒内，有超过10个key改变，则持久化
> save 60 10000 # 如果60秒内，有超过10000个key改变，则持久化
> save "" # 禁止保存到rdb数据库
> stop-writes-on-bgsave-error yes # 默认情况下，当开启保存rdb快照，并且最近的一次快照保存失败，那么redis会禁止写入， 这样能让业务方感知到数据未持久化到硬盘，防止发生未知灾难。一旦bgsave可以正常运行时，redis也会开始正常写入，如果有对 redis持久化硬盘监控，或者不需要redis持久化的功能，也可以禁止掉这个特性
> rdbcompression yes # 默认开启使用LZF算法压缩string对象，以减少dump.rdb大小，但是也会损耗cpu
> rdbchecksum yes # 默认开启rdb checksum，防止出现数据损坏
> dbfilename dump.rdb # 数据库 文件名称
> dir ./ # rdb、aof文件写入的目录地址，默认是当前目录
> slaveof 192.168.2.55 7000 # slaveof <masterip> <masterport> ，指定当前redis为某个redis的slave(cluster集群不需要配置)
> masterauth 123455 # masterauth <master-password>，当master 配置requirepass，那么slave需要配置认证密码
> slave-serve-stale-data yes # 当slave与master失去连接，或者slave正在同步master的数据时
> 如果设置为yes，当客户端请求到slave时，继续响应请求，只是数据可能不是最新的
> 如果设置为false，当客户端响应请求时，那么会返回SYNC with master in progress错误
> redis是建议slave仅仅作为备份而已，不接收请求，所以就不会产生这种问题
> slave-read-only yes # 默认开启slave只读模式，如果需要对slave写临时数据，也可以关闭此开关(此参数在集群模式下无效， 在集群模式下，直接使用连接级命令readonly即可，或者使用readwrite命令管理只读命令)；如果为yes时，将数据写入到slave 会提示错误((error) READONLY You can't write against a read only slave.)
> slave 同步策略
> disk-backed: redis master启用新的线程把rdb写入到磁盘，随后父进程增量将文件同步到slave，如果有多个slave，那么会将 同步的文件按照队列的形式一一同步
> diskless: redis master 创建一个新的rdb文件到slave sockets中，而不是操作rdb文件，如果有多个slave，可以按照指定时间 预热后并行的同步到slave，如果服务器的带宽非常大，采用此方式会更加好
> repl-diskless-sync no # 默认关闭diskless
> repl-diskless-sync-delay 5: # 默认预热5秒后才是同步数据到slave(比如在一主多从的场景，可能server突然重启等， 如果按照常规，那么是一个一个的服务。redis提供这个参数，可以让server等待一定的时间，然后一次性同步给所有的slave)
> repl-ping-slave-period 10 # slave向master发送心跳时间间隔，默认10s(在cluster模式下,如果设置了slave-validity-factor=0 参数，则这个参数无效)
> 同步超时情况：
> 繁重的IO数据同步导致的超时
> slave检测到master超时
> master检测到slave超时
> repl-timeout 60 # 同步超时，默认60s
> repl-timeout # slave与master连接超时时间，如果master数据量非常大，在进行全量同步时，如果超过这个时间还未同步完毕， 那么slave会关闭此连接，然后再清空数据，导致无法完成同步，如果数据量比较大，增加这个值。(比如一个6G的数据，在1G的带宽 下，每秒最高同步100MB，将会超过60S)
> repl-disable-tcp-nodelay no # redis默认开启tcp-nodelay，即禁用nagle算法，如果网络带宽拥塞，或者网络的hop数过多，那么可以将开关改为yes
> repl-backlog-size 1mb # slave与master断连后，master会把增量的数据写入一个临时文件，用于下次slave重连后同步增量数据
> repl-backlog-ttl 3600 # 超过这个时间后，slave还未连接上，那么释放backlog
> slave-priority 100 # 晋升master的优先级，数值越低优先级越高，如果设置为0则表示不参数master晋升
> min-slaves-to-write 3 # 至少存在3个slave才可以写入数据，低于三个slave则master停止写入，如果设置为0则表示禁止此特性， redis默认是禁止
> min-slaves-max-lag 10 # 与min-slaves-to-write配合使用，设置当一个master端的可用slave少于N个， 延迟时间大于M秒时，不接收写操作(需要两个参数同时配合才会生效)
> slave-announce-ip 192.168.2.22 # slave向master上报自己的ip，slave连上master时候，master其实已经知道了 slave的ip和port但是由于存在端口跳转或者NAT技术，所以获取的ip不一定是真实的，redis提供了这个配置让slave 自动上报自己真实的ip，这个在使用docker部署redis cluster的时候必须指定，否则部署cluster失败
> slave-announce-port 6379 # slave向master上报自己的port
> requirepass test # 设置连接redis服务器密码
> rename-command shutdown server-close # 重命名命令，比如像关闭服务这种特殊的命令，不应该暴露给外部调用，但是可以提供给 管理员使用。或者直接禁止某个命令，则改为 rename-command shutdown ""
> maxclients 10000 # 客户端最大的连接数，默认是10000(如果系统限制了最大连接符数量，那么默认是最大连接符减去32， redis内部需要使用一些文件描述符)，如果超过了这个数，redis会返 max number of clients reached，客户端也是需要设置 最大连接数，防止出现连接泄漏问题
> maxmemory 10gb # 最大内存，超过内存后会按照清理策略清理缓存
> maxmemory-policy volatile-lru # 以lru的方式清理缓存
> maxmemory-samples 5 # 清理缓存时采集的样本数量，值越大那么越精确，但是消耗cpu越高，值越小，速度越快，但是精确度降低 redis默认是5(redis是使用采样的方式移除缓存，并不是真正的lru，而是近似lru)
> redis删除key有两种方式：
> 第一种是传统的阻塞型(命令为DEL)，如果对象非常小的话，删除速度非常快，时间复杂度为O(1)或者O(log_N)，但是如果key 关联的对象非常多，比如set、list等，那么需要花费的时间就会非常多
> 由于阻塞导致时间变长，所以redis提供了以非阻塞的方式删除key(命令为UNLINK)，客户端以异步的方式提交命令后， 会立刻返回给客户端，redis会有一个后台线程进行删除key和重新整理内存
> redis 删除key或者刷新缓存的场景有下面几种：
> redis内存达到最大值，需要按照清理缓存策略清理key
> 缓存key已经到了过期时间，开始清理key
> 客户端命令操作而引起的删除key操作，比如set一个已经存在的key，那么会导致先删除旧的内容，然后重新替换新的内容；或者是 执行rename操作，那么会先删除旧的key，然后将新的key加入redis
> 在slave同步master的时候，slave执行了全量的重复制
> 在性能和数据一致性上，redis提供了几个参数，让我们控制
> lazyfree-lazy-eviction no # 异步释放由于内存达到最高值而需要清理的对象空间
> lazyfree-lazy-expire no # 异步释放过期key对象空间
> lazyfree-lazy-server-del no # 异步释放del操作key的对象空间
> slave-lazy-flush no # 异步刷新slave数据库
> appendonly no # 是否开启aof，如果开启则以aof的方式加载文件，否则以rdb的方式加载文件(aof文件就是客户端操作命令 的集合日志，redis重启后直接对日志进行重做以达到恢复功能)
> appendfilename "appendonly.aof"
> redis 数据落盘策略
> appendfsync always # 每次执行操作完，都会执行一次fsync刷盘操作，这样会保证数据不会丢失，但是性能会非常低
> appendfsync everysec # 每隔一秒钟执行一次fsync刷盘操作，这样最多也就是1秒钟出现数据丢失，redis默认的方式
> appendfsync no # 不进行fsync刷盘操作，这样最大的数据丢失依赖于系统缓存刷盘策略，默认是30s(这个时间是系统 级别的，不提供配置，系统只是保证最长30s能落盘，系统尽量保证快速的落盘，其实理论上是写入马上就会落盘的)
> 上面说的数据丢失，针对的是服务器突然宕机而言，而不是redis服务crash，因为每次操作都是write进系统，真正落盘由系统 决定，而执行fsync只是强制系统落到磁盘。所以如果想要高性能，而且最数据不是非常敏感，其实可以考虑设置appendfync no
> no-appendfsync-on-rewrite no # 在执行BGSAVE或者BGREWRITEAOP时候，虽然是异步线程操作，但是因为使用了大量的IO操作， 也会影响到主业务操作redis，导致延迟增大，通过这个参数可以避免这个问题，如果设置为yes，则表示在BGSAVE等操作的时候， 不进行fsync刷盘操作，这样最坏的情况，也会出现最大30s的数据丢失(这个配置会使appendfsync在BGSAVE情况下配置失效)
> redis rewrite: redis的aof文件是对redis命令的一个redo日志，所以会存在大量的重复日志(比如一个set操作了100次， 只有最后一次才有效，但是aof日志记录了100次)，redis 提供了日志重写的特性
> auto-aof-rewrite-percentage 100 # 设置aof文件达到指定大小的百分比后开始重写aof文件，redis会记录上一次重写后的 aof文件大小，然后以上一次aof文件大小为基数，如果当前的aof文件超过上次重写后的100%，那么开始再次触发重写操作(比如第一次 aof文件为1G，那么当aof文件达到2G的时候则执行重写，重写完毕后可能是1.5G，那么下次再触发重写则是3G)
> auto-aof-rewrite-min-size 64mb # 设置aof文件最小值达到多少才开始进行重写aof文件，虽然有上面的百分比基数，但是 在初始时，一般文件很小，所以触发重写的频率会非常高，所以设置当aof后续的增长至少达到指定值才开始执行aof重写，也就是说 aof重写必须要满足这两个条件才真正的触发
> aof-load-truncated yes # 由于服务器宕机或者文件系统损坏等原因导致aof文件损坏，redis启动时候检查到aof文件已经损坏， 那么会截断文件末尾损坏的部分，加载未损坏的部分，这样就会导致一些数据丢失。如果设置为no，那么启动的时候redis就会 报错，由人工进行修复
> aof-use-rdb-preamble no # 如果配置了appendonly yes，那么表示redis每次都是加载aof文件，而不会加载rdb文件，而aof文件 仅仅是一些操作集合的命令，如果数据量非常大的情况，那么加载的时间会变得非常长。如果开启了aof-use-rdb-preamble配置 后，那么每次重写aof文件的时候，都会把rdb文件写入到aof文件前面，然后再追加真正的aof增量数据，这样就将rdb文件的快速 和aof增量文件结合在一起，大大提高性能(如果开启aof方式，那么可以关闭rdb生成快照了)
> cluster-enabled yes # 开启redis cluster特性
> cluster-config-file nodes.conf # cluster集群配置文件，当集群内节点发生信息变化时，如添加节点、节点下线、故障转移等。 节点会自动保存集群的状态到配置文件中。该配置文件由redis自行维护，不要手动修改，防止节点重启时产生集群信息错乱
> cluster-node-timeout 15000 # cluster节点超时时间，单位ms，slave检查到master超过时间还未获取到心跳，则认为master下线
> slave晋升成master时候有多个匹配条件
> 每个slave之间会检查自己同步数据的offset，值最大的表示同步的数据最大，最有机会晋升为master
> 如果slave与master断连了超过一定的时间，那么当前slave是不会参与晋升master，超过 (node-timeout * slave-validity-factor) + repl-ping-slave-period 时间的slave不会参与晋升master
> 一个节点下线分为两个阶段：
> 第一个阶段为主观下线(redis日志中显示的pfail)，也就是当达到cluster-node-timeout时间后，会判定当前节点主观下线
> 第二个阶段为客观下载(redis日志中显示fail)，当某个节点主观下线后，相应的节点状态会在集群中传播，当半数以上的主节点 都标记某个节点主观下线后，触发客观下线流程，也就是当前节点真正下线了
> 为什么要分为两个阶段呢？因为有可能存在网络分区的请求，导致误判节点
> 为什么必须是负责槽的主节点参与故障发现决策？因为集群模式下，只有处理槽的主节点才负责读写请求和集群槽等关键信息的维护， 而从节点只进行主节点数据和状态信息的复制
> 为什么必须是半数以上处理槽的主节点？因为是为了应对网络分区等原因造成的集群分割请求，所以cluster集群也必须要求3个以上的节点
> slave晋升为master耗时：
> 主观下线时间=cluster-node-timeout
> 主观下线消息传播时间cluster-node-timeout/2：cluster与cluster/slave之间是通过ping/pong进行心跳检测的， 集群中的服务都会在每秒随机选择另外一个服务进行心跳检测，然后更新本地信息(每个节点一定会主动ping那些自己在 NODE_TIMEOUT/2时间内没有发送过ping或从之接收过pong的节点)
> 从节点转移时间1000ms，由于存在延迟发起选举机制(根据节点同步数据的偏移量来确定延迟时间)，偏移量最大的从节点会最多延迟1s发起选举
> failover-time <= cluster-node-timeout + cluster-node-timeout/2 + 1000
> cluster-slave-validity-factor 10 # 验证slave合法性的因子，如果这个值越大，slave越有可能参与master晋升，那么新的master 存在数据丢失的情况就越高，设置为0表示所有的slave都参数晋升master
> cluster-migration-barrier 1 # 如果某个master下没有slave，那么称这个master为孤儿，redis为了保证可用性， 会把其它master下多余的slave迁移到孤儿master中，成为孤儿master的slave。cluster-migration-barrier 表示master下最少有多少个slave，超过这个数的slave可以把多余的slave迁移给孤儿master。 这也就是为什么redis建议slave的数量一定要比预计slave数量多N个的原因(如果某个master和slave同时crash， 或者slave还未晋升为master之前也挂了，那么多余的slave是不会迁移成为旧的master的slave，出现某个master 有多个slave，而某个slot直接不存在任何的服务)
> cluster-require-full-coverage yes # 如果其中某些hash slot未覆盖到(slot未分配正确)redis默认会停止接收请求， 如果希望其它的节点继续接收请求则改为no(如果某个master和slave都crash，虽然也是出现某个hash slot未提供服务，但是 不此配置不影响)
> cluster-slave-no-failover no # 设置当前slave不参与failover
> slowlog-log-slower-than 10000 # 超过这个时间的命令都记录日志(单位微妙)，设置负数表示禁止日志，设置0表示每个命令都记录日志 这个时间是不包括IO时间或者网络请求时间，而是命令真正执行的时间
> slowlog-max-len 128 # slowlog记录数量(因为slowlog是不存储在磁盘，所以防止慢日志非常多，所以设置数量)
> aof-rewrite-incremental-fsync yes # 在执行重写aof文件时，每次生成32MB的增量数据后就强制刷盘到磁盘，而不是一次性 把整个文件写入到磁盘，防止出现过高的IO导致性能抖动
> redis主从复制可以根据是否是全量分为全量同步和增量同步(线上不要重启服务器，防止出现全量同步大量的数据时导致IO抖动)
> 全量同步,redis全量复制一般发生在slave初始化阶段，这时slave需要将master上的所有数据都复制一份。具体步骤如下：
> 从服务器连接主服务器，发送sync命令；
> 主服务器接收到SYNC命名后，开始执行bgsave命令生成rdb文件并使用缓冲区记录此后执行的所有写命令；
> 主服务器bgsave执行完后，向所有从服务器发送快照文件，并在发送期间继续记录被执行的写命令；
> 从服务器收到快照文件后丢弃所有旧数据，载入收到的快照；
> 主服务器快照发送完毕后开始向从服务器发送缓冲区中的写命令；
> 从服务器完成对快照的载入，开始接收命令请求，并执行来自主服务器缓冲区的写命令；
> 增量同步,redis增量复制是指slave初始化后开始正常工作时主服务器发生的写操作同步到从服务器的过程。 增量复制的过程主要是主服务器每执行一个写命令就会向从服务器发送相同的写命令，从服务器接收并执行收到的写命令
> 增量同步的概念
> 内存缓存队列(in-memory backlog): 记录连接断开时master收到的写操作
> 复制偏移量(replication offset): master,slave都有一个偏移，记录当前同步记录的位置
> master服务器id(master run id): master服务器唯一标识
> 增量同步条件
> slave记录的master服务器id和当前要连接的master服务器id相同
> slave的复制偏移量比master的偏移量靠前。比如slave是1000， master是1100
> slave的复制偏移量所指定的数据仍然保存在主服务器的内存缓存队列中(设置repl-backlog-size大小)
> 主从刚刚连接的时候，进行全量同步；全同步结束后，进行增量同步。当然，如果有需要,slave在任何时候都可以发起全量同步。 redis策略是，无论如何，首先会尝试进行增量同步，如不成功，要求从机进行全量同步(如果配置了diskless则无需生成)