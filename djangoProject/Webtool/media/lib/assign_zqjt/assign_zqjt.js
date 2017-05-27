var editIndex = undefined; 
var lastState= []; 
var currentSheet="ust_hangulstrings";
var lastQA=[];
var currentQA="";
var onEdit=[];
var AfterAllOperation=false;
$(function(){
	$('#svn_maingrid').datagrid({
		//singleSelect:true,
		selectOnCheck:true,
        checkOnSelect:true,
		url:'/webtool/assign_zqjt/getDataFromMysql/',
		fitColumns:true,
		height:'auto',
		rownumbers:true,

		pagination:true,
		pageSize:50,
		pageList:[50,100,150,200],
		collapsible:false,
		fit:true,
		nowrap:false,
		columns:[[
			{ field: 'check', title:'checkbox', align: 'left',checkbox:true},
			{ field: 'column0', title:'column0', align: 'left', sortable:true,width:5},
			{ field: 'column1', title:'column1', align: 'left', sortable:true,width:10,
				formatter: function (value, row){
					if(value!=undefined)
						return value.replace(/</g,"&lt;").replace(/>/g,"&gt;");
					else
						return value;
				}
			},
			{ field: 'column2', title:'column2', align: 'left', sortable:true,width:50,
				formatter: function (value, row){
					if(value!=undefined)
						return value.replace(/</g,"&lt;").replace(/>/g,"&gt;");
					else
						return value;
				}
			},
			{ field: 'column3', title:'column3', align: 'left', sortable:true,width:10},
			{ field: 'column4', title:'column4', align: 'left', sortable:true,width:80,
				formatter: function (value, row){
					if(value!=undefined)
						return value.replace(/</g,"&lt;").replace(/>/g,"&gt;");
					else
						return value;
				}
			},
			{ field: 'column5', title:'column5', align: 'left', sortable:true,width:10},
			{ field: 'column6', title:'column6', align: 'left', sortable:true,width:10},
			{ field: 'QAer', title:'跟进QA', align: 'center', sortable:true,width:10,                  
				editor:{
					type:'combobox',
					options:{
						valueField:'id',
						textField:'QAer',
						data:[{id:'请选择',QAer:'请选择'},{id:'黄超群',QAer:'黄超群'},{id:'汪斌',QAer:'汪斌'},
						{id:'朱军',QAer:'朱军'},{id:'徐勇军',QAer:'徐勇军'}],
						required:true
					}
				}               
			},
			{ field: 'isFinished', title:'状态', align: 'center', sortable:true,width:20,
				formatter:function(value,rowData,rowIndex){
							if(value == '完成'){
								return "<font color='red'>"+ value +"<\/font>";
							}else{
								return value;
							}
						},   
				editor:{
					type:'combobox',
					options:{
						valueField:'id',
						textField:'isFinished',
						data:[{id:'完成',isFinished:'完成'},{id:'未完成',isFinished:'未完成'},{id:'文本已测',isFinished:'文本已测'},{id:'暂未找到',isFinished:'暂未找到'},{id:'未翻译',isFinished:'未翻译'}],
						required:true
					}
				}  
			},
			
			{field:'action',title:'Action',align:'center',width:20,
				formatter:function(value,row,index){
					var s = "<a href='#' onclick=saverow("+index+")>Save</a>";
					return s;
				} 
			}
		]],
		
		onDblClickRow: function(rowIndex, rowData){
				lastState[rowIndex]=rowData.isFinished;
				lastQA[rowIndex]=rowData.QAer;
				onEdit[rowIndex]=true;
				$(this).datagrid('checkRow',rowIndex);
				$(this).datagrid('beginEdit', rowIndex); 
				editIndex = rowIndex;
		},
		onSelect: function(rowIndex, rowData){
			if(AfterAllOperation==true)
			{
				AfterAllOperation=false;
				$('#svn_maingrid').datagrid('unselectAll');
				$('#svn_maingrid').datagrid('selectRow',rowIndex);					
			}				
		},
	});
	
	$('#svn_treegrid').treegrid({
		singleSelect:true,
		selectOnCheck:true,
        checkOnSelect:true,
		url:'/webtool/assign_zqjt/findAllSqlName/',
		idField:'Tables_in_leiting',
		treeField:'name',
		columns:[[
			{ field: 'check', title:'checkbox', align: 'left', width: 10,checkbox:true},
			{title:'主目录',field:'Tables_in_leiting',
				formatter:function(value,rowData){
					var s = "<a href='#' onclick=selectTable('"+value+"')>"+value+"</a>";
					return s;
				}
			}
		]]
	});
	
	selectQA();	
})

