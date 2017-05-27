















function affectedMapformatter(value,row,index)
{
	var index = row.affectedFile.indexOf(';')
	var ret = row.affectedMap.replace(/;/g,"<br>"+row.affectedFile.substr(0,index)+"<br>")
	return ret;
}


var editIndex = undefined;
var markFinished=[];

function onClickRow(index){
	if (editIndex != index){
		if (endEditing()){
			$('#dg').datagrid('selectRow', index)
			$('#dg').datagrid('beginEdit', index);
			editIndex = index;
		} else {
			$('#dg').datagrid('selectRow', editIndex);
		}
	}
}



function gmformatter(value,row,index)
{
	var affectedMapInfo=row.affectedMap.split(";")
	//var ret = "<textarea class=\"form-control\" rows=\"10\">" 
	var ret=""
	for(var i = 0;i<affectedMapInfo.length-1;i++)
	{
		var b = affectedMapInfo[i].split(',')
		var mapid = b[0]
		var x = b[1]
		var y = b[2]
		if( mapid.indexOf("160") == -1 )
		{
			ret = ret + "GM_COMMAND(playerid,\"teleport\"," + mapid.toString() +  "," + x.toString() + "," + y.toString() + ")<br>"
		}
		else
		{
			ret = ret + "RUN_SCRIPT_ON_ALLGAS([===[local p = g_ServerPlayerMgr:GetPlayerById(playerid)\r\nif not p then return end\r\nlocal scene = g_SceneMgr:CreateScene(" + mapid.toString() + ")\r\ng_TeleportMgr:TeleportPlayer(p, scene.m_Id," + x.toString() + "," + y.toString() + ")]===])\r\n\r\n"
		}
	}
	//ret = ret + "</textarea>"
	return ret;
}



function doSearch(){
	$('#dg').datagrid(
		'reload',
		{
			starttime:$('#starttime').datetimebox('getValue'),
			endtime:$('#endtime').datetimebox('getValue'),
			QA:$('#QA').combobox('getValue'),
			STATUS:$('#STATUS').combobox('getValue'),
		}
	);
}


function reload(){
	$('#dg').datagrid(
		'reload',
		{
			starttime:$('#starttime').datetimebox('getValue'),
			endtime:$('#endtime').datetimebox('getValue'),
			QA:$('#QA').combobox('getValue'),
			STATUS:$('#STATUS').combobox('getValue'),
		}
	);
}


function cancel(){
	$('#dg').datagrid('rejectChanges');
}


function expt(){
	alert('导出为excel的功能还没有开放，sorry')
}


function onSortColumn(sort,order){
	$('#dg').datagrid(
		'reload',
		{
			sort:sort,
			order:order,
			starttime:$('#starttime').datetimebox('getValue'),
			endtime:$('#endtime').datetimebox('getValue'),
			QA:$('#QA').combobox('getValue'),
			STATUS:$('#STATUS').combobox('getValue'),
		}
	);
}

var markFinished=[];

function markall(){
	var rows = $('#dg').datagrid('getSelections');
	if(rows.length){
		for (var i = 0; i < rows.length; i++) {
			var rowindex = $('#dg').datagrid('getRowIndex', rows[i]);
			$('#dg').datagrid('updateRow',{
				index: rowindex,
				row: {
					bFinished: '完成'
				}
			});
			markFinished.push(rows[i]);
		}
		endEditing();
	}
}


function saveall(){
	if (endEditing()){
		if ($('#dg').datagrid('getChanges').length) {
			var insertRows = $('#dg').datagrid('getChanges', "inserted");
			var updateRows = $('#dg').datagrid('getChanges', "updated");
			var deleteRows = $('#dg').datagrid('getChanges', "deleted");
			
			var changesRows = {
				 inserted : [],
				 updated : [],
				 deleted : [],
			 };
			 if (insertRows.length > 0) {
				 for (var i=0;i<insertRows.length;i++) {
					delete insertRows[k]['svnAction']
					delete insertRows[k]['affectedMap']
					delete insertRows[k]['svnPath']
					delete insertRows[k]['affectedFile']
					delete insertRows[k]['buildVersion']
					delete insertRows[k]['trackerDate']
					delete insertRows[k]['Assigner']
					delete insertRows[k]['svnLogDate']
					changesRows.inserted.push(insertRows[i]);
				 }
			 }

			 if (updateRows.length > 0) {
				 for (var k=0;k<updateRows.length;k++) {
					delete updateRows[k]['svnAction']
					delete updateRows[k]['affectedMap']
					delete updateRows[k]['svnPath']
					delete updateRows[k]['affectedFile']
					delete updateRows[k]['buildVersion']
					delete updateRows[k]['trackerDate']
					delete updateRows[k]['Assigner']
					delete updateRows[k]['svnLogDate']
					changesRows.updated.push(updateRows[k]);
				 }
			 }
			
			 if (deleteRows.length > 0) {
				 for (var j=0;j<deleteRows.length;j++) {
					delete deleteRows[k]['svnAction']
					delete deleteRows[k]['affectedMap']
					delete deleteRows[k]['svnPath']
					delete deleteRows[k]['affectedFile']
					delete deleteRows[k]['buildVersion']
					delete deleteRows[k]['trackerDate']
					delete deleteRows[k]['Assigner']
					delete deleteRows[k]['svnLogDate']
					changesRows.deleted.push(deleteRows[j]);
				 }
			 }
			 
			var postdata = "inserted="+JSON.stringify(changesRows.inserted)+"&updated="+JSON.stringify(changesRows.updated)+"&deleted="+JSON.stringify(changesRows.deleted);
			$.ajax({
				type: "post",
				url: "save_arp2mysql.php",	
				data: postdata,
				datatype: "json",
				success:function(returnData){
					//alert(returnData);
					$('#dg').datagrid('acceptChanges');
					$('#dg').datagrid('clearSelections');
				},
				error:function(errorMsg) {
					//alert(errorMsg);
					$('#dg').datagrid('rejectChanges');
				}
			});
		}
		else
		{
			if(markFinished.length > 0){
				var postdata = "updated="+JSON.stringify(markFinished);
				$.ajax({
					type: "post",
					url: "save_arp2mysql.php",	
					data: postdata,
					datatype: "json",
					success:function(returnData){
						$('#dg').datagrid('acceptChanges');
						$('#dg').datagrid('clearSelections');
					},
					error:function(errorMsg) {
						$('#dg').datagrid('rejectChanges');
					}
				});
				markFinished=[];
			}
		}
	}
}


function endEditing(){
	if (editIndex == undefined){return true}
	if ($('#dg').datagrid('validateRow', editIndex)){
		var rows = $('#dg').datagrid('getRows');
		for ( var i = 0; i < rows.length; i++) {
		   $('#dg').datagrid('endEdit', i);
		}
		editIndex = undefined;
		return true;
	} else {
		return false;
	}
}

function blockAssign(){
	if ( $('#dg').datagrid('getData') )
	{
		var qaerNum = $("#qaerNum").combobox('getValue');
		var myData = $('#dg').datagrid('getRows');
		var postdata = "blockData="+JSON.stringify(myData)+"&qaerNum="+qaerNum;
		$.ajax({
			type:"post",
			url: "blockDataAssign.php",	
			data: postdata,
			datatype: "json",
			success:function(returnData){
				window.open ('blockDataAssign.php')
			},
			error:function(errorMsg) {
			}
		});
	}
	else
	{
		alert("no data")
	}
}
