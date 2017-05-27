<?php  
require("showfunc.php");
$input=$_REQUEST['comparelist'];
$ids = comparegames($input);
//$pltname = draw_compare_DP($ids);
$name = get_compare_filename($ids);
$pltname = draw_compare_DP($ids);
exec_gluplot($pltname);
?>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Compare Games</title>
</head>

<body>

<table  border="1" width="500"> 
<tr>
	<td width="100">Rank</td>	
	<td width="100">GameID</td>
	<td width="200">GameName</td>
	<td width="120">Date</td>
	<td width="80">DP</td>
</tr>
<?php
$num = count($ids);
for ($jj=0; $jj<$num; $jj++)
{
  $row = getInfoById($ids[$jj]);
  $showgamename = get_gamename($ids[$jj]);
  echo "<tr>";
  echo "<td>".$row[3]."</td>";
  echo "<td>".$row[0]."</td>";
  echo "<td>".$showgamename."</td>";
  echo "<td>".$row[2]."</td>";
  echo "<td><a href=\"dptrace.php?gameid=$row[0]\" target=\"_blank\">".$row[1]."</td>";
  echo "<tr>";
}
?>
</table>
<img src = "./pic/<?=$name?>.png" />
</body>
</html>
