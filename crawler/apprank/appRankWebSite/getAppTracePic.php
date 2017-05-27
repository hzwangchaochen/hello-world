
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Compare Games</title>
</head>

<body>



<?php

function formatDateTime($timestr){
	if(strstr($timestr,"/")){
		$arrdatetime=explode(' ', $timestr);
		$time=$arrdatetime[1];
		$date=$arrdatetime[0];
		$arrdate=explode('/', $date);
		if(intval($arrdate[0]) <= 9){
			$arrdate[0] = "0" . $arrdate[0];
		}
		if(intval($arrdate[1]) <= 9){
			$arrdate[1] = "0" . $arrdate[1];
		}
		$timestr=$arrdate[2] . "-" . $arrdate[0] . "-" . $arrdate[1] . " " . $time;
	}
	return $timestr;
}

function draw_single_DP($tempFileName)
{
	$rankname = "./pic4app/".$tempFileName.".txt";

	//$str = "set terminal png size 550,450 \n";
	$str.= "set output \"./pic4app/". $tempFileName .".png\"\n";
    //$str.= "set size 1,1 \n";
	$str.= "set xdata time\n";
	$str.= "set xlabel 'date'\n";
	$str.= "set timefmt \"%Y-%m-%d\"\n";
	$str.= "set format x \"%m-%d\"\n";
	//$str.= "set mxtics 0\n";

	$str.= "set ylabel 'rank'\n";
	$str.= "set terminal png \n";
	
	$str.= "plot \"".$rankname."\" using 1:2 ls 1 with linespoints smooth csplines title 'app rank'\n";

	$pltname = "./pic4app/".$tempFileName.".plt";
    $write = fopen($pltname , "w+");
    fwrite($write, $str);
    fclose($write);
	return $pltname;

}

function exec_gluplot($file)
{
	$draw = "gnuplot ".$file;
	exec($draw);
}

$tableName = $_GET['tableName'];
$tempFileName = $_GET['fileName'];

$mysqlStr = "select * from " . $tableName . " where gameName is not null ";

if ( isset($_GET["gameName"]) && (string)$_GET["gameName"] != "" )
{
	$gameName = $_GET["gameName"];
	$mysqlStr .= " and gameName='" . $gameName . "'";
}
else
{
	return;
}



$con = mysql_connect("192.168.131.82","gamerank","gamerank");
mysql_query('SET NAMES utf8');
if (!$con)
{
	echo "mysql connect error";
	return;
}
mysql_select_db("gamerank",$con);


echo $mysqlStr;
//file_put_contents("zjtest", $mysqlStr, FILE_APPEND);
$result = mysql_query($mysqlStr);

$str = "";
$submitCount = Array();
$str .= "#date " . "rank\n";
while ($row = mysql_fetch_array($result))
{
	$str = $str . substr($row['rankDate'],0,10) . " " . "-" . $row['ranking'] . "\n";
}

$filename = "./pic4app/" . $tempFileName . ".txt";
$write = fopen($filename , "w+");
fwrite($write, $str);
fclose($write);

$pltname = draw_single_DP($tempFileName);
exec_gluplot($pltname);
echo "下面是" . $gameName . "的排名趋势图：";
echo "<br>";
echo "<br>";
$str = "<img src=\"./pic4app/" . $tempFileName . ".png\"/>";
echo $str;
echo '<br>';
echo '<br>';
?>


<table  border="1" width="500"> 
<tr>
	<td width="100">Rank</td>	
	<td width="200">gameName</td>
	<td width="120">rankDate</td>
</tr>
<?php
$result = mysql_query($mysqlStr);

while ($row = mysql_fetch_array($result))
{
	if ( $tableName == "selfrank" )
	{
		echo "<tr>";
		echo "<td>".$row['selfrank']."</td>";
		echo "<td>".$row['gameName']."</td>";
		echo "<td>".$row['rankDate']."</td>";
		echo "<tr>";
	}
	else
	{
		echo "<tr>";
		echo "<td>".$row['ranking']."</td>";
		echo "<td>".$row['gameName']."</td>";
		echo "<td>".$row['rankDate']."</td>";
		echo "<tr>";
	}
}

mysql_close($con);
?>
</table>
</body>
</html>
