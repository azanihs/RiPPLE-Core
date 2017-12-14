from ripple.util import util
from bs4 import BeautifulSoup

from django.db import IntegrityError, transaction
from questions.models import Question, Distractor, QuestionImage, ExplanationImage, DistractorImage
import bleach
from questions.allowed_tags import allowed_tags, allowed_attributes, allowed_styles

from ripple.util import util

def add_question(question_request, host, user):
    explanation = question_request.get("explanation", None)
    question = question_request.get("question", None)
    responses = question_request.get("responses", None)
    topics = question_request.get("topics", None)

    if explanation is None or question is None or responses is None or topics is None:
        return {"state": "Error", "error": "Invalid Question"}
    for i in ["A", "B", "C", "D"]:
        if responses.get(i, None) is None:
            return {"state": "Error", "error": "Missing response " + i}

    question_content = question.get("content", None)
    explanation_content = explanation.get("content", None)

    if len(question_content) == 0:
        return {"state": "Error", "error": "Question content is blank"}
    elif len(explanation_content) == 0:
        return {"state": "Error", "error": "Explanation content is blank"}

    # Cleans question and explanation content before saving as Question
    questionObj = Question(
    content="",
    explanation="",
    difficulty=0,
    quality=0,
    difficultyCount=0,
    qualityCount=0,
    author=user
    )
    if (util.verify_content(questionObj.content) and util.verify_content(questionObj.explanation)):
        questionObj.save()
    else:
        # INVALID CONTENT
        return {"state": "Error", "error": "Invalid Question"}
    try:
        with transaction.atomic():
            # Question Images
            images = question.get("payloads", None)
            if images:
                util.extract_image_from_html(str(questionObj.id), questionObj, images, "q", host)
            else:
                questionObj.content = cleanContent(question_content)
                questionObj.save()

            # Explanation Images
            images = explanation.get("payloads", None)
            if images:
                util.extract_image_from_html(str(questionObj.id), questionObj, images, "e", host)
            else:
                questionObj.explanation = cleanContent(explanation_content)
                questionObj.save()

            # Topics
            topicList = []
            for i in topics:
                topicList.append(i.get("id", None))
            questionObj.topics = topicList

            # Distractors
            _response_choices = ["A", "B", "C", "D"]
            if True not in [responses[i].get("isCorrect", False) for i in _response_choices]:
                raise IntegrityError("No correct answer for question")

            for i in _response_choices:
                distractor_content = responses[i].get("content", None)
                if(len(distractor_content) == 0):
                    return {"state": "Error", "error": "Distractor content is blank"}
                #cleans distractor content before saving
                distractor = Distractor(
                    content="",
                    isCorrect=responses[i].get("isCorrect", None),
                    response=i,
                    question=questionObj
                )

                if util.verify_content(distractor.content):
                    distractor.save()
                else:
                    raise IntegrityError("Invalid Distractor")

                # Distractor Images
                images = responses[i].get("payloads", None)
                if images:
                    util.extract_image_from_html(str(distractor.id), distractor, images, "d", host)
                else:
                    distractor.content = cleanContent(distractor_content)
                    distractor.save()
    except IntegrityError as e:
        return {"state": "Error", "error": str(e)}
    except Exception as e:
        return {"state": "Error", "error": str(e)}
    return {"state": "Question Added", "question": Question.objects.get(pk=questionObj.id).toJSON()}

def cleanContent(content):
    cleaned = bleach.clean(content, tags = allowed_tags + bleach.sanitizer.ALLOWED_TAGS,
            attributes=allowed_attributes, styles = allowed_styles)
    return cleaned

