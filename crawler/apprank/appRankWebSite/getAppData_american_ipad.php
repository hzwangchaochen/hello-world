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

if ( isset($_REQUEST['type_american_sell_ipad']) )
{
	$mysqlStr="select * from ipad_american_sell where gameName is not null";
	$mysqlStrCount = "select count(*) from ipad_american_sell where gameName is not null";
}
elseif ( isset($_REQUEST['type_american_free_ipad']) )
{
	$mysqlStr="select * from ipad_american_free where gameName is not null";
	$mysqlStrCount = "select count(*) from ipad_american_free where gameName is not null";
}
elseif( isset($_REQUEST['type_american_pay_ipad']) )
{
	$mysqlStr="select * from ipad_american_pay where gameName is not null";
	$mysqlStrCount = "select count(*) from ipad_american_pay where gameName is not null";
}

if ( isset($_REQUEST['starttime_american_free_ipad']) && strval($_REQUEST['starttime_american_free_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_american_free_ipad']));
	$mysqlStr =$mysqlStr . " and rankDate like '" . $starttime . "%'  order by $sort $order";
	$mysqlStrCount =$mysqlStrCount . " and rankDate like '" . $starttime . "%' ";
}
elseif ( isset($_REQUEST['starttime_american_pay_ipad']) && strval($_REQUEST['starttime_american_pay_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_american_pay_ipad']));
	$mysqlStr =$mysqlStr . " and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount =$mysqlStrCount . " and rankDate like '" . $starttime . "%'";
}
elseif ( isset($_REQUEST['starttime_american_sell_ipad']) && strval($_REQUEST['starttime_american_sell_ipad']) != "" )
{
	$starttime=formatDateTime(strval($_REQUEST['starttime_american_sell_ipad']));
	$mysqlStr =$mysqlStr . " and rankDate like '" . $starttime . "%' order by $sort $order";
	$mysqlStrCount =$mysqlStrCount . " and rankDate like '" . $starttime . "%'";
}
else
{
	$starttime=$yesterday;
	$mysqlStr =$mysqlStr . " and rankDate like '" . $starttime . "%'order by $sort $order";
	$mysqlStrCount =$mysqlStrCount . " and rankDate like '" . $starttime . "%'";
}

$offset = ($page-1)*$rows;

$result = array();

//file_put_contents("zjtest", $mysqlStr, FILE_APPEND);

$rs = mysql_query($mysqlStrCount,$con);
$row = mysql_fetch_row($rs);
//echo $row[0];
$result["total"] = $row[0];

$mysqlStr=$mysqlStr . " limit $offset,$rows";
$rs = mysql_query($mysqlStr);

$Rows = array();
while($row = mysql_fetch_object($rs)){
	array_push($Rows, $row);
}
$result["rows"] = $Rows;
echo json_encode($result);

?>
