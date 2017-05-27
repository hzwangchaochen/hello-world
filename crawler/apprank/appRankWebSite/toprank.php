<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<head>
<title>DP ranktop</title>
<script language="javescript" type="text/javascript" src="ajaxpage.js"></script>
<script language="javascript" type="text/javascript" src="testcompareinput.js"></script>
<style type="text/css">
<!--
a:link{text-decoration:none; color:#1E90FF}
a:active{text-decoration:none;color:#9400D3}
a:hover{text-decoration:underline;color:#9400D3}
a:visited{text-decoraion:none;color:#1E90FF}
-->
</style>
</head>

<body>
<div id="result">
<?php 
include("constant.php");
require("showfunc.php");
function check_date()
{
   //check if db has today's records 
   $rsc_date = mysql_query("SELECT max(cast(date as date)) as date from ranklist");
   $date_db = mysql_result($rsc_date,0,"date");
   $date_OS = date("Y-m-d");
//   if($date_db != $date_OS)
//   {
//        echo "date error";
//   }
//   else 
//   {
        return $date_db;
//   }
}
function get_page($page,$pagenum)
{
    //deal input page which is over-range 
    if($page < 1 || $page > $pagenum)
    {
        $page = 1;
    }
    return $page;
}
function get_ranknum($date)
{
    //get the total num of gamerank list
    if ($date)
    {
        $result = mysql_query("select distinct gameid,dp,date,rank from ranklist where date=\"$date\" order by rank desc");
    }
    $total = mysql_num_rows($result) or die(mysql_error());
    return $total;
}
function tag_all()
{
    //get array holds all tags group by type  
    for($l=1; $l<8; $l++)
    {
        $tag_all_show[$l]=array();
        $rs=mysql_query("select tagid from tagindex where tagtype=$l");
        while($row = mysql_fetch_array($rs))
        {
            array_push($tag_all_show[$l],$row[0]);
        }
    }
    return $tag_all_show;
}
//get array holds chinese titles 
$title=get_title();
$con = dbconnection();   
$date = check_date();
//get array holds tags and tagnames
$tag_result=get_tags();
$tag_name=$tag_result[1];
$tag_all_show=tag_all();
//count records of toplist
$total=get_ranknum($date);
//show 163 list
$rank_163_info = get163games($date);
//varables to show page show dynamic
$page=isset($_GET['page'])?intval($_GET['page']):1;
$page_size=25; 
$pagenum=ceil($total/$page_size);  
$page=get_page($page,$pagenum);
$pageset=($page-1)*$page_size;
//page line to display 
$pagenav='';
$pagenav.="显示第"."<font color='#000080'>".($total?($pageset+1):0)."-".min($pageset+$page_size,$total)."</font>"."记录&nbsp;共"."<b><font 
color='#000080'>".$total."</font></b>"."条记录&nbsp;现在是第&nbsp;"."<b><font color='#C71585'>".$page."</font></b>&nbsp;页&nbsp;";
$pagenav.="共"."<font color='#000080'>".$pagenum."</font>"."页";
?>

<table border="0" frame="void">
<td border="0" width="40%" align="left">
<table  rules=none > 
   <tr><td colspan="5" align="center"><b><font size='4px' color='#DA70D6'><?php echo $title['rank']['all'];?></font></b></td></tr>
   <tr>
	<td><font color='#000080'>Rank</font></td>	
	<td><font color='#000080'>GameID</font></td>
	<td><font color='#000080'>GameName</font></td>
	<td><font color='#000080'>DP</font></td>
<td><font color='#000080'>Compare</font></td>
   </tr>
  <?php
  $src = "select gameid,dp,date,rank from ranklist where date=\"".$date."\" group by gameid order by rank asc limit ".$pageset.",".$page_size;
  $info=mysql_query($src);
while ($row = mysql_fetch_array($info))
 {
$showGameName=get_gamename($row[0]);
  if ($row[0]!=$qn_id)
  {
        echo "<tr>";
        echo "<td>".$row[3]."</td>";
        echo "<td>".$row[0]."</td>";
        echo "<td><font color='#7B68EE'>".$showGameName."</font></td>";
  }
  else
  {
	echo "<tr>";
	echo "<td><B><font color='red'>".$row[3]."</font></B></td>";
	echo "<td><B><font color='red'>".$row[0]."</font></B></td>";
	echo "<td><B><font color='red'>".$showGameName."</font></B></td>";
  }

  ?>
  <td>
      <B>
	<a href="dptrace.php?gameid=<?=$row[0]?>" target="_blank"><?=$row[1]?></a>
      </B> 
  </td>
<td>
      <input  type="button" style="cursor:hand" onclick="javascript:Insert('<?=$row[0]?>'+';')" value="<?=$row[0]?> " /> 
  </td>
<?php
  echo "</tr>";
}
?>
<tr>
  <td colspan="5" align="left">
    <?php
      echo $pagenav;
    ?>
        <a href="toprank.php?page=1"><?php echo $title['page']['first'];?></a>
        <a href="toprank.php?page=<?php if($page>1) echo $page-1;else echo "1";?>"><?php echo $title['page']['before'];?></a>
        <a href="toprank.php?page=<?php if($page<$pagenum)echo $page+1;else echo $pagenum;?>"><?php echo $title['page']['next'];?></a>
        <a href="toprank.php?page=<?php echo $pagenum;?>"><?php echo $title['page']['last'];?></a>

        <form style="display:inline"  method="get" action="toprank.php">
          Page:<input style="width=40;height=25" type="text" name="page" id="page" >
        <input style="width=25;height=25" type="submit" name="submit" value="go" > 
        </form></p>
  </td>
</tr>
</table></td>


<td  border="0" width="50%" frame="void" align="left">
<table  width="60%" rules=none>
<tr>
<td>
 <table  border="1" frame="void" align="left" rules=none>
<tr>
<td><b><font color='#8B008B'><?php  echo $title['search']['id'];?></font></b></td>
<td><b><font color='#8B008B'><?php  echo $title['search']['name'];?></font></b></td>
<td><b><font color='#8B008B'><?php  echo $title['search']['compare'];?><font></b></td>
</tr>
<tr>
<td>
        <form action="searchid.php" method="post">
         <input style="width=180" type="text" name="gameid" value="" size="20" /><br />
        <input type="submit" value="Submit" />
        <input type="reset" value="Reset">
        </form>
      </td>
     <td>
        <form action="searchname.php" method="post">
         <input style="width=180" type="text" name="gamename" value="" size="20"/><br />
        <input type="submit"  value="Submit" />
        <input type="reset" value="Reset">
        </form>
     </td>
     <td>
        <form action="comparegames.php" method="post">
        <input  style="width=180" type="text" id="content" name="comparelist" size="20"><br />
        <input type="submit"  value="Submit" onclick="javascript:return CheckInputCompare()"/>
        <input type="reset" value="Reset">
        </form>
     </td></tr>
</table>
</td>


<tr><td>
<table  border="2" width="90%" rules=none frame=box align="center">
     <tr><td colspan="4" align="center"><b><font color='#DA70D6'><?php echo $title['rank']['163'];?></font></b></td></tr>
     <tr>
     <td><font color='#000080'>Rank</font></td> 
     <td><font color='#000080'>GameID</font></td> 
     <td><font color='#000080'>GameName</font></td> 
     <td><font color='#000080'>DP</font></td> 
     </tr>
<?php
while ($row = mysql_fetch_array($rank_163_info))
{
        if ($row[0]!=$qn_id)
        {
            echo "<tr>";
            echo "<td>".$row[4]."</td>";
            echo "<td>".$row[0]."</td>";
            echo "<td><font color='#7B68EE'>".$row[1]."</font></td>";
        }
        else
        {
                echo "<tr>";
                echo "<td><B><font color='#FF1493'>".$row[4]."</font></B></td>";
                echo "<td><B><font color='#FF1493'>".$row[0]."</font></B></td>";
                echo "<td><B><font color='#FF1493'>".$row[1]."</font></B></td>";
        }
?>
<td><B><font color='#FF1493'>
        <a href="dptrace.php?gameid=<?=$row[0]?>" target="_blank"><?=$row[2]?></a>
</font> </B> </td>

<?php
    echo "</tr>";
}
?>
</table>
</td></tr>
  

<tr>
<td>
<table  width="20%" border="1" frame=void align="left" rules=none>
<tr>
<form action="rankbytag.php" method="post" target="blank">
<b><font color='#8B008B'><?php  echo $title['search']['tag'];?><font></b>
        <input  style="width=150" type="text" id="tag" name="taglist" size="40">
        <input type="text" id="tagid" name="taglist" ></tr>
<tr> 
        <input type="submit"  value="Submit" onclick="javascript:return CheckInputTag()"/>
        <input type="reset" value="Reset"/>
</form>
</tr>
<tr>
     <?php
       $tag="";
     for($l=1;$l <= 7 ;$l++)
     { 
        echo "<td><b><font color='#DA70D6'>$l:</font></b></td>";  
        for($n=0;$n<count($tag_all_show[$l],0) ;$n++)
        {
        $key_tag=$tag_all_show[$l][$n];
        echo "<td border=\"0\" frame=\"void\ style=\"margin-left:20px\">";
        echo "<input type=\"button\" style=\"cursor:hand\" onclick=\"javascript:InsertTag('$tag_name[$key_tag]'+';');InsertTagID('$key_tag'+';')\" value=\"$tag_name[$key_tag]\" /></td>";
        }
        echo "</tr><tr>";
     }
     ?>
     
</tr>
</table>
</td></tr>
<tr><td><b><a href="tagstudio.php" target="_blank"><?php echo $title['addtag']['alltitle'];?>...</a></b></td></tr>
<tr><td><b><a href="newgamerank.php" target="_blank">Newgame on rank, go check...</a></b></td></tr>
</table>

</body>
</html>
