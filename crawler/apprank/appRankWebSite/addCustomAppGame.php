<?php

$personName=$_POST["personName"];
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
	$mysqlStr = "INSERT INTO customMade(personName,gameName) values('$personName','$gameName')";
	mysql_query($mysqlStr);
	//file_put_contents("zjtest", $mysqlStr, FILE_APPEND);
}
