<?php

function HexToStr($input)
{
    $a=unpack("C*",$input);
    for ($i=1;$i<=count($a);$i++)
    {
        $tmp=DecHex($a[$i]);
        if (strlen($tmp)==1)
            $tmp="0" . $tmp;
        $result.=$tmp;
    }
    return $result;
}



$Date = $_GET["date"];
//$MachineName = $_GET["machine"];
$projectName = $_GET["projectName"];



if($_FILES["file"]["type"] == "application/x-zip-compressed" || $_FILES["file"]["type"] == "application/octet-stream")
{
    if ($_FILES["file"]["error"] > 0)
    {
                echo "Return Code: " . $_FILES["file"]["error"] . "<br />";
    }
        else
    {
                echo "Upload: " . $_FILES["file"]["name"] . "<br />";
                echo "Type: " . $_FILES["file"]["type"] . "<br />";
                echo "Size: " . ($_FILES["file"]["size"] / 1024) . " Kb<br />";
                echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br />";




        $len = strlen($_FILES["file"]["name"]);

                //$SavePath = "uploadedLogs/" . $Date . "/" . $MachineName . "/";
                $SavePath = "../" . $projectName . "/" . $Date . "/";
                $ZipFile = $SavePath . $_FILES["file"]["name"];
                //mkdir($SavePath, 0777, true);
                if (file_exists($ZipFile))
                {
                        echo $ZipFile . " already exists. ";
                }
                else
                {
                        move_uploaded_file($_FILES["file"]["tmp_name"], $ZipFile);
                        $ZipFileName = $_FILES["file"]["name"];
                        echo "Stored in: " . $ZipFile;
                        //`cp logParser.lua $SavePath && cp SendResultMail.py $SavePath && cd $SavePath && unzip -o $ZipFileName && lua -e "timestamp=[[$Date]]" logParser.lua > ErrorMsg.txt && python SendResultMail.py`;
                        `cp logParser.lua $SavePath && cp SendResultMail.py $SavePath && cd $SavePath && unzip -o $ZipFileName && lua -e "timestamp=[[$Date]]" logParser.lua > ErrorMsg.txt && python SendResultMail.py`;
                        echo "logParser finished : " . $Date;
                        $ErrFile = fopen($SavePath . "ErrorMsg.txt","r");
                        $str=fgets($ErrFile);
                        $msg="";
                        while ($str)
                        {
                                $msg = $msg . $str;
                                $str = fgets($ErrFile);
                        }
                        $ResultTxt = $SavePath . "Result.txt";
        
                        $ResultHtml = $SavePath . "Result.html";
                        //`python SendResultMail.py`;
                }
        }
}
else
{


 echo "Invalid file" . $_FILES["file"]["name"] . $_FILES . "\n";
}

