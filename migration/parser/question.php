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

        var $question_image;
        var $explanation_image;
        var $alternative_a_image;
        var $alternative_b_image;
        var $alternative_c_image;
        var $alternative_d_image;

        var $correct_alternative;

        var $explanation;
        var $tags;
        var $author;

        var $average_rating;
        var $average_difficulty;
        var $total_ratings;
    
        public function assign_values($key, $value) {
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

        public function question_as_json($topics) {
            $this->extract_images();
            $questionJSON = array("question" => 
                        array("content" => $this->get_colvalue("question"),
                            "payloads" => $this->question_image),
                    "explanation" => 
                        array("content" => $this->get_colvalue("explanation"),
                            "payloads" => $this->explanation_image),
                    "responses" => $this->get_responses(),
                    "topics" => $this->get_topics($topics, $this->get_colvalue("tags")));
            return $questionJSON;
            //return json_encode($questionJSON,JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        }

        public function get_responses() {
            $correct = $this->get_colvalue("correct_alternative");

            $arr = array("A" => array("content" => $this->get_colvalue("alternative_a"),
                        "payloads" => $this->alternative_a_image,
                        "isCorrect" => false),
                "B" => array("content" => $this->get_colvalue("alternative_b"),
                        "payloads" => $this->alternative_b_image,
                        "isCorrect" => false),
                "C" => array("content" => $this->get_colvalue("alternative_c"),
                        "payloads" => $this->alternative_c_image,
                        "isCorrect" => false),
                "D" => array("content" => $this->get_colvalue("alternative_d"),
                        "payloads" => $this->alternative_d_image,
                        "isCorrect" => false));

            $arr[$correct]["isCorrect"] = true;

            return $arr;
        }

        public function get_topics($topics, $tags) {
            $tag_list = array();
            $used_tags = array();
            foreach (explode(", ", $tags) as $i) {
                array_push($tag_list, array("name"=>$i,"id"=>0));
            }
            return array_values($tag_list);
        }

        public function extract_images() {
            $doc = new domDocument();
            $arr = array("question","explanation","alternative_a","alternative_b",
                    "alternative_c","alternative_d");
            foreach ($arr as $obj) {
                $image_field = $obj."_image";
                $doc->loadHTML(mb_convert_encoding($this->$obj, 'HTML-ENTITIES', 'UTF-8'));
                $imgs = $doc->getElementsByTagName('img');
                $i = 0;
                foreach ($imgs as $img) {
                    if ($this->$image_field == null) {
                        $this->$image_field = new stdClass();
                    }
                    $src = $img->getAttribute("src");
                    $img->setAttribute("src", "#:".$i);
                    $this->$obj = $this->get_inner_html($doc->getElementsByTagName("body")->item(0));
                    $phpPath = str_replace("png", "php", $src);
                    $data = file_get_contents(getcwd()."/../".$phpPath);
                    $base64 = "data:image/png;base64,".base64_encode($data);
                    $this->$image_field->$i = $base64;
                    $i++;
                }
                if ($i == 0) {
                    $this->$image_field = new stdClass();
                }
            }

        }

        function get_inner_html( $node ) {
            $innerHTML= '';
            $children = $node->childNodes;

            foreach ($children as $child)
            {
                $innerHTML .= $child->ownerDocument->saveXML( $child );
            }       
            return $innerHTML;
        }     
}
?>