function selectQA()
{
	var currentuser=document.getElementById('currentuser').innerHTML;
	switch(currentuser)
	{
		case 'hzhuangchaoqun':
			currentQA="黄超群";
			break;
		case 'hzwangbin2013':
			currentQA="汪斌";
			break;
		case 'wb.lh.zhujun':
			currentQA="朱军";
			break;
		case 'wb.lh.xuyongjun':
			currentQA="徐勇军";
			break;
		default:
			currentQA="";
			break;
	}
}

function selectTable(value)
{
	currentSheet=value;
	editIndex = undefined;
	$('#svn_maingrid').datagrid(
		'reload',
		{
			Sheet:currentSheet,
			QA:$('#QA_to_select').combobox('getValue'),
			state:$('#state_to_select').combobox('getValue')
		}
	)
}

function export_excel()
{
	if(currentSheet=='' ||currentSheet=='ust_hangulstrings')
		alert('请选择所要导出的表格');
	else	window.open("http://192.168.131.233:9090/webtool/assign_zqjt/exportToExcel/"+currentSheet);
}

function delete_table()
{
	var nodes = $('#svn_treegrid').treegrid('getSelections');

	if(currentQA!="黄超群") 
	{
		alert("权限未开放!!");
		return;
	}
	
	if(nodes.length==0) 
	{
		alert('请选择要删除的表');
		return; 	
	}

	for(var i=0; i<nodes.length; i++)
	{
		var r=confirm("确定要删除表"+nodes[i].Tables_in_leiting+"?");
		if(r){
			$.ajax(
					{
						url: "/webtool/assign_zqjt/deleteTable/"+nodes[i].Tables_in_leiting+"/",
						type: 'POST',
						cache: false,
						success: function () {
							reloadTreeGrid();
						}
					}
				);	
		}
	}
	$("#svn_treegrid").treegrid("unselectAll");	 
}

function reloadTreeGrid()
{
	$('#svn_treegrid').treegrid('reload');
}


function saverow(index){
	onEdit[index]=false;
	$('#svn_maingrid').datagrid('endEdit',index);
	var rows = $('#svn_maingrid').datagrid('getData').rows;
	if(lastState[index]=='完成' && rows[index]['isFinished']=='未完成'&&currentQA!='黄超群') 
	{
		alert("不能将已完成的任务改为未完成!!");
		$('#svn_maingrid').datagrid('beginEdit',index);
		onEdit[index]=true;
	}
	if(lastState[index]=='完成' && rows[index]['isFinished']=='文本已测'&&currentQA!='黄超群') 
	{
		alert("不能将已完成的任务改为文本已测!!");
		$('#svn_maingrid').datagrid('beginEdit',index);
		onEdit[index]=true;
	}
	else if(rows[index]['QAer']!=currentQA&&rows[index]['QAer']!=lastQA[index]&&currentQA!='黄超群')
	{		
		alert("不能将任务分配给他人!!");	
		$('#svn_maingrid').datagrid('beginEdit',index);
		onEdit[index]=true;
	}
	else	
		$.post("/webtool/assign_zqjt/updateDataToMysql/",{Sheet:currentSheet,column0:rows[index]['column0'],QAer:rows[index]['QAer'],isFinished:rows[index]['isFinished']});
}

