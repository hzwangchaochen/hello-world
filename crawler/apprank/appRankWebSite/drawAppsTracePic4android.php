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

			var series_free=[];

			var url = location.href;
			var gameNameStr = decodeURI($.getUrlVar('gameNameStr'));
			var channel = decodeURI($.getUrlVar('channel'));
			var option = decodeURI($.getUrlVar('option'));
			$.ajax({
				type: "post",
				url: "get_app_charts_data_android.php",	
				data:{'gameNameStr':gameNameStr,'channel':channel,'option':option},
				datatype: "text",
				success:function(returnData){
					var JSONObject = eval('(' + returnData + ')');

					var ii = 0;
					for(var key in JSONObject)
					{
						series_free.push({
							name: key,
							data: []
						});
						for(var value in JSONObject[key])
						{
							Names_free.push(value);
							series_free[ii].data.push(parseInt(JSONObject[key][value]));
						}
						ii++;
					}

					//for (var i in JSONObject.everydayResult_free){
						//Names_free.push(i);
						//rank_free.push(parseInt(JSONObject.everydayResult_free[i][0]));
					//}
					//for (var i in JSONObject.everydayResult_pay){
						//Names_pay.push(i);
						//rank_pay.push(parseInt(JSONObject.everydayResult_pay[i][0]));
					//}
					//for (var i in JSONObject.everydayResult_sell){
						//Names_sell.push(i);
						//rank_sell.push(parseInt(JSONObject.everydayResult_sell[i][0]));
					//}
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
						series: series_free
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
	<br>
	<br>
	<div id="container2" style="max-width: 800px; height: 600px; margin-left: 200px;"></div>
	<br>
	<br>
	<div id="container3" style="max-width: 800px; height: 600px; margin-left: 200px;"></div>
	</body>
</html>
