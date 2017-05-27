
function GetDateTimeStr(AddDayCount) {
	var dd = new Date();
	dd.setDate(dd.getDate()+AddDayCount);//»ñÈ¡AddDayCountÌìºóµÄÈÕÆÚ
	var y = dd.getFullYear();
	var m = dd.getMonth()+1;//»ñÈ¡µ±Ç°ÔÂ·ÝµÄÈÕÆÚ
	var d = dd.getDate();
	var h = dd.getHours();
	var min = dd.getMinutes();
	return y+"-"+m+"-"+d+" "+h+":"+min;
}

function GetDateStr(AddDayCount) {
	var dd = new Date();
	dd.setDate(dd.getDate()+AddDayCount);//»ñÈ¡AddDayCountÌìºóµÄÈÕÆÚ
	var y = dd.getFullYear();
	var m = dd.getMonth()+1;//»ñÈ¡µ±Ç°ÔÂ·ÝµÄÈÕÆÚ
	var d = dd.getDate();
	return y+"-"+m+"-"+d;
}

$(function(){
	var dd = new Date();
	if(dd.getDay()==1){
		$('#starttime').datetimebox('setValue', GetDateStr(-3)+" 00:00");
	}
	else
	{
		$('#starttime').datetimebox('setValue', GetDateStr(-1)+" 00:00");
	}
	$('#endtime').datetimebox('setValue', GetDateTimeStr(0));
	$('#dg').datagrid(
		'reload',
		{
			starttime:$('#starttime').datetimebox('getValue'),
			endtime:$('#endtime').datetimebox('getValue'),
			QA:$('#QA').combobox('getValue'),
			STATUS:$('#STATUS').combobox('getValue'),
			submiter:$('#submiter').combobox('getValue')
		}
	);
})

var static_qaer = ['Y姚金飞','W王佳','Y袁磊','W吴磊','L李飞','W王晓欣','C陈文婉','Z朱洁','L李海','F冯潞潞','F冯丹平','Q其他','Z赵莹','L李伟','H黄超群','W王立部']

function sendMail()
{
	if ( window.confirm("确定分发邮件吗？") )
	{
		var pkstring2="";
		var QAerstring2="";
		var Redminestring2="";
		var Submiterstring2="";
		var psstring2="";
		var svninfostring2="";
		var svnlogNum=0;

		var rows = $('#dg').datagrid('getSelections');
		if(rows.length && rows.length > 0)
		{
			for (var i = 0; i < rows.length; i++)
			{
				var qaer = rows[i].QAer;
	            var redmine = rows[i].Redmine;
	            var submitIndex = rows[i].submitIndex;
	            var submitDate = rows[i].submitDate;
	            var submiter = rows[i].submiter;
				if ( submitIndex != "" && qaer != 0 && ( (redmine.length > 2) || (submitDate.length > 2 ) || (submiter.length > 2) ) )
				{
	                 svnlogNum = svnlogNum + 1;

	                 pkstring2 = pkstring2 + rows[i].submitIndex + ";";
	                 QAerstring2 = QAerstring2 + rows[i].QAer + ";";
	                 psstring2 = psstring2 + rows[i].ps + "|";

	                 Submiterstring2 = Submiterstring2 + rows[i].submiter + ";";
	                 Redminestring2 = Redminestring2 + rows[i].Redmine + "|";
	                 svninfostring2 = svninfostring2 + rows[i].svnInfo + "|";
				}
				else
				{
				}
			}
			if ( svnlogNum > 0 && svnlogNum <= rows.length )
			{
				$.ajax({
					url:'svnlog2note.php',
					data:{'pk':pkstring2,'QAer':QAerstring2,'ps':psstring2,'Submiter':Submiterstring2,'Redmine':Redminestring2,'svninfo':svninfostring2},
					type:'post',
					success:function(res){
						alert("你已成功的分配了" + svnlogNum + "条svn记录")
					}
				})

			}
		}
		else
		{
			alert("你选择了0行，请重新选择！")
		}
	}
}


