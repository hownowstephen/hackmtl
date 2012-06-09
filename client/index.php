<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Home Safe</title>
	<script src="js/jquery-1.7.1.min.js"></script>
	<script src="js/bootstrap.js"></script>
	<script src="assets/countdown/jquery.countdown.js"></script>
	<script src="assets/js/script.js"></script>

	<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Open+Sans+Condensed:300" />
	<link rel="stylesheet" href="css/bootstrap.css" />
	<link rel="stylesheet" href="css/app.css" />
	
	<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Open+Sans+Condensed:300" />

    <link rel="stylesheet" href="assets/countdown/jquery.countdown.css" />
	<script>
	$(document).ready(function(){
	

	$("#destination").hide();
	$("#timer").hide();
	$("#hitmiss").hide();
	$("#miss").hide();
	$("#hit").hide();
	
	$("#blueLine").click(function(){
		 if( $("#destination").is(":hidden") ) {
			$("#destination").slideDown(250, 'linear');
  			$("#home").slideUp(250, 'linear');
		}
		$.getJSON("http://50.57.65.176:5000/metros?lat=45.5081&lng=-73.5550", function(json) {
  			 for (var i=0; i<json.response.length; i++) {
  				 $("#destinations").append("<li><a href='#'>"+json.response[i].name+"</a></li>");
  			 }
  			
 		});
	});
	
	$(".backBtn").click(function(){
		 if( $("#home").is(":hidden") ) {
			$("#home").slideDown(250, 'linear');
  				$("#destination").hide();
				$("#timer").hide();
				$("#hitmiss").hide();
				$("#miss").hide();
				$("#hit").hide();
				$("#destinations").html("");
		}
	});
	
     $("#destinations").click(function(){
		 if( $("#timer").is(":hidden") ) {
			$("#timer").slideDown(250, 'linear');
  				$("#destination").hide();
				$("#hitmiss").hide();
				$("#miss").hide();
				$("#hit").hide();
				$("#home").hide();
		}
		$.getJSON("http://50.57.65.176:5000/metro/13/", function(json) {
			$("#cntdwn").html(json.results[0].diff);
			var count = json.results[0].diff;
			function dump(){
				count --;
				if(count < 0){
					alert("FAIL, maybe you should try a bixi?");
				}
				$("#cntdwn").html(count);
			}
			setInterval(function(){ count --; if(count <0) alert("FAIL, maybe you should take a Taxi, Bixi or just give up and go back to the bar");
$("#cntdwn").html(count);
}, 1000);
		});
	});


	
	});
	
	</script>	
</head>
<body>
<div class="container">
<section id="home">
    <div class="row-fluid">
    <div class="span12">
		<header><img id="logo" alt="home safe" src="img/logo.png" width="204" height="123"></header>
      </div>
	</div>
    <div class="row-fluid">
      <div class="span6">
    	<a href="#" id="blueLine"><div id="blueLineBtn"></div></a>
      </div>
      <div class="span6">
      <div id="orangeLineBtn"></div>
      </div>
    </div>
    <div class="row-fluid">
      <div class="span6">
      <div id="greenLineBtn"></div>
      </div>
      <div class="span6">
      <div id="yellowLineBtn"></div>
      </div>
    </div>
</section>
<section id="destination">
<div class="backBtn"><a class="backBtn"><img alt="back" src="img/back.png" width="70" height="70"></a></div>
Select a destination:
<ul id="destinations">

</ul>
</section>

<section id="timer">
<div class="backBtn"><a class="backBtn"><img alt="back" src="img/back.png" width="70" height="70"></a></div>
<p>You have <div id="cntdwn"></div> seconds until next metro arrives.</p>


</section>

<section id="miss">
<div class="backBtn"><a class="backBtn"><img alt="back" src="img/back.png" width="70" height="70"></a></div>
miss
</section>

<section id="hit">
<div class="backBtn"><a class="backBtn"><img alt="back" src="img/back.png" width="70" height="70"></a></div>
hit
</section>

<!-- javascripts --//>

</div>
</body>
</html>
