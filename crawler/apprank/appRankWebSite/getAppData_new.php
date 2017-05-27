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


$mysqlStr="";
$mysqlStrCount="";

$time = $_SERVER['REQUEST_TIME'];
$SQLTime=date('Y_m',$time);

$yesterday = date("Y-m-d",mktime(0,0,0,date("m"),date("d")-1,date("Y")));
$now = date("Y-m-d H:i",mktime(date("H"),date("i"),date("s"),date("m"),date("d"),date("Y")));

$starttime = isset($_REQUEST['starttime_new']) ? formatDateTime(strval($_REQUEST['starttime_new'])) : "$yesterday";

$tableName = "NewappGameName";

$mysqlStr="select * from " . $tableName . "  where gameName is not null and addDate like '" . $starttime . "%'";
$mysqlStrCount="select count(*) from " . $tableName . "  where gameName is not null and addDate like '" . $starttime . "%'";

$offset = ($page-1)*$rows;

$result = array();

$rs = mysql_query($mysqlStrCount,$con);
$row = mysql_fetch_row($rs);

$mysqlStr=$mysqlStr . " limit $offset,$rows";
$rs = mysql_query($mysqlStr);
$GameName=array();

while($row = mysql_fetch_object($rs))
{
	array_push($GameName, $row->gameName);
}

$Rows = array();
$gameCount = 0;

$strT  = "select * from NewappRank_".$SQLTime." where rankDate like '" . $starttime . "%'";
$rsT = mysql_query($strT,$con);
while($rowT = mysql_fetch_object($rsT))
{
	if(in_array($rowT->gameName,$GameName))
	{
		array_push($Rows, $rowT);
		$gameCount =$gameCount +1;
	}
}
	//file_put_contents("zjcheck", $strT, FILE_APPEND);

$result["total"] = $gameCount;
$result["rows"] = $Rows;
//file_put_contents("zjcheck", json_encode($result), FILE_APPEND);
echo json_encode($result);

?>
