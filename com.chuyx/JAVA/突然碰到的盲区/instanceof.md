# 关键字: instanceof

**instanceof是一个位运算符（二目运算符）**

## 用法：
```java
boolean result = obj instanceof class
```
其中 obj是一个对象，class 代表一个类或者一个接口，返回boolean类型。返回true: 表示obj这个对象是class这个对象的直接子类或间接子类

### 注意点：
    - obj 不能为基本数据类型，会抛出 ClassCastException 异常
    - obj 为null 的时候永远返回false
    - obj 为引用类型的时候才会判断

## 底层设计逻辑：
    先判断 obj是否为null，为null返回false，然后强转obj为class对象不抛出异常即返回true否则为false

伪代码：
```java
if (obj == null){
    return false;
} else {
    try {
        T temp = (T)obj;
        return true;
    } catch (ClassCastException e){
        return false;
    }
}
```
## 实现逻辑：
- 看这个[大佬](https://www.zhihu.com/question/21574535)的吧  简直牛逼吼吼 