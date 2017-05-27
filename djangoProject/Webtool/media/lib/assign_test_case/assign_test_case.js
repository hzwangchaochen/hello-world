var editIndex = undefined; 
var currentSheet='';
var currentProject='L13';
var currentUser='';

$(function(){
	$('#mtl_maingrid').datagrid({
		singleSelect:true,
		url:'/webtool/assign_test_case/getDataFromMysql/',
		fitColumns:true,
		height:'auto',
		rownumbers:true,
		pagination:true,
		pageSize:50,
		pageList:[50,100,150,200],
		collapsible:false,
		fit:true,
		nowrap : false,
		columns:[[
			{ field: 'check', title:'checkbox', align: 'center',checkbox:true},
			{ field: 'id', title:'序号', align: 'center', sortable:true},
			{ field: 'superClass', title:'大类型', align: 'center', sortable:true,width:10},
			{ field: 'mainClass', title:'类型', align: 'center', sortable:true,width:5},
			{ field: 'subClass', title:'子类型', align: 'center', sortable:true},
			{ field: 'detail', title:'描述', align: 'left'},
			{ field: 'testStep', title:'测试步骤', align: 'left'},
			{ field: 'expectedResult', title:'预期结果', align: 'left'},
			{ field: 'timeNode', title:'时间节点', align: 'center', sortable:true,
			editor:{
					type:'combobox',
					options:{
						valueField:'id',
						textField:'timeNode',
						data:[{id:'公司内测',timeNode:'公司内测'},{id:'渠道测试',timeNode:'渠道测试'},{id:'正式上线',timeNode:'正式上线'},{id:'每月例检',timeNode:'每月例检'}],
					}
				}  
			},
			{ field: 'ifExists', title:'是否有该功能', align: 'center', sortable:true,
			editor:{
					type:'combobox',
					options:{
						valueField:'id',
						textField:'ifExists',
						data:[{id:'是',ifExists:'是'},{id:'否',ifExists:'否'}],
					}
				}  
			},
			
			{ field: 'ifPass', title:'是否通过', align: 'center',
				editor:{
					type:'combobox',
					options:{
						valueField:'id',
						textField:'ifPass',
						data:[{id:'1',ifPass:'1'},{id:'0',ifPass:'0'}],
					}
				}  
			},
			
			{ field: 'executor', title:'执行者', align: 'center',
				editor:{
					type:'combobox',
					options:{
						valueField:'id',
						textField:'executor',
						data:[
							{id:'空',executor:''},
							{id:'MTL',executor:'MTL'},
							{id:'项目组',executor:'项目组'},
							{id:'不适用',executor:'不适用'},
							{id:'分页加载',executor:'分页加载'},
							{id:'接了微策略',executor:'接了微策略'}
						],
					}
				}  
			},
			{field: 'comments', title:'备注', align: 'center',editor:'text',sortable:true},
			{field: 'phonetype', title:'测试机型(安卓:A&苹果B)', align: 'center',editor:'text',sortable:true,
				editor:{
						type:'combobox',
						options:{
							valueField:'id',
							textField:'phonetype',
							data:[
								{id:'空',phonetype:''},
								{id:'A',phonetype:'A'},
								{id:'B',phonetype:'B'},
								{id:'AB',phonetype:'AB'}
							],
						}
					} 
			},
			{field:'action',title:'Action',align:'center',
				formatter:function(value,row,index){
					var s = "<a href='#' onclick=saverow("+index+")>Save</a>";
					return s;
				} 
			}
		]],
	
		onDblClickRow: function(rowIndex, rowData){
			if (editIndex != rowIndex){
				if (endEditing()){
					$('#mtl_maingrid').datagrid('selectRow', rowIndex)
					$('#mtl_maingrid').datagrid('beginEdit', rowIndex);
					editIndex = rowIndex;
				} else {
					$('#mtl_maingrid').datagrid('selectRow', editIndex);
				}
			}
		},
	});
	$('#Project_to_select').combobox({
		onChange: function(newValue,oldValue){
			selectProject(newValue);
			editIndex = undefined;
		}
	});

	$('#mtl_tree').tree({
		url:'/webtool/assign_test_case/findAllSqlName/'+currentProject+'/',
		onlyLeafCheck:true,
		onClick:function(node){
			if($('#mtl_tree').tree('isLeaf',node.target))
			{
				selectTable(node.text);
			}
		},
		onContextMenu: function (e,node) { //右键时触发事件  
			//三个参数：e里面的内容很多，真心不明白，rowIndex就是当前点击时所在行的索引，rowData当前行的数据
			if(!$('#mtl_tree').tree('isLeaf',node.target))
			{
				e.preventDefault(); //阻止浏览器捕获右键事件
				$('#mtl_tree').tree('select', node.target);			
				$('#menu').menu('show', {  
					//显示右键菜单  
					left: e.pageX,//在鼠标点击处显示菜单  
					top: e.pageY  
				});  
				e.preventDefault();  //阻止浏览器自带的右键菜单弹出  	
			}			

		} 		
	});
	currentUser=document.getElementById('currentuser').innerHTML;
});


