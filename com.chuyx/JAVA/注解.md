# 注解

ps: 以前一直以为注解是个很高级的东西，为什么一个简单的`@XXX` 就可以实现那么多功能呢？如：@Data等

## 什么是注解？
JAVA注解也叫做JAVA标注，是jdk5.0后开始支持加入源代码的特殊语法元数据。

Java语言中的类、方法、变量、参数和包等都可以被标注。和Javadoc不同，Java标注可以通过反射获取注解内容。
在编译器生成类文件时，注解可以被嵌入到字节码中。Java虚拟机可以保留注解内容，在运行时可以获取到注解内容。


## JAVA中的内置注解
1. 作用在方法的注解是

**@Override** - 检查该方法是否是重写方法。如果发现其父类，或者是引用的接口中并没有该方法时，会报编译错误。
**@Deprecated** - 标记过时方法。如果使用该方法，会报编译警告。
**@SuppressWarnings** - 指示编译器去忽略注解中声明的警告。

2. 作用在其他注解的注解(或者说元注解)是:

**@Retention** - 标识这个注解怎么保存，是只在代码中，还是编入class文件中，或者是在运行时可以通过反射访问。
**@Documented** - 标记这些注解是否包含在用户文档中。
**@Target** - 标记这个注解应该是哪种 Java 成员。
**@Inherited** - 标记这个注解是继承于哪个注解类(默认 注解并没有继承于任何子类)

3. 从 Java 7 开始，额外添加了 3 个注解:

`@SafeVarargs` - Java 7 开始支持，忽略任何使用参数为泛型变量的方法或构造函数调用产生的警告。
`@FunctionalInterface` - Java 8 开始支持，标识一个匿名函数或函数式接口。
`@Repeatable` - Java 8 开始支持，标识某注解可以在同一个声明上使用多次。
### 元注解
1. **@Retention**

`@Retention` annotation指定标记注释的存储方式：

- RetentionPolicy.SOURCE - 标记的注释仅保留在源级别中，并由编译器忽略。
- RetentionPolicy.CLASS - 标记的注释在编译时由编译器保留，但Java虚拟机（JVM）会忽略。
- RetentionPolicy.RUNTIME - 标记的注释由JVM保留，因此运行时环境可以使用它。
2. **@Documented**

`@Documented` 注释表明，无论何时使用指定的注释，都应使用Javadoc工具记录这些元素。（默认情况下，注释不包含在Javadoc中。）有关更多信息，请参阅 Javadoc工具页面。

3. **@Target**

@Target 注释标记另一个注释，以限制可以应用注释的Java元素类型。目标注释指定以下元素类型之一作为其值

- ElementType.TYPE 可以应用于类的任何元素。
- ElementType.FIELD 可以应用于字段或属性。
- ElementType.METHOD 可以应用于方法级注释。
- ElementType.PARAMETER 可以应用于方法的参数。
- ElementType.CONSTRUCTOR 可以应用于构造函数。
- ElementType.LOCAL_VARIABLE 可以应用于局部变量。
- ElementType.ANNOTATION_TYPE 可以应用于注释类型。
- ElementType.PACKAGE 可以应用于包声明。
- ElementType.TYPE_PARAMETER
- ElementType.TYPE_USE

4. **@Inherited**

`@Inherited` 注释表明注释类型可以从超类继承。当用户查询注释类型并且该类没有此类型的注释时，将查询类的超类以获取注释类型（默认情况下不是这样）。此注释仅适用于类声明。

5. **@Repeatable**

Repeatable Java SE 8中引入的，`@Repeatable`注释表明标记的注释可以多次应用于相同的声明或类型使用(即可以重复在同一个类、方法、属性等上使用)。


## 自定义注解

> 直接上代码

```java
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Target(ElementType.FIELD)
public @interface FieldName {

    String value() default "";
}
```

```java
public class Student {

    @FieldName(value = "姓名")
    private String name;

    @FieldName(value = "年龄")
    private int age;

    @FieldName(value = "性别")
    private String sex;

    // 忽略setter和getter以及构造方法
}
```

```java
public class TestDemo {

    public static void main(String[] args) {
        try{
            // 模拟oldData
            Student oldData = new Student("小明", 23, "男");
            Student newData = new Student("大明", 26, "男");
            if (!oldData.getName().equals(newData.getName())){
                Class<? extends Student> aClass = oldData.getClass();
                Field name = aClass.getDeclaredField("name");
                if (name.isAnnotationPresent(FieldName.class)){
                    System.out.println(oldData.getName() + "->" + newData.getName());
                }
            }
        }catch (Exception e){
            e.printStackTrace();
        }

    }
}
```

