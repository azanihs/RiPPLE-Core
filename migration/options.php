<?php
	/*shell_exec("chmod 755 parser");
	shell_exec("chmod 755 parser/");
	shell_exec("chmod 755 parser/parser.php");	
	shell_exec("chmod 755 parser/question.php");	*/
?>
<html>
<!-- options.php -->
<head>
	<link rel="stylesheet" href="assets/css/bootstrap.min.css">
	<link rel="stylesheet" href="assets/css/base.css">
	<script src="assets/js/jquery-2.1.3.min.js"></script>
	<script src="assets/js/bootstrap.file-input.js"></script>
</head>
<body>	
<div class="container text-center">
	<?php
		static $email = 'pwadmin@cs.ubc.ca';
		static $password_hash = '2845a5bc69d0e3b793373cd596844b48fb51efed8da5c0c422d898648d52eee8'; //pwadmin123

		if($_POST['email'] != $email){
			echo "Username does not exist. Go back and please try again.";
		}
		else{
			//Hash the password
			$provided_password_hash = hash('sha256', $_POST['password']);
			if($provided_password_hash != $password_hash){
				echo "Password does not match. Go back and please try again.";
			}
			else {
	?>
	<!-- Alerts begin -->
	<div class="alert alert-danger alert-dismissible" id="parser_error" role="alert" style="display: none;">
  		<button type="button" class="close" id="close-parser-error-alert" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
  		<h5>There was an error when trying to parse the HTML File. Please try again</h5>
	</div>


	<div class="alert alert-danger alert-dismissible" id="folder_not_found" role="alert" style="display: none;">
  		<button type="button" class="close" id="close-folder-alert" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
  		<h5>Folder <b><span id='folder_name'></span></b> not found . Please refer to <b>Step 1</b> to copy the folder and try again</h5>
	</div>


	<div class="alert alert-success alert-dismissible" id="parser_success" role="alert" style="display: none;">
  		<button type="button" class="close" id="close-parser-success-alert" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
  		<h5>Successfully imported <b><span id='save_count'></span> questions</b>. </h5>
  		<h5>To import another file, please refer to <b>Step 1</b> again</h5>
	</div>


	<div class="alert alert-success alert-dismissible" id="delete_success" role="alert" style="display: none;">
  		<button type="button" class="close" id="close-delete-success-alert" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
  		<h5>Successfully deleted <b>pw_orig.db</b>. </h5>
  		<h5>To import a file, please refer to <b>Step 1</b></h5>
	</div>

	<div class="alert alert-danger alert-dismissible" id="delete_error" role="alert" style="display: none;">
  		<button type="button" class="close" id="close-delete-error-alert" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
  		<h5>Could not delete file. Please try again or manually delete the file from <?php echo getcwd(); ?></h5>
	</div>

	<!-- Alerts end -->

	<h3>Welcome! This tool supports imports from questions on PeerWise</h3>

	<hr>

	<div id="parser_before">
		<h4>If you want to import questions, please follow Steps 1 &amp; 2 below</h4>

		<div class="voffset4"></div>

		<h4><span class="label label-default"><b>Step 1:</b> To get started, please drag the folder 
		(with the same name as the HTML file) into  <b><?php echo getcwd(); ?></b></span></h4>

		<div class="voffset4"></div>


		<h4><span class="label label-default"><b>Step 2:</b> Please select the HTML File exported from PeerWise</span></h4>

		<div class="voffset4"></div>

		<form id="import_form">
			<input id="html_file_input" name="file" class="btn-primary" type="file" title="Select a file to import" accept=".html, .htm" required>
			
			<div class="voffset4"></div>

			<button id="confirm_import" type="submit" class="btn btn-lg btn-success" >Confirm Import</button>
		</form>	

	</div>

	<div id="parser_during" style="display: none;">
		<img src="assets/images/loading.gif">
		
		<h4>Importing Data. Please wait ...</h4>

	</div>
	
	<hr>

	<div id="parser_after" class="show_if_file_exists" style="display: none;">		
		<div class="col-md-6 content_left">
			<h4>If you want to modify quiz topics, please click on <b>Modify Questions</b> below</h4>
			<form action="modify.php" method="POST">
				<button type="submit" class="btn btn-warning btn-lg">Modify Questions</button>
			</form>
		</div>

		<div class="col-md-6 content_right">
			<h4>If you want to delete the database, please click on <b>Delete Database</b> below</h4>
			<button type="button" id="delete_db" class="btn btn-danger btn-lg">Delete <b>pw_orig.db</b></button>
		</div>

	</div>

</div>

<?php
		}
	}
