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

$xpath = new DOMXPath($doc);
$idname = 'displayQuestionTable';
$questionTable = $xpath->query("//table[@id='" . $idname . "']");

function sendJSON($json) {  
	$url = "http://localhost:8000/questions/add/";
	$auth = "B45JJmX6wOFpYawMWCcVSWWyZ6pBo0GY";
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

			$question->assign_values($key, $value);
		}
	}

	$json = $question->question_as_json();

	sendJson($json);
	
	$questionsAdded++;
}

echo json_encode(array("result"=>"success", "questionsAdded"=>$questionsAdded));
?>