<?php 
	$file = "pw_orig.db";
	if(file_exists($file)){
		unlink($file);
	}

	echo json_encode(array("result" => "success"));
?>