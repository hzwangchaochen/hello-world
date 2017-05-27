<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<head>
<title>TestCompare</title>
<script language="javascript">
	//移动光标到最后
	var setPos=function(o){
		if(o.setSelectionRange){//W3C
			setTimeout(function(){
				o.setSelectionRange(o.value.length,o.value.length);
				o.focus();
			},0);
		}else if(o.createTextRange){//IE
			var textRange=o.createTextRange();
			textRange.moveStart("character",o.value.length);
			textRange.moveEnd("character",0);
			textRange.select();
		}
	};
function Insert(str) { 
	var obj = document.getElementById('content'); 
	setPos(obj);
	if(document.selection) { 
		obj.focus(); 
		var sel=document.selection.createRange(); 
		document.selection.empty(); 
		sel.text = str; 
	} else { 
		var prefix, main, suffix; 
		prefix = obj.value.substring(0, obj.selectionStart); 
		main = obj.value.substring(obj.selectionStart, obj.selectionEnd); 
		suffix = obj.value.substring(obj.selectionEnd);
		obj.value = prefix +  str +  suffix; 
	} 
	obj.focus(); 
}         

function CheckInput(){
	var input = document.getElementById('content').value;
	if (input == ''){
		alert("不能为空");
		return false;
	}
	else{
		var num = 0 , i = 0;		
		for (i=0; i<input.length; i++)
			if (input[i]==';') num++;
		if (num>5){
			alert("请不要超过五个选项");
			return false;
		
		else{
			return true;
		}
	}
	return false;	
}
</script>
</head>

<body>
<?php 
include("constant.php");
require("showfunc.php");
$result = toprank($qn_id);
?>

<form action="comparegames.php" method="post">
Compare Games:
<label>
       <input type="text" id="content" name="comparelist" size="60"></textarea>
</label>
<input type="submit"  value="have a compare" onclick="javascript:return CheckInput()"/>
</form>

<table  border="1" width="600"> 
<tr>
	<td width="100">Rank</td>	
	<td>GameID</td>
	<td>GameName</td>
	<td>DP</td>
	<td>Compare</td>
</tr>
<?php
while ($row = mysql_fetch_array($result))
{
        $gameName = get_game($row[0]);
	if ($row[0]!=$qn_id)
	{
	    echo "<tr>";
	    echo "<td>".$row[4]."</td>";
	    echo "<td>".$row[0]."</td>";
	    echo "<td>".$gameName."</td>";
	}
	else
	{
		echo "<tr>";
		echo "<td><B><font color='red'>".$row[4]."</font></B></td>";
		echo "<td><B><font color='red'>".$row[0]."</font></B></td>";
		echo "<td><B><font color='red'>".$gameName."</font></B></td>"; 
	}
?>
<td><B><font color='red'>
	<a href="dptrace.php?gameid=<?=$row[0]?>" target="_blank"><?=$row[2]?></a>
</font> </B> </td>
<td>
<input  type="button" style="cursor:hand" onclick="javascript:Insert('<?=$row[0]?>'+';')" value="<?=$row[0]?> " /> 
</td>
<?php
    echo "</tr>";
}
?>
</table>
</body>
</html>
