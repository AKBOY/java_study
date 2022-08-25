# Redis的删除策略

## 惰性删除策略
放任过期键不管，但是每次从键空间中获取键时，都检查取得的键是否过期，如果过期就删除该键，如果没有过期就返回。这种策略的缺点是，当有大量过期键，但是这些键又没有被访问到时，会消耗大量内存。
## 定期删除策略
每个一段时间，程序对数据库进行一次检查，删除里面的过期键。

redis服务器时间使用的是惰性删除和定期删除两种策略：通过配合使用这两种删除策略，服务器可以很好的在合理使用CPU时间和浪费内存空间之间取得平衡。
## 自定义：定时删除策略
在设置键的过期时间的同时，创建一个定时器（timer），让定时器在键的过期时间来临时，立即执行对键的删除。这种策略的缺点是消耗cpu，在cpu紧张的场景，会影响响应时间和吞吐量。


## Redis内存不足时的清理策略：
### 3.0支持的清理策略有6种：
**noeviction: ** 不删除策略, 达到最大内存限制时, 如果需要更多内存, 直接返回错误信息。 大多数写命令都会导致占用更多的内存(有极少数会例外, 如 DEL )。
**allkeys-lru: ** 所有key通用; 优先删除最近最少使用(less recently used ,LRU) 的 key。
**volatile-lru: ** 只限于设置了 expire 的部分; 优先删除最近最少使用(less recently used ,LRU) 的 key。
**allkeys-random: ** 所有key通用; 随机删除一部分 key。
**volatile-random: ** 只限于设置了 expire 的部分; 随机删除一部分 key。
**volatile-ttl: ** 只限于设置了 expire 的部分; 优先删除剩余时间(time to live,TTL) 短的key。
Redis4.0新加了一种淘汰策略LFU（least frequently userd），它的核心思想是根据key的最近被访问的频率进行淘汰，很少被访问优先淘汰，被访问的多就会被留下来！LFU算法能更好的表示一个key被访问的热度。
### LFU一共两种策略：
**volatile-lfu：**再设置了过期时间的key中使用LFU算法淘汰key
**allkeys-lfu：**在所有key中使用LFU淘汰算法。


# 置换策略的选择：

当Redis内存使用达到maxmemory时，就会使用设置好的maxmemory-policy进行对老数据的置换。
设置maxmemory-policy的方法和设置maxmemory方法类似，通过redis.conf或是通过CONFIG SET动态修改。
如果没有匹配到可以删除的key，那么volatile-lru、volatile-random和volatile-ttl策略和noeviction替换策略一样——不对任何key进行置换。
选择合适的置换策略是很重要的，这主要取决于你的应用的访问模式，当然你也可以动态的修改置换策略，并通过用Redis命令——INFO去输出cache的命中率情况，进而可以对置换策略进行调优。

# 针对一些策略所使用的场景：
1）allkeys-lru：如果我们的应用对缓存的访问符合幂律分布（也就是存在相对热点数据），或者我们不太清楚我们应用的缓存访问分布状况，我们可以选择allkeys-lru策略。
在所有的key都是最近最经常使用，那么就需要选择allkeys-lru进行置换最近最不经常使用的key，如果你不确定使用哪种策略。
设置是失效时间expire会占用一些内存，而采用allkeys-lru就没有必要设置失效时间，进而更有效的利用内存
2）allkeys-random：如果我们的应用对于缓存key的访问概率相等，则可以使用这个策略。
如果所有的key的访问概率都是差不多的，那么可以选用allkeys-random策略去置换数据。
3）volatile-ttl：这种策略使得我们可以向Redis提示哪些key更适合被eviction。
如果对数据有足够的了解，能够为key指定hint（通过expire/ttl指定），那么可以选择volatile-ttl进行置换
4）volatile-lru策略和volatile-random策略适合我们将一个Redis实例既应用于缓存和又应用于持久化存储的时候，然而我们也可以通过使用两个Redis实例来达到相同的效果，值得一提的是将key设置过期时间实际上会消耗更多的内存，因此我们建议使用allkeys-lru策略从而更有效率的使用内存。