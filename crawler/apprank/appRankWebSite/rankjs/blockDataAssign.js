
	$(function(){

		$("tr").each(function(ind,item){
			$(item).find("ol").hide();
			})

  		$("td").click(function(){
	  		$(this).find("ol").toggle();
   			});
 	})



		$(function(){
			$("#btn_confirmAssign").click(function(){
			 if ( window.confirm("您确定要分配任务吗？"))
			{
				var pkstring=""
				var QAerstring="";
				$("tr").each(function(ind,item){
					if ( $(item).children("td:nth-child(1)").text() != "" )
					{
						var qaer = $(item).children("td:nth-child(3)").find('option:selected').text();
						if (  ! qaer.match("选择") )
						{
							$(item).children("td:nth-child(1)").find("li").each(function(i,j){
							pkstring = pkstring + $(j).text() + "," + $(item).children("td:nth-child(3)").find('option:selected').text() + ";";
							})
						}
					}
				})
				$.ajax({
					url:'autoarp2mysql.php',
					data:{'pk':pkstring},
					type:'post',
					success:function(res){
					//alert("您已成功分配模型！") 
					window.close()
					}
				})			
			}
		})
	})
