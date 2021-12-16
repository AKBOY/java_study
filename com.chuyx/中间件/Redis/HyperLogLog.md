# Redis 之HyperLogLog

Redis在2.8.9版本中添加了hyperLogLog结构（估算）
它是用来做基数统计的结构。
**优点：**
输入元素非常大的时候，计算基数所需要的空间是固定且很小的（当存储的元素达到某个阈值后，需要花12kb来存这个键，可以存2^64个不同元素）
**缺点：**
hyperLogLog结构只能记录有多少个不同的元素，无法像集合一样拿出元素使用

```shell
pfadd key element [element...]  // 添加指定元素到key
pfcount key [key...]  // 返回给定的键得基数估算值
pfmerge destKey sourcekey[sourcekey...] // 将sourcekeys合并成一个destKey
```

## HyperLogLog的实现原理
实际上，HyperLogLog不会存储每个元素的值，它使用的是概率算法。
// todo


## HyperLogLog相关命令详解：
pfadd hll ele：将ele添加进hll的基数计算中。流程：
先对ele求hash（使用的是一种叫做MurMurHash的算法） 
将hash的低14位(因为总共有2的14次方个桶)作为桶的编号，选桶，记桶中当前的值为count
从的hash的第15位开始数0，假设从第15位开始有n个连续的0（即前导0）
如果n大于count，则把选中的桶的值置为n，否则不变
pfcount hll：计算hll的基数。就是使用上面给出的DV公式根据桶中的数值，计算基数
pfmerge hll3 hll1 hll2：将hll1和hll2合并成hll3。合并方法是将所有的HyperLogLog对象合并到一个名为max的对象中，max采用的  是密集存储结构，如果被合并的对象也是密集存储结构，则循环比较每一个计数值，将大的那个存入max。

Redis的所有HyperLogLog结构都是固定的16384个桶（2的14次方），并且有两种存储格式：

稀疏格式：HyperLogLog算法在刚开始的时候，大多数桶其实都是0，稀疏格式通过存储连续的0的数目，而不是每个0存一遍，大大减小了HyperLogLog刚开始时需要占用的内存

紧凑格式：用6个bit表示一个桶，需要占用12KB内存

## pf 的内存占用为什么是 12k？
我们在上面的算法中使用了1024个桶进行独立计数，不过在Redis的HyperLogLog实现中用到的是16384个桶，也就是2^14，每个桶的maxbits需要6个bits来存储，最大可以表示maxbits=63，于是总共占用内存就是2^14 * 6/8 = 12k 字节。