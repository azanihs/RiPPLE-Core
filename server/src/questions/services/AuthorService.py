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
                decodeImages(str(questionObj.id), questionObj, question_content, images, "q", host)
            else:
                questionObj.content = cleanContent(question_content)
                questionObj.save()

            # Explanation Images
            images = explanation.get("payloads", None)
            if images:
                decodeImages(str(questionObj.id), questionObj, explanation_content, images, "e", host)
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
                    decodeImages(str(distractor.id), distractor, distractor_content, images, "d", host)
                else:
                    distractor.content = cleanContent(distractor_content)
                    distractor.save()
    except IntegrityError as e:
        return {"state": "Error", "error": str(e)}
    except Exception as e:
        return {"state": "Error", "error": str(e)}
    return {"state": "Question Added", "question": Question.objects.get(pk=questionObj.id).toJSON()}


def decodeImages(image_id, obj, content, images, image_type, host):
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
        obj.explanation = cleanContent(newSource(urls, content, host))
    else:
        obj.content = cleanContent(newSource(urls, content, host))

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

