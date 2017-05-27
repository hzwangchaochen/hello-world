
	$(function(){
		$("#btn_query").click(function(){
			var formStr = $("#myForm").serialize(); 
			formStr = decodeURIComponent(formStr,true);

			//str = "playManage.php?svnStatus=" +"222" + "&qaer=" + "33333" + "&play=" + "1111";
			str = "qnPlay.php?" + formStr;
			location.href = str;
/*
			var svnStatus = $("#select_status").find('option:selected').text();
			var qaer=$("#select_qaer").find('option:selected').text();
			var play=$("#select_play").find('option:selected').text();

			//var str = "arp.php?beginBuild=" + beginBuild + "&endBuild=" + endBuild + "&arpStatus=" + arpStatus + "&qaer=" + qaer;

			
			var beginBuild="";
			var endBuild="";
			
			var str="";

			if ( $("#checkbox_build").is(":checked") == true )
			{
				beginBuild=$("#select_beginBuild").find('option:selected').text();
				endBuild=$("#select_endBuild").find('option:selected').text();
				str = "svnlog.php?beginBuild=" + beginBuild + "&endBuild=" + endBuild + "&svnStatus=" + svnStatus + "&qaer=" + qaer + "&play=" + play;
			}
			else
			{
				str = "svnlog.php?svnStatus=" +svnStatus + "&qaer=" + qaer + "&play=" + play;
			}
			location.href = str;
			*/
		})
	})



	$(function(){
	  $("#btn_saveNewPlay").click(function(){
		if ( window.confirm("确定增加该玩法吗？") )
		{
			var playname=$("#val_playName").val();
			var	playstate = $("#val_playState").find('option:selected').text();
			var	expectdate = $("#val_expectDate").find('option:selected').text();
			var	qaer = $("#val_qaer").find('option:selected').text();
			var	programmer = $("#val_programmer").find('option:selected').text();
			var	designer = $("#val_designer").find('option:selected').text();
			var lastedit=new Date();
			if ( playname && ! playname.match( " ") )
			{					    
				if ( (playname.charAt(0) >= 'a' && playname.charAt(0) <= 'z') || (playname.charAt(0) >= 'A' && playname.charAt(0) <= 'Z') || (playname.charAt(0) >= '0' && playname.charAt(0) <= '9') )
				{
				$.ajax({
					url:'newplay2mysql.php',
					data:{'playname':playname,'playstate':playstate,'qaer':qaer,'expectdate':expectdate,'programmer':programmer,'designer':designer},
					type:'post',
					success:function(res){
					window.location.reload()
					}
				})
				}
				else
				{
					alert("玩法首字符需为字母或数字")
				}
			}
			else
			{
				alert("玩法名称不可以为空")
			}
		}
	  })
	})


	$(function(){
	  $("#btn_modify").click(function(){
		if ( window.confirm("确定修改玩法属性吗？") )
		{
			var pkstring=""
			var Statestring=''
			var Timestring=''
			var QAerstring=''
			var Programmerstring=''
			var Designerstring=''
	         $("#myTable tr").each(function(ind, item){
	            var playState = $(item).children("td:nth-child(2)").find('option:selected').text();
				if ( playState != "" )
				{
	                 pkstring = pkstring + $(item).children("td:nth-child(1)").text() + ";";
	                 Statestring = Statestring + $(item).children("td:nth-child(2)").find('option:selected').text() + ";";
	                 Timestring = Timestring + $(item).children("td:nth-child(3)").find('option:selected').text() + ";";
	                 QAerstring = QAerstring + $(item).children("td:nth-child(4)").find('option:selected').text() + ";";
	                 Programmerstring = Programmerstring + $(item).children("td:nth-child(5)").find('option:selected').text() + ";";
	                 Designerstring = Designerstring + $(item).children("td:nth-child(6)").find('option:selected').text() + ";";
				}
	       });
			$.ajax({
				url:'modifyplay2mysql.php',
				data:{'pk':pkstring,'State':Statestring,'QAer':QAerstring,'expectdate':Timestring,'Programmer':Programmerstring,'Designer':Designerstring},
				type:'post',
				success:function(res){
					window.location.reload()
				}
			})
		}
	  })
	})

	function queryMysql(flag)
	{
		if (flag == 0 )
		{
			var formStr = $("#myForm").serialize(); 
			formStr = decodeURIComponent(formStr,true);

			var str = "qnPlay.php?" + formStr;
			location.href = str;
		}
		else
		{
			var formStr = $("#myForm").serialize(); 
			formStr = decodeURIComponent(formStr,true);

			//str = "playManage.php?svnStatus=" +"222" + "&qaer=" + "33333" + "&play=" + "1111";
			var str = "qnPlay.php?" + "modify=on&" + formStr;
			location.href = str;
		}
	}











	$(function(){
	  $("#btn_modify_playName").click(function(){
		if ( window.confirm("确定修改玩法名字吗？") )
		{
	           var playName_before = $("#val_playName_before").val();
	           var playName_after = $("#val_playName_after").val();
				if ( playName_before != "" && playName_after != "" )
				{
				alert(11)
				$.ajax({
					url:'modifyPlayName.php',
					data:{'before':playName_before,'after':playName_after},
					type:'post',
					success:function(res){
						alert("修改成功！")
				window.location.reload()
					}
				})
			}
			else
			{
				alert("请输入你需要修改的玩法名字！")
			}
		}
	 })
	})





function showPlay(which,showTag)
{
	if ( window.confirm("确定修改是否显示？") )
	{
		var pk = $(which).parents("tr").children("td:nth-child(1)").text()
		if (showTag == 1)
		{
			 $.ajax({
			   url:'show_close_play.php',
			   data:{'pk':pk,'tag':1},
			   type:'post',
			   success:function(res){
							alert("修改成功！")
					window.location.reload()
			   }
			 })
		}
		else
		{
			 $.ajax({
			   url:'show_close_play.php',
			   data:{'pk':pk,'tag':0},
			   type:'post',
			   success:function(res){
							alert("修改成功！")
					window.location.reload()
			   }
			 })

		}
	}
}

