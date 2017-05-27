import java.util.Arrays;
import java.util.Comparator;

/**
 * Created by hzwangchaochen on 2017/5/16.
 */

class Person{
    String name;
    int age;
    public Person(String name,int age) {
        this.name = name;
        this.age = age;
    }
}
public class PersonComparator implements Comparator<Person>{

    public int compare(Person a,Person b){
        return a.age-b.age;
    }

    public static void main(String [] args){
        Person a=new Person("a",10);
        Person b=new Person("b",15);
        Person[] pc=new Person[]{new Person("a",15),new Person("a",10),new Person("a",20)};
        Arrays.sort(pc,new PersonComparator());
        for (Person pcc : pc){
            System.out.println(pcc.age);
        }

    }
}
