
function GetDateTimeStr(AddDayCount) {
	var dd = new Date();
	dd.setDate(dd.getDate()+AddDayCount);//»ñÈ¡AddDayCountÌìºóµÄÈÕÆÚ
	var y = dd.getFullYear();
	var m = dd.getMonth()+1;//»ñÈ¡µ±Ç°ÔÂ·ÝµÄÈÕÆÚ
	var d = dd.getDate();
	var h = dd.getHours();
	var min = dd.getMinutes();
	return y+"-"+m+"-"+d+" "+"00"+":"+"00";
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

	$('#starttime_person').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_person').datagrid(
		'reload',
		{
			starttime:$('#starttime_person').datetimebox('getValue'),
			personName:$('#custom_person').combobox('getValue'),
		}
	);

	$('#starttime_new').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_new').datagrid(
		'reload',
		{
			starttime:$('#starttime_new').datetimebox('getValue'),
		}
	);
	$('#starttime_free').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_free').datagrid(
		'reload',
		{
			starttime:$('#starttime_free').datetimebox('getValue'),
		}
	);
	$('#starttime_pay').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_pay').datagrid(
		'reload',
		{
			starttime:$('#starttime_pay').datetimebox('getValue'),
		}
	);
	$('#starttime_sell').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_sell').datagrid(
		'reload',
		{
			starttime:$('#starttime_sell').datetimebox('getValue'),
		}
	);



	$('#starttime_japan_free').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_japan_free').datagrid(
		'reload',
		{
			starttime:$('#starttime_japan_free').datetimebox('getValue'),
		}
	);
	$('#starttime_japan_pay').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_japan_pay').datagrid(
		'reload',
		{
			starttime:$('#starttime_japan_pay').datetimebox('getValue'),
		}
	);
	$('#starttime_japan_sell').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_japan_sell').datagrid(
		'reload',
		{
			starttime:$('#starttime_japan_sell').datetimebox('getValue'),
		}
	);
	$('#starttime_american_free').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_american_free').datagrid(
		'reload',
		{
			starttime:$('#starttime_american_free').datetimebox('getValue'),
		}
	);
	$('#starttime_american_sell').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_american_sell').datagrid(
		'reload',
		{
			starttime:$('#starttime_american_sell').datetimebox('getValue'),
		}
	);
	$('#starttime_american_pay').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_american_pay').datagrid(
		'reload',
		{
			starttime:$('#starttime_american_pay').datetimebox('getValue'),
		}
	);
	$('#starttime_korea_free').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_korea_free').datagrid(
		'reload',
		{
			starttime:$('#starttime_korea_free').datetimebox('getValue'),
		}
	);
	$('#starttime_korea_sell').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_korea_sell').datagrid(
		'reload',
		{
			starttime:$('#starttime_korea_sell').datetimebox('getValue'),
		}
	);
	$('#starttime_korea_pay').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_korea_pay').datagrid(
		'reload',
		{
			starttime:$('#starttime_korea_pay').datetimebox('getValue'),
		}
	);
	
	$('#starttime_qq').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_qq').datagrid(
		'reload',
		{
			starttime:$('#starttime_qq').datetimebox('getValue'),
		}
	);
	$('#starttime_91').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_91').datagrid(
		'reload',
		{
			starttime:$('#starttime_91').datetimebox('getValue'),
		}
	);
	$('#starttime_360').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_360').datagrid(
		'reload',
		{
			starttime:$('#starttime_360').datetimebox('getValue'),
		}
	);
	$('#starttime_baidu').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_baidu').datagrid(
		'reload',
		{
			starttime:$('#starttime_baidu').datetimebox('getValue'),
		}
	);
	$('#starttime_google').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_google').datagrid(
		'reload',
		{
			starttime:$('#starttime_google').datetimebox('getValue'),
		}
	);
	$('#starttime_self').datetimebox('setValue', GetDateTimeStr(-1));
	$('#dg_self').datagrid(
		'reload',
		{
			starttime:$('#starttime_self').datetimebox('getValue'),
		}
	);
})


/*
function trend_new()
{
		alert('没开放')
}
*/




function drawPic(rows,channel,op)
{
	if( rows.length && rows.length >= 1 )
	{
		var str = ""
		for (var i = 0; i < rows.length; i++)
		{
			str = str + rows[i].gameName + "||"
		}
	   	window.open ('drawAppsTracePic.php?gameNameStr=' + str + "&channel=" + channel+"&option="+op)
	}
	else
	{
		alert("请选择至少一个app对象！")
	}
}


function drawPic4android(rows,channel,op)
{
	if( rows.length && rows.length >= 1 )
	{
		var str = ""
		for (var i = 0; i < rows.length; i++)
		{
			str = str + rows[i].gameName + "||"
		}
	   	window.open ('drawAppsTracePic4android.php?gameNameStr=' + str + "&channel=" + channel+"&option="+op)
	}
	else
	{
		alert("请选择至少一个app对象！")
	}
}


function trend_person()
{
	var rows = $('#dg_person').datagrid('getSelections');
	//var op= $("#op_pay").find("option:selected").text();
	var op=$('#op_person').combobox('getValue');
	if( rows.length && rows.length >= 1 )
	{
		var $flag=true;
		for (var i = 1; i < rows.length; i++)
		{
			if(rows[i].channel!=rows[i-1].channel)
			{
				alert("请选择相同来源的app对象！");
				return 0;
			}
		}
		drawPic(rows,rows[0].channel,op);
	}
	else
	{
		alert("请选择至少一个app对象！")
	}
}

