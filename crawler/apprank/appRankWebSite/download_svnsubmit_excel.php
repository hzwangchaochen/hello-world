<?php
$file_name = $_GET['name'];
$file_path=realpath($file_name);
$file_size=filesize($file_path);
$fp=fopen($file_path,"r"); 
header("Content-type: application/octet-stream"); 
header("Accept-Ranges: bytes");  
header("Accept-Length: $file_size"); 
header("Content-Disposition: attachment; filename=" . urlencode($file_name));
$buffer=1024;
$file_count=0;
while(!feof($fp) && ($file_size-$file_count)>0){
	$file_data=fread($fp,$buffer);
	$file_count+=$buffer;
	echo $file_data;
}
fclose($fp);
?>