$(function(){
  $("#btn_saveNewSvnLog").click(function(){
	if ( window.confirm("确定增加该测试用例吗？") )
	{
		var context=$("#val_Context").find('textarea').val();
		var submitIndex=$("#val_submitIndex").find("textarea").val();
		var	qaer = $("#val_qaer").find('option:selected').text();

		var	submiter = $("#val_submiter").find("textarea").val();
		var	buildVersion = $("#val_buildVersion").find("textarea").val();
		var	submitDate = $("#val_submitDate").find("textarea").val();
		if ( context && context.length >2 )
		{					    
			$.ajax({
				url:'newSvnLog2mysql.php',
				data:{'submitIndex':submitIndex,'context':context,'qaer':qaer,'submiter':submiter,'buildVersion':buildVersion,'submitDate':submitDate},
				type:'post',
				success:function(res){
				window.location.reload()
				}
			})
		}
		else
		{
			alert("检查条目不能为空")
		}
	}
  })
})

function addNewTest()
{
	$("#m_addNewSvnLog").modal('show').css({

			});
}

function cancelSplit()
{
	if ( window.confirm("确定撤销拆分操作吗？") )
	{
		var id = $("#val_splitId").val();
		if ( id != "" )
		{
			$.ajax({
				url:'cancelSplit.php',
				data:{'id':id},
				type:'post',
				success:function(res){
					alert("撤销成功！")
					window.location.reload()
				}
			})
		}
		else
		{
			alert("请输入你需要撤销的svn提交号！")
		}
	}
}







function splitSvn()
{
	var rows = $('#dg').datagrid('getSelections');
	if(rows.length && rows.length == 1)
	{
		var num = $("#splitNum").combobox('getValue');	
		$("#splitpage").modal('show').css({

			});

		var str = "将提交内容拆分为" + num
		$("#myModalTitle").html(str)

		str = rows[0].svnInfo
		$("#myModalContext").html(str)

		$("#myModalTable tr:not(:first)").empty()
		
		$("#myModalTable").css("backgroundColor","white");

		for (var i=1;i<=num;i++)
		{
		    var tab=document.getElementById('myModalTable').insertRow(1)

			var x1=tab.insertCell(0);
			var x2=tab.insertCell(1);
		    var x3=tab.insertCell(2);
			var x4=tab.insertCell(3);
			var x5=tab.insertCell(4);
			var x6=tab.insertCell(5);
			var x7=tab.insertCell(6);
			var x8=tab.insertCell(7);
			var x9=tab.insertCell(8);
			var x10=tab.insertCell(9);
			
			var splitNum = num - i + 1;
			var pk = rows[0].submitIndex;
			var value = pk + "_" + splitNum;
			x1.innerText=value;
		    x2.innerHTML='<textarea class="form-control" rows="5"></textarea>';
			var redminestr=""
			var redmineArray = rows[0].Redmine.split(";")
			for(var j =0;j<redmineArray.length-1;j++)
			{
				redminestr = redminestr + "<label class='checkbox'><input type='checkbox' checked='checked' value='" + redmineArray[j] + "'>" + '<a href="http://qn.pm.netease.com:8120/issues/' + redmineArray[j] + ' target="_blank" ' + "title='" + rows[0][redmineArray[j]].replace(/\|/g,"&#10;") + "'>" + redmineArray[j] + ";</a>" + "</label><br>";
			}
		    x3.innerHTML=redminestr
		    x4.innerText=rows[0].submitDate;
		    x5.innerText=rows[0].submiter;


			var str = '<td> <select class="form-control"> <option selected="selected">请选择</option> ';
			for (var n=0;n<static_qaer.length;n++)
			{
				str = str + "<option>" + static_qaer[n] + "</option>"
			}
			str = str + "</select> </td>"
		    x6.innerHTML=str;
		    var str = '<td> <select class="form-control"> <option>未完成</option> <option>完成</option> </select> </td>';
		    x7.innerHTML=str;
		    x8.innerHTML='<textarea class="form-control" rows="5"></textarea>';
		    x9.innerText=rows[0].buildVersion;
		    x10.innerText=rows[0].submitClass;

			x9.style.display="none";
			x10.style.display="none";
			x1.style.display="none";
			x8.style.display="none";
			x4.style.display="none";
			x5.style.display="none";

		}

		var tableline=$('#dg').datagrid('getRowIndex', rows[0]);
		var ebutt=document.getElementById("btn_saveSplitContext")
		var argstr = "saveSplitContext()"
		ebutt.setAttribute("onclick",argstr)

	}
	else
	{
		alert("你选择的列为空或者超过2行！")
	}
}


