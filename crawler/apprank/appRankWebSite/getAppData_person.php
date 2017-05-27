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
		$timestr=$arrdate[2] . "-" . $arrdate[0] . "-" . $arrdate[1];
	}
	return $timestr;
}

$con = mysql_connect("192.168.131.82","gamerank","gamerank");
mysql_query('SET NAMES utf8');
if (!$con)
{
	echo "mysql connect error";
	return;
}
mysql_select_db("gamerank",$con);


if( isset($_REQUEST['neteasy']) || $_REQUEST['dataType'] == "neteasy")
{
	$mysqlStr_netease = "select * from NewappGameName where company like '%netease%' or company like '%网易%'";
	$rs = mysql_query($mysqlStr_netease);
	$allNetEaseGame = array();
	while($row = mysql_fetch_object($rs))
	{
		array_push($allNetEaseGame, $row->gameName);
	}


	$sort = isset($_REQUEST['sort']) ? strval($_REQUEST['sort']) : 'ranking';
	$order = isset($_REQUEST['order']) ? strval($_REQUEST['order']) : 'asc';

	$yesterday = date("Y-m-d",mktime(0,0,0,date("m"),date("d")-1,date("Y")));
	$now = date("Y-m-d H:i",mktime(date("H"),date("i"),date("s"),date("m"),date("d"),date("Y")));

	$mysqlStr="";

	$starttime = isset($_REQUEST['starttime']) ? formatDateTime(strval($_REQUEST['starttime'])) : "$yesterday";
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$offset = ($page-1)*$rows;

	$result = array();
	$count = 0;
	$Rows = array();
	$mysqlStr = "select * from NewappRank_".$SQLTime." where rankDate like '" . $starttime . "%' order by " . $sort . " " . $order;
	$rs = mysql_query($mysqlStr);
	while($row = mysql_fetch_object($rs))
	{
		if(in_array($row->gameName,$allNetEaseGame))
		{
			array_push($Rows, $row);
			$count =$count +1;
		}
	}
	$result["rows"] = $Rows;
	$result["total"] = $count;
	echo json_encode($result);
}
elseif( isset($_REQUEST['leocool']) || $_REQUEST['dataType'] == "leocool")
{
	$mysqlStr_netease = "select * from NewappGameName where company like '%leocool%'";
	$rs = mysql_query($mysqlStr_netease);
	$allNetEaseGame = array();
	while($row = mysql_fetch_object($rs))
	{
		array_push($allNetEaseGame, $row->gameName);
	}


	$sort = isset($_REQUEST['sort']) ? strval($_REQUEST['sort']) : 'ranking';
	$order = isset($_REQUEST['order']) ? strval($_REQUEST['order']) : 'asc';

	$yesterday = date("Y-m-d",mktime(0,0,0,date("m"),date("d")-1,date("Y")));
	$now = date("Y-m-d H:i",mktime(date("H"),date("i"),date("s"),date("m"),date("d"),date("Y")));

	$mysqlStr="";

	$starttime = isset($_REQUEST['starttime']) ? formatDateTime(strval($_REQUEST['starttime'])) : "$yesterday";
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$offset = ($page-1)*$rows;

	$result = array();
	$count = 0;
	$Rows = array();

	$mysqlStr = "select * from NewappRank_".$SQLTime." where gameName = '" . $oneAppName . "' and rankDate like '" . $starttime . "%' order by " . $sort . " " . $order;

	$rs = mysql_query($mysqlStr);
	while($row = mysql_fetch_object($rs))
	{
		if(in_array($row->gameName,$allNetEaseGame))
		{
			array_push($Rows, $row);
			$count =$count +1;
		}
	}
	$result["rows"] = $Rows;
	$result["total"] = $count;
	echo json_encode($result);
}
else if( isset($_REQUEST['shuru']) || $_REQUEST['dataType'] == "shuru")
{

	$shuruAppName = trim($_REQUEST['shuru']);

	$sort = isset($_REQUEST['sort']) ? strval($_REQUEST['sort']) : 'ranking';
	$order = isset($_REQUEST['order']) ? strval($_REQUEST['order']) : 'asc';

	$yesterday = date("Y-m-d",mktime(0,0,0,date("m"),date("d")-1,date("Y")));
	$now = date("Y-m-d H:i",mktime(date("H"),date("i"),date("s"),date("m"),date("d"),date("Y")));

	$mysqlStr="";

	$starttime = isset($_REQUEST['starttime']) ? formatDateTime(strval($_REQUEST['starttime'])) : "$yesterday";
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$fiveDaysBefore =  date('Y-m-d',strtotime($starttime) - 3600*24*3);
		//file_put_contents("zjtest",strtotime($starttime), FILE_APPEND);
		//file_put_contents("zjtest",$fiveDaysBefore, FILE_APPEND);

	$offset = ($page-1)*$rows;

	$result = array();
	$count = 0;
	$Rows = array();

	//$mysqlStr = "select * from NewappRank where gameName like '%" . $shuruAppName . "%' and rankDate like '" . $starttime . "%'";
	$mysqlStr2 = "select * from NewappRank_".$SQLTime." where gameName like '%" . $shuruAppName . "%' and rankDate >= '" . $fiveDaysBefore . "' and rankDate <= '" . $starttime . "' order by " . $sort . " " . $order;
		//file_put_contents("zjtest", $mysqlStr2, FILE_APPEND);
	$rs = mysql_query($mysqlStr2);
	while($row = mysql_fetch_object($rs))
	{
		$count =$count +1;
		array_push($Rows, $row);
	}


	$result["rows"] = $Rows;
	$result["total"] = $count;
	echo json_encode($result);
}
else
{

	//$page = isset($_REQUEST['page']) ? intval($_REQUEST['page']) : 1;
	//$rows = isset($_REQUEST['rows']) ? intval($_REQUEST['rows']) : 20;

	$sort = isset($_REQUEST['sort']) ? strval($_REQUEST['sort']) : 'ranking';
	$order = isset($_REQUEST['order']) ? strval($_REQUEST['order']) : 'asc';

	$yesterday = date("Y-m-d",mktime(0,0,0,date("m"),date("d")-1,date("Y")));
	$now = date("Y-m-d H:i",mktime(date("H"),date("i"),date("s"),date("m"),date("d"),date("Y")));

	$mysqlStr="";
	$mysqlStrCount="";

	$starttime = isset($_REQUEST['starttime']) ? formatDateTime(strval($_REQUEST['starttime'])) : "$yesterday";
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	if ( isset($_REQUEST['personName']) )
	{
		$offset = ($page-1)*$rows;

		$result = array();

		$count = 0;
		$row = mysql_fetch_row($rs);

		$mysqlStr = "select * from customMade where personName = '" . $_REQUEST['personName'] . "'";
		$rs = mysql_query($mysqlStr);
		$Rows = array();
		while($row = mysql_fetch_object($rs))
		{
			$tempRows = array();
			//$str = "select * from " . $row->country . " where gameName = '" . $row->gameName . "' and rankDate like '" . $starttime . "%'";
			$str = "select * from NewappRank_".$SQLTime." where gameName = '" . $row->gameName . "' and rankDate like '" . $starttime . "%'";
			//file_put_contents("zjtest", $str, FILE_APPEND);
			$rs2 = mysql_query($str);
			while($row2 = mysql_fetch_object($rs2))
			{
				$count =$count +1;
				array_push($Rows, $row2);
			}
		}
		$result["rows"] = $Rows;
		$result["total"] = $count;
		
		echo json_encode($result);
	}
}
?>
