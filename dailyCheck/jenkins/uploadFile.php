<?php
     //echo  $_FILES [ 'myFile' ][ 'name' ];
     /*echo phpinfo();
     echo $_SERVER [ 'DOCUMENT_ROOT' ]. "/Checker/test.txt";
     echo "<br>";
     echo $_SERVER [ 'DOCUMENT_ROOT' ]. "/Checker/LuaXml/test.txt" ;
     echo "<br>";
     if (move_uploaded_file( $_SERVER [ 'DOCUMENT_ROOT' ]. "/Checker/test.txt" , $_SERVER [ 'DOCUMENT_ROOT' ]. "/Checker/LuaXml/test.txt" )){
             echo  "upload image succeed" ;
         } else {
             echo  "upload image failed" ;
     }*/
     if  (isset( $_FILES [ 'myFile' ]))
     {
         $names  =  $_FILES [ "myFile" ][ 'name' ];
         $arr    =  explode ( '.' ,  $names );
         $name   =  $arr [0];  //图片名称
         $date   =  date ( 'Y-m-d H:i:s' );  //上传日期
         $fp     =  fopen ( $_FILES [ 'myFile' ][ 'tmp_name' ],  'rb' );
         $type   =  $_FILES [ 'myFile' ][ 'type' ];
         $filename  =  $_FILES [ 'myFile' ][ 'name' ];
         $tmpname  =  $_FILES [ 'myFile' ][ 'tmp_name' ];
         //将文件传到服务器根目录的 upload 文件夹中
         echo $tmpname;
         echo "<br>";
         echo $_FILES [ 'myFile' ][ 'tmp_name' ];
         echo "<br>";
         if (move_uploaded_file( $tmpname, $_SERVER [ 'DOCUMENT_ROOT' ]. "/Checker/LuaXml/test.jpg" )){
             echo  "upload image succeed" ;
             } 
         else {
             echo  "upload image failed" ;
          }
         
     }
?>
