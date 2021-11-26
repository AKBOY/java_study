# 序列化

Java提供了一种对象序列化的机制。在机制内，一个对象可以被标识位一个字节序列， 该字节序列包括该对象的数据、类型的信息、储存在对象中数据的类型。
将序列化对象写入文件后，可以从文件中读取出来，并且对它进行反序列化，即：可以生成一个新的一模一样的对象。

序列化的整个过程都是JVM独立的，在不同平台上可以序列化和反序列化该对象。

类**ObjectInputStream**和**ObjectOutputStream**是高层次的数据流，他们拥有着序列化和反序列化的对象的方法。

> ObjectOutputStream类包含了很多方法用来输出各种数据类型，但是一个特别的方法例外
>```java
>public final void writeObject(Object x) throws IOException
>```
>这个方法用来序列化一个对象，并把它发送到输出流中。类似的 ObjectInputStream 类包含了一个反序列化的方法
>```java
>public final Object readObject() throws IOException, ClassNotFoundException
>```

## 示例
employee.java
```java
public class Employee implements Serializable {

    public String name;
    public String address;
    public transient int SSN;
    public int number;

    public void testSerializable(){
        System.out.println(name + ":" + address);
    }
}
```
SerializeDemo.java
```java
public class SerializeDemo {

    public static void main(String[] args) {
        Employee employee = new Employee();
        employee.name = "无敌大大";
        employee.address = "火星球水国木村二河道一户";
        employee.SSN = 11223344;
        employee.number = 110;

        try{

            FileOutputStream fileOutputStream = new FileOutputStream("F:/tem/employee.ser");
            ObjectOutputStream objectOutputStream = new ObjectOutputStream(fileOutputStream);
            objectOutputStream.writeObject(employee);
            objectOutputStream.close();
            fileOutputStream.close();
            System.out.println("序列化完成");
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
```

DeserializeDemo.java
```java
public class DeserializeDemo {

    public static void main(String [] args)
    {
        Employee e = null;
        try
        {
            FileInputStream fileIn = new FileInputStream("F:/tem/employee.ser");
            ObjectInputStream in = new ObjectInputStream(fileIn);
            e = (Employee) in.readObject();
            in.close();
            fileIn.close();
        }catch(IOException i)
        {
            i.printStackTrace();
            return;
        }catch(ClassNotFoundException c)
        {
            System.out.println("Employee class not found");
            c.printStackTrace();
            return;
        }
        System.out.println("Deserialized Employee...");
        System.out.println("Name: " + e.name);
        System.out.println("Address: " + e.address);
        System.out.println("SSN: " + e.SSN);
        System.out.println("Number: " + e.number);
    }
}
```




## transient 关键词
 被 该关键词修饰的属性不会序列化，因为该属性是短暂的，该值没有被发送到输出流。