function trend_pay()
{
	var rows = $('#dg_pay').datagrid('getSelections');
	//var op= $("#op_pay").find("option:selected").text();
	var op=$('#op_pay').combobox('getValue');
	drawPic(rows,'ios_chinaIphone_pay',op);
}


function trend_free()
{
	var rows = $('#dg_free').datagrid('getSelections');
	var op=$('#op_free').combobox('getValue');
	drawPic(rows,'ios_chinaIphone_free',op);
}

function trend_sell()
{
	var rows = $('#dg_sell').datagrid('getSelections');
	var op=$('#op_sell').combobox('getValue');
	drawPic(rows,'ios_chinaIphone_sell',op);
}


function trend_pay_ipad()
{
	var rows = $('#dg_pay_ipad').datagrid('getSelections');
	var op=$('#op_pay_ipad').combobox('getValue');
	drawPic(rows,'ios_chinaIpad_pay',op);
}


function trend_free_ipad()
{
	var rows = $('#dg_free_ipad').datagrid('getSelections');
	var op=$('#op_free_ipad').combobox('getValue');
	drawPic(rows,'ios_chinaIpad_free',op);
}

function trend_sell_ipad()
{
	var rows = $('#dg_sell_ipad').datagrid('getSelections');
	var op=$('#op_sell_ipad').combobox('getValue');
	drawPic(rows,'ios_chinaIpad_sell',op);
}
function trend_japan_free()
{
	var rows = $('#dg_japan_free').datagrid('getSelections');
	var op=$('#op_japan_free').combobox('getValue');
	drawPic(rows,'ios_japanIphone_free',op);
}
function trend_japan_sell()
{
	var rows = $('#dg_japan_sell').datagrid('getSelections');
	var op=$('#op_japan_sell').combobox('getValue');
	drawPic(rows,'ios_japanIphone_sell',op);
}
function trend_japan_pay()
{
	var rows = $('#dg_japan_pay').datagrid('getSelections');
	var op=$('#op_japan_pay').combobox('getValue');
	drawPic(rows,'ios_japanIphone_pay',op);
}

function trend_american_free()
{
	var rows = $('#dg_american_free').datagrid('getSelections');
	var op=$('#op_american_free').combobox('getValue');
	drawPic(rows,'ios_americanIphone_free',op);
}
function trend_american_sell()
{
	var rows = $('#dg_american_sell').datagrid('getSelections');
	var op=$('#op_american_sell').combobox('getValue');
	drawPic(rows,'ios_americanIphone_sell',op);
}
function trend_american_pay()
{
	var rows = $('#dg_american_pay').datagrid('getSelections');
	var op=$('#op_american_pay').combobox('getValue');
	drawPic(rows,'ios_americanIphone_pay',op);
}

function trend_korea_free()
{
	var rows = $('#dg_korea_free').datagrid('getSelections');
	var op=$('#op_korea_free').combobox('getValue');
	drawPic(rows,'ios_koreaIphone_free',op);
}
function trend_korea_sell()
{
	var rows = $('#dg_korea_sell').datagrid('getSelections');
	var op=$('#op_korea_sell').combobox('getValue');
	drawPic(rows,'ios_koreaIphone_sell',op);
}
function trend_korea_pay()
{
	var rows = $('#dg_korea_pay').datagrid('getSelections');
	var op=$('#op_korea_pay').combobox('getValue');
	drawPic(rows,'ios_koreaIphone_pay',op);
}




function trend_taiwan_free()
{
	var rows = $('#dg_taiwan_free').datagrid('getSelections');
	var op=$('#op_taiwan_free').combobox('getValue');
	drawPic(rows,'ios_taiwanIphone_free',op);
}
function trend_taiwan_sell()
{
	var rows = $('#dg_taiwan_sell').datagrid('getSelections');
	var op=$('#op_taiwan_sell').combobox('getValue');
	drawPic(rows,'ios_taiwanIphone_sell',op);
}
function trend_taiwan_pay()
{
	var rows = $('#dg_taiwan_pay').datagrid('getSelections');
	var op=$('#op_taiwan_pay').combobox('getValue');
	drawPic(rows,'ios_taiwanIphone_pay',op);
}



function trend_japan_free_ipad()
{
	var rows = $('#dg_japan_free_ipad').datagrid('getSelections');
	var op=$('#op_japan_free_ipad').combobox('getValue');
	drawPic(rows,'ios_japanIpad_free',op);
}

function trend_japan_sell_ipad()
{
	var rows = $('#dg_japan_sell_ipad').datagrid('getSelections');
	var op=$('#op_japan_sell_ipad').combobox('getValue');
	drawPic(rows,'ios_japanIpad_sell',op);
}
function trend_japan_pay_ipad()
{
	var rows = $('#dg_japan_pay_ipad').datagrid('getSelections');
	var op=$('#op_japan_pay_ipad').combobox('getValue');
	drawPic(rows,'ios_japanIpad_pay',op);
}