function saveSplitContext()
{
	var rows = $('#dg').datagrid('getSelections');
	if(rows.length && rows.length == 1)
	{
		if ( window.confirm("确定拆分提交内容吗？请仔细核对拆分内容是否正确！") )
		{
			var pkstring="";
			var QAerstring="";
			var svninfostring="";
			var redminestring="";
			var submitTimestring="";
			var submiterstring="";
			var psstring="";
			var svnStatusstring="";
			var dirFlagstring="";
			var buildVersionstring="";
			var rowNum=0
			 //删除原先表格中被拆分的列,并将其在数据库的bFinished状态设置为被拆分
			 $.ajax({
			   url:'change2splitStatus.php',
			   data:{'pk':rows[0].submitIndex},
			   type:'post',
			   success:function(res){
			   }
			 })

			var rowindex = $('#dg').datagrid('getRowIndex', rows[0]);
			$('#dg').datagrid('updateRow',{
				index: rowindex,
				row: {
					bFinished: '',
					svnInfo:'被拆分了！！',
					Redmine:'',
					submitDate:'',
					submiter:'',
					QAer:'',
					ps:'',
				}
			});

			 $("#myModalTable tr").each(function(ind, item){
				var pkvalue = $(item).children("td:nth-child(1)").text()
				if ( pkvalue.match("_") )
				{
					pkstring = pkstring + $(item).children("td:nth-child(1)").text() + ";";
					svninfostring = svninfostring + $(item).children("td:nth-child(2)").find('textarea').val() + "|";
					$(item).children("td:nth-child(3)").children("label").each(function(m,n){
						if($(n).find("input").is(":checked") == true)
						{
							redminestring = redminestring + $(n).find("input").val() + ";"
						}
						else
						{
						}
					})
					redminestring = redminestring + "|"
					submitTimestring = submitTimestring + $(item).children("td:nth-child(4)").text() + ";"
					submiterstring = submiterstring + $(item).children("td:nth-child(5)").text() + ";"
					QAerstring = QAerstring + $(item).children("td:nth-child(6)").find('option:selected').text() + ";";
					svnStatusstring = svnStatusstring + $(item).children("td:nth-child(7)").find('option:selected').text() + ";";
					psstring = psstring + $(item).children("td:nth-child(8)").find('textarea').val() + ";";
					dirFlagstring=dirFlagstring + $(item).children("td:nth-child(10)").text() + ";";
					buildVersionstring=buildVersionstring + $(item).children("td:nth-child(9)").text() + ";";

				}
			 })

			$.ajax({
				url:'splitcontext2mysql.php',
				data:{'pk':pkstring,'svninfo':svninfostring,'redmine':redminestring,'submiter':submiterstring,'submitTime':submitTimestring,'QAer':QAerstring,'svnStatus':svnStatusstring,'ps':psstring,'buildVersion':buildVersionstring,'dirFlag':dirFlagstring},
				type:'post',
				success:function(res){
				}
			})
		}
	}
	else
	{
		alert("你选择的列为空或者超过2行！")
	}
}


function redmineformatter(value,row,index)
{
	var RedmineArray = row.Redmine.split(";");
	var str="";
	for(var i=0;i<RedmineArray.length-1;i++)
	{
		str = str + "<a href=\"http://qn.pm.netease.com:8120/issues/" + RedmineArray[i] + "\" target=\"_blank\" title=\"" + (row[RedmineArray[i]]).replace(/\|/g,"&#10;") + "\">" + RedmineArray[i] + ";</a>";
		str = str + "<br>";
	}
	return str
}