function save_to_db(){
	var Index;
	var rows = $('#svn_maingrid').datagrid('getData').rows;
	for (Index = 0; Index < rows.length; Index++)
	{
		if(onEdit[Index]==true)
		{
			$('#svn_maingrid').datagrid('endEdit',Index);
			onEdit[Index]=false;
			if(lastState[Index]=='完成' && rows[Index]['isFinished']=='未完成'&&currentQA!='黄超群') 
			{
				alert("不能将已完成的任务改为未完成!!");
				$('#svn_maingrid').datagrid('beginEdit',Index);
				onEdit[Index]=true;
				return;
			}
			else if(lastState[Index]=='完成' && rows[Index]['isFinished']=='文本已测'&&currentQA!='黄超群') 
			{
				alert("不能将已完成的任务改为文本已测!!");
				$('#svn_maingrid').datagrid('beginEdit',Index);
				onEdit[Index]=true;
				return;
			}
			else if(rows[Index]['QAer']!=currentQA&&currentQA!='黄超群'&&rows[Index]['QAer']!=lastQA[Index])
			{		
				alert("不能将任务分配给他人!!");	
				$('#svn_maingrid').datagrid('beginEdit',Index);
				onEdit[Index]=true;
				return;
			}
			else	$.post("/webtool/assign_zqjt/updateDataToMysql/",{Sheet:currentSheet,column0:rows[Index]['column0'],QAer:rows[Index]['QAer'],isFinished:rows[Index]['isFinished']});
		}		
	}
	AfterAllOperation=true;
}


function completeAll()
{
	var rows = $('#svn_maingrid').datagrid('getChecked');
	if(rows.length){
		for (var i = 0; i < rows.length; i++) 
		{
			var rowindex = $('#svn_maingrid').datagrid('getRowIndex', rows[i]);
			$('#svn_maingrid').datagrid('beginEdit', rowindex);
			$('#svn_maingrid').datagrid('updateRow',{index:rowindex,row:{isFinished:'完成',QAer:currentQA}});
			$('#svn_maingrid').datagrid('endEdit', rowindex);
			$.post("/webtool/assign_zqjt/updateDataToMysql/",{Sheet:currentSheet,column0:rows[i].column0,QAer:currentQA,isFinished:'完成'});
			onEdit[rowindex]=false;		
		}
	}
	AfterAllOperation=true;
}
function texttestedAll()
{
	var rows = $('#svn_maingrid').datagrid('getChecked');
	if(rows.length){
		for (var i = 0; i < rows.length; i++) 
		{
			var rowindex = $('#svn_maingrid').datagrid('getRowIndex', rows[i]);
			$('#svn_maingrid').datagrid('beginEdit', rowindex);
			$('#svn_maingrid').datagrid('updateRow',{index:rowindex,row:{isFinished:'文本已测',QAer:currentQA}});
			$('#svn_maingrid').datagrid('endEdit', rowindex);
			$.post("/webtool/assign_zqjt/updateDataToMysql/",{Sheet:currentSheet,column0:rows[i].column0,QAer:currentQA,isFinished:'文本已测'});
			onEdit[rowindex]=false;			
		}
	}
	AfterAllOperation=true;
}

function notfoundAll()
{
	var rows = $('#svn_maingrid').datagrid('getChecked');
	if(rows.length){
		for (var i = 0; i < rows.length; i++) 
		{
			var rowindex = $('#svn_maingrid').datagrid('getRowIndex', rows[i]);
			$('#svn_maingrid').datagrid('beginEdit', rowindex);
			$('#svn_maingrid').datagrid('updateRow',{index:rowindex,row:{isFinished:'暂未找到',QAer:currentQA}});
			$('#svn_maingrid').datagrid('endEdit', rowindex);
			$.post("/webtool/assign_zqjt/updateDataToMysql/",{Sheet:currentSheet,column0:rows[i].column0,QAer:currentQA,isFinished:'暂未找到'});	
			onEdit[rowindex]=false;	
		}
	}
	AfterAllOperation=true;
}

