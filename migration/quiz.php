<!-- quiz.php -->
<?php
	$quiz_topic = $_POST["quiz_select"];

	$db = new SQLite3('pw_mod.db');
	$questions = $db->query("SELECT * FROM peerwise_questions WHERE quiz_topic LIKE '" . $quiz_topic . "'");
	$question_number = 0;
	$alternatives = array("A", "B", "C", "D", "E");

	function display_alternatives($question){
		global $alternatives;

		for ($i=0; $i < count($alternatives) ; $i++) { 
			$option = $alternatives[$i];

			$opt_label = "alternative_" . strtolower($option);
			
			if(isset($question[$opt_label])){
				echo "<b> $option </b>";
				echo ". ";
				echo $question[$opt_label];
			}
		}

	}


	function display_options($question){
		global $alternatives;

		for ($i=0; $i < count($alternatives) ; $i++) { 
			$option = $alternatives[$i];

			$opt_label = "alternative_" . strtolower($option);
			
			if(isset($question[$opt_label])){
				echo "<option value='" . $option ."'>$option</option>";
			}
		}
	}


?>


<html>
	<head>
		<title>Select Topic for Quiz</title>
		<link rel="stylesheet" href="assets/css/bootstrap.min.css">
		<link rel="stylesheet" href="assets/css/signin.css">
		<link rel="stylesheet" href="assets/css/base.css">
		
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
		<meta charset="UTF-16">
	</head>

	<body>
		<div class="container" id="questions_container">
			<?php while($question = $questions->fetchArray(SQLITE3_ASSOC)) { ?>
				<?php $question_number++; ?>
				<div class="jumbotron" id="parent-div" data-number="<?php echo $question_number; ?>" style="background-color: #DADADA; font-size: 14px; display: none;">
					<h3 class="text-center">Question <?php echo $question_number;?></h3>

					<?php echo $question["question"]; ?>
					<hr>

					<h4>Alternatives</h4>
					<?php display_alternatives($question); ?>

					<hr>

					<h4>Select your answer</h4>
					<div class="form-group">
						<select class="form-control text-center answer_select" data-number="<?php echo $question_number; ?>" tabindex="-1">
							<?php display_options($question); ?>
						</select>
						<br>
						<button class="check_answer btn btn-warning" data-number="<?php echo $question_number; ?>">Check My Answer</button>
					</div>

					<div id="answer_feedback" data-number="<?php echo $question_number; ?>" data-correct-alternative="<?php echo $question["correct_alternative"]; ?>">
						<h3 id="feedback-correct" style="display: none;"><span class="label label-success">Your answer was correct </span></h3>					
						<h3 id="feedback-incorrect" style="display: none;"><span class="label label-danger">Your answer was incorrect </span></h3>					
					</div>

					<div id="chosen_answer" style='display:none;' data-number="<?php echo $question_number; ?>">
						<hr>
						<h4>Author's answer</h4>
						<?php echo $question["correct_alternative"]; ?>
 					</div>
					<div id="explanation" style='display:none;' data-number="<?php echo $question_number; ?>" >
						<hr>
						<h4>Author's Explanation</h4>
						<?php echo $question["explanation"]; ?>
					</div>
					<hr>

					<div class="text-center">
						<div class="btn-group" role="group" aria-label="...">
	  						<button type="button" class="previous_question btn btn-primary" data-number="<?php echo $question_number; ?>" >Previous Question</button>
							<button type="button" class="next_question btn btn-primary" data-number="<?php echo $question_number; ?>" >Next Question</button>
							<hr>
							<form action="select.php" method="POST">
								<button class="btn btn-danger text-center" type="submit">Click here to select another quiz</button>
							</form>
						</div>
					</div>
				</div>

			<?php } ?>


			<?php $question_number++; ?>
			
			<div class="jumbotron text-center" id="parent-div" data-number="<?php echo $question_number; ?>" 
				style="background-color: #DADADA; font-size: 14px; display: none;">
				<form action="select.php" method="POST">
					<h3>You have reached the end of the quiz</h3>
					<button type="button" class="previous_question btn btn-primary" data-number="<?php echo $question_number; ?>" >Previous Question</button>
					<button class="btn btn-warning text-center" type="submit">Click here to select another quiz</button>
				</form>
			</div>

		</div>

		<script type="text/javascript">
		$(document).ready( function() {
			$("#questions_container div#parent-div[data-number='1']").show();
		});

		function hide_all(number){
			$("div#chosen_answer[data-number='" + number + "']").hide();
			$("div#explanation[data-number='" + number + "']").hide();
			var $feedback = $("div#answer_feedback[data-number='" + number + "']");
			$feedback.children().hide();


		}

		$(".check_answer").on("click", function(e){
			var number = $(this).data('number');
			var chosen = $("select[data-number='" + number + "']").val();
			var $feedback = $("div#answer_feedback[data-number='" + number + "']");
			var correct = $feedback.data("correct-alternative");

			$feedback.children().hide();
			
			if(chosen == correct){
				$feedback = $feedback.find("#feedback-correct"); 
			}
			else{				
				$feedback = $feedback.find("#feedback-incorrect"); 
			}

			$feedback.fadeIn("slow");
			$("div#chosen_answer[data-number='" + number + "']").fadeIn("slow");
			$("div#explanation[data-number='" + number + "']").fadeIn("slow");
		});

		$(".previous_question").on("click", function(e){
			e.preventDefault();
			var number = $(this).data('number');
			if(number == 1) return false;

			hide_all(number);
			
			$("#questions_container div#parent-div[data-number='" + number + "']").slideDown(500, function(){
				$(this).hide(300);
				number--;
				$("#questions_container div#parent-div[data-number='" + number + "']").show();
				$(window).scrollTop(0);
			});

		});	

		$(".next_question").on("click", function(e){
			var number = $(this).data('number');
			hide_all(number);
			
			$("#questions_container div#parent-div[data-number='" + number + "']").slideDown(500, function(){
				$(this).hide(300);
				number++;
				$("#questions_container div#parent-div[data-number='" + number + "']").show();
				$(window).scrollTop(0);
			});

		});	
		</script>	
		

	</body>

</html>