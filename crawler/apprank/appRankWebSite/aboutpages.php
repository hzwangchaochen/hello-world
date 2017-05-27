<?php
include_once("constant.php");
require_once("showfunc.php");

$result = toprank($qn_id);
$total=mysql_num_rows($result) or die(mysql_error());
$page=isset($_GET['page'])?intval($_GET['page']):1;
$page_size=30; 
$url = 'toprank.php';

$pagenum=ceil($total/$page_size);
$page=min($pagenum,$page);
$prepage=$page-1;
$nextpage=($page==$pagenum?0:$page+1);
$pageset=($page-1)*$page_size;
$pagenav='';

$pagenav.="显示第<font color='red'>".($total?($pageset+1):0)."-".min($pageset+$page_size,$total)."</font>记录&nbsp;共<b><font 
color='blue'>".$total."</font></b>条记录&nbsp;现在是第&nbsp;<b><font color='blue'>".$page."</font></b>&nbsp;页&nbsp;";

if($page<=1)
	$pagenav.="<a style=cursor:not-allowed;>首页</a>&nbsp;";
else
	$pagenav.="<a onclick=javascript:dopage('result','$url?page=1') style=cursor:pointer;>首页</a>&nbsp;";

if($prepage)
	$pagenav.="<a onclick=javascript:dopage('result','$url?page=$prepage') style=cursor:pointer;>上一页</a>&nbsp;";
else
	$pagenav.="<a style=cursor:not-allowed;>上一页</a>&nbsp;";

if($nextpage)
	$pagenav.="<a onclick=javascript:dopage('result','$url?page=$nextpage') style=cursor:pointer;>下一页</a>&nbsp;";
else
	$pagenav.="<a style=cursor:not-allowed;>下一页</a>&nbsp;";

if($pagenum)
	$pagenav.="<a onclick=javascript:dopage('result','$url?page=$pagenum') style=cursor:pointer;>尾页</a>&nbsp;";
else
	$pagenav.="<a style=cursor:not-allowed;>尾页</a>&nbsp;";

$pagenav.="共".$pagenum."页";

if($page>$pagenum){
    echo "error:没有此页".$page;
    exit();
}


$con = dbconnection();
$result_date = mysql_query("SELECT max(date) as date from ranklist");
$date = mysql_result($result_date,0,"date");
$src = "select * from ranklist where date=\"".$date."\" order by rank asc limit ".$pageset.",".$page_size;
$info=mysql_query($src);
?>
