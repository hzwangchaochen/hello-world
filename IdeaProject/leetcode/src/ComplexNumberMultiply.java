/**
 * Created by hzwangchaochen on 2017/5/24.
 */
public class ComplexNumberMultiply {
    public String complexNumberMultiply(String a,String b){
        String[] aArray=a.split("\\+");
        String[] bArray=b.split("\\+");
        int a1,a2,b1,b2;
        a1=Integer.parseInt(aArray[0]);
        a2=Integer.parseInt(aArray[1].split("i")[0]);
        b1=Integer.parseInt(bArray[0]);
        b2=Integer.parseInt(bArray[1].split("i")[0]);
        int res1=a1*b1-a2*b2;
        int res2=a1*b2+a2*b1;
        StringBuilder sb=new StringBuilder();
        sb.append(res1+"+"+res2+"i");
        //return String.valueOf(res1)+"+"+String.valueOf(res2)+"i";
        return sb.toString();
    }
    public static void main(String[] args){
        ComplexNumberMultiply cnm=new ComplexNumberMultiply();
        System.out.println(cnm.complexNumberMultiply("1+1i","2+2i"));
    }
}
