from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from questions.models import Topic, Question, Distractor, QuestionResponse, QuestionRating, Competency, CompetencyMap, QuestionImage, ExplanationImage, DistractorImage
from users.models import Course, User, CourseUser

from questions.services import QuestionService

from random import randint, randrange, sample, choice
from faker import Factory
fake = Factory.create()

import json
from bs4 import BeautifulSoup
import base64
import imghdr


def chance(n):
    return choice(range(n)) is n - 1


def make_question_responses(user, distractors):
    if chance(2):
        user_choice = choice(distractors)
        response = QuestionResponse(
            response=user_choice,
            user=user
        )
        response.save()
        user_competency = QuestionService.update_competency(
            user, user_choice.question, response)
        user_competency.competency = randrange(0, 100)
        user_competency.confidence = randrange(0, 100)

        user_competency.save()
        if chance(2):
            rating = QuestionRating(
                quality=randrange(0, 10),
                difficulty=randrange(0, 10),
                response=user_choice,
                user=user
            )
            rating.save()


def get_topics(file):
    with open(file) as data_file:
        data = json.load(data_file)
    return data["topics"]

def parse_questions(file, course_users, all_topics):
    host = "localhost:8000"
    distractors = []

    with open(file) as data_file:
        data = json.load(data_file)
    
    questions = data["questions"]

    for q in questions:
        question = Question(
            content = q["question"]["content"],
            explanation = q["explanation"]["content"],
            difficulty = randrange(0, 5),
            quality=randrange(0, 5),
            difficultyCount = randrange(0, 100),
            qualityCount = randrange(0, 100),
            author = choice(course_users)
        )
        question.save()
        decode_images(question.id, question, q["question"]["payloads"], "q", host)
        decode_images(question.id, question, q["explanation"]["payloads"], "e", host)

        q_topics = q["topics"]
        for topic in q_topics:
            idx = 0
            while idx < len(all_topics):
                if topic["name"] == all_topics[idx].name:
                    break
                idx+=1
            question.topics.add(all_topics[idx])
        question.save()

        for i in ["A", "B", "C", "D"]:
            response = q["responses"][i]
            distractor = Distractor(
                content = response["content"],
                response = i,
                isCorrect = response["isCorrect"],
                question = question
            )
            distractor.save()
            decode_images(distractor.id, distractor, response["payloads"],"d", host)
            distractors.append(distractor)


    return distractors

def decode_images(id, obj, images, objType, host):
    if len(images) == 0:
        return True
    # objType q=question, d=distractor
    urls = []
    for i in range(0, len(images)):
        format, imgstr = images[str(i)].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),
                           name=objType + str(id) + "_" + str(i) + "." + ext)
        # Validate image
        if imghdr.what(data) != ext:
            return False

        # Save Images
        if objType == "q":
            content = obj.content
            questionImage = QuestionImage(question=obj, image=data)
            questionImage.save()
            url = questionImage.image.url
        elif objType == "d":
            content = obj.content
            distractorImage = DistractorImage(distractor=obj, image=data)
            distractorImage.save()
            url = distractorImage.image.url
        else:
            content = obj.explanation
            explanationImage = ExplanationImage(question=obj, image=data)
            explanationImage.save()
            url = explanationImage.image.url
        urls.append(url)

    if objType == "e":
        obj.explanation = new_source(urls, content, host)
    else:
        obj.content = new_source(urls, content, host)

    obj.save()
    return True


def new_source(urls, content, host):
    soup = BeautifulSoup(content, "html.parser")

    images = soup.find_all('img')
    for i in range(0, len(urls)):
        images[i]['src'] = "http://" + host + urls[i]

    immediate_children = soup.findChildren(recursive=False)
    return ''.join([str(x) for x in immediate_children])



class Command(BaseCommand):
    args = ''
    help = 'Populates the Questions database using a quesiton set in a JSON file'

    def add_arguments(self, parser):
        parser.add_argument("course_name")
        parser.add_argument("course_code")
        parser.add_argument("course_file")

    def handle(self, *args, **options):
        course_name = options["course_name"]
        course_code = options["course_code"]
        course_file = options["course_file"]

        def populate_course(file, topics, course, users):
            all_topics = [Topic.objects.create(
                name=x, course=course) for x in topics]
            print("\t-Enrolling Users")
            course_users = []
            for user in users:
                if chance(2):
                    course_users.append(
                        CourseUser.objects.create(user=user, course=course))

            print("\t-Making Questions")
            distractors = parse_questions(file, course_users, all_topics)
            '''distractors = []
            for i in range(0, 50):
                distractors.extend(make_questions(course_users, all_topics))'''

            print("\t-Answering and Rating Questions")
            for user in course_users:
                for i in range(0, 10):
                    make_question_responses(user, distractors)

        courses = [
            {"courseCode": course_code, "courseName": course_name}
        ]

        unique_topics = get_topics(course_file)

        users = [User.objects.create(user_id=user_id, first_name=fake.first_name(), last_name=fake.last_name(), image=fake.image_url())
                 for user_id in range(5)]
        
        all_courses = [Course.objects.create(
            available=True,
            course_code=x["courseCode"], course_name=x["courseName"]) for x in courses]
        for course in all_courses:
            print("Populating Course: " + course.course_code)
            populate_course(course_file, unique_topics, course, users)