Date.prototype.Format = function(fmt)   
{ //author: meizz   
  var o = {   
    "M+" : this.getMonth()+1,                 //月份   
    "d+" : this.getDate(),                    //日   
    "h+" : this.getHours(),                   //小时   
    "m+" : this.getMinutes(),                 //分   
    "s+" : this.getSeconds(),                 //秒   
    "q+" : Math.floor((this.getMonth()+3)/3), //季度   
    "S"  : this.getMilliseconds()             //毫秒   
  };   
  if(/(y+)/.test(fmt))   
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));   
  for(var k in o)   
    if(new RegExp("("+ k +")").test(fmt))   
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
  return fmt;   
}  

function endEditing(){
	if (editIndex == undefined)
		return true;
	
	if ($('#mtl_maingrid').datagrid('validateRow', editIndex)){
		$('#mtl_maingrid').datagrid('endEdit', editIndex);
		saverow(editIndex);
		editIndex = undefined;
		
		return true;
	} 
	else 
		return false;

}
	
function export_excel()
{
    //alert(currentSheet);
    if(currentSheet==null || currentSheet=="")
        alert('请选择所要导出的表格');
    else
        window.open("/webtool/assign_test_case/exportToExcel/"+currentSheet+"/");
}
            
function search_tb(){
	$('#mtl_maingrid').datagrid({
		url:'/webtool/assign_test_case/searchDataFromMysql/',
		queryParams:
		{
			Sheet:currentSheet,
			superClass:document.getElementById('input_superClass').value,
			mainClass:document.getElementById('input_mainClass').value
		}
	});
}

function selectProject(newValue)
{
	currentSheet='';
	currentProject=newValue;

	$('#mtl_maingrid').datagrid(
		'reload',
		{
			Sheet:'EmptyForTestCase'
		}
	);
	
	$('#mtl_tree').tree({
		url:'/webtool/assign_test_case/findAllSqlName/'+currentProject+'/',
	});	
};

function selectTable(value)
{
	currentSheet=value;
	editIndex = undefined;
	$('#mtl_maingrid').datagrid(
		'reload',
		{
			Sheet:currentSheet
		}
	);
};


function getResult()
{
	if(currentSheet=='') 
		alert('请选择测试用例集');
	else 
		window.open('/webtool/assign_test_case/getResultIndex/'+currentSheet+'/');
};

		
function saverow(index){
	//alert('该功能尚未完善');
	$('#mtl_maingrid').datagrid('endEdit',index);
	editIndex = undefined;
	var rows = $('#mtl_maingrid').datagrid('getData').rows;
	$.post("/webtool/assign_test_case/updateDataToMysql/",
	{
		Sheet:currentSheet,
		id:rows[index]['id'],
		detail:rows[index]['detail'],
		testStep:rows[index]['testStep'],
		expectedResult:rows[index]['expectedResult'],
		timeNode:rows[index]['timeNode'],
		ifExists:rows[index]['ifExists'],
		ifPass:rows[index]['ifPass'],
		executor:rows[index]['executor'],
		comments:rows[index]['comments'],
		phonetype:rows[index]['phonetype']	
	});	
};

function showColumn(obj)
{          	
	if (obj.checked) {
		switch (obj.value)
		{
			case '大类型':
				$('#mtl_maingrid').datagrid('showColumn','superClass');
				break;
			case '类型':
				$('#mtl_maingrid').datagrid('showColumn','mainClass');
				break;
			case '子类型':
				$('#mtl_maingrid').datagrid('showColumn','subClass');
				break;
			case '描述':
				$('#mtl_maingrid').datagrid('showColumn','detail');
				break;
			case '测试步骤':
				$('#mtl_maingrid').datagrid('showColumn','testStep');
				break;
			case '预期结果':
				$('#mtl_maingrid').datagrid('showColumn','expectedResult');
				break;
			case '时间节点':
				$('#mtl_maingrid').datagrid('showColumn','timeNode');
				break;
			case '是否有该功能':
				$('#mtl_maingrid').datagrid('showColumn','ifExists');
				break;
			case '是否通过':
				$('#mtl_maingrid').datagrid('showColumn','ifPass');
				break;
			case '执行者':
				$('#mtl_maingrid').datagrid('showColumn','executor');
				break;
			case '备注':
				$('#mtl_maingrid').datagrid('showColumn','comments');
				break;
			default:
				break;	 
		}				
	}
	
	else	
	{
		switch (obj.value)
		{
			case '大类型':
				$('#mtl_maingrid').datagrid('hideColumn','superClass');
				break;
			case '类型':
				$('#mtl_maingrid').datagrid('hideColumn','mainClass');
				break;
			case '子类型':
				$('#mtl_maingrid').datagrid('hideColumn','subClass');
				break;
			case '描述':
				$('#mtl_maingrid').datagrid('hideColumn','detail');
				break;
			case '测试步骤':
				$('#mtl_maingrid').datagrid('hideColumn','testStep');
				break;
			case '预期结果':
				$('#mtl_maingrid').datagrid('hideColumn','expectedResult');
				break;
			case '时间节点':
				$('#mtl_maingrid').datagrid('hideColumn','timeNode');
				break;
			case '是否有该功能':
				$('#mtl_maingrid').datagrid('hideColumn','ifExists');
				break;
			case '是否通过':
				$('#mtl_maingrid').datagrid('hideColumn','ifPass');
				break;
			case '执行者':
				$('#mtl_maingrid').datagrid('hideColumn','executor');
				break;
			case '备注':
				$('#mtl_maingrid').datagrid('hideColumn','comments');
				break;
			default:
				break;	
		} 
	}
}

