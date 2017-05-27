<?php
include '../common/common.php';
include '../common/conn.php';

include '../PHPExcel/PHPExcel.php';
include '../PHPExcel/PHPExcel/Writer/Excel2007.php';
$personData=$_POST["rows"];
//file_put_contents("zjtest", $personData, FILE_APPEND);
$qanames = json_decode($personData, true);


$objPHPExcel = new PHPExcel();

// Set properties
$objPHPExcel->getProperties()->setCreator("qiannv");
$objPHPExcel->getProperties()->setLastModifiedBy("qiannv");
$objPHPExcel->getProperties()->setTitle("网易手游");
$objPHPExcel->getProperties()->setSubject("网易手游");
$objPHPExcel->getProperties()->setDescription("网易手游");

// Add some data
$objPHPExcel->setActiveSheetIndex(0);
$rowline=1;
$objPHPExcel->getActiveSheet()->SetCellValue('A' . $rowline, "gameName");
$objPHPExcel->getActiveSheet()->SetCellValue('B' . $rowline, "channel");
$objPHPExcel->getActiveSheet()->SetCellValue('C' . $rowline, "rank");
$objPHPExcel->getActiveSheet()->SetCellValue('D' . $rowline, "date");
$objPHPExcel->getActiveSheet()->getColumnDimension('A')->setWidth(60);    
$objPHPExcel->getActiveSheet()->getColumnDimension('B')->setWidth(10);  
$rowline=$rowline+1;


foreach($qanames as $a)
{
	//echo 			'<option>' . $a["QAer"] . '</option>';
		$objPHPExcel->getActiveSheet()->SetCellValue('A' . $rowline, (string)$a["gameName"]);
		$objPHPExcel->getActiveSheet()->SetCellValue('B' . $rowline, (string)$a["channel"]);
		$objPHPExcel->getActiveSheet()->SetCellValue('C' . $rowline, (string)$a["ranking"]);
		$objPHPExcel->getActiveSheet()->SetCellValue('D' . $rowline, (string)$a["rankDate"]);
		$rowline=$rowline+1;
}


$objPHPExcel->getActiveSheet()->setTitle('网易手游');

// Rename sheet
$file_name="NetEase_Game_Rank__" . date("YmdH") . ".xlsx";
$objWriter = new PHPExcel_Writer_Excel2007($objPHPExcel);
$objWriter->save($file_name);
echo $file_name

?>
