<!DOCTYPE HTML>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>Highcharts Example</title>
		<link rel="stylesheet" type="text/css" href="../common/common.css">
		<script type="text/javascript" src="../easyui/jquery.min.js"></script>
		<script type="text/javascript">
		$.extend({
			getUrlVars: function(){
		    var vars = [], hash;
			var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
			for(var i = 0; i < hashes.length; i++)
			{
				hash = hashes[i].split('=');
				vars.push(hash[0]);
				vars[hash[0]] = hash[1];
			}
			return vars;
		},
			getUrlVar: function(name){
				return $.getUrlVars()[name];
			}
		});
		
		
		$(function () {
			var Names=[];

			var series=[];
			
			var titles=[];
			var url = location.href;
			var gameNameStr = decodeURI($.getUrlVar('gameNameStr'));
			var channel = decodeURI($.getUrlVar('channel'));
			var option = decodeURI($.getUrlVar('option'));
			$.ajax({
				type: "post",
				url: "get_app_charts_data.php",	
				data:{'gameNameStr':gameNameStr,'channel':channel,'option':option},
				datatype: "text",
				success:function(returnData){
					var JSONObject = eval('(' + returnData + ')');
					var ii = 0;
					for(var key in JSONObject)
					{
						series.push({
							name: key,
							data: []
						});

						for(var value in JSONObject[key])
						{
							Names.push(value);
							series[ii].data.push(parseInt(JSONObject[key][value]));
						}
						ii++;
					}

					if(channel.indexOf("free")!=-1) titles.push('app免费榜排名');
					if(channel.indexOf("sell")!=-1)  titles.push('app畅销榜排名');
					if(channel.indexOf("pay")!=-1)  titles.push('app付费榜排名');
					
					$('#container').highcharts({
						chart: {
            				type: 'line'
			        	},
						title: {
							text: titles
						},
						xAxis: {
							categories: Names
						},
						yAxis: {
            				title: {
			                	text: 'rank'
							}
						},
						series: series
					});
					
				},
				error:function(errorMsg) {
					alert(errorMsg);
				}
			});
		});
	</script>
	</head>
	<body>
	<script src="../Highcharts-4.0.3/js/highcharts.js"></script>
	<script src="../Highcharts-4.0.3/js/modules/exporting.js"></script>
	<div id="container" style="max-width: 800px; height: 600px; margin-left: 200px;"></div>
	</body>
</html>
