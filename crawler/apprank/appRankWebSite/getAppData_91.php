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





$page = isset($_REQUEST['page']) ? intval($_REQUEST['page']) : 1;
$rows = isset($_REQUEST['rows']) ? intval($_REQUEST['rows']) : 20;

$sort = isset($_REQUEST['sort']) ? strval($_REQUEST['sort']) : 'ranking';
//$order = isset($_REQUEST['order']) ? strval($_REQUEST['order']) : 'asc';
if ( isset($_REQUEST['order']) )
{
	if( $_REQUEST['order'] == 'asc')
	{
		$order = 'desc';
	}
	else
	{
		$order = 'asc';
	}
}
else
{
	$order='asc';
}

$yesterday = date("Y-m-d",mktime(0,0,0,date("m"),date("d")-1,date("Y")));
$now = date("Y-m-d H:i",mktime(date("H"),date("i"),date("s"),date("m"),date("d"),date("Y")));

$mysqlStr="";
$mysqlStrCount="";


$yesterday = date("Y-m-d",mktime(0,0,0,date("m"),date("d")-1,date("Y")));
$now = date("Y-m-d H:i",mktime(date("H"),date("i"),date("s"),date("m"),date("d"),date("Y")));

$starttime = isset($_REQUEST['starttime_91']) ? formatDateTime(strval($_REQUEST['starttime_91'])) : "$yesterday";

$tableName = "channel_91";

$mysqlStr="select * from " . $tableName . "  where gameName is not null and rankDate like '" . $starttime . "%' order by $sort $order";
$mysqlStrCount="select count(*) from " . $tableName . "  where gameName is not null and rankDate like '" . $starttime . "%'";


//echo $mysqlStr;
$offset = ($page-1)*$rows;

$result = array();

$tables=array("ios_china_free","ios_china_pay","ios_china_sell","ipad_china_free","ipad_china_pay","ipad_china_sell","ipad_japan_free","ipad_japan_sell","ipad_japan_pay","ipad_korea_sell","ipad_korea_free","ipad_korea_pay","ipad_american_free","ipad_american_pay","ipad_american_sell","ios_taiwan_free","ios_taiwan_pay","ios_taiwan_sell","ipad_taiwan_sell","ipad_taiwan_free","ipad_taiwan_pay","ios_japan_sell","ios_japan_free","ios_japan_pay","ios_korea_free","ios_korea_pay","ios_korea_sell","ios_american_sell","ios_american_free","ios_american_pay","channel_91","channel_360","channel_qq");
//file_put_contents("zjtest", $mysqlStr, FILE_APPEND);

$rs = mysql_query($mysqlStrCount,$con);
$row = mysql_fetch_row($rs);
$result["total"] = $row[0];

$mysqlStr=$mysqlStr . " limit $offset,$rows";
$rs = mysql_query($mysqlStr);

$Rows = array();
while($row = mysql_fetch_object($rs)){
	$localstr = "select description,website from appGameName where gameName = '" . $row->gameName . "'";
	$localrs = mysql_query($localstr,$con);
	$localrow = mysql_fetch_object($localrs);
	$row->description=$localrow->description;
	$row->website = $localrow->website;
	for( $i=0;$i<sizeof($tables)-1;$i++)
	{
		if ( ! strstr($tables[$i],$countryFrom) )
		{
			$str1 = "select ranking from " . $tables[$i] . " where gameName = '" . $row->gameName . "' and rankDate like '" . $starttime . "%'";
			//$str1 = "select ranking from " . $tables[$i] . " where gameName = '" . "Plague Inc." . "'";
			$result1 = mysql_query($str1);
			$row1 = mysql_fetch_array($result1);
			if( $row1 && $row1['ranking'] != "" )
			{
				if ( $tables[$i] == "ios_china_free" )
				{
					$row->chinafree=$row1['ranking'];
				}
				elseif( $tables[$i] == "ios_china_sell" )
				{
					$row->chinasell=$row1['ranking'];
				}
				elseif ( $tables[$i] == "ios_china_pay" )
				{
					$row->chinapay=$row1['ranking'];
				}
				elseif ( $tables[$i] == "channel_91" )
				{
					$row->nineone=$row1['ranking'];
				}
				elseif ( $tables[$i] == "channel_360" )
				{
					$row->weishi=$row1['ranking'];
				}
				elseif( $tables[$i] == "channel_qq" )
				{
					$row->qq=$row1['ranking'];
				}
				elseif( $tables[$i] == "ipad_china_free" )
				{
					$row->chinafreeipad=$row1['ranking'];
				}
				elseif( $tables[$i] == "ipad_china_sell" )
				{
					$row->chinasellipad=$row1['ranking'];
				}
				elseif( $tables[$i] == "ipad_china_pay" )
				{
					$row->chinapayipad=$row1['ranking'];
				}
				elseif( $tables[$i] == "ipad_taiwan_free" )
				{
					$row->taiwanfreeipad=$row1['ranking'];
				}
				elseif( $tables[$i] == "ipad_taiwan_sell" )
				{
					$row->taiwansellipad=$row1['ranking'];
				}
				elseif( $tables[$i] == "ipad_taiwan_pay" )
				{
					$row->taiwanpayipad=$row1['ranking'];
				}
				elseif( $tables[$i] == "ios_taiwan_free" )
				{
					$row->taiwanfree=$row1['ranking'];
				}
				elseif( $tables[$i] == "ios_taiwan_sell" )
				{
					$row->taiwansell=$row1['ranking'];
				}
				elseif( $tables[$i] == "ios_taiwan_pay" )
				{
					$row->taiwanpay=$row1['ranking'];
				}
			}

		}
	}
	array_push($Rows, $row);
}
$result["rows"] = $Rows;
echo json_encode($result);

?>
