<?php
	$filename = $_POST['filename'];
	$filenameWithoutExt = pathinfo($filename, PATHINFO_FILENAME);
	$dirname = $filenameWithoutExt . '_files';
	
	if(file_exists($dirname)){

		//Do a shell exec
		$amp = ' && ';
		$cmd = 'chmod 755 ' . $dirname . $amp; //chmod the directory
		$cmd .= 'cd ' . $dirname . $amp;
		$cmd .= 'rename .php .png *.php' . $amp; //Rename php to png		
		$cmd .= 'chmod 755 * '; //Chmod all files within the directory

		$out = shell_exec($cmd);
		
		// $output = array("result" => "success", "dirname" => $dirname, "cmd" => $cmd, "out" => $out);
		$output = array("result" => "success", "dirname" => $dirname);
		echo json_encode($output);
	}
	else{
		$output = array("result" => "fail", "dirname" => $dirname);
		echo json_encode($output);
	}
?>