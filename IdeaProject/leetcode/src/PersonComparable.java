import java.util.Arrays;
/**
 * Created by hzwangchaochen on 2017/5/16.
 */

public class PersonComparable implements Comparable<PersonComparable> {
    String name;
    int age;
    public PersonComparable(String name, int age)
    {
        this.name = name;
        this.age = age;
    }
    public int compareTo(PersonComparable o){
        return this.age-o.age;
    }

    public static void main(String[] args){
        PersonComparable ct1=new PersonComparable("ct1",10);
        PersonComparable ct2=new PersonComparable("ct2",20);
        PersonComparable [] ct=new PersonComparable[]{new PersonComparable("ct1",1),new PersonComparable("ct1",10),new PersonComparable("ct1",5)};
        Arrays.sort(ct);
        for (PersonComparable ctt : ct){
            System.out.println(ctt.age);
        }
    }
}