function trend_american_free_ipad()
{
	var rows = $('#dg_american_free_ipad').datagrid('getSelections');
	var op=$('#op_american_free_ipad').combobox('getValue');
	drawPic(rows,'ios_americanIpad_free',op);
}
function trend_american_sell_ipad()
{
	var rows = $('#dg_american_sell_ipad').datagrid('getSelections');
	var op=$('#op_american_sell_ipad').combobox('getValue');
	drawPic(rows,'ios_americanIpad_sell',op);
}
function trend_american_pay_ipad()
{
	var rows = $('#dg_american_pay_ipad').datagrid('getSelections');
	var op=$('#op_american_pay_ipad').combobox('getValue');
	drawPic(rows,'ios_americanIpad_pay',op);
}

function trend_korea_free_ipad()
{
	var rows = $('#dg_korea_free_ipad').datagrid('getSelections');
	var op=$('#op_korea_free_ipad').combobox('getValue');
	drawPic(rows,'ios_koreaIpad_free',op);
}
function trend_korea_sell_ipad()
{
	var rows = $('#dg_korea_sell_ipad').datagrid('getSelections');
	var op=$('#op_korea_sell_ipad').combobox('getValue');
	drawPic(rows,'ios_koreaIpad_sell',op);
}
function trend_korea_pay_ipad()
{
	var rows = $('#dg_korea_pay_ipad').datagrid('getSelections');
	var op=$('#op_korea_pay_ipad').combobox('getValue');
	drawPic(rows,'ios_koreaIpad_pay',op);
}




function trend_taiwan_free_ipad()
{
	var rows = $('#dg_taiwan_free_ipad').datagrid('getSelections');
	var op=$('#op_taiwan_free_ipad').combobox('getValue');
	drawPic(rows,'ios_taiwanIpad_free',op);
}
function trend_taiwan_sell_ipad()
{
	var rows = $('#dg_taiwan_sell_ipad').datagrid('getSelections');
	var op=$('#op_taiwan_sell_ipad').combobox('getValue');
	drawPic(rows,'ios_taiwanIpad_sell',op);
}
function trend_taiwan_pay_ipad()
{
	var rows = $('#dg_taiwan_pay_ipad').datagrid('getSelections');
	var op=$('#op_taiwan_pay_ipad').combobox('getValue');
	drawPic(rows,'ios_taiwanIpad_pay',op);
}


function trend_self()
{
	var rows = $('#dg_self').datagrid('getSelections');
}

function trend_qq()
{
	var rows = $('#dg_qq').datagrid('getSelections');
	var op=$('#op_qq').combobox('getValue');
	drawPic4android(rows,'android_qq',op);
}

function trend_91()
{
	var rows = $('#dg_91').datagrid('getSelections');
	var op=$('#op_91').combobox('getValue');
	drawPic4android(rows,'android_91',op);
}
function trend_360()
{
	var rows = $('#dg_360').datagrid('getSelections');
	var op=$('#op_360').combobox('getValue');
	drawPic4android(rows,'android_360',op);
}
function trend_baidu()
{
	var rows = $('#dg_baidu').datagrid('getSelections');
	var op=$('#op_baidu').combobox('getValue');
	drawPic4android(rows,'android_baidu',op);
}
function trend_google()
{
	var rows = $('#dg_google').datagrid('getSelections');
	var op=$('#op_google').combobox('getValue');
	drawPic4android(rows,'android_google',op);
}


function expt_japan_sell()
{
	var rows = $('#dg_japan_sell').datagrid('getSelections');
	addcustomGame(rows);
}
function expt_japan_free()
{
	var rows = $('#dg_japan_free').datagrid('getSelections');
	addcustomGame(rows);
}
function expt_japan_pay()
{
	var rows = $('#dg_japan_pay').datagrid('getSelections');
	addcustomGame(rows);
}

function expt_american_sell()
{
	var rows = $('#dg_american_sell').datagrid('getSelections');
	addcustomGame(rows);
}
function expt_american_free()
{
	var rows = $('#dg_american_free').datagrid('getSelections');
	addcustomGame(rows);
}
function expt_american_pay()
{
	var rows = $('#dg_american_pay').datagrid('getSelections');
	addcustomGame(rows);
}
function expt_korea_sell()
{
	var rows = $('#dg_korea_sell').datagrid('getSelections');
	addcustomGame(rows);
}
function expt_korea_free()
{
	var rows = $('#dg_korea_free').datagrid('getSelections');
	addcustomGame(rows);
}
function expt_korea_pay()
{
	var rows = $('#dg_korea_pay').datagrid('getSelections');
	addcustomGame(rows);
}

function expt_pay()
{
	var rows = $('#dg_pay').datagrid('getSelections');
	addcustomGame(rows);
}


function expt_free()
{
	var rows = $('#dg_free').datagrid('getSelections');
	addcustomGame(rows);
}

function expt_sell()
{
	var rows = $('#dg_sell').datagrid('getSelections');
	addcustomGame(rows);
}


function addcustomGame(rows)
{
	var name = $('#custom_person').attr("name");	
	var num =0;
	if ( window.confirm("确定添加关注吗") )
	{
		if(rows.length && rows.length > 0)
		{
			for (var i = 0; i < rows.length; i++)
			{
				num = num +1
				var gameName = rows[i].gameName;
				$.ajax({
					url:'addCustomAppGame.php',
					data:{'personName':name,'gameName':gameName},
					type:'post',
					success:function(res){
					}
				})
			}
		}
		alert("你已成功的添加了" + num + "条关注")
	}
}

