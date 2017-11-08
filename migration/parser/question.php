<?php
    class Question {
        var $peerwise_id;
        var $created_on;
        var $question;
        
        var $alternative_a;
        var $alternative_b;
        var $alternative_c;
        var $alternative_d;
        var $alternative_e;

        var $correct_alternative;

        var $explanation;
        var $tags;
        var $author;

        var $average_rating;
        var $average_difficulty;
        var $total_ratings;
    
        public function assign_values($key, $value){
            switch ($key) {
                case 'ID':
                    $d = new domDocument; 
                    $d->loadHTML($value);
                    $this->peerwise_id =  intval($d->textContent);
                    unset($d);
                    break;

                case 'Created':
                    $this->created_on = $value;
                    break;                    
                
                case 'Question':
                    $this->question = $this->replace_occurences($value);
                    break;

                case '*A*':
                    $this->correct_alternative = 'A';
                case 'A':
                    $this->alternative_a = $this->replace_occurences($value);
                    break;

                case '*B*':
                    $this->correct_alternative = 'B';
                case 'B':
                    $this->alternative_b = $this->replace_occurences($value);
                    break;

                case '*C*':
                    $this->correct_alternative = 'C';
                case 'C':
                    $this->alternative_c = $this->replace_occurences($value);
                    break;

                case '*D*':
                    $this->correct_alternative = 'D';
                case 'D':
                    $this->alternative_d = $this->replace_occurences($value);
                    break;

                case '*E*':
                    $this->correct_alternative = 'E';
                case 'E':
                    $this->alternative_e = $this->replace_occurences($value);
                    break;

                case 'Explanation':
                    $this->explanation = $this->replace_occurences($value);
                    break;

                case 'Tags':
                    $this->tags = $value;
                    break;

                case 'Author':
                    $this->author = $value;
                    break;

                case 'Avg Rating':
                    $this->average_rating = intval($value);
                    break;
                
                case 'Avg Difficulty':                    
                    $this->average_difficulty = intval($value);
                    break;
                
                case 'Total ratings':
                    $this->total_ratings = intval($value);
                    break;

                default:
                    break;
            }
        }

        public function replace_occurences($data){
            return str_replace('.php', '.png', $data);
        }

        public function get_colvalue($colname){
            switch ($colname) {
                case 'peerwise_id':
                    return $this->peerwise_id;

                case 'created_on':
                    return $this->created_on;
                
                case 'question':
                    return $this->question;
                
                case 'alternative_a':
                    return $this->alternative_a;
                
                case 'alternative_b':
                    return $this->alternative_b;
                
                case 'alternative_c':
                    return $this->alternative_c;

                case 'alternative_d':
                    return $this->alternative_d;
                
                case 'alternative_e':
                    return $this->alternative_e;

                case 'correct_alternative':
                    return $this->correct_alternative;

                case 'explanation':
                    return $this->explanation;

                case 'tags':
                    return $this->tags;

                case 'author':
                    return $this->author;

                case 'average_rating':
                    return $this->average_rating;

                case 'average_difficulty':
                    return $this->average_difficulty;

                case 'total_ratings':
                    return $this->total_ratings;
            }
        }

        
        public function save_to_db($db, $schema){
            $query = "INSERT INTO peerwise_questions ";

            $keys = '';
            $bindings = '';
            foreach ($schema as $colname => $coltype) {
                $keys .= $colname . ',';
                $bindings .= ':' . $colname . ',';
            }
            $keys = rtrim($keys, ",");
            $bindings = rtrim($bindings, ",");
            echo "KEYS:\n".$keys."\nBINDINGS:\n ".$bindings."\n";
            $query .= "( " . $keys . " )";
            $query .= " VALUES ( " . $bindings . " )";
            echo "QUERY:\n".$query."\n";
            $stmt = $db->prepare( $query );


            foreach ($schema as $colname => $coltype) {
                $value = $this->get_colvalue($colname);
                echo "VALUE:\n".$value."\n";
                $stmt->bindValue( ':' . $colname, $value, $coltype);
            }

            $result = $stmt->execute();
            if($result != FALSE){
                return TRUE;
            }
        }

        public function question_as_json($schema) {
            $questionJSON = array("question" => mv_str_replace($this->get_colvalue("question"),
                    "explanation" => $this->get_colvalue("explanation"),
                    "responses" => $this->get_responses($schema),
                    "topics" => $this->get_colvalue("tags"));

            echo json_encode($questionJSON)."\n\n\n\n";
        }

        public function get_responses() {
            $correct = $this->get_colvalue("correct_alternative");

            $arr = array("A" => array("content" => $this->get_colvalue("alternative_a"),
                        "isCorrect" => "false"),
                "B" => array("content" => $this->get_colvalue("alternative_b"),
                        "isCorrect" => "false"),
                "C" => array("content" => $this->get_colvalue("alternative_c"),
                        "isCorrect" => "false"),
                "D" => array("content" => $this->get_colvalue("alternative_d"),
                        "isCorrect" => "false"));

            $arr[$correct]["isCorrect"] = "true";

            return $arr;

        }
        
}


?>