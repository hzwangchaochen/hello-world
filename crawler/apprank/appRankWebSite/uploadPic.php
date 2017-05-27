<?php
if ($_FILES["file"]["error"]>0)
	{
	echo "Errors:".$_FILES["file"]["error"]."<br />";
	}
else
	{
	echo "Upload:".$_FILES["file"]["name"] ."<br />";
	echo "Type:".$_FILES["file"]["type"] ."<br />";
	echo "Size:".($_FILES["file"]["size"] / 1024). "Kb<br />";
	echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br />";

	$Savepath = "/home/qa/test/picForDB/";
	$Picfile = $Savepath . $_FILES["file"]["name"];	
	echo $Picfile;
	if (file_exists($Picfile))
		{
		echo $_FILES["file"]["name"] . " already exists.";
		}
	else
		{
		move_uploaded_file($_FILES["file"]["tmp_name"], $Picfile);
		echo "Stored in:" . $Picfile;
		}
	}
?>