function expt_pay_ipad()
{
	var rows = $('#dg_pay_ipad').datagrid('getSelections');
	addcustomGame(rows);
}


function expt_free_ipad()
{
	var rows = $('#dg_free_ipad').datagrid('getSelections');
	addcustomGame(rows);
}

function expt_sell_ipad()
{
	var rows = $('#dg_sell_ipad').datagrid('getSelections');
	addcustomGame(rows);
}



function expt_qq()
{
	var rows = $('#dg_qq').datagrid('getSelections');
	addcustomGame(rows);
}

function expt_360()
{
	var rows = $('#dg_360').datagrid('getSelections');
	addcustomGame(rows);
}

function expt_91()
{
	var rows = $('#dg_91').datagrid('getSelections');
	addcustomGame(rows);
}
function expt_baidu()
{
	var rows = $('#dg_baidu').datagrid('getSelections');
	addcustomGame(rows);
}
function expt_google()
{
	var rows = $('#dg_google').datagrid('getSelections');
	addcustomGame(rows);
}
function expt_new()
{
	alert("导出")
}

function delete_person()
{
	var name = $("#custom_person").attr('name');	
	var str  = "确定删除 " + name + " 名下的私人定制吗?" 
	if ( window.confirm(str) )
	{
		var rows = $('#dg_person').datagrid('getSelections');
		if(rows.length && rows.length > 0)
		{
			var count=0
			for (var i = 0; i < rows.length; i++)
			{
				count=count+1
				var gameName = rows[i].gameName
				var country = rows[i].country
				$.ajax({
					url:'deleteCustomAppGame.php',
					data:{'personName':name,'gameName':gameName,'country':country},
					type:'post',
					success:function(res){
					}
					})
			}
			alert("你已经删除了" + count + "私人定制")
		}
		else
		{
			alert("请选择你要删除的定制app!")
		}
	}
}

function excel()
{
	var rows = $('#dg_person').datagrid('getSelections');
	if(rows.length && rows.length > 0)
	{
		$.ajax({
	      url:'generatePersonData.php',
	      data:{'rows':JSON.stringify(rows)},
	      type:'post',
	      success:function(returnData){
	      $.messager.show({
	          title:'ee',
	          msg:'Success to export to excel ' + returnData,
	          timeout:3000,
	          showType:'slide'
	            });
	    javascript:window.location='download_svnsubmit_excel.php?name='+returnData;
	    }
	   })
	}
	else
	{
		alert("请选择你要导出的行!")
	}
}

function doSearch_neteasy(){
	document.getElementById("dataType").value = "neteasy"
	$('#dg_person').datagrid(
		'reload',
		{
			starttime:$('#starttime_person').datetimebox('getValue'),
			neteasy:true,
		}
	);
}

function doSearch_leocool(){
	document.getElementById("dataType").value = "leocool"
	$('#dg_person').datagrid(
		'reload',
		{
			starttime:$('#starttime_person').datetimebox('getValue'),
			leocool:true,
		}
	);
}

function doSearch_shuru(){
	document.getElementById("dataType").value = "shuru"
	var shuru = $("#shuru_name").val();
	if( jQuery.trim(shuru) == "" )
	{
		alert("请输入app name！")
		return
	}
	else
	{
		$('#dg_person').datagrid(
			'reload',
			{
				starttime:$('#starttime_person').datetimebox('getValue'),
				shuru:$("#shuru_name").val(),
			}
		);
	}
}



function doSearch_person(){
	document.getElementById("dataType").value = "person"
	$('#dg_person').datagrid(
		'reload',
		{
			starttime:$('#starttime_person').datetimebox('getValue'),
			personName:$('#custom_person').attr('name'),
		}
	);
}

function doSearch_new(){
	$('#dg_new').datagrid(
		'reload',
		{
			starttime_new:$('#starttime_new').datetimebox('getValue'),
		}
	);
}


function doSearch_sell(){
	$('#dg_sell').datagrid(
		'reload',
		{
			starttime_sell:$('#starttime_sell').datetimebox('getValue'),
			type_sell:$('#type_sell').attr("name"),
		}
	);
}

function doSearch_free(){
	$('#dg_free').datagrid(
		'reload',
		{
			starttime_free:$('#starttime_free').datetimebox('getValue'),
			type_free:$('#type_free').attr("name"),
		}
	);
}

function doSearch_pay(){
	$('#dg_pay').datagrid(
		'reload',
		{
			starttime_pay:$('#starttime_pay').datetimebox('getValue'),
			type_pay:$('#type_pay').attr("name"),
		}
	);
}


function doSearch_sell_ipad(){
	$('#dg_sell_ipad').datagrid(
		'reload',
		{
			starttime_sell_ipad:$('#starttime_sell_ipad').datetimebox('getValue'),
			type_sell_ipad:$('#type_sell_ipad').attr("name"),
		}
	);
}

function doSearch_free_ipad(){
	$('#dg_free_ipad').datagrid(
		'reload',
		{
			starttime_free_ipad:$('#starttime_free_ipad').datetimebox('getValue'),
			type_free_ipad:$('#type_free_ipad').attr("name"),
		}
	);
}