function QAerformatter(value,row,index)
{
	if ( row.QAer == 0 )
	{
		var redmineArray = row.Redmine.split(";")
		var defaultQAer = "<font color='red'>请选择</font>"
		for(var j =0;j<redmineArray.length-1;j++)
		{
			var redmineStr = row[redmineArray[j]].split('\|')
			if ( redmineStr[1] && redmineStr[1] != "" && static_qaer.indexOf(redmineStr[1]) != -1 )
			{
				//row.QAer = redmineStr[1]
				var pkstring = row.submitIndex + ";";
	            var QAerstring = redmineStr[1] + ";";
	            var svnStatusstring = row.bFinished + ";";
	            var psstring = row.ps + "|";
				$.ajax({
					url:'svnlog2mysql.php',
					data:{'pk':pkstring,'QAer':QAerstring,'ps':psstring,'svnStatus':svnStatusstring},
					type:'post',
					success:function(res){
						window.location.reload()
					}
				})
				return redmineStr[1]
			}
			else if ( redmineStr[2] && redmineStr[2] != "" && static_qaer.indexOf(redmineStr[2]) != -1 )
			{
				//row.QAer = redmineStr[2]
				var pkstring = row.submitIndex + ";";
	            var QAerstring = redmineStr[2] + ";";
	            var svnStatusstring = row.bFinished + ";";
	            var psstring = row.ps + "|";
				$.ajax({
					url:'svnlog2mysql.php',
					data:{'pk':pkstring,'QAer':QAerstring,'ps':psstring,'svnStatus':svnStatusstring},
					type:'post',
					success:function(res){
						window.location.reload()
					}
				})
				return redmineStr[2]
			}
		}
		return defaultQAer
	}
	else
	{
		return row.QAer
	}
}



function affectedMapformatter(value,row,index)
{
	var index = row.affectedFile.indexOf(';')
	var ret = row.affectedMap.replace(/;/g,"<br>"+row.affectedFile.substr(0,index)+"<br>")
	return ret;
}



function onClickRow(index){
			var row = $('#dg').datagrid('getSelected');
			var postdata = "id="+row.submitIndex;
			$.ajax({
				type: "post",
				url: "get_log_change_paths.php",	
				data: postdata,
				datatype: "json",
				success:function(returnData){
					$('#Paths').html(returnData);
				},
				error:function(errorMsg) {
					alert(errorMsg);
				}
			});
}


var editIndex = undefined;
var markFinished=[];

function onDblClickRow(index){
	if (editIndex != index)
	{
		if (1){
			$('#dg').datagrid('selectRow', index)
			$('#dg').datagrid('beginEdit', index);
			editIndex = index;
		} else {
			$('#dg').datagrid('selectRow', editIndex);
		}
	}
}


function doSearch(){
	$('#dg').datagrid(
		'reload',
		{
			starttime:$('#starttime').datetimebox('getValue'),
			endtime:$('#endtime').datetimebox('getValue'),
			QA:$('#QA').combobox('getValue'),
			STATUS:$('#STATUS').combobox('getValue'),
			submiter:$('#submiter').combobox('getValue'),
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
			submiter:$('#submiter').combobox('getValue'),
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
					changesRows.inserted.push(insertRows[i]);
				 }
			 }

			 if (updateRows.length > 0) {
				 for (var k=0;k<updateRows.length;k++) {
					//delete updateRows[k]['svnInfo']
					changesRows.updated.push(updateRows[k]);
				 }
			 }
			
			 if (deleteRows.length > 0) {
				 for (var j=0;j<deleteRows.length;j++) {
					changesRows.deleted.push(deleteRows[j]);
				 }
			 }
			 
			var postdata = "inserted="+JSON.stringify(changesRows.inserted)+"&updated="+JSON.stringify(changesRows.updated)+"&deleted="+JSON.stringify(changesRows.deleted);
			$.ajax({
				type: "post",
				url: "save_svnlog2mysql.php",	
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
		}
		else
		{
			if(markFinished.length > 0){
				var postdata = "updated="+JSON.stringify(markFinished);
				$.ajax({
					type: "post",
					url: "save_svnlog2mysql.php",	
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

			if(markQAer.length > 0){
				var postdata = "updated="+JSON.stringify(markFinished);
				$.ajax({
					type: "post",
					url: "save_svnlog2mysql.php",	
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
				markQAer=[];
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


var markQAer = []

function blockAssign(){
	var qaer = $('#allocate_qaer').combobox('getValue')
	if ( ! qaer.match("选择") )
	{
		var rows = $('#dg').datagrid('getSelections');
		if(rows.length){
			for (var i = 0; i < rows.length; i++) {
				var rowindex = $('#dg').datagrid('getRowIndex', rows[i]);
				$('#dg').datagrid('updateRow',{
					index: rowindex,
					row: {
						QAer: qaer
					}
				});
				markQAer.push(rows[i]);
			}
			endEditing();
		}
	}
	else
	{
		alert("请选择一键分配的QA")
	}
}
