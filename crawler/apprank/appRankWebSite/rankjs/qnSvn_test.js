
	$(function(){
		$("#btn_query").click(function(){
			var formStr = $("#myForm").serialize(); 
			formStr = decodeURIComponent(formStr,true);
			str = "qnSvn.php?" + formStr;
			location.href = str;
		})
	})


	function changeQAer(which)
	{
		//var a = which.options[which.selectedIndex].value;
		var a = $(which).parents("tr").children("td:nth-child(7)").find('option:selected').text()
		var objSelect = $(which).parents("tr").children("td:nth-child(7)")
		//if ( a.match('请选择') )
		//{
			var b = $(which).parents("tr").children("td:nth-child(6)").find('option:selected').val()
			for (var i = 0; i < objSelect.find('option').length; i++)
			{        
				//var qaname = $(which).parents("tr").children("td:nth-child(7)").find('option')[i].text
				var qaname = objSelect.find('option')[i].text
				if (qaname == b)
				{        
					objSelect.find('option')[i].selected = true; 
					break;        
				}        
			} 
		//}

	}

	function changeQAer4fade(which)
	{
			//alert($(which).parents("tr").children("td:nth-child(6)").find('option:selected').val())
		//var a = which.options[which.selectedIndex].value;
		//var a = $(which).parents("tr").children("td:nth-child(7)").find('option:selected').text()
		var objSelect = $(which).parents("tr").children("td:nth-child(7)")
			var b = $(which).parents("tr").children("td:nth-child(6)").find('option:selected').val()
			for (var i = 0; i < objSelect.find('option').length; i++)
			{        
				//var qaname = $(which).parents("tr").children("td:nth-child(7)").find('option')[i].text
				var qaname = objSelect.find('option')[i].text
				if (qaname == b)
				{        
					objSelect.find('option')[i].selected = true; 
					break;        
				}        
			} 
	}


	function splitContext(which,num,qaerstring)
	{
		var arr = new Array();

		$("#splitpage").modal('show').css({

			});

		var str = "将提交内容拆分为" + num
		$("#myModalTitle").html(str)
		var str = $(which).parents("tr").children("td:nth-child(2)").text()
		$("#myModalContext").html(str)

		$("#myModalTable tr:not(:first)").empty()
		
		$("#myModalTable").css("backgroundColor","white");

		var tableline = $(which).parents("tr").attr("id");
		var qaer = qaerstring.split("|")
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
			var pk = $(which).parents("tr").children("td:nth-child(1)").text()
			var value = pk + "_" + splitNum;
			x1.innerText=value;
		    x2.innerHTML='<textarea class="form-control" rows="5"></textarea>';
			var redmineTag=new Array(); 
			var redminestr="";
				$(which).parents("tr").children("td:nth-child(3)").children("a").each(function(m,n){
					var zj = $(n).attr("title")
					var a = $(n).text()
					var b = a.replace(";","")
					var c = parseInt(b);
					redmineTag[c]=zj;
					redminestr = redminestr + "<label class='checkbox'><input type='checkbox' checked='checked' value='" + c + "'>" + '<a href="http://qn.pm.netease.com:8120/issues/' + c + ' target="_blank" ' + "title='" + zj + "'>" + c + ";</a>" + "</label><br>";
					})
		    x3.innerHTML=redminestr
		    x4.innerText=$(which).parents("tr").children("td:nth-child(4)").text();
		    x5.innerText=$(which).parents("tr").children("td:nth-child(5)").text();


			var str = '<td> <select class="form-control"> <option>请选择</option> ';
			for(var j =0;j<qaer.length-1;j++)
			{
				str = str + "<option>" + qaer[j] + "</option> "
			}
			str = str + "</select> </td>"
		    x6.innerHTML=str;
		    var str = '<td> <select class="form-control"> <option>未完成</option> <option>完成</option> </select> </td>';
		    x7.innerHTML=str;
		    x8.innerHTML='<textarea class="form-control" rows="5"></textarea>';
		    x9.innerText=$(which).parents("tr").children("td:nth-child(10)").text();
		    x10.innerText=$(which).parents("tr").children("td:nth-child(11)").text();

			x9.style.display="none";
			x10.style.display="none";
			x1.style.display="none";
			x8.style.display="none";
			x4.style.display="none";
			x5.style.display="none";

		}

		var ebutt=document.getElementById("btn_saveSplitContext")
		var argstr = "saveSplitContext('" + pk + "','" + tableline + "','" + qaerstring + "')"
		ebutt.setAttribute("onclick",argstr)

	}


	function saveSplitContext(pk,tableline,select1)
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
		   data:{'pk':pk},
		   type:'post',
		   success:function(res){
		   }
		 })
		 var atr = document.getElementById(tableline).cells[0].style.background="#5CACEE";
		 document.getElementById(tableline).cells[2].innerHTML='';
		 document.getElementById(tableline).cells[3].innerHTML='';
		 document.getElementById(tableline).cells[4].innerHTML='';
		 document.getElementById(tableline).cells[5].innerHTML='';
		 document.getElementById(tableline).cells[6].innerHTML='';
		 document.getElementById(tableline).cells[7].innerHTML='';
		 document.getElementById(tableline).cells[8].innerHTML='';
		 document.getElementById(tableline).cells[9].innerHTML='';



	     $("#myModalTable tr").each(function(ind, item){
			var pkvalue = $(item).children("td:nth-child(1)").text()
			if ( pkvalue.match("_") )
			{
				//本来设计的是点击浮动窗口的保存按钮后存入数据库的操作放到和外层myTable一起存,但发现如要存入的数据量不一样，故放这里单独存入数据库
				pkstring = pkstring + $(item).children("td:nth-child(1)").text() + ";";
				svninfostring = svninfostring + $(item).children("td:nth-child(2)").find('textarea').val() + "|";
				$(item).children("td:nth-child(3)").children("label").each(function(m,n){
					//var zj = $(n).children("a").attr("title")
					//alert(zj)
					if($(n).find("input").is(":checked") == true)
					{
						redminestring = redminestring + $(n).find("input").val() + ";"
					}
					else
					{
					}
					})
				redminestring = redminestring + "|"
				//alert(redminestring)
				submitTimestring = submitTimestring + $(item).children("td:nth-child(4)").text() + ";"
				submiterstring = submiterstring + $(item).children("td:nth-child(5)").text() + ";"
				QAerstring = QAerstring + $(item).children("td:nth-child(6)").find('option:selected').text() + ";";
				svnStatusstring = svnStatusstring + $(item).children("td:nth-child(7)").find('option:selected').text() + ";";
				psstring = psstring + $(item).children("td:nth-child(8)").find('textarea').val() + ";";
				dirFlagstring=dirFlagstring + $(item).children("td:nth-child(10)").text() + ";";
				buildVersionstring=buildVersionstring + $(item).children("td:nth-child(9)").text() + ";";

				var tab=document.getElementById('mySplitTable').insertRow(1)
				var x1=tab.insertCell(0);
				var x2=tab.insertCell(1);
				var x3=tab.insertCell(2);
				var x4=tab.insertCell(3);
				var x5=tab.insertCell(4);
				var x6=tab.insertCell(5);
				var x7=tab.insertCell(6);
				var x8=tab.insertCell(7);
				//var x9=tab.insertCell(8);
				//var x10=tab.insertCell(9);
			
				x1.innerText=$(item).children("td:nth-child(1)").text() + ";";
				x1.style.background="#5CACEE"
				x2.innerText=$(item).children("td:nth-child(2)").find('textarea').val();

				var b="";
				$(item).children("td:nth-child(3)").children("label").each(function(m,n){
					if($(n).find("input").is(":checked") == true)
					{
						var one_redmine =  $(n).find("input").val()
						b = b + "<a href='http://qn.pm.netease.com:8120/issues/" + one_redmine + "' target='_blank'>" + one_redmine + ";</a><br>";
					}
				})

				x3.innerHTML=b
				x4.innerText=$(item).children("td:nth-child(4)").text();
				x5.innerText=$(item).children("td:nth-child(5)").text();


				var select_qaer = select1.split("|")
				var str = '<td> <select class="form-control">';
				for(var j =0;j<select_qaer.length-1;j++)
				{
					if ( select_qaer[j].match($(item).children("td:nth-child(6)").find('option:selected').text()) )
					{
						str = str + "<option selected='selected'>" + select_qaer[j] + "</option> "
					}
					else
					{
						//str = str + "<option>" + select_qaer[j] + "</option> "
					}
				}
				str = str + "</select> </td>"
				x6.innerHTML=str;

				var str = '<td> <select class="form-control">';
				var bf = $(item).children("td:nth-child(7)").find('option:selected').text();
				if ( bf.match('未完成') )
				{
					str = str + "<option selected='selected'>未完成</option>"
				}
				else
				{
					str = str + "<option selected='selected'>完成</option>"
				}
				str = str + "</select> </td>"
				x7.innerHTML=str;

				x8.innerHTML=$(item).children("td:nth-child(8)").find('textarea').val();

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


	$(function(){
	    $("#btn_confirmAssign").click(function(){
	        if ( window.confirm("确定分配任务吗？") )
	        {
	         var pkstring="";
	         var QAerstring="";
			 var svnStatusstring="";
			 var psstring="";
	         var svnlogNum=0;

	         $("#myTable tr").each(function(ind, item){
	             var qaer = $(item).children("td:nth-child(6)").find('option:selected').text();
	             var redmine = $(item).children("td:nth-child(3)").text();
	             var submitIndex = $(item).children("td:nth-child(1)").text();
	             var submitDate = $(item).children("td:nth-child(4)").text();
	             var submiter = $(item).children("td:nth-child(5)").text();
				if ( submitIndex != "" && ! qaer.match("选择") && ( (redmine.length > 2) || (submitDate.length > 2 ) || (submiter > 2) ) )
				{
	                 svnlogNum = svnlogNum + 1;
	                 pkstring = pkstring + $(item).children("td:nth-child(1)").text() + ";";
	                 QAerstring = QAerstring + $(item).children("td:nth-child(6)").find('option:selected').text() + ";";
	                 svnStatusstring = svnStatusstring + $(item).children("td:nth-child(7)").find('option:selected').text() + ";";
	                 psstring = psstring + $(item).children("td:nth-child(8)").find('textarea').val() + "|";
				 }

	       });
			if ( svnlogNum > 0 )
			{
				$.ajax({
					url:'svnlog2mysql.php',
					data:{'pk':pkstring,'QAer':QAerstring,'ps':psstring,'svnStatus':svnStatusstring},
					type:'post',
					success:function(res){
						window.location.reload()
					}
				})
				alert("你已成功的分配了" + svnlogNum + "条svn记录")
			}
	      }

	    })
      })


	$(function(){
	    $("#btn_sendMail").click(function(){
	        if ( window.confirm("确定分发邮件吗？") )
	        {
	         var pkstring2="";
	         var QAerstring2="";
			 var Redminestring2="";
			 var Submiterstring2="";
			 var psstring2="";
			 var svninfostring2="";
			 var svnlogNum=0;


	         $("#myTable tr").each(function(ind, item){
	             var qaer = $(item).children("td:nth-child(6)").find('option:selected').text();
	             var redmine = $(item).children("td:nth-child(3)").text();
	             var submitIndex = $(item).children("td:nth-child(1)").text();
	             var submitDate = $(item).children("td:nth-child(4)").text();
	             var submiter = $(item).children("td:nth-child(5)").text();
				if ( submitIndex != "" && ! qaer.match("选择") && ( (redmine.length > 2) || (submitDate.length > 2 ) || (submiter > 2) ) )
				{
	                 svnlogNum = svnlogNum + 1;

	                 pkstring2 = pkstring2 + $(item).children("td:nth-child(1)").text() + ";";
	                 QAerstring2 = QAerstring2 + $(item).children("td:nth-child(6)").find('option:selected').text() + ";";
	                 psstring2 = psstring2 + $(item).children("td:nth-child(8)").find('textarea').val() + "|";

	                 Submiterstring2 = Submiterstring2 + $(item).children("td:nth-child(5)").text() + ";";
	                 Redminestring2 = Redminestring2 + $(item).children("td:nth-child(3)").text() + "|";
	                 svninfostring2 = svninfostring2 + $(item).children("td:nth-child(2)").text() + "|";
				}
	       });
			if ( svnlogNum > 0 )
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

	    })
      })


	$(function(){
	    $("#btn_cancelSplit").click(function(){
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
	    })
      })





	$(function(){
	    $("#btn_allocate").click(function(){
	        if ( window.confirm("确定要一键分配吗？") )
	        {
	           var qaer = $("#allocate_qaer").find('option:selected').text();
	           //var play = $("#allocate_play").find('option:selected').text();
				if ( ! qaer.match("选择") )
				{

					 $("#myTable tr").each(function(ind, item){
						 $(item).children("td:nth-child(6)").find('option:selected').empty();
						 var str ="<option>" + play + "</option>";
						 $(item).children("td:nth-child(6)").find('option:selected').prepend(str);
					});
				}
				else
				{
					alert("请选择一键分配的qa！")
				}
	      }


	    })
      })



	$(function(){
	    $("#btn_finished").click(function(){
			alert("未开放开功能")
	        //if ( window.confirm("确定全部完成吗？") )
	        //{

	      //}


	    })
      })






	$(function(){
	  $("#btn_saveNewSvnLog").click(function(){
		if ( window.confirm("确定增加该玩法吗？") )
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