function doSearch_pay_ipad(){
	$('#dg_pay_ipad').datagrid(
		'reload',
		{
			starttime_pay_ipad:$('#starttime_pay_ipad').datetimebox('getValue'),
			type_pay_ipad:$('#type_pay_ipad').attr("name"),
		}
	);
}
function doSearch_japan_free(){
	$('#dg_japan_free').datagrid(
		'reload',
		{
			starttime_japan_free:$('#starttime_japan_free').datetimebox('getValue'),
			type_japan_free:$('#type_japan_free').val(),
		}
	);
}
function doSearch_japan_pay(){
	$('#dg_japan_pay').datagrid(
		'reload',
		{
			starttime_japan_pay:$('#starttime_japan_pay').datetimebox('getValue'),
			type_japan_pay:$('#type_japan_pay').val(),
		}
	);
}
function doSearch_japan_sell(){
	$('#dg_japan_sell').datagrid(
		'reload',
		{
			starttime_japan_sell:$('#starttime_japan_sell').datetimebox('getValue'),
			type_japan_sell:$('#type_japan_sell').val(),
		}
	);
}
function doSearch_american_free(){
	$('#dg_american_free').datagrid(
		'reload',
		{
			starttime_american_free:$('#starttime_american_free').datetimebox('getValue'),
			type_american_free:$('#type_american_free').val(),
		}
	);
}
function doSearch_american_pay(){
	$('#dg_american_pay').datagrid(
		'reload',
		{
			starttime_american_pay:$('#starttime_american_pay').datetimebox('getValue'),
			type_american_pay:$('#type_american_pay').val(),
		}
	);
}
function doSearch_american_sell(){
	$('#dg_american_sell').datagrid(
		'reload',
		{
			starttime_american_sell:$('#starttime_american_sell').datetimebox('getValue'),
			type_american_sell:$('#type_american_sell').val(),
		}
	);
}
function doSearch_korea_free(){
	$('#dg_korea_free').datagrid(
		'reload',
		{
			starttime_korea_free:$('#starttime_korea_free').datetimebox('getValue'),
			type_korea_free:$('#type_korea_free').val(),
		}
	);
}
function doSearch_korea_pay(){
	$('#dg_korea_pay').datagrid(
		'reload',
		{
			starttime_korea_pay:$('#starttime_korea_pay').datetimebox('getValue'),
			type_korea_pay:$('#type_korea_pay').val(),
		}
	);
}
function doSearch_korea_sell(){
	$('#dg_korea_sell').datagrid(
		'reload',
		{
			starttime_korea_sell:$('#starttime_korea_sell').datetimebox('getValue'),
			type_korea_sell:$('#type_korea_sell').val(),
		}
	);
}


function doSearch_taiwan_free(){
	$('#dg_taiwan_free').datagrid(
		'reload',
		{
			starttime_taiwan_free:$('#starttime_taiwan_free').datetimebox('getValue'),
			type_taiwan_free:$('#type_taiwan_free').val(),
		}
	);
}
function doSearch_taiwan_pay(){
	$('#dg_taiwan_pay').datagrid(
		'reload',
		{
			starttime_taiwan_pay:$('#starttime_taiwan_pay').datetimebox('getValue'),
			type_taiwan_pay:$('#type_taiwan_pay').val(),
		}
	);
}
function doSearch_taiwan_sell(){
	$('#dg_taiwan_sell').datagrid(
		'reload',
		{
			starttime_taiwan_sell:$('#starttime_taiwan_sell').datetimebox('getValue'),
			type_taiwan_sell:$('#type_taiwan_sell').val(),
		}
	);
}


function doSearch_japan_free_ipad(){
	$('#dg_japan_free_ipad').datagrid(
		'reload',
		{
			starttime_japan_free_ipad:$('#starttime_japan_free_ipad').datetimebox('getValue'),
			type_japan_free_ipad:$('#type_japan_free_ipad').val(),
		}
	);
}
function doSearch_japan_pay_ipad(){
	$('#dg_japan_pay_ipad').datagrid(
		'reload',
		{
			starttime_japan_pay_ipad:$('#starttime_japan_pay_ipad').datetimebox('getValue'),
			type_japan_pay_ipad:$('#type_japan_pay_ipad').val(),
		}
	);
}
function doSearch_japan_sell_ipad(){
	$('#dg_japan_sell_ipad').datagrid(
		'reload',
		{
			starttime_japan_sell_ipad:$('#starttime_japan_sell_ipad').datetimebox('getValue'),
			type_japan_sell_ipad:$('#type_japan_sell_ipad').val(),
		}
	);
}
function doSearch_american_free_ipad(){
	$('#dg_american_free_ipad').datagrid(
		'reload',
		{
			starttime_american_free_ipad:$('#starttime_american_free_ipad').datetimebox('getValue'),
			type_american_free_ipad:$('#type_american_free_ipad').val(),
		}
	);
}
function doSearch_american_pay_ipad(){
	$('#dg_american_pay_ipad').datagrid(
		'reload',
		{
			starttime_american_pay_ipad:$('#starttime_american_pay_ipad').datetimebox('getValue'),
			type_american_pay_ipad:$('#type_american_pay_ipad').val(),
		}
	);
}
function doSearch_american_sell_ipad(){
	$('#dg_american_sell_ipad').datagrid(
		'reload',
		{
			starttime_american_sell_ipad:$('#starttime_american_sell_ipad').datetimebox('getValue'),
			type_american_sell_ipad:$('#type_american_sell_ipad').val(),
		}
	);
}
function doSearch_korea_free_ipad(){
	$('#dg_korea_free_ipad').datagrid(
		'reload',
		{
			starttime_korea_free_ipad:$('#starttime_korea_free_ipad').datetimebox('getValue'),
			type_korea_free_ipad:$('#type_korea_free_ipad').val(),
		}
	);
}
function doSearch_korea_pay_ipad(){
	$('#dg_korea_pay_ipad').datagrid(
		'reload',
		{
			starttime_korea_pay_ipad:$('#starttime_korea_pay_ipad').datetimebox('getValue'),
			type_korea_pay_ipad:$('#type_korea_pay_ipad').val(),
		}
	);
}
function doSearch_korea_sell_ipad(){
	$('#dg_korea_sell_ipad').datagrid(
		'reload',
		{
			starttime_korea_sell_ipad:$('#starttime_korea_sell_ipad').datetimebox('getValue'),
			type_korea_sell_ipad:$('#type_korea_sell_ipad').val(),
		}
	);
}


