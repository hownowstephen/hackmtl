<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Home Safe</title>
	<script src="js/jquery-1.7.1.min.js"></script>
	<script src="js/bootstrap.js"></script>
	<link rel="stylesheet" href="css/bootstrap.css" />
	<link rel="stylesheet" href="css/app.css" />
	
	<script>
	$(document).ready(function(){
	
	
	$("#destination").hide();
	$("#countdown").hide();
	$("#hitmiss").hide();
	$("#miss").hide();
	$("#hit").hide();
	
	$("#blueLine").click(function(){
		 if( $("#destination").is(":hidden") ) {
			$("#destination").slideDown(250, 'linear');
  			$("#home").slideUp(250, 'linear');
		}
		$.getJSON("http://50.57.65.176:5000/metros?lat=45.5081&lng=-73.5550", function(json) {
  			 console.log(json.response.name);
  			
 		});
	});
	
	$(".backBtn").click(function(){
		 if( $("#home").is(":hidden") ) {
			$("#home").slideDown(250, 'linear');
  				$("#destination").hide();
				$("#countdown").hide();
				$("#hitmiss").hide();
				$("#miss").hide();
				$("#hit").hide();
		}
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
destination selected
<ul id="destinations">

</ul>
</section>

<section id="countdown">
<div class="backBtn"><a class="backBtn"><img alt="back" src="img/back.png" width="70" height="70"></a></div>
countdown
</section>

<section id="miss">
<div class="backBtn"><a class="backBtn"><img alt="back" src="img/back.png" width="70" height="70"></a></div>
miss
</section>

<section id="hit">
<div class="backBtn"><a class="backBtn"><img alt="back" src="img/back.png" width="70" height="70"></a></div>
hit
</section>

</body>
</html>
