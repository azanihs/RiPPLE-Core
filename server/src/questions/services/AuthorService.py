from ..models import Question, Topic, Distractor, QuestionRating, QuestionResponse, Competency, CompetencyMap, QuestionScore, QuestionImage, ExplanationImage, DistractorImage
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.conf import settings
from ripple.util import util
from bs4 import BeautifulSoup
import base64
import imghdr


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

    # Question
    questionObj = Question(
        content=question.get("content", None),
        explanation=explanation.get("content", None),
        difficulty=0,
        quality=0,
        difficultyCount=0,
        qualityCount=0,
        author=user
    )
    if (verifyContent(questionObj.content) and verifyContent(questionObj.explanation)):
        questionObj.save()
    else:
        # INVALID CONTENT
        return {"state": "Error", "error": "Invalid Question"}

    # Question Images
    images = question.get("payloads", None)
    if images:
        if not decodeImages(str(questionObj.id), images, "q", host):
            # INVALID IMAGE
            questionObj.delete()
            return {"state": "Error", "error": "Invalid Question Image"}

    # Explanation Images
    images = explanation.get("payloads", None)
    if images:
        if not decodeImages(str(questionObj.id), images, "e", host):
            # INVALID IMAGE
            questionObj.delete()
            return {"state": "Error", "error": "Invalid Explanation Image"}

    # Topics
    topicList = []
    for i in topics:
        topicList.append(i.get("id", None))
    questionObj.topics = topicList

    # Distractors
    for i in ["A", "B", "C", "D"]:
        distractor = Distractor(
            content=responses[i].get("content", None),
            isCorrect=responses[i].get("isCorrect", None),
            response=i,
            question=questionObj
        )

        if verifyContent(distractor.content):
            distractor.save()
        else:
            # INVALID CONTENT
            questionObj.delete()
            return {"state": "Error", "error": "Invalid Distractor"}

        # Distractor Images
        images = responses[i].get("payloads", None)
        if images:
            if not decodeImages(str(distractor.id), images, "d", host):
                # INVALID IMAGE
                questionObj.delete()
                return {"state": "Error", "error": "Invalid Distractor Image"}

    return {"state": "Question Added", "question": questionObj.toJSON()}


def decodeImages(id, images, type, host):
    # type q=question, d=distractor
    urls = []
    for i in range(0, len(images)):
        format, imgstr = images[str(i)].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),
                           name=type + id + "_" + str(i) + "." + ext)
        # Validate image
        if imghdr.what(data) != ext:
            return False

        # Question + Explanation in the same object
        if type == "q" or type == "e":
            object = Question.objects.get(pk=id)
        else:
            object = Distractor.objects.get(pk=id)

        # Save Images
        if type == "q":
            content = object.content
            questionImage = QuestionImage(question=object, image=data)
            questionImage.save()
            url = questionImage.image.url
        elif type == "d":
            content = object.content
            distractorImage = DistractorImage(distractor=object, image=data)
            distractorImage.save()
            url = distractorImage.image.url
        else:
            content = object.explanation
            explanationImage = ExplanationImage(question=object, image=data)
            explanationImage.save()
            url = explanationImage.image.url
        urls.append(url)

    if type == "e":
        object.explanation = newSource(urls, content, host)
    else:
        object.content = newSource(urls, content, host)

    object.save()
    return True


def newSource(urls, content, host):
    soup = BeautifulSoup(content, "html.parser")

    images = soup.find_all('img')
    for i in range(0, len(urls)):
        images[i]['src'] = "http://" + host + urls[i]

    immediate_children = soup.find("body").findChildren(recursive=False)
    return ''.join([str(x) for x in immediate_children])


def verifyContent(content):
    if len(content) == 0:
        return False

    soup = BeautifulSoup(content, "html.parser")

    scripts = soup.find_all('script')
    if len(scripts) > 0:
        return False
    return True