function doSearch_taiwan_free_ipad(){
	$('#dg_taiwan_free_ipad').datagrid(
		'reload',
		{
			starttime_taiwan_free_ipad:$('#starttime_taiwan_free_ipad').datetimebox('getValue'),
			type_taiwan_free_ipad:$('#type_taiwan_free_ipad').val(),
		}
	);
}
function doSearch_taiwan_pay_ipad(){
	$('#dg_taiwan_pay_ipad').datagrid(
		'reload',
		{
			starttime_taiwan_pay_ipad:$('#starttime_taiwan_pay_ipad').datetimebox('getValue'),
			type_taiwan_pay_ipad:$('#type_taiwan_pay_ipad').val(),
		}
	);
}
function doSearch_taiwan_sell_ipad(){
	$('#dg_taiwan_sell_ipad').datagrid(
		'reload',
		{
			starttime_taiwan_sell_ipad:$('#starttime_taiwan_sell_ipad').datetimebox('getValue'),
			type_taiwan_sell_ipad:$('#type_taiwan_sell_ipad').val(),
		}
	);
}


function doSearch_qq(){
	$('#dg_qq').datagrid(
		'reload',
		{
			starttime_qq:$('#starttime_qq').datetimebox('getValue'),
		}
	);
}
function doSearch_91(){
	$('#dg_91').datagrid(
		'reload',
		{
			starttime_91:$('#starttime_91').datetimebox('getValue'),
		}
	);
}
function doSearch_360(){
	$('#dg_360').datagrid(
		'reload',
		{
			starttime_360:$('#starttime_360').datetimebox('getValue'),
		}
	);
}
function doSearch_baidu(){
	$('#dg_baidu').datagrid(
		'reload',
		{
			starttime_baidu:$('#starttime_baidu').datetimebox('getValue'),
		}
	);
}
function doSearch_google(){
	$('#dg_google').datagrid(
		'reload',
		{
			starttime_google:$('#starttime_google').datetimebox('getValue'),
		}
	);
}

