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

$channel = $_REQUEST['channel'];

$mysqlStr="";
$mysqlStrCount="";
$countryFrom = "";
$SQLTime="";
//$mysqlStr="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "'";
//$mysqlStrCount = "select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "'";

if ( isset($_REQUEST['starttime_free']) && strval($_REQUEST['starttime_free']) != "" )
{
    $starttime=formatDateTime(strval($_REQUEST['starttime_free']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
    $mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
    $mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_pay']) && strval($_REQUEST['starttime_pay']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_pay']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_sell']) && strval($_REQUEST['starttime_sell']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_sell']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_free_ipad']) && strval($_REQUEST['starttime_free_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_free_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_pay_ipad']) && strval($_REQUEST['starttime_pay_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_pay_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_sell_ipad']) && strval($_REQUEST['starttime_sell_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_sell_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_japan_free']) && strval($_REQUEST['starttime_japan_free']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_japan_free']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_japan_pay']) && strval($_REQUEST['starttime_japan_pay']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_japan_pay']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_japan_sell']) && strval($_REQUEST['starttime_japan_sell']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_japan_sell']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_japan_free_ipad']) && strval($_REQUEST['starttime_japan_free_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_japan_free_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_japan_pay_ipad']) && strval($_REQUEST['starttime_japan_pay_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_japan_pay_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_japan_sell_ipad']) && strval($_REQUEST['starttime_japan_sell_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_japan_sell_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_american_free']) && strval($_REQUEST['starttime_american_free']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_american_free']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'  order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' ";
}
elseif ( isset($_REQUEST['starttime_american_pay']) && strval($_REQUEST['starttime_american_pay']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_american_pay']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_american_sell']) && strval($_REQUEST['starttime_american_sell']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_american_sell']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_american_free_ipad']) && strval($_REQUEST['starttime_american_free_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_american_free_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'  order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' ";
}
elseif ( isset($_REQUEST['starttime_american_pay_ipad']) && strval($_REQUEST['starttime_american_pay_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_american_pay_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_american_sell_ipad']) && strval($_REQUEST['starttime_american_sell_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_american_sell_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_korea_free']) && strval($_REQUEST['starttime_korea_free']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_korea_free']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_korea_pay']) && strval($_REQUEST['starttime_korea_pay']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_korea_pay']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_korea_sell']) && strval($_REQUEST['starttime_korea_sell']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_korea_sell']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_korea_free_ipad']) && strval($_REQUEST['starttime_korea_free_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_korea_free_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_korea_pay_ipad']) && strval($_REQUEST['starttime_korea_pay_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_korea_pay_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_korea_sell_ipad']) && strval($_REQUEST['starttime_korea_sell_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_korea_sell_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_taiwan_free']) && strval($_REQUEST['starttime_taiwan_free']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_taiwan_free']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_taiwan_pay']) && strval($_REQUEST['starttime_taiwan_pay']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_taiwan_pay']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_taiwan_sell']) && strval($_REQUEST['starttime_taiwan_sell']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_taiwan_sell']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_taiwan_free_ipad']) && strval($_REQUEST['starttime_taiwan_free_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_taiwan_free_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_taiwan_pay_ipad']) && strval($_REQUEST['starttime_taiwan_pay_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_taiwan_pay_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_taiwan_sell_ipad']) && strval($_REQUEST['starttime_taiwan_sell_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_taiwan_sell_ipad']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif (isset($_REQUEST['starttime_qq']) && strval($_REQUEST['starttime_qq']) != "")
{
	$starttime = formatDateTime(strval($_REQUEST['starttime_qq']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif (isset($_REQUEST['starttime_360']) && strval($_REQUEST['starttime_360']) != "")
{
	$starttime = formatDateTime(strval($_REQUEST['starttime_360']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif (isset($_REQUEST['starttime_91']) && strval($_REQUEST['starttime_91']) != "")
{
	$starttime = formatDateTime(strval($_REQUEST['starttime_91']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif (isset($_REQUEST['starttime_baidu']) && strval($_REQUEST['starttime_baidu']) != "")
{
	$starttime = formatDateTime(strval($_REQUEST['starttime_baidu']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
elseif (isset($_REQUEST['starttime_google']) && strval($_REQUEST['starttime_google']) != "")
{
	$starttime = formatDateTime(strval($_REQUEST['starttime_google']));
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}
else
{
	$starttime=$yesterday;
	$SQLTime=substr($starttime,0,7);
	$SQLTime=str_replace("-","_",$SQLTime);
	$mysqlStr ="select * from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount ="select count(*) from NewappRank_".$SQLTime." where channel = '" . $channel . "' and rankDate like '" . $starttime . "%'";
}



$offset = ($page-1)*$rows;

$result = array();


$rs = mysql_query($mysqlStrCount,$con);
$row = mysql_fetch_row($rs);
$result["total"] = $row[0];

$mysqlStr=$mysqlStr . " limit $offset,$rows";
$rs = mysql_query($mysqlStr);

$Rows = array();
while($row = mysql_fetch_object($rs))
{
	/*
	$str1 = "select * from NewappRank_".$SQLTime." where gameName = '" . $row->gameName . "' and rankDate like '" . $starttime . "%'";
	$result1 = mysql_query($str1);
	$row->other = "";
	while($row1 = mysql_fetch_object($result1))
	{
		$row->other = $row->other . $row1->channel . "," . $row1->ranking . ";" ;
	}
*/
	array_push($Rows, $row);
}
$result["rows"] = $Rows;
echo json_encode($result);

?>
