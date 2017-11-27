<?php
ini_set('max_execution_time', 0);
// Load the DOM parser
include_once('question.php');

//Make the parent dir readable

$file = $_FILES['file']['tmp_name'];

$doc = new DOMDocument();
libxml_use_internal_errors(true);
$doc->loadHTMLFile($file);
libxml_clear_errors();

$courseCode = $_POST['course_id'];
$courseName = $_POST['course_name'];

$xpath = new DOMXPath($doc);
$idname = 'displayQuestionTable';
$questionTable = $xpath->query("//table[@id='" . $idname . "']");

function sendJSON($json, $courseCode) {  
	$url = "http://localhost:8000/questions/add/";
	$auth = get_auth($courseCode)->{"token"};
	$options = [
		"http" => [
			"header" => "Content-Type: application/json\r\nAccept: application/json\r\nAuthorization: $auth",
			"method" => "POST",
			"content" => $json
		]
	];
	$context = stream_context_create($options);
	$result = file_get_contents($url,false,$context);
}

function get_auth($courseCode) {
	$url = "http://localhost:8000/users/getUser/".$courseCode;
	$options = [
		"http" => [
			"header" => "Content-Type: application/json\r\nAccept: application/json",
			"method" => "GET"
		]
	];
	$context = stream_context_create($options);
	$result = file_get_contents($url, false, $context);
	return json_decode($result);
}


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

$topics = [];
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

	$json = $question->question_as_json($topics);

	foreach ($json["topics"] as $topic) {
		array_push($topics, $topic["name"]);
	}

}

$topics = array_values(array_unique($topics));
$questions = Array();

$questionsAdded = 0;

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

			$question->assign_values($key, $value, $topics);
		}
	}

	$json = $question->question_as_json($topics);
	array_push($questions, $json);
	//sendJson($json, $courseCode);
	
	$questionsAdded++;
}

$result = ["topics"=>$topics,"questions"=>$questions];

$jsonFile = fopen("../".$courseName.".json", "w");

//echo json_encode($result,JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
fwrite($jsonFile, json_encode($result));
fclose($jsonFile);


?>