?>
</body>


<script type="text/javascript">
	
	<?php  if(file_exists("pw_orig.db")){ ?>
		$("#parser_after").show();
	<?php }?>

	$(document).ready(function(){
		$('#html_file_input').bootstrapFileInput();
		reset_file_input_form();
		hide_all_alerts();
	});

	function reset_file_input_form(){
		$(".file-input-name").text("");
		$("#import_form")[0].reset();
	}

	function hide_all_alerts(){
		$('#folder_not_found').slideUp("slow");
		$('#parser_error').slideUp("slow");
		$('#parser_success').slideUp("slow");
		$('#delete_error').slideUp("slow");
		$('#delete_success').slideUp("slow");
	}

	function send_form_data(){
		var form = $('#import_form')[0];
		var formData = new FormData(form);
		
		/*form.setAttribute("action", 'parser/parser.php');
		form.setAttribute("method", 'POST');
		form.setAttribute("data", formData);
		form.submit();*/

  		$.ajax({
        	url: 'parser/parser.php',
        	type: 'POST',
        	data: formData,
        	processData: false,
    		contentType: false,
    		cache: false,
         	success: function (data) {		
         		console.log(data);
           		var res = JSON.parse(data);
           		if(res.result == "success"){
           			hide_all_alerts();

         			$('#save_count').text(res.totalSaveCount);
         			$('#parser_success').slideDown("slow");

         			reset_file_input_form();

         			$('#parser_during').slideUp("slow");
         			$('#parser_before').slideDown("slow");
         			$('#parser_after').show("slow");
           		}
         	},
         	error: function(data){
     			$('#parser_during').slideUp("slow");
     			$('#parser_before').slideDown("slow");
         		$('#parser_error').slideDown("slow");
         	},
      	});
	}

	$('#import_form').on('submit', function(e){
		e.preventDefault();
		hide_all_alerts();
		var file_name = $('.file-input-name').text();

		$.ajax({
        	url: 'check_folder.php',
        	type: 'POST',
        	data: {filename: file_name},
    		cache: false,
         	success: function (data) {
         		var res = JSON.parse(data);
         		if(res.result != "success"){
         			$('#folder_name').text(res.dirname);
         			$('#folder_not_found').slideDown("slow");
         		}
         		else{
         			hide_all_alerts();
	     			$('#parser_before').slideUp("slow");
	     			$('#parser_after').hide("slow");         			         			
	     			$('#parser_during').slideDown("slow");
         			send_form_data();
         		}
         	},
         	error: function(data){
         		debugger
         		$('#parser_error').slideDown("slow");
         	},
      	});
	});

	$("#delete_db").on("click", function(e){
		if(window.confirm("Are you sure?")){
			$.ajax({
	        	url: 'delete_db.php',
	        	type: 'POST',
	    		cache: false,
	         	success: function (data) {
	         		var res = JSON.parse(data);
	         		if(res.result == "success"){
	         			reset_file_input_form();
	         			hide_all_alerts();
	         			$('#parser_after').hide();
	         			$('#delete_success').slideDown("slow");
	         		}
	         	},
	         	error: function(data){
	         		hide_all_alerts();
	         		$('#delete_error').slideDown("slow");
	         	},
	      	});
		}

	});

	//Hide alert on 'X' button click
	$('#close-folder-alert').on('click',function(){
		$('#folder_not_found').slideUp("slow");
	});


	$('#close-parser-error-alert').on('click',function(){
		$('#parser_error').slideUp("slow");
	});
	
	$('#close-parser-success-alert').on('click',function(){
		$('#parser_success').slideUp("slow");
	});


	$('#close-delete-error-alert').on('click',function(){
		$('#delete_error').slideUp("slow");
	});
	
	$('#close-delete-success-alert').on('click',function(){
		$('#delete_success').slideUp("slow");
	});
	
</script>

</html>