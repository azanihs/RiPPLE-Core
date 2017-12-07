from ripple.util import util
from bs4 import BeautifulSoup

from django.db import IntegrityError, transaction
from questions.models import Question, Distractor, QuestionImage, ExplanationImage, DistractorImage
import bleach
from questions.allowed_tags import allowed_tags, allowed_attributes, allowed_styles


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
    content=cleanContent(question_content),
    explanation=cleanContent(explanation_content),
    difficulty=0,
    quality=0,
    difficultyCount=0,
    qualityCount=0,
    author=user
    )
    questionObj.save()
    try:
        with transaction.atomic():
            # Question Images
            images = question.get("payloads", None)
            if images:
                decodeImages(str(questionObj.id), questionObj, images, "q", host)

            # Explanation Images
            images = explanation.get("payloads", None)
            if images:
                decodeImages(str(questionObj.id), questionObj, images, "e", host)

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
                    content=cleanContent(distractor_content),
                    isCorrect=responses[i].get("isCorrect", None),
                    response=i,
                    question=questionObj
                )
                distractor.save()

                # Distractor Images
                images = responses[i].get("payloads", None)
                if images:
                    decodeImages(str(distractor.id), distractor, images, "d", host)
    except IntegrityError as e:
        return {"state": "Error", "error": str(e)}
    except Exception as e:
        return {"state": "Error", "error": str(e)}
    return {"state": "Question Added", "question": Question.objects.get(pk=questionObj.id).toJSON()}


def decodeImages(image_id, obj, images, image_type, host):
    # type q=question, d=distractor, e=explanation
    urls = []
    database_image_types = {
        "q": QuestionImage,
        "d": DistractorImage,
        "e": ExplanationImage
    }
    ImageToSaveClass = database_image_types.get(image_type, None)

    for i, image in images.items():
        contentfile_image = util.save_image(image, image_id)
        if contentfile_image is None:
            raise IntegrityError("Image is not of valid type")

        # Question + Explanation in the same object
        if image_type == "q" or image_type == "e":
            new_image = ImageToSaveClass.objects.create(question=obj, image=contentfile_image)
        else:
            new_image = ImageToSaveClass.objects.create(distractor=obj, image=contentfile_image)
        urls.append(new_image.image.name)

    if image_type == "e":
        obj.explanation = newSource(urls, obj.explanation, host)
    else:
        obj.content = newSource(urls, obj.content, host)

    obj.save()
    return True


def newSource(urls, content, host):
    soup = BeautifulSoup(content, "html.parser")

    images = soup.find_all('img')
    for i in range(0, len(urls)):
        if urls[i] is None:
            continue
        images[i]['src'] = "//" + host + urls[i]
        images[i]['src'] = util.merge_url_parts([host, urls[i]])
    immediate_children = soup.findChildren(recursive=False)
    return ''.join([str(x) for x in immediate_children])


def cleanContent(content):
    cleaned = bleach.clean(content, tags = allowed_tags + bleach.sanitizer.ALLOWED_TAGS,
                            attributes=allowed_attributes, styles = allowed_styles)
    return cleaned

#'<img src="blob:http://localhost:8080/089dde17-c848-40d6-b730-355015c96940" alt="download.jpg" width="241" height="209" />' 
