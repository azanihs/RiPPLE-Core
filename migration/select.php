<!-- select.php -->
<?php

	function get_topics(){
		$db = new SQLite3('pw_mod.db');
		$topics = $db->query("SELECT DISTINCT quiz_topic FROM peerwise_questions WHERE quiz_topic NOT LIKE 'dni'");
		$alltopics = array();
		while($topic = $topics->fetchArray(SQLITE3_ASSOC)){
			$curr_topic = $topic['quiz_topic'];
			echo "<option value='" . $curr_topic . "'>$curr_topic</option>";	
		}
	}
?>


<html>
	<head>
		<title>Select Topic for Quiz</title>
		<link rel="stylesheet" href="assets/css/bootstrap.min.css">
		<link rel="stylesheet" href="assets/css/signin.css">
		<link rel="stylesheet" href="assets/css/selectize.default.css">
		<link rel="stylesheet" href="assets/css/base.css">

		<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
		<script type="text/javascript" src="assets/js/selectize.min.js"></script>
	</head>

	<body>
		<div class="container text-center">
			<form action="quiz.php" method="POST">
				<h3>Step 1. Select A Quiz Below</h3>
				<hr>
				<select id="quiz_select" name="quiz_select" class="demo-default selectized" tabindex="-1" style="display: none;">
					<?php get_topics(); ?>
				</select>

				<hr>

				<button class="btn btn-primary " type="submit">Step 2. Start Quiz</button>
			</form>
		</div>	

	</body>

	<script type="text/javascript">
		$('#quiz_select').selectize({
   			create: true,
    		sortField: 'text'
		});
	</script>
</html>