<?php
if(isset($_COOKIE["nickname"]) && $_COOKIE["nickname"]!=''){
}
else
{
	header("Location:../login/try_auth.php");
	exit;
}
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>app排行榜</title>
    <link href="rankcss/bootstrap.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="rankthemes/default/easyui.css">
    <link rel="stylesheet" type="text/css" href="rankthemes/icon.css">
    <link rel="stylesheet" type="text/css" href="rankcss/demo.css">
	<link rel="stylesheet"  type="text/css" href="rankcss/style.css">

	<link href="rankcss/navbar.css" rel="stylesheet">

    <script type="text/javascript" src="rankjs/jquery.min.js"></script>
    <script type="text/javascript" src="rankjs/jquery.easyui.min.js"></script>
    <script type="text/javascript" src="rankjs/appRank.js"></script>
	<script src="rankjs/bootstrap.js"></script> 

	<!--下面的是解决firefox不支持innerText的问题-->
	<script language="javascript">
	function isIE(){ //ie? 
		if (window.navigator.userAgent.toLowerCase().indexOf("msie")>=1) 
		    return true; 
		else 
		    return false; 
	} 

	if(!isIE()){ //firefox innerText define
	    HTMLElement.prototype.__defineGetter__("innerText", 
	    function(){
	        var anyString = "";
	        var childS = this.childNodes;
	        for(var i=0; i<childS.length; i++) { 
	            if(childS[i].nodeType==1)
	            //anyString += childS[i].tagName=="BR" ? "\n" : childS[i].innerText;
	            anyString += childS[i].innerText;
	            else if(childS[i].nodeType==3)
	                anyString += childS[i].nodeValue;
		        }
	        return anyString;
	    } 
	   ); 
	   HTMLElement.prototype.__defineSetter__("innerText", 
	   function(sText){
	   this.textContent=sText; 
	   } 
	  ); 
	}
	</script>
</head>


<body>
<?php
    echo "<div class='easyui-layout' style='width:1600px; height:1000px;' id='custom_person' name = '" . $_COOKIE["nickname"] . "' >";
