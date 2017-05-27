<?php
header("Content-Type: application/text; charset=utf-8");
include '../common/conn_rank.php';
include '../common/common.php';

$gameNameStr = $_POST["gameNameStr"];
$channel = $_POST["channel"];
$option = $_POST["option"];

$gameNames = explode("||",$gameNameStr);

$result=array();
$time = $_SERVER['REQUEST_TIME'];

if($option=="1")
{
	$SQLTime1=date("Y_m", strtotime("-1 months",$time));
	$SQLTime2=date("Y_m", $time);
	$startTime=date("Y-m-d", strtotime("-1 months",$time));
	for($i =0 ;$i<sizeof($gameNames)-1;$i++)
	{
		$gameName = $gameNames[$i];
		$everydayResult=array();

		$mysqlStr = "select * from NewappRank_".$SQLTime1." where gameName = '" . $gameName . "' and channel='" . $channel . "'and rankDate>'".$startTime."' order by rankDate";
		$rs = mysql_query($mysqlStr);
		while($row = mysql_fetch_object($rs))
		{
			$everydayResult[substr($row->rankDate,5,5)] = $row->ranking;
		}
		$mysqlStr = "select * from NewappRank_".$SQLTime2." where gameName = '" . $gameName . "' and channel='" . $channel  . "'order by rankDate";
		$rs = mysql_query($mysqlStr);
		while($row = mysql_fetch_object($rs))
		{
			$everydayResult[substr($row->rankDate,5,5)] = $row->ranking;
		}
		$result[$gameName] = $everydayResult;
	}
	echo json_encode($result);
}

else if($option=="2")
{
	for($i =0 ;$i<sizeof($gameNames)-1;$i++)
	{
		$gameName = $gameNames[$i];
		$everydayResult=array();	
		for($j=12;$j>=0;$j--)
		{
			$SQLTime=date("Y_m", strtotime("-".$j." months", $time));
			$mysqlStr = "select * from NewappRank_".$SQLTime." where gameName = '" . $gameName . "' and channel='" . $channel . "'order by rankDate";
			$rs = mysql_query($mysqlStr);
			while($row = mysql_fetch_object($rs))
			{
				$everydayResult[substr($row->rankDate,5,5)] = $row->ranking;
			}
		}
		$result[$gameName] = $everydayResult;
		
	}
	echo json_encode($result);
}

?>
