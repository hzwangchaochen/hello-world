import java.util.HashMap;
import java.util.Random;

/**
 * Created by hzwangchaochen on 2017/5/14.
 */
public class Codec {
    HashMap<String, String> hashToUrl=new HashMap<>();
    HashMap<String,String> urlToHash=new HashMap<>();

    String tinyUrlBase="http://tinyurl.com/";
    String characters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    Random random =new Random();


    public String encode(String longUrl){
        if(urlToHash.containsKey(longUrl))
            return tinyUrlBase+urlToHash.get(longUrl);

        StringBuilder hash=new StringBuilder();

        do{
            for(int i=0;i<6;i++){
                hash.append(characters.charAt(random.nextInt(characters.length())));
            }
        }while(urlToHash.containsValue(hash.toString()));
        urlToHash.put(longUrl,hash.toString());
        hashToUrl.put(hash.toString(),longUrl);
        return tinyUrlBase+hash.toString();
    }

    public String decode(String shortUrl){
        return hashToUrl.get(shortUrl.substring(tinyUrlBase.length()));

    }
    public static void main(String []args){
        String url="https://leetcode.com/problems/design-tinyurl";
        Codec codec = new Codec();

        System.out.println(codec.decode(codec.encode(url)));
    }
}
