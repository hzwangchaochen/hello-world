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
			var Names_free=[];
			var rank_free=[];
			var url = location.href;
			var gameName = decodeURI($.getUrlVar('gameNameStr'));
			var channel = decodeURI($.getUrlVar('channel'));
			$.ajax({
				type: "post",
				url: "get_app_charts_data_android.php",	
				data:{'gameName':gameName,'channel':channel},
				datatype: "text",
				success:function(returnData){
					var JSONObject = eval('(' + returnData + ')');
					for (var i in JSONObject.everydayResult){
						Names_free.push(i);
						rank_free.push(parseInt(JSONObject.everydayResult[i][0]));
					}
					$('#container1').highcharts({
						chart: {
            				type: 'line'
			        	},
						title: {
							text: 'android app排名曲线'
						},
						xAxis: {
							categories: Names_free
						},
						yAxis: {
            				title: {
			                	text: 'rank'
							}
						},
						series: [{
            				name: gameName,
			            	data: rank_free 
						 }] 
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
	<div id="container1" style="max-width: 800px; height: 600px; margin-left: 200px;"></div>
	</body>
</html>
