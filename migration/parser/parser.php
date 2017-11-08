<?php

// Load the DOM parser
include_once('question.php');

//Make the parent dir readable
// shell_exec("chmod 773 ..");
$file = $_FILES['file']['tmp_name'];
// $file = "data1.html";

$doc = new DOMDocument();
libxml_use_internal_errors(true);
$doc->loadHTMLFile($file);
libxml_clear_errors();

$xpath = new DOMXPath($doc);

// $html = file_get_html('dummy-data.html');            
// $html = file_get_html('buggy4.html');            
$db = setupDatabaseOrig();
$dbMod = setupDatabaseMod();

$schema = array(
	'peerwise_id' => SQLITE3_INTEGER,
	'created_on' => SQLITE3_BLOB,	
	'question' => SQLITE3_BLOB,
	'alternative_a' => SQLITE3_BLOB,
	'alternative_b' => SQLITE3_BLOB,
	'alternative_c' => SQLITE3_BLOB,
	'alternative_d' => SQLITE3_BLOB,	
	'alternative_e' => SQLITE3_BLOB,
	'correct_alternative' => SQLITE3_BLOB,
	'explanation' => SQLITE3_BLOB,
	'tags' => SQLITE3_BLOB,
	'author' => SQLITE3_BLOB,
	'average_rating' => SQLITE3_INTEGER,
	'average_difficulty' => SQLITE3_INTEGER,
	'total_ratings' => SQLITE3_INTEGER
);


$idname = 'displayQuestionTable';
$questionTable = $xpath->query("//table[@id='" . $idname . "']");

$totalSaveCount = 0;

function get_inner_html( $node ) 
{
    $innerHTML= '';
    $children = $node->childNodes;
     
    foreach ($children as $child)
    {
        $innerHTML .= $child->ownerDocument->saveXML( $child );
    }
     
    return $innerHTML;
}

foreach ($questionTable as $node) {
	$question = new Question();

	$tbody = $node->getElementsByTagName('tbody');
	foreach ($tbody as $q) {
		$rows = $q->getElementsByTagName('tr');
		$numrows = $rows->length;
		$d = new DOMDocument();
		for ($i = 1; $i < $numrows; $i++) {
			$row = $rows->item($i);

			$key = get_inner_html($row->childNodes->item(0)); //td 1 (leftClear)
			$value = get_inner_html($row->childNodes->item(1)); // td 2 (middleClear)

			$question->assign_values($key, $value);
		}
	}

	if ($question->question_as_json($schema) == TRUE) {
		echo 'ha';
	}
	/*if( $question->save_to_db($db, $schema) == TRUE){
		
		$question->save_to_db($dbMod, $schema);
		
		$totalSaveCount++;
	}*/
}

echo json_encode( array('totalSaveCount' => $totalSaveCount, 'result' => 'success' ) );

function setupDatabaseOrig(){
	$db = new SQLite3(__DIR__."/../pw_orig.db");

	$db->exec('CREATE TABLE IF NOT EXISTS peerwise_questions (
		id 				INTEGER PRIMARY KEY AUTOINCREMENT,
		peerwise_id 	INTEGER UNIQUE, 
		created_on 		BLOB,
		question 		BLOB,
		alternative_a	BLOB,
		alternative_b	BLOB,
		alternative_c	BLOB,
		alternative_d	BLOB,
		alternative_e	BLOB,
		correct_alternative BLOB, 
		explanation		BLOB,
		tags 			BLOB,
		author 			BLOB,
		average_rating 		INTEGER,
		average_difficulty 	INTEGER,
		total_ratings 		INTEGER
		)');

	return $db;
}

function setupDatabaseMod(){
	$db = new SQLite3("../pw_mod.db");
	
	$db->exec('CREATE TABLE IF NOT EXISTS peerwise_questions (
		id 				INTEGER PRIMARY KEY AUTOINCREMENT,
		peerwise_id 	INTEGER UNIQUE, 
		created_on 		BLOB,
		question 		BLOB,
		alternative_a	BLOB,
		alternative_b	BLOB,
		alternative_c	BLOB,
		alternative_d	BLOB,
		alternative_e	BLOB,
		correct_alternative BLOB, 
		explanation		BLOB,
		tags 			BLOB,
		author 			BLOB,
		average_rating 		INTEGER,
		average_difficulty 	INTEGER,
		total_ratings 		INTEGER,
		quiz_topic BLOB DEFAULT dni
		)');

	return $db;
}

?>