<?php
	/*
	$root = getcwd();
	$db = setupDatabase(); //Open new database 

	shell_exec("chmod 775 pw_mod.db");
	
	//Alter the database
	$cmd = "ATTACH DATABASE '".$root."/pw_orig.db' AS pw_orig"; //Attach first database
	$db->exec($cmd);
	
	$db->query('ALTER TABLE peerwise_questions ADD COLUMN quiz_topic BLOB DEFAULT dni');

	$cmd = getInsertStatement();
	$db->exec($cmd);



	function getInsertStatement(){
		$insert_into = 'INSERT INTO peerwise_questions(id, peerwise_id, created_on, question, alternative_a, alternative_b, alternative_c, alternative_d, alternative_e, correct_alternative, explanation, tags, author, average_rating, average_difficulty, total_ratings) ';
		$select_all = 'SELECT * FROM pw_orig.peerwise_questions;';
		$cmd = $insert_into . $select_all;
		return $cmd;
	}
	*/

	$db = new SQLite3("pw_mod.db");
	$tags = $db->query("SELECT DISTINCT quiz_topic FROM peerwise_questions WHERE quiz_topic NOT LIKE 'dni'");

	$alltags = array();
	while($tag = $tags->fetchArray(SQLITE3_ASSOC)){
		array_push($alltags, $tag['quiz_topic']);
	}
	$alltags = implode($alltags, ', ');
?>

<html>
	<head>
		<title>Select Tags for Questions</title>
		<link rel="stylesheet" href="assets/css/bootstrap.min.css">
		<link rel="stylesheet" href="assets/css/signin.css">
		<link rel="stylesheet" href="assets/css/selectize.default.css">

		<script src="assets/js/jquery-2.1.3.min.js"></script>
		<script src="assets/js/selectize.min.js"></script>
	</head>


	<body>
		<div class="container text-center">
			<form method="POST" action="assign.php">
				<h3 for="input-tags">Add Quiz Topics</h3>

				<hr>
				<p>Step 1. Click on the text box and start typing to add more topics or delete existing topics</p>
				<input type="text" autocomplete="off" tabindex="" id="input-tags" name="input-tags" value="<?php echo $alltags; ?>" >		
				
				<hr>

	            <button class="btn btn-primary " type="submit">Step 2. Assign topics to questions</button>

			</form>

		</div>

		<script type="text/javascript">
			$('#input-tags').selectize({
   				delimiter: ',',
	    		persist: false,
    			create: function(input) {
        			return {
			            value: input,
            			text: input,
        			}
    			}
			});
		</script>		

	</body>
</html>