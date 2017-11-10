<!-- save.php -->
<?php
	$db = new SQLite3('pw_mod.db');

	foreach ($_POST as $id => $quiz_topic) {
		if(strcmp($quiz_topic, 'delete') != 0){ //If not delete
			$query = "UPDATE peerwise_questions SET quiz_topic = '". $quiz_topic ."' WHERE id = $id";
		}
		else{ //If delete
			$query = "DELETE FROM peerwise_questions WHERE id = $id";
		}
		$db->query($query);
	}
?>


<html>
	<head>
		<title>Saving Topics ... </title>
		<link rel="stylesheet" href="assets/css/bootstrap.min.css">
		<link rel="stylesheet" href="assets/css/signin.css">
		<link rel="stylesheet" href="assets/css/base.css">
	</head>


	<body>
		<div class="container text-center">
			<h2><div class="alert alert-success">Topics have now been assigned to questions </div></h2>
			<h2>You are now ready to serve quizzes </h2>

			<h4>If you want to serve quizzes from another folder, you will need the following from <b><?php echo getcwd(); ?></b> : </h5>
			<div class="container text-left" style="padding-left: 120px;">
				<h5>1. assets/</h5>
				<h5>2. Folders containing the data</h5>
				<h5>3. select.php</h5>
				<h5>4. quiz.php</h5>
			</div>

		</div>
	</body>
</html>