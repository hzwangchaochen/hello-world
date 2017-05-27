import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by hzwangchaochen on 2017/5/14.
 */
public class ArrayPairSum {

    public int arrayPairSum(int[] nums) {
        Arrays.sort(nums);
        int sum=0;
        for(int i=0;i<(nums.length)/2;i++){
            sum=sum+nums[i*2];
        }
        return sum;
    }

    public static void main(String[]args){
        int[]nums=new int[]{1,4,3,2};
        ArrayPairSum aps=new ArrayPairSum();
        System.out.println(aps.arrayPairSum(nums));
    }
}