?>
	<div data-options="region:'south',border:false" style="height:40px;text-align:center;">有问题请联系 hzzhujie@corp.netease.com</div>
	<div data-options="region:'north',border:false" style="height:100px;text-align:center;background-image:url(rankimage/background.jpg);background-position:left 0px;"><img src="rankimage/biaoti.png" alt=""></div>
	<div data-options="region:'center'" style="width:1560px; height:840px;">
		<div id="tt" class="easyui-tabs" style="width:1560px; height:840px;">	
			<?php
				echo " <div title='个人定制 " . $_COOKIE["nickname"] . "' >";
			?>
				<table id="dg_person" class="easyui-datagrid" title="排行榜" toolbar="#toolbar_person" fitColumns='true' data-options="rownumbers:true,pagePosition:'both',onSortColumn:onSortColumn,pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData_person.php',method:'get',fit:true,nowrap:false">
					<thead>
						<th field="ck" checkbox="true"></th>
						<th data-options="field:'gameName',width:50">App名字</th>
						<th data-options="field:'channel',sortable:true,formatter:channelformatter,width:20">来源</th>
						<th data-options="field:'ranking',sortable:true,formatter:rankingFormatter,width:10">排名</th>
						<th data-options="field:'rankDate',formatter:dateformatter,width:10">日期</th>
					</thead>
				</table>
				<div id="toolbar_person" style="padding:5px;height:100px">
					<div id="edit_person">
						<select id="op_person" class="easyui-combobox">
							<option value='1'>近30天</option>
							<option value='2'>近1年</option>
						</select>
						<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_person()">查看趋势</a>
						<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_person()">刷新</a>
						<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="delete_person()">删除定制</a>
						<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="excel()">导出excel</a>
					</div>
					<div id="search_person" style="padding:3px">
						<span>时间:</span>
						<input id="starttime_person" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
						<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_person()">个人关注查询</a>
						&nbsp;&nbsp;&nbsp;&nbsp;
						<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_neteasy()">网易系手游查询</a>
						&nbsp;&nbsp;&nbsp;&nbsp;
						<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_leocool()">leocool手游查询</a>
						&nbsp;&nbsp;&nbsp;&nbsp;
						<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_shuru()">输入查询</a>
						<input id="shuru_name" type="text">
						<br>
						<input id="dataType" disabled='disabled' type="text">						
					</div>
				</div>
			</div>
			<div title="每日新晋" data-options="tools:'#p-tools'">
				<table id="dg_new" class="easyui-datagrid" style="width:1000px;height:auto" title="排行榜" toolbar="#toolbar_new" fitColumns='true' data-options="rownumbers:true,pagePosition:'both',pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData_new.php',method:'get',fit:true,nowrap:false">
					<thead>
						<th field="ck" checkbox="true"></th>
						<th data-options="field:'gameName',width:50">App名字</th>
						<th data-options="field:'channel',formatter:channelformatter,width:20">渠道</th>
						<th data-options="field:'ranking',width:10">排名</th>
						<th data-options="field:'rankDate',formatter:dateformatter,width:10">日期</th>
					</thead>
				</table>
				<div id="toolbar_new" style="padding:5px;height:100px">
					<div id="edit_new">
						<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_new()">刷新</a>
						<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_new()">导出</a>
					</div>
					<div id="search_new" style="padding:3px">
						<span>时间:</span>
						<input id="starttime_new" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
						<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_new()">查询</a>
					</div>
				</div>
			</div>
			<div title="Iphone中国">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div title="付费榜">
						<table id="dg_pay" class="easyui-datagrid" style="width:1000px;height:auto" toolbar="#toolbar_pay" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_chinaIphone_pay',method:'get',fit:true,nowrap:false,onClickRow:onClickRow_china_pay,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_pay" style="padding:5px;height:100px">
							<div id="edit_pay">
								<select id="op_pay" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_pay()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_pay()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_pay()">添加关注</a>
							</div>
							<div id="search_pay" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_pay" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_pay()">查询</a>
							</div>
						</div>
					</div>
					<div title="免费榜">
						<table id="dg_free" class="easyui-datagrid" style="width:1000px;height:auto"toolbar="#toolbar_free" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_chinaIphone_free',method:'get',fit:true,nowrap:false,onClickRow:onClickRow_china_free,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_free" style="padding:5px;height:100">
							<div id="edit_free">
								<select id="op_free" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_free()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_free()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_free()">添加关注</a>
							</div>
							<div id="search_free" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_free" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_free()">查询</a>
							</div>
						</div>
					</div>
					<div title="畅销榜">
						<table id="dg_sell" class="easyui-datagrid" style="width:1000px;height:auto"toolbar="#toolbar_sell" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_chinaIphone_sell',method:'get',fit:true,nowrap:false,onClickRow:onClickRow_china_sell,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_sell" style="padding:5px;height:100">
							<div id="edit_sell">
								<select id="op_sell" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_sell()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_sell()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_sell()">添加关注</a>
							</div>
							<div id="search_sell" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_sell" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_sell()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div title="Ipad中国">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div title="付费榜">
						<table id="dg_pay_ipad" class="easyui-datagrid" style="width:1000px;height:auto"  toolbar="#toolbar_pay_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_chinaIpad_pay',method:'get',fit:true,nowrap:false,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_pay_ipad" style="padding:5px;height:100">
							<div id="edit_pay_ipad">
								<select id="op_pay_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_pay_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_pay_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_pay_ipad()">添加关注</a>
							</div>
							<div id="search_pay_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_pay_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_pay_ipad()">查询</a>
							</div>
						</div>
					</div>
					<div title="免费榜">
						<table id="dg_free_ipad" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_free_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_chinaIpad_free',method:'get',fit:true,nowrap:false,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_free_ipad" style="padding:5px;height:100">
							<div id="edit_free_ipad">
								<select id="op_free_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_free_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_free_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_free_ipad()">添加关注</a>
							</div>
							<div id="search_free_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_free_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_free_ipad()">查询</a>
							</div>
						</div>
					</div>
					<div title="畅销榜">
						<table id="dg_sell_ipad" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_sell_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_chinaIpad_sell',method:'get',fit:true,nowrap:false,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_sell_ipad" style="padding:5px;height:100">
							<div id="edit_sell_ipad">
								<select id="op_sell_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_sell_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_sell_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_sell_ipad()">添加关注</a>
							</div>
							<div id="search_sell_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_sell_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_sell_ipad()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div title="Iphone日本">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div  title="付费榜">
						<table id="dg_japan_pay" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_japan_pay" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_japanIphone_pay',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_japan_pay" style="padding:5px;height:100">
							<div id="edit_japan_pay">
								<select id="op_japan_pay" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_japan_pay()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_japan_pay()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_japan_pay()">添加关注</a>
							</div>
							<div id="search_japan_pay" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_japan_pay" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_japan_pay()">查询</a>
							</div>
						</div>
					</div>
					<div  title="免费榜">
						<table id="dg_japan_free" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_japan_free" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_japanIphone_free',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_japan_free" style="padding:5px;height:100">
							<div id="edit_japan_free">
								<select id="op_japan_free" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_japan_free()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_japan_free()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_japan_free()">添加关注</a>
							</div>
							<div id="search_japan_free" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_japan_free" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_japan_free()">查询</a>
							</div>
						</div>
					</div>
					<div title="畅销榜">
						<table id="dg_japan_sell" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_japan_sell" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_japanIphone_sell',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_japan_sell" style="padding:5px;height:100">
							<div id="edit_japan_sell">
								<select id="op_japan_sell" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_japan_sell()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_japan_sell()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_japan_sell()">添加关注</a>
							</div>
							<div id="search_japan_sell" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_japan_sell" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_japan_sell()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div title="Ipad日本">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div title="付费榜">
						<table id="dg_japan_pay_ipad" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_japan_pay_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_japanIpad_pay',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_japan_pay_ipad" style="padding:5px;height:100">
							<div id="edit_japan_pay_ipad">
								<select id="op_japan_pay_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_japan_pay_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_japan_pay_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_japan_pay_ipad()">添加关注</a>
							</div>
							<div id="search_japan_pay_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_japan_pay_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_japan_pay_ipad()">查询</a>
							</div>
						</div>
					</div>
					<div  title="免费榜">
						<table id="dg_japan_free_ipad" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_japan_free_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_japanIpad_free',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_japan_free_ipad" style="padding:5px;height:100">
							<div id="edit_japan_free_ipad">
								<select id="op_japan_free_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_japan_free_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_japan_free_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_japan_free_ipad()">添加关注</a>
							</div>
							<div id="search_japan_free_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_japan_free_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_japan_free_ipad()">查询</a>
							</div>
						</div>
					</div>
					<div title="畅销榜">
						<table id="dg_japan_sell_ipad" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_japan_sell_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_japanIpad_sell',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_japan_sell_ipad" style="padding:5px;height:100">
							<div id="edit_japan_sell_ipad">
								<select id="op_japan_sell_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_japan_sell_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_japan_sell_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_japan_sell_ipad()">添加关注</a>
							</div>
							<div id="search_japan_sell_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_japan_sell_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_japan_sell_ipad()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div title="Iphone美国">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div title="付费榜">
						<table id="dg_american_pay" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_american_pay" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_americanIphone_pay',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_american_pay" style="padding:5px;height:100">
							<div id="edit_american_pay">
								<select id="op_american_pay" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_american_pay()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_american_pay()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_american_pay()">添加关注</a>
							</div>
							<div id="search_american_pay" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_american_pay" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_american_pay()">查询</a>
							</div>
						</div>
					</div>
					<div title="免费榜">
						<table id="dg_american_free" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_american_free" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_americanIphone_free',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_american_free" style="padding:5px;height:100">
							<div id="edit_american_free">
								<select id="op_american_free" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_american_free()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_american_free()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_american_free()">添加关注</a>
							</div>
							<div id="search_american_free" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_american_free" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_american_free()">查询</a>
							</div>
						</div>
					</div>
					<div title="畅销榜">
						<table id="dg_american_sell" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_american_sell" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_americanIphone_sell',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_american_sell" style="padding:5px;height:100">
							<div id="edit_american_sell">
								<select id="op_american_sell" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_american_sell()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_american_sell()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_american_sell()">添加关注</a>
							</div>
							<div id="search_american_sell" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_american_sell" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_american_sell()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div title="Ipad美国">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div title="付费榜" >
						<table id="dg_american_pay_ipad" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_american_pay_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_americanIpad_pay',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_american_pay_ipad" style="padding:5px;height:100">
							<div id="edit_american_pay_ipad">
								<select id="op_american_pay_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_american_pay_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_american_pay_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_american_pay_ipad()">添加关注</a>
							</div>
							<div id="search_american_pay_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_american_pay_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_american_pay_ipad()">查询</a>
							</div>
						</div>
					</div>
					<div title="免费榜" >
						<table id="dg_american_free_ipad" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_american_free_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_americanIpad_free',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_american_free_ipad" style="padding:5px;height:100">
							<div id="edit_american_free_ipad">
								<select id="op_american_free_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_american_free_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_american_free_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_american_free_ipad()">添加关注</a>
							</div>
							<div id="search_american_free_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_american_free_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_american_free_ipad()">查询</a>
							</div>
						</div>
					</div>
					<div title="畅销榜">
						<table id="dg_american_sell_ipad" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_american_sell_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_americanIpad_sell',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_american_sell_ipad" style="padding:5px;height:100">
							<div id="edit_american_sell_ipad">
								<select id="op_american_sell_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_american_sell_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_american_sell_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_american_sell_ipad()">添加关注</a>
							</div>
							<div id="search_american_sell_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_american_sell_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_american_sell_ipad()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>		
			<div title="Iphone韩国">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div title="付费榜">
						<table id="dg_korea_pay" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_korea_pay" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_koreaIphone_pay',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_korea_pay" style="padding:5px;height:100">
							<div id="edit_korea_pay">
								<select id="op_korea_pay" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_korea_pay()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_korea_pay()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_korea_pay()">添加关注</a>
							</div>
							<div id="search_korea_pay" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_korea_pay" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_korea_pay()">查询</a>
							</div>
						</div>
					</div>
					<div title="免费榜" >
						<table id="dg_korea_free" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_korea_free" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_koreaIphone_free',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_korea_free" style="padding:5px;height:100">
							<div id="edit_korea_free">
								<select id="op_korea_free" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_korea_free()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_korea_free()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_korea_free()">添加关注</a>
							</div>
							<div id="search_korea_free" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_korea_free" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_korea_free()">查询</a>
							</div>
						</div>
					</div>
					<div title="畅销榜" >
						<table id="dg_korea_sell" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_korea_sell" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_koreaIphone_sell',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_korea_sell" style="padding:5px;height:100">
							<div id="edit_korea_sell">
								<select id="op_korea_sell" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_korea_sell()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_korea_sell()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_korea_sell()">添加关注</a>
							</div>
							<div id="search_korea_sell" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_korea_sell" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_korea_sell()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div title="Ipad韩国">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div  title="付费榜">
						<table id="dg_korea_pay_ipad" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_korea_pay_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_koreaIpad_pay',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_korea_pay_ipad" style="padding:5px;height:100">
							<div id="edit_korea_pay_ipad">
								<select id="op_korea_pay_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_korea_pay_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_korea_pay_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_korea_pay_ipad()">添加关注</a>
							</div>
							<div id="search_korea_pay_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_korea_pay_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_korea_pay_ipad()">查询</a>
							</div>
						</div>
					</div>
					<div title="免费榜" >
						<table id="dg_korea_free_ipad" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_korea_free_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_koreaIpad_free',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_korea_free_ipad" style="padding:5px;height:100">
							<div id="edit_korea_free_ipad">
								<select id="op_korea_free_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_korea_free_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_korea_free_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_korea_free_ipad()">添加关注</a>
							</div>
							<div id="search_korea_free_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_korea_free_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_korea_free_ipad()">查询</a>
							</div>
						</div>
					</div>
					<div title="畅销榜" >
						<table id="dg_korea_sell_ipad" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_korea_sell_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_koreaIpad_sell',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_korea_sell_ipad" style="padding:5px;height:100">
							<div id="edit_korea_sell_ipad">
								<select id="op_korea_sell_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_korea_sell_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_korea_sell_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_korea_sell_ipad()">添加关注</a>
							</div>
							<div id="search_korea_sell_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_korea_sell_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_korea_sell_ipad()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div title="Iphone台湾">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div title="付费榜">
						<table id="dg_taiwan_pay" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_taiwan_pay" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_taiwanIphone_pay',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_taiwan_pay" style="padding:5px;height:100">
							<div id="edit_taiwan_pay">
								<select id="op_taiwan_pay" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_taiwan_pay()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_taiwan_pay()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_taiwan_pay()">添加关注</a>
							</div>
							<div id="search_taiwan_pay" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_taiwan_pay" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_taiwan_pay()">查询</a>
							</div>
						</div>
					</div>
					<div title="免费榜">
						<table id="dg_taiwan_free" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_taiwan_free" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_taiwanIphone_free',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_taiwan_free" style="padding:5px;height:100">
							<div id="edit_taiwan_free">
								<select id="op_taiwan_free" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_taiwan_free()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_taiwan_free()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_taiwan_free()">添加关注</a>
							</div>
							<div id="search_taiwan_free" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_taiwan_free" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_taiwan_free()">查询</a>
							</div>
						</div>
					</div>
					<div title="畅销榜">
						<table id="dg_taiwan_sell" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_taiwan_sell" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_taiwanIphone_sell',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_taiwan_sell" style="padding:5px;height:100">
							<div id="edit_taiwan_sell">
								<select id="op_taiwan_sell" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_taiwan_sell()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_taiwan_sell()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_taiwan_sell()">添加关注</a>
							</div>
							<div id="search_taiwan_sell" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_taiwan_sell" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_taiwan_sell()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div title="Ipad台湾">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div  title="付费榜" >
						<table id="dg_taiwan_pay_ipad" class="easyui-datagrid" style="width:1000;height:auto"toolbar="#toolbar_taiwan_pay_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_taiwanIpad_pay',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_taiwan_pay_ipad" style="padding:5px;height:100">
							<div id="edit_taiwan_pay_ipad">
								<select id="op_taiwan_pay_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_taiwan_pay_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_taiwan_pay_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_taiwan_pay_ipad()">添加关注</a>
							</div>
							<div id="search_taiwan_pay_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_taiwan_pay_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_taiwan_pay_ipad()">查询</a>
							</div>
						</div>
					</div>
					<div  title="免费榜">
						<table id="dg_taiwan_free_ipad" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_taiwan_free_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_taiwanIpad_free',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_taiwan_free_ipad" style="padding:5px;height:100">
							<div id="edit_taiwan_free_ipad">
								<select id="op_taiwan_free_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_taiwan_free_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_taiwan_free_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_taiwan_free_ipad()">添加关注</a>
							</div>
							<div id="search_taiwan_free_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_taiwan_free_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_taiwan_free_ipad()">查询</a>
							</div>
						</div>
					</div>
					<div title="畅销榜">
						<table id="dg_taiwan_sell_ipad" class="easyui-datagrid" style="width:1000;height:auto"  toolbar="#toolbar_taiwan_sell_ipad" fitColumns='true' data-options="pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=ios_taiwanIpad_sell',method:'get',fit:true,nowrap:false">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_taiwan_sell_ipad" style="padding:5px;height:100">
							<div id="edit_taiwan_sell_ipad">
								<select id="op_taiwan_sell_ipad" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_taiwan_sell_ipad()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_taiwan_sell_ipad()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_taiwan_sell_ipad()">添加关注</a>
							</div>
							<div id="search_taiwan_sell_ipad" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_taiwan_sell_ipad" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_taiwan_sell_ipad()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div title="Android渠道">
				<div class="easyui-tabs"  style="width:1557px;height:805px;">
					<div title="腾讯渠道">
						<table id="dg_qq" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_qq" fitColumns='true' data-options="pagePosition:'both',pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=android_qq',method:'get',fit:true,nowrap:false,onClickRow:onClickRow_qq,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',width:150,formatter:gameNameformatter">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_qq" style="padding:5px;height:100">
							<div id="edit_qq">
								<select id="op_qq" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_qq()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_qq()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_qq()">添加关注</a>
							</div>
							<div id="search_qq" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_qq" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_qq()">查询</a>
							</div>
						</div>
					</div>
					<div title="91渠道">
						<table id="dg_91" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_91" fitColumns='true' data-options="pagePosition:'both',pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=android_91',method:'get',fit:true,nowrap:false,onClickRow:onClickRow_91,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',formatter:gameNameformatter,width:150">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_91" style="padding:5px;height:100">
							<div id="edit_91">
								<select id="op_91" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_91()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_91()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_91()">添加关注</a>
							</div>
							<div id="search_91" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_91" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_91()">查询</a>
							</div>
						</div>
					</div>
					<div title="360渠道">
						<table id="dg_360" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_360" fitColumns='true' data-options="pagePosition:'both',pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=android_360',method:'get',fit:true,nowrap:false,onClickRow:onClickRow_360,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',formatter:gameNameformatter,width:150">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_360" style="padding:5px;height:100">
							<div id="edit_360">
								<select id="op_360" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_360()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_360()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_360()">添加关注</a>
							</div>
							<div id="search_360" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_360" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_360()">查询</a>
							</div>
						</div>
					</div>
					<div title="百度渠道">
						<table id="dg_baidu" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_baidu" fitColumns='true' data-options="pagePosition:'both',pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=android_baidu',method:'get',fit:true,nowrap:false,onClickRow:onClickRow_baidu,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',formatter:gameNameformatter,width:150">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_baidu" style="padding:5px;height:100">
							<div id="edit_baidu">
								<select id="op_baidu" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_baidu()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_baidu()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_baidu()">添加关注</a>
							</div>
							<div id="search_baidu" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_baidu" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_baidu()">查询</a>
							</div>
						</div>
					</div>
					<div title="Google(待完善)">
						<table id="dg_google" class="easyui-datagrid" style="width:1000;height:auto" toolbar="#toolbar_google" fitColumns='true' data-options="pagePosition:'both',pagination:true,pageSize:100,pageList:[100,160,180,200],collapsible:false,url:'getAppData.php?channel=android_google',method:'get',fit:true,nowrap:false,onClickRow:onClickRow_google,ctrlSelect:true">
							<thead>
								<th field="ck" checkbox="true"></th>
								<th data-options="field:'ranking',sortable:true,width:20">Rank</th>
								<th data-options="field:'gameName',formatter:gameNameformatter,width:150">App名字</th>
								<th data-options="field:'rankDate',formatter:dateformatter,width:50">日期</th>
							</thead>
						</table>
						<div id="toolbar_google" style="padding:5px;height:100">
							<div id="edit_google">
								<select id="op_google" class="easyui-combobox">
									<option value='1'>近30天</option>
									<option value='2'>近1年</option>
								</select>
								<a href="#" class="easyui-linkbutton" iconCls="icon-redo" plain="true" onclick="trend_google()">查看趋势</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-reload" plain="true" onclick="reload_google()">刷新</a>
								<a href="#" class="easyui-linkbutton" iconCls="icon-large-smartart" plain="true" onclick="expt_google()">添加关注</a>
							</div>
							<div id="search_google" style="padding:3px">
								<span>时间:</span>
								<input id="starttime_google" class="easyui-datetimebox"  data-options="showSeconds:false" style="width:200px"></input>
								<a href="#" class="easyui-linkbutton" iconCls="icon-search" plain="true" onclick="doSearch_google()">查询</a>
							</div>
						</div>
					</div>
				</div>
			</div>	
		</div>
	</div>
	<div data-options="region:'west',border:false" style="width:40px;padding:10px;"></div>
	</div>
</body>
</html>
