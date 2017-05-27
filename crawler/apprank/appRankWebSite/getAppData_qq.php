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


include '../common/conn_rank.php';

$page = isset($_REQUEST['page']) ? intval($_REQUEST['page']) : 1;
$rows = isset($_REQUEST['rows']) ? intval($_REQUEST['rows']) : 100;

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

$mysqlStr="";
$mysqlStrCount="";


$yesterday = date("Y-m-d",mktime(0,0,0,date("m"),date("d")-1,date("Y")));
$now = date("Y-m-d H:i",mktime(date("H"),date("i"),date("s"),date("m"),date("d"),date("Y")));

$starttime = isset($_REQUEST['starttime_qq']) ? formatDateTime(strval($_REQUEST['starttime_qq'])) : "$yesterday";

$tableName = "NewappRank";

$mysqlStr="select * from " . $tableName . " where gameName is not null and rankDate like '" . $starttime . "%' order by $sort $order";
$mysqlStrCount="select count(*) from " . $tableName . "  where gameName is not null and rankDate like '" . $starttime . "%'";


$offset = ($page-1)*$rows;

$result = array();

//file_put_contents("zjcheck", $mysqlStr, FILE_APPEND);

$rs = mysql_query($mysqlStrCount,$con);
$row = mysql_fetch_row($rs);


$mysqlStr=$mysqlStr . " limit $offset,$rows";
$rs = mysql_query($mysqlStr);

$Rows = array();
while($row = mysql_fetch_object($rs)){
	$localstr = "select website from NewappGameName where gameName = '" . $row->gameName . "'";
	$localrs = mysql_query($localstr,$con);
	$localrow = mysql_fetch_object($localrs);
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
$result["total"] = $row[0];
$result["rows"] = $Rows;
echo json_encode($result);

?>