function nottransAll()
{
	var rows = $('#svn_maingrid').datagrid('getChecked');
	if(rows.length){
		for (var i = 0; i < rows.length; i++) 
		{
			var rowindex = $('#svn_maingrid').datagrid('getRowIndex', rows[i]);
			$('#svn_maingrid').datagrid('beginEdit', rowindex);
			$('#svn_maingrid').datagrid('updateRow',{index:rowindex,row:{isFinished:'未翻译',QAer:currentQA}});
			$('#svn_maingrid').datagrid('endEdit', rowindex);
			$.post("/webtool/assign_zqjt/updateDataToMysql/",{Sheet:currentSheet,column0:rows[i].column0,QAer:currentQA,isFinished:'未翻译'});	
			onEdit[rowindex]=false;	
		}
	}
	AfterAllOperation=true;
}

function notcompleteAll()
{
	if(currentQA!="黄超群"){
		alert("权限未开放");
		return;
	}
	var rows = $('#svn_maingrid').datagrid('getChecked');
	if(rows.length){
		for (var i = 0; i < rows.length; i++) 
		{
			var rowindex = $('#svn_maingrid').datagrid('getRowIndex', rows[i]);
			$('#svn_maingrid').datagrid('beginEdit', rowindex);
			$('#svn_maingrid').datagrid('updateRow',{index:rowindex,row:{isFinished:'未完成',QAer:currentQA}});
			$('#svn_maingrid').datagrid('endEdit', rowindex);
			$.post("/webtool/assign_zqjt/updateDataToMysql/",{Sheet:currentSheet,column0:rows[i].column0,QAer:currentQA,isFinished:'未完成'});	
			onEdit[rowindex]=false;	
		}
	}
	AfterAllOperation=true;
}

function search_data(){
	$('#svn_maingrid').datagrid({
		url:'/webtool/assign_zqjt/getDataFromMysql/',
		queryParams:
		{
			Sheet:currentSheet,
			QA:$('#QA_to_select').combobox('getValue'),
			state:$('#state_to_select').combobox('getValue')
		}
	});
}

function search_tb(){
	$('#svn_maingrid').datagrid({
		url:'/webtool/assign_zqjt/searchDataFromMysql/',
		queryParams:
		{
			Sheet:currentSheet,
			QA:$('#QA_to_select').combobox('getValue'),
			state:$('#state_to_select').combobox('getValue'),
			column0:document.getElementById('input_column0').value,
			column1:document.getElementById('input_column1').value,
			column2:document.getElementById('input_column2').value,
			column4:document.getElementById('input_column4').value
			
		}
	});
}
document.onkeydown=keyListener;   
function keyListener(e){
	//  当按下回车键，执行我们的代码
	if(e.keyCode == 13){
		search_tb();
		}
}  
function assign(){
	if(currentQA!="黄超群") 
	{
		alert("权限未开放!!");
	}
	else{
		var rows = $('#svn_maingrid').datagrid('getChecked');	
		var qa_name=$('#allocate_qaer').combobox('getValue');
		if(rows.length){
			for (var i = 0; i < rows.length; i++) 
			{
				var rowindex = $('#svn_maingrid').datagrid('getRowIndex', rows[i]);
				$('#svn_maingrid').datagrid('beginEdit', rowindex);
				$('#svn_maingrid').datagrid('updateRow',{index:rowindex,row:{QAer:qa_name}});
				$('#svn_maingrid').datagrid('endEdit', rowindex);
				$.post("/webtool/assign_zqjt/updateDataToMysql/",{Sheet:currentSheet,column0:rows[i].column0,QAer:qa_name,isFinished:rows[i].isFinished});
			}
		}
	}
	AfterAllOperation=true;
}

function get_result()
{
		if(currentSheet=="ust_hangulstrings")
			alert("请选择表格");
		else 
			window.open('/webtool/assign_zqjt/getResultIndex/'+currentSheet+'/');
}


















