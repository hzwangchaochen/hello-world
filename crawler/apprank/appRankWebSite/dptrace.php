<?php  
require("showfunc.php");
$type_num=7;
$con=dbconnection();
$title=get_title();
$gameid=$_GET['gameid'];
$add1=$_GET['add'];
$remove1=$_GET['remove'];
for($l=1; $l<=$type_num; $l++)
{
    $tag_all_show[$l]=array();
    $rs=mysql_query("select tagid from tagindex where tagtype=$l");
   while($row = mysql_fetch_array($rs))
   {
     array_push($tag_all_show[$l],$row[0]);
   }
}
if(!empty($add1))
{
    $sql1="update gameindex set ". $add1. "=1 where gameid=". $gameid;
    mysql_query($sql1);
}
if(!empty($remove1))
{
    $sql2="update gameindex set ". $remove1. "=0 where gameid=". $gameid;
    mysql_query($sql2);
}
$result = single_trace($gameid);
$showGameName = get_gamename($gameid);
$allowchange=strstr($showGameName,"img");
$fixname= $_POST['fixname'];
if(!empty($fixname)and $allowchange)
{
    $sql="UPDATE gameindex SET gamename=\"".$fixname ."\" WHERE gameid=". $gameid.";";
    $flag= mysql_query($sql);
}
$tag_resource=mysql_query("select * from tagindex");
while($tag_rs=mysql_fetch_array($tag_resource))
{ 
    $tag_name[$tag_rs['tagid']]=$tag_rs['tagname'];
    $tag_value_std[$tag_rs['tagid']]=1;
}
$sql_gettag="select * from gameindex where gameid=".$gameid; 
$game_tag_resource=mysql_query($sql_gettag);
$result1=mysql_fetch_assoc($game_tag_resource);
$inter=array_intersect_assoc($result1,$tag_value_std);
$diff=array_diff_assoc($tag_value_std,$inter);
$i=0;
$j=0;
$inter_show1=array();
while($key = key($inter))
{
  $inter_show1[$i]= $key;
  next($inter);
  $i++;
}
 while($key = key($diff))
{
  
  $diff_show1[$j]= $key;
  next($diff);
  $j++;
}
for($l=1;$l <= $type_num;$l++)
{
   $inter_show[$l]=array_intersect($tag_all_show[$l],$inter_show1);
   $diff_show[$l]=array_intersect($tag_all_show[$l],$diff_show1);
}
?>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>GameID <?=$gameid?> DP Trace </title>
</head>

<body>
<?php
echo "GameID: <font color='#7B68EE'><b>".$gameid."</b></font>";
echo "  || GameName: <font color='#7B68EE'><b>".$showGameName."</b></font><br></br>";
if(!empty($fixname))
{
if($allowchange)  
 echo "<font color='#C71585'>".$title['fix']['ok'].$fixname."</font>";
else
 echo "<font color='#C71585'>".$title['fix']['no']."</font>";
}
else
echo "   ";
?>
<br></br>
<b><font color='#8B008B'><?php echo $title['fix']['tofix'];?></font></b>
<form action="dptrace.php?gameid=<?php echo $gameid;?>" method="POST">
<input type="text" name="fixname" id="fix" >
<input type="submit" name="submit" value="submit">
</form>
<br></br>
<table frame="box">
<td width="40%" align="left">
<table frame="void"  align="left">
<tr><th align="left"><font color='#8B008B'><?php echo $title['tag']['had']; ?></font></th></tr>
<tr>
<?php 
$deltag="";
for($l=1;$l<=$type_num;$l++)
{
    $deltag.="<td><font size='2px' color='#DA70D6'>$l:".$title['type'][$l]."</font></td></tr><tr>";
    while($now=current($inter_show[$l]))
    {
       $key_inter=$now;
       $deltag.="<td><form frame=\"void\" style=\"display:in line\" action=\"dptrace.php?gameid=$gameid&remove=$key_inter\" method=\"POST\">";
       $deltag.="<input type=\"submit\" name=\"submit\"  value=\"$tag_name[$key_inter]\" ></form></td>";
       next($inter_show[$l]);
    }
$deltag.="</tr><tr>";
}
echo $deltag;
?>  
</td>
</tr>
</table>
</td>
<td width="80%" align="right">


<table frame="void" width="90%" align="center">
      <tr><th align="left"><font color='#8B008B'><?php echo $title['tag']['add']; ?></font></th></tr>
<tr>      
<?php
$addtag="";

for($l=1;$l<=$type_num;$l++)
{
  $addtag.="<td><font size='2px' color='#DA70D6'>$l:".$title['type'][$l]."</font></td></tr><tr>";
   while($now=current($diff_show[$l])) 
   {
      $key_diff=$now;
      $addtag.="<td border=\"0\" frame=\"void\ style=\"margin-left:20px\"><form frame=\"void\" style=\"display:in line\" action=\"dptrace.php?gameid=$gameid&add=$key_diff\" method=\"POST\">";
      $addtag.="<input type=\"submit\" name=\"submit\" value=\"$tag_name[$key_diff]\" ></form></td>";
     next($diff_show[$l]);
   }
   $addtag.="</tr><tr>";
}
echo $addtag;
?>
      
      </tr>
      </table>
</td>
<table>


<table  border="1" width="100%"> 
<tr>
<td width="20%">Date</td>
	<td width="10%">Rank</td>	
	<td width="10%">DP</td>
	<td rowspan = "20"><img src="./pic/<?=$gameid?>.png" /></td>
</tr>

<?php
while ($row = mysql_fetch_array($result))
{
	echo "<tr>";
echo "<td>".$row[2]."</td>";
	echo "<td>".$row[3]."</td>";
	echo "<td>".$row[1]."</td>";
	echo "</tr>";    
}

single_rank($gameid);
$pltname = draw_single_DP($gameid);
exec_gluplot($pltname);
?>
</table>
</body>
</html>
