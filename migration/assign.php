<!-- assign.php -->
<?php
	$topics = $_POST['input-tags'];
	$topics = explode(',', $topics);
	$topics = array_map('trim', $topics);
	$topics = array_unique($topics);

	$db = new SQLite3('pw_mod.db');
	$questions = $db->query('SELECT * FROM peerwise_questions ORDER BY average_rating DESC;');
	$question_number = 0;

	function display_alternative($question, $option){
		$opt_label = "alternative_" . strtolower($option);
		
		if(isset($question[$opt_label])){
			echo "<b> $option </b>";
			echo ". ";
			echo $question[$opt_label];
		}
	}

	function display_options($question){
		global $topics;
		$assigned_topic = $question["quiz_topic"];

		for ($i=0; $i < count($topics) ; $i++) {
			$curr_topic = $topics[$i];
			if(strcmp($curr_topic, $assigned_topic) != 0 && $curr_topic !== ''){
				echo "<option value='" . $curr_topic . "'>$curr_topic</option>";	
			}
		}
		
		//Assigned topic is dni	
		if(strcmp($assigned_topic,'dni') == 0){
			echo "<option value='dni' selected='selected'>Do Not Include</option>";
		}
		else{ //Assigned topic is not dni
			if(in_array($assigned_topic, $topics)){
				echo "<option value='" . $assigned_topic ."' selected='selected'>$assigned_topic</option>";
				echo "<option value='dni'>Do Not Include</option>";
			}
			else{
				echo "<option value='dni' selected='selected'>Do Not Include</option>";
			}
		}

		//Put Delete at the end
		echo "<option value='delete'>Delete this question</option>";

	}
?>


<html>
	<head>
		<title>Select Tags for Questions</title>
		<link rel="stylesheet" href="assets/css/bootstrap.min.css">
		<link rel="stylesheet" href="assets/css/signin.css">
		<link rel="stylesheet" href="assets/css/base.css">

		<script src="assets/js/jquery-2.1.3.min.js"></script>
		<script src="assets/js/bootstrap.min.js"></script>
		<meta charset="UTF-16">
	</head>


	<body>
		<div class="container">
			<form method="POST" id="save_topics" action="save.php">
				
				<?php while($question = $questions->fetchArray(SQLITE3_ASSOC)) { ?>
					<?php $question_number++; ?>
					<!-- Question Display -->
					<div class="jumbotron" id="question_display" style="background-color: #DADADA; font-size: 14px;">
						<!-- <h3 class="text-center">Question <?php echo $question['id']; ?></h3> -->
						<h3 class="text-center">Question <?php echo $question_number;?></h3>

						<?php echo $question["question"]; ?>

						<hr>
						
						<h4>Alternatives</h4>
						<?php 
						display_alternative($question, "A");
						display_alternative($question, "B");
						display_alternative($question, "C");
						display_alternative($question, "D");
						display_alternative($question, "E");

						?>

						<hr>

						<div>
						  	<div class="col-md-4">
							  	<h4><span class="label label-default">Select Topic:</span></h4>
								<select class="form-control quiz_topic_select text-center" name="<?php echo $question['id']; ?>"placeholder="Select a quiz topic" tabindex="-1">
									<?php display_options($question); ?>
								</select>

								<div class="voffset2"></div>
						  		<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#modal_question_<?php echo $question['id']; ?>">
									Show Correct Answer and Author's Explanation
								</button>				  		
						  	</div>

						  	<div class="col-md-8 text-right">
								  	<h4><span class="label label-default">Question Statistics:</span></h4>
								  	<h5>Average Rating: <?php echo $question["average_rating"]; ?></h5>
								  	<h5>Average Difficulty: <?php echo $question["average_difficulty"]; ?></h5>
								  	<h5>Total Ratings: <?php echo $question["total_ratings"]; ?></h5>
						  	</div>

						</div>



					</div>

					<!-- Modal -->
					<div class="modal fade" id="modal_question_<?php echo $question['id']; ?>" tabindex="-1" role="dialog" aria-labelledby="modal_label_<?php echo $question['id']; ?>" aria-hidden="true">
					  <div class="modal-dialog">
					    <div class="modal-content">
					      <div class="modal-header">
					        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
					        <h4 class="modal-title" id="modal_label_<?php echo $question['id']; ?>">Question <?php echo $question_number;?> Answer &amp; Explanation</h4>
					      </div>
					      <div class="modal-body">
					        	<h4>Correct Alternative: <b><?php echo $question["correct_alternative"]; ?></b></h4>
					        	
					        	<hr>
					        	
					        	<h4>Author's Explanation: </h4>		
								<?php echo $question['explanation']; ?>
					      </div>
					    </div>
					  </div>
					</div>

				<?php } ?>

				<div class="text-center">
		            <button id="submit-btn" class="btn btn-primary btn-lg text-center" type="submit">Save Topics</button>				
				</div>
			</form>

		</div>
	</body>
</html>