function addNewTestCases()
{
    if(currentUser!='dong.xd'&&currentUser!='hzzhujie'&&currentUser!='hzwangchaochen') alert('权限未开放');
    else{
			layer.prompt({
			title: '请输入要添加的测试用例集',
			formType: 0, //prompt风格，支持0-2
			value:null
			},
			function(value,index,elem){
				var re=/^[\u4E00-\u9FA5]+$/;
				var timeString=new Date().Format("yyyyMM"); 
				if(value.length>10) 
				{
					layer.alert('输入的名称过长');
					return;
				}
				for(var i=0;i<value.length;i++)
				{
					if(!(value[i]>='0'&&value[i]<='9') && !(value[i]>='a'&&value[i]<='z') && !(value[i]>='A'&&value[i]<='Z')&&!re.test(value[i]))
					{
						layer.alert('命名不规范');
						return;						
					}
				}
				var roots=$('#mtl_tree').tree('getRoots');
				var newname=value+'_'+timeString;
				for(i=0;i<roots.length;i++){
					if(roots[i].text===newname) 
					{
						layer.alert('测试用例集'+newname+'已存在');
						return;
					}	
				}
				layer.alert('创建新的测试用例集:'+value, 1);
				$.post("/webtool/assign_test_case/addTestCase/",
				{
					casename:newname,
					projectname:currentProject
				});
				setTimeout(function(){$('#mtl_tree').tree({url:'/webtool/assign_test_case/findAllSqlName/'+currentProject+'/'});},1000);
			});
        }
}	


function deleteTestCases()
{
	if(currentUser!='dong.xd'&&currentUser!='hzzhujie'&&currentUser!='hzwangchaochen') alert('权限未开放');
	else{
		layer.prompt({
		title: '请输入要删除的测试用例集',
		formType: 0, //prompt风格，支持0-2
		value:null
		},
		function(value,index,elem){
			if(value=="标准测试用例集") 
			{
				layer.msg("不能删除标准测试用例集!");
				return ;
			}
			var roots=$('#mtl_tree').tree('getRoots');
			for(i=0;i<roots.length;i++)
			{
				if(roots[i].text===value) 
				{
					var childnodes=$('#mtl_tree').tree('getChildren',roots[i].target);
					layer.alert('已删除测试用例集:'+value, 1);
					$.post("/webtool/assign_test_case/deleteTestCase/",
					{
						tablename1:childnodes[0].text,
						tablename2:childnodes[1].text
					});
					setTimeout(function(){$('#mtl_tree').tree({url:'/webtool/assign_test_case/findAllSqlName/'+currentProject+'/'});},1000);
					return;
				}
			}
			layer.alert('测试用例集'+value+'不存在');
			return;		
		});
    }
}

function removeIt()
{
	if(currentUser!='dong.xd'&&currentUser!='hzzhujie') alert('权限未开放');
    else{
		var node = $('#mtl_tree').tree('getSelected');
		if(node.text=="标准测试用例集")
		{
			layer.msg("不能删除标准测试用例集!");
			return;	
		}
		layer.confirm('是否删除此测试用例集？',function(index){
			//do something
			//alert('删除成功');
			var childnodes=$('#mtl_tree').tree('getChildren',node.target);
			$.post("/webtool/assign_test_case/deleteTestCase/",
			{
				tablename1:childnodes[0].text,
				tablename2:childnodes[1].text
			});
			setTimeout(function(){$('#mtl_tree').tree({url:'/webtool/assign_test_case/findAllSqlName/'+currentProject+'/'});},1000);
			layer.close(index);
		});	
	}
	
}

function getMTLTrend()
{
	window.open('/webtool/assign_test_case/getTrend/'+currentProject+'/');
}

function getAllTrend()
{
	window.open('/webtool/assign_test_case/getTrendAllIndex/');
}

function scenePowerConsumption()
{
	window.open('/webtool/assign_test_case/sceneIndex/');
}








