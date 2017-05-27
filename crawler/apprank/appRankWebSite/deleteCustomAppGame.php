<?php

$personName=$_POST["personName"];
$country=$_POST["country"];
$gameName=$_POST["gameName"];


$con = mysql_connect("192.168.131.82","gamerank","gamerank");
mysql_query('SET NAMES utf8');
if (!$con)
{
	echo "connect mysql error";
	return;
}
else
{
	mysql_select_db("gamerank",$con);
	$mysqlStr = "delete from customMade where personName = '" . $personName . "' and gameName='" . $gameName . "' and country = '" . $country . "'";

	//file_put_contents("zjtest", $mysqlStr, FILE_APPEND);
	mysql_query($mysqlStr);
}