function doSearch_self(){
	$('#dg_self').datagrid(
		'reload',
		{
			starttime_self:$('#starttime_self').datetimebox('getValue'),
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

function gameNameformatter(value,row,index)
{
	/*
	if( row.website && row.website != "" )
	{
		var str = "<a href=\"" + row.website + "\" target=\"_blank\""  + "\">" + row.gameName + ";</a>";
		return str
	}
	else
	{
		return row.gameName
	}
	*/
	return value
}


function dateformatter(value,row,index)
{
	return row.rankDate.substring(5,10)
}


function channelformatter(value,row,index)
{
	if ( row.channel.match("ios_chinaIphone_free") )
	{
		return "iphone中国区免费榜";
	}
	else if ( row.channel.match("ios_chinaIphone_pay") )
	{
		return "iphone中国区付费榜";
	}
	else if ( row.channel.match("ios_chinaIphone_sell") )
	{
		return "iphone中国区畅销榜";
	}
	else if ( row.channel.match("ios_japanIphone_free") )
	{
		return "iphone日本区免费榜";
	}
	else if ( row.channel.match("ios_japanIphone_pay") )
	{
		return "iphone日本区付费榜";
	}
	else if ( row.channel.match("ios_japanIphone_sell") )
	{
		return "iphone日本区畅销榜";
	}
	else if ( row.channel.match("ios_americanIphone_free") )
	{
		return "iphone美国区免费榜";
	}
	else if ( row.channel.match("ios_americanIphone_pay") )
	{
		return "iphone美国区付费榜";
	}
	else if ( row.channel.match("ios_americanIphone_sell") )
	{
		return "iphone美国区畅销榜";
	}
	else if ( row.channel.match("ios_koreaIphone_free") )
	{
		return "iphone韩国区免费榜";
	}
	else if ( row.channel.match("ios_koreaIphone_pay") )
	{
		return "iphone韩国区付费榜";
	}
	else if ( row.channel.match("ios_koreaIphone_sell") )
	{
		return "iphone韩国区畅销榜";
	}
	else if ( row.channel.match("ios_taiwanIphone_sell") )
	{
		return "iphone台湾区付费榜";
	}
	else if ( row.channel.match("ios_taiwanIphone_free") )
	{
		return "iphone台湾区免费榜";
	}
	else if ( row.channel.match("ios_taiwanIphone_pay") )
	{
		return "iphone台湾区畅销榜";
	}
	else if ( row.channel.match("ios_chinaIpad_sell") )
	{
		return "ipad中国区畅销榜";
	}
	else if ( row.channel.match("ios_chinaIpad_free") )
	{
		return "ipad中国区免费榜";
	}
	else if ( row.channel.match("ios_chinaIpad_pay") )
	{
		return "ipad中国区付费榜";
	}
	else if ( row.channel.match("ios_taiwanIpad_free") )
	{
		return "ipad台湾区免费榜";
	}
	else if ( row.channel.match("ios_taiwanIpad_pay") )
	{
		return "ipad台湾区免付费榜";
	}
	else if ( row.channel.match("ios_taiwanIpad_sell") )
	{
		return "Ipad台湾区畅销榜";
	}
	else if ( row.channel.match("ios_japanIpad_free") )
	{
		return "Ipad日本区免费榜";
	}
	else if ( row.channel.match("ios_japanIpad_pay") )
	{
		return "Ipad日本区付费榜";
	}
	else if ( row.channel.match("ios_japanIpad_sell") )
	{
		return "Ipad日本区畅销榜";
	}
	else if ( row.channel.match("ios_americanIpad_free") )
	{
		return "Ipad美国区免费榜";
	}
	else if ( row.channel.match("ios_americanIpad_pay") )
	{
		return "Ipad美国区付费榜";
	}
	else if ( row.channel.match("ios_americanIpad_sell") )
	{
		return "Ipad美国区畅销榜";
	}
	else if ( row.channel.match("ios_koreaIpad_free") )
	{
		return "Ipad韩国区免费榜";
	}
	else if ( row.channel.match("ios_koreaIpad_pay") )
	{
		return "Ipad韩国区付费榜";
	}
	else if ( row.channel.match("ios_koreaIpad_sell") )
	{
		return "Ipad韩国区畅销榜";
	}
	else if( row.channel.match("android_360") )
	{
		return "360渠道";
	}
	else if( row.channel.match("android_baidu") )
	{
		return "百度渠道";
	}
	else
	{
		return row.channel;
	}
}




function expt_japan_sell_ipad()
{
	var name = $("#follower_japan_sell_ipad").attr('name');	
	var num = 0
	if ( window.confirm("确定添加关注吗？") )
	{
		var rows = $('#dg_japan_sell_ipad').datagrid('getSelections');
		if(rows.length && rows.length > 0)
		{
			var table = "ipad_japan_sell"
			for (var i = 0; i < rows.length; i++)
			{
				num = num +1
				var gameName = rows[i].gameName;
				$.ajax({
					url:'addCustomAppGame.php',
					data:{'personName':name,'gameName':gameName,'country':table},
					type:'post',
					success:function(res){
					}
				})
			}
		}
		alert("你已成功的添加了" + num + "条关注")
	}
}
function expt_japan_free_ipad()
{
	var name = $("#follower_japan_free_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_japan_free_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_japan_free"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}
function expt_japan_pay_ipad()
{
	var name = $("#follower_japan_pay_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_japan_pay_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_japan_pay"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}

function expt_american_sell_ipad()
{
	var name = $("#follower_american_sell_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_american_sell_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_american_sell"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}
function expt_american_free_ipad()
{
	var name = $("#follower_american_free_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_american_free_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_american_free"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}
function expt_american_pay_ipad()
{
	var name = $("#follower_american_pay_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_american_pay_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_american_pay"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}
function expt_korea_sell_ipad()
{
	var name = $("#follower_korea_sell_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_korea_sell_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_korea_sell"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}
function expt_korea_free_ipad()
{
	var name = $("#follower_korea_free_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_korea_free_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_korea_free"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}
function expt_korea_pay_ipad()
{
	var name = $("#follower_korea_pay_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_korea_pay_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_korea_pay"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}



function expt_taiwan_sell()
{
	var name = $("#follower_taiwan_sell").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_taiwan_sell').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ios_taiwan_sell"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}
function expt_taiwan_free()
{
	var name = $("#follower_taiwan_free").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_taiwan_free').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ios_taiwan_free"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}
function expt_taiwan_pay()
{
	var name = $("#follower_taiwan_pay").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_taiwan_pay').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ios_taiwan_pay"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}

function expt_taiwan_sell_ipad()
{
	var name = $("#follower_taiwan_sell_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_taiwan_sell_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_taiwan_sell"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}
function expt_taiwan_free_ipad()
{
	var name = $("#follower_taiwan_free_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_taiwan_free_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_taiwan_free"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}
function expt_taiwan_pay_ipad()
{
	var name = $("#follower_taiwan_pay_ipad").attr('name');	
	var num = 0
		if ( window.confirm("确定添加关注吗？") )
		{
			var rows = $('#dg_taiwan_pay_ipad').datagrid('getSelections');
			if(rows.length && rows.length > 0)
			{
				var table = "ipad_taiwan_pay"
				for (var i = 0; i < rows.length; i++)
				{
					num = num +1
					var gameName = rows[i].gameName;
					$.ajax({
						url:'addCustomAppGame.php',
						data:{'personName':name,'gameName':gameName,'country':table},
						type:'post',
						success:function(res){
						}
					})
				}
			}
			alert("你已成功的添加了" + num + "条关注")
		}
}


function affectedMapformatter(value,row,index)
{
	var index = row.affectedFile.indexOf(';')
	var ret = row.affectedMap.replace(/;/g,"<br>"+row.affectedFile.substr(0,index)+"<br>")
	return ret;
}



function onClickRow_china_pay(index){
	var row = $('#dg_pay').datagrid('getSelected');
	var rr1 = /;/g;
	var rr2 = /,/g;
	var a = row.other.replace(rr1,'    ')
	var b = a.replace(rr2,' 中排名:')
	$('#Ranks_china').html(b);
}

function onClickRow_china_free(index)
{
	var row = $('#dg_free').datagrid('getSelected');
	//var postdata = row.description;
	//$('#Paths_china').html(postdata);
	var rr1 = /;/g;
	var rr2 = /,/g;
	var a = row.other.replace(rr1,'    ')
	var b = a.replace(rr2,' 中排名:')
	$('#Ranks_china').html(b);
}

function onClickRow_china_sell(index){
	var row = $('#dg_sell').datagrid('getSelected');
	var rr1 = /;/g;
	var rr2 = /,/g;
	var a = row.other.replace(rr1,'    ')
	var b = a.replace(rr2,' 中排名:')
	$('#Ranks_china').html(b);
}

function onClickRow_qq(index){
	var row = $('#dg_qq').datagrid('getSelected');
	var rr1 = /;/g;
	var rr2 = /,/g;
	var a = row.other.replace(rr1,'    ')
	var b = a.replace(rr2,' 中排名:')
	$('#Ranks_qq').html(b);
}
function onClickRow_91(index)
{
	var row = $('#dg_91').datagrid('getSelected');
	var rr1 = /;/g;
	var rr2 = /,/g;
	var a = row.other.replace(rr1,'    ')
	var b = a.replace(rr2,' 中排名:')
	$('#Ranks_91').html(b);
}
function onClickRow_360(index){
	var row = $('#dg_360').datagrid('getSelected');
	var rr1 = /;/g;
	var rr2 = /,/g;
	var a = row.other.replace(rr1,'    ')
	var b = a.replace(rr2,' 中排名:')
	$('#Ranks_360').html(b);
}
function onClickRow_baidu(index){
	var row = $('#dg_baidu').datagrid('getSelected');
	var rr1 = /;/g;
	var rr2 = /,/g;
	var a = row.other.replace(rr1,'    ')
	var b = a.replace(rr2,' 中排名:')
	$('#Ranks_baidu').html(b);
}
function onClickRow_google(index){
	var row = $('#dg_google').datagrid('getSelected');
	var rr1 = /;/g;
	var rr2 = /,/g;
	var a = row.other.replace(rr1,'    ')
	var b = a.replace(rr2,' 中排名:')
	$('#Ranks_google').html(b);
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




function expt(){
	alert('导出为excel的功能还没有开放，sorry')
}


function onSortColumn(sort,order){
	$('#dg').datagrid(
		'reload',
		{
			sort:sort,
			order:order,
			starttime:$('#starttime_person').datetimebox('getValue'),
			shuru:$("#shuru_name").val(),
			dataType:$("#dataType").val(),
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


function rankingFormatter(value,row,index)
{
	    if ( value <= 150 )
		{
			return "<font color='red'>" + value + "</font>";
		}
		else
		{
			return value;
		}
}

/*function channelTrans(channel)
{
	switch (channel)
	{
		case "ios_chinaIphone_free":
		case "ios_chinaIphone_pay":
		case "ios_chinaIphone_sell":
		  return "ios_chinaIphone";
		  
		case "ios_chinaIpad_free":
		case "ios_chinaIpad_pay":
		case "ios_chinaIpad_sell":
		  return "ios_chinaIpad";
		  
		case "ios_americanIphone_free":
		case "ios_americanIphone_pay":
		case "ios_americanIphone_sell":
		  return "ios_americanIphone";
		  
		case "ios_americanIpad_free":
		case "ios_americanIpad_pay":
		case "ios_americanIpad_sell":
		  return "ios_americanIpad";
		  
		case "ios_koreaIphone_free":
		case "ios_koreaIphone_pay":
		case "ios_koreaIphone_sell":
		  return "ios_koreaIphone";
		  
		case "ios_koreaIpad_free":
		case "ios_koreaIpad_pay":
		case "ios_koreaIpad_sell":
		  return "ios_koreaIpad";
		  
		case "ios_taiwanIphone_free":
		case "ios_taiwanIphone_pay":
		case "ios_taiwanIphone_sell":
		  return "ios_taiwanIphone";
		  
		case "ios_taiwanIpad_free":
		case "ios_taiwanIpad_pay":
		case "ios_taiwanIpad_sell":
		  return "ios_taiwanIpad";
	    
		case "ios_japanIphone_free":
		case "ios_japanIphone_pay":
		case "ios_japanIphone_sell":
		  return "ios_japanIphone";
		  
		case "ios_japanIpad_free":
		case "ios_japanIpad_pay":
		case "ios_japanIpad_sell":
		  return "ios_japanIpad";
		  
		default:
		  return channel;
	}
}
*/
