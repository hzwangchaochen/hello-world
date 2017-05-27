
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

function draw_compare_DP($tempFileName,$gameNameArray)
{
	$rankname = "./pic4app/".$tempFileName.".txt";

    $str = "set terminal png size 550,450 font \"./simsun.ttc,12\" \n";
    $str.= "set output \"./pic4app/". $tempFileName .".png\"\n";

    $str.= "set xdata time\n";
	$str.= "set xlabel 'date'\n";

    $str.= "set timefmt \"%Y-%m-%d\"\n";
	$str.= "set format x \"%m-%d\"\n";
	//$str.= "set mxtics 0\n";

	$str.= "set ylabel 'rank'\n";

	$str.= "plot ";
	for($i=0;$i<sizeof($gameNameArray)-1;$i++)
	{
		if ($i!=0)
			$str.=",";
		$str.= " \"".$rankname."\" using 1:".($i+2)." title \"".$gameNameArray[$i]."\" with linespoints smooth csplines ";				

	}
	$str.="\n";
	
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

$con = mysql_connect("192.168.131.82","gamerank","gamerank");
mysql_query('SET NAMES utf8');
if (!$con)
{
	echo "mysql connect error";
	return;
}

mysql_select_db("gamerank",$con);


$filename = "./pic4app/" . $tempFileName . ".txt";
$write = fopen($filename , "w+");

$str = "";
$str .= "#date " . "rank\n";


$map = array();

if ( isset($_GET["gameNameStr"]) && (string)$_GET["gameNameStr"] != "" )
{
	$gameNameStr = $_GET["gameNameStr"];
	$gameNameArray = explode('|',$gameNameStr);
	for($i=0;$i<sizeof($gameNameArray)-1;$i++)
	{
		$mysqlStr = "select * from " . $tableName . " where gameName is not null ";
		$mysqlStr .= " and gameName='" . $gameNameArray[$i] . "'";
		$result = mysql_query($mysqlStr);
		while ($row = mysql_fetch_array($result))
		{
			if( $tableName == "selfrank" )
			{
				$map[$row['rankDate']][$row['gameName']] = $row['selfrank'];
			}
			else
			{
				$map[$row['rankDate']][$row['gameName']] = $row['ranking'];
			}
		}
	}
	foreach($map as $key1 => $value1)
	{
		$str = $str . substr($key1,0,10);
		for($j=0;$j<sizeof($gameNameArray)-1;$j++)
		{
			if( $value1[$gameNameArray[$j]] )
			{
				$str = $str . " " . "-" . (string)$value1[$gameNameArray[$j]];
			}
			else
			{
				$str = $str . " " . " ";
			}
		}
		$str = $str . "\n";
	}
	fwrite($write, $str);
	fclose($write);
}
else
{
	return;
}

//file_put_contents("zjtest", $mysqlStr, FILE_APPEND);


$pltname = draw_compare_DP($tempFileName,$gameNameArray);
exec_gluplot($pltname);
echo "下面是  " . str_replace("|","   ",$gameNameStr) . "的排名对比图：";
echo "<br>";
echo "<br>";
$str = "<img src=\"./pic4app/" . $tempFileName . ".png\"/>";
echo $str;
echo '<br>';
echo '<br>';
?>


<table  border="1" width="500"> 
<tr>
	<?php
	  for($i=0;$i<sizeof($gameNameArray)-1;$i++)
	  {
		echo "<td width='100'>".$gameNameArray[$i]."</td>";
	  }
	?>
	<td width="120">rankDate</td>
</tr>
<?php

	foreach($map as $key1 => $value1)
	{
		echo "<tr>";
		for($j=0;$j<sizeof($gameNameArray)-1;$j++)
		{
			if( $value1[$gameNameArray[$j]] )
			{
				echo "<td>".$value1[$gameNameArray[$j]]."</td>";
			}
			else
			{
				echo "<td></td>";
			}
		}
		echo "<td>".$key1."</td>";
		echo "<tr>";
	}

mysql_close($con);

?>

</body>
</html>
