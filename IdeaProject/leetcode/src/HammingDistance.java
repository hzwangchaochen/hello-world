/**
 * Created by hzwangchaochen on 2017/5/14.
 */
public class HammingDistance {
    public int hammingDistance(int x,int y){
        int res = 0;
        for (int i = 0; i < 32; ++i) {
            int val=1<<i;
            if(val>x && val>y) break;
            if((val&x)!=(val&y)){
                ++res;
            }
        }
        return res;
    }
//    public int hammingDistance(int x,int y){
//        String a=intToBit(x);
//        String b=intToBit(y);
//        System.out.println(a);
//        System.out.println(b);
//        int result=0;
//        for(int i=0;i<32;i++){
//            if(a.charAt(i)!=b.charAt(i)) {
//                result++;
//            }
//        }
//        return result;
//    }
//
//    public String intToBit(int x){
//        StringBuilder sb=new StringBuilder();
//        int index=31;
//        while(index>=0){
//            if(x%2==1)
//                sb.append(1);
//            else
//                sb.append(0);
//            x=x/2;
//            index--;
//        }
//        return sb.reverse().toString();
//    }

    public static void main(String [] args){
        System.out.println(10&2);
        HammingDistance hd=new HammingDistance();
        System.out.println(hd.hammingDistance(10,4));
    }
}
