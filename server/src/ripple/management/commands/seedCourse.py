from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import IntegrityError, transaction
from django.core.files.base import ContentFile
from questions.models import Topic, Question, Distractor, QuestionResponse, QuestionRating, Competency, QuestionImage,\
    ExplanationImage, DistractorImage, ReportReason
from users.models import Course, User, CourseUser, Engagement, ConsentForm
from recommendations.models import Day, Time, Availability, StudyRole, AvailableRole
from base64 import b64decode
import imghdr
import sys

from questions.services import QuestionService

from random import randint, randrange, sample, choice
from datetime import datetime
from faker import Factory
fake = Factory.create()

import json
from bs4 import BeautifulSoup
import base64
import imghdr
from ripple.util import util
from django.conf import settings

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


def chance(n):
    return choice(range(n)) is n - 1

def _format(x):
    if len(x) == 0: return x
    return (x + "/") if x[-1] != "/" else x

def merge_url_parts(parts, url=""):
    if len(parts) == 0:
        return url
    return merge_url_parts(parts, urljoin(url, parts.pop(0)))


def make_question_responses(user, distractors):
    if chance(2):
        user_choice = choice(distractors)
        response = QuestionResponse(
            response=user_choice,
            user=user
        )
        response.save()
        QuestionService.update_competency(
            user, user_choice.question, response)

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


def parse_questions(file, course_users, all_topics, host):
    host = merge_url_parts([
        _format(host),
        _format(settings.FORCE_SCRIPT_NAME),
        _format("static")
    ])
    distractors = []

    with open(file) as data_file:
        data = json.load(data_file)

    questions = data["questions"]
    counter = 0
    for q in questions:
        try:
            with transaction.atomic():
                distractor_count = 0
                counter = counter+1
                if q["explanation"]["content"] is None:
                        q["explanation"]["content"] = " "

                question = Question(
                    content = q["question"]["content"],
                    explanation = q["explanation"]["content"],
                    difficulty = randrange(0, 5),
                    quality = randrange(0, 5),
                    difficultyCount = randrange(0, 100),
                    qualityCount = randrange(0, 100),
                    author = choice(course_users)
                )
                question.save()
                d = decode_images(question.id, question, q["question"]["payloads"], "q", host)
                if not d:
                    raise IntegrityError("Invalid Question Image")
                d = decode_images(question.id, question, q["explanation"]["payloads"], "e", host)
                if not d:
                    raise IntegrityError("Invalid Explanation Image")

                q_topics = q["topics"]
                for topic in q_topics:
                    idx = 0
                    while idx < len(all_topics):
                        if topic["name"] == all_topics[idx].name:
                            break
                        idx+=1
                    question.topics.add(all_topics[idx])
                question.save()

                _response_choices = ["A", "B", "C", "D"]
                if True not in [q["responses"][i].get("isCorrect", False) for i in _response_choices]:
                    raise IntegrityError("No correct answer for question")

                for i in _response_choices:
                    response = q["responses"][i]
                    if response["content"] is None:
                        response["content"] = " "
                    distractor = Distractor(
                        content = response["content"],
                        response = i,
                        isCorrect = response["isCorrect"],
                        question = question
                    )
                    distractor.save()
                    distractor_count+=1
                    d = decode_images(distractor.id, distractor, response["payloads"],"d", host)
                    if not d:
                        raise IntegrityError("Invalid Distractor Image")
                    distractors.append(distractor)
        except IntegrityError as e:
            distractors=distractors[:len(distractors)-distractor_count]
            print("Invalid question: " + str(counter))

    return distractors

def decode_images(image_id, obj, images, image_type, host):
    if len(images) == 0:
        return True
    # objType q=question, d=distractor
    urls = []
    database_image_types = {
        "q": QuestionImage,
        "d": DistractorImage,
        "e": ExplanationImage
    }
    ImageToSaveClass = database_image_types.get(image_type, None)

    for i, image in images.items():
        contentfile_image = save_image_course_seeder(image, image_id)
        if contentfile_image is None:
            return False
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
        images[i]['src'] = util.merge_url_parts([host, urls[i]])

    immediate_children = soup.findChildren(recursive=False)
    return ''.join([str(x) for x in immediate_children])

def make_days():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for x in days:
        if len(Day.objects.filter(day=x)) == 0:
            day = Day.objects.create(day=x)
            day.save()

def make_times(times):
    for i in range(len(times) - 1):
        if len(Time.objects.filter(start=times[i], end=times[i + 1])) == 0:
            time_range = Time.objects.create(start=times[i], end=times[i + 1])
            time_range.save()

def make_study_roles():
    study_roles = [
    {"role": "mentor", "description": "Provide Mentorship"},
    {"role": "mentee", "description": "Seek Mentorship"},
    {"role": "partner", "description": "Find Study Partners"}]

    for x in study_roles:
        study_role = StudyRole.objects.create(role=x["role"], description=x["description"])
        study_role.save()

class Command(BaseCommand):
    args = ''
    help = 'Populates the Questions database using a question set in a JSON file'

    def add_arguments(self, parser):
        parser.add_argument("--name", nargs="+")
        parser.add_argument("--course", nargs="+")
        parser.add_argument("--file", nargs="+")
        parser.add_argument("--host")

    def handle(self, *args, **options):
        if(len(options["name"])!=len(options["course"]) or len(options["name"])!=len(options["file"])):
            print("Please ensure you have a course code, name and file for each course")
            sys.exit(1)

        course_names = options["name"]
        course_codes = options["course"]
        course_files = options["file"]
        host = options["host"]

        def populate_course(file, topics, course, users):
            all_topics = [Topic.objects.create(
                name=x, course=course) for x in topics]
            print("\t-Creating Report Reasons")
            reason_list = ["custom", "Inappropriate Content", "Incorrect Answer",  "Incorrect Tags"]
            for r in reason_list:
                reason = ReportReason (
                    reason=r,
                    course=course
                )
                reason.save()

            print("\t-Adding Engagements")
            engagements = ["Questions Answered", "Questions Authored", "Questions Rated",
                    "Competent Topics", "Achievements Earned"]
            e_models = ["questionresponse", "question", "questionrating", "competency",
                    "userachievement"]
            e_filter_name = ["isCorrect", "", "", "", ""]
            e_key_user = ["user_id", "author_id", "user_id", "user_id", "user"]
            for i in range(len(engagements)):
                e = Engagement(name=engagements[i], course=course,
                        model=e_models[i], filter_name=e_filter_name[i],
                        key_user=e_key_user[i])
                e.save()

            print("\t-Enrolling Users")
            course_users = []
            for user in users:
                if chance(2):
                    course_users.append(
                        CourseUser.objects.create(user=user, course=course))

            print("\t-Adding Consent Form")
            form = ConsentForm (
                text="Testing consent form",
                author=course_users[0]
            )
            form.save()

            print("\t-Making Questions")
            distractors = parse_questions(file, course_users, all_topics, host)

            print("\t-Answering and Rating Questions")
            for user in course_users:
                for i in range(0, 10):
                    make_question_responses(user, distractors)

        def populate_availability(course_users, days, times):
            for i in range(len(course_users)):
                course_user = course_users[i]
                for j in range(randint(3, 10)):
                    random_day = Day.objects.get(pk=randint(1, len(days)))
                    random_time = Time.objects.get(pk=randint(1, len(times)))
                    # Add availability
                    availability = Availability.objects.create(course_user=course_user, day=random_day, time=random_time)
                    availability.save()

        def populate_available_roles(course_users, study_roles):
            for course_user in course_users:
                topics = Topic.objects.filter(course=course_user.course)
                for topic in topics:
                    role_id = randint(0, 1)
                    if role_id > 0:
                        study_role = study_roles[1]
                        availableRole = AvailableRole.objects.create(course_user=course_user, topic=topic, study_role=study_role)

                    role_id = randint(0, 1)
                    if role_id:
                        study_role = study_roles[2]
                        availableRole = AvailableRole.objects.create(course_user=course_user, topic=topic, study_role=study_role)

        courses = []
        for i in range(0,len(course_names)):
            courses.append({"courseCode": course_codes[i], "courseName": course_names[i], "courseFile": course_files[i]})

        users = [User.objects.create(user_id=user_id, first_name=fake.first_name(), last_name=fake.last_name(), image="//loremflickr.com/320/240/person")
                 for user_id in range(50)]

        all_courses = [Course.objects.create(
            available=True,
            course_code=x["courseCode"], course_name=x["courseName"]) for x in courses]
        for i in range(0,len(all_courses)):
            print("Populating Course: " + all_courses[i].course_code)
            unique_topics = get_topics(courses[i]["courseFile"])
            populate_course(courses[i]["courseFile"], unique_topics, all_courses[i], users)

        print("Populating Availabilities")
        print("\t-Making Days")
        make_days()

        print("\t-Making Times")
        time_inputs = [datetime(2017, 11, 6, hour, 0).time() for hour in range(0, 24)]
        time_inputs.append(datetime(2017, 11, 7, 0, 0).time())
        make_times(time_inputs)

        print("\t-Making Study Roles")
        make_study_roles()

        course_users = CourseUser.objects.all()
        days = Day.objects.all()
        times = Time.objects.all()
        print("\t-Populating Availabilities")
        populate_availability(course_users, days, times)
        study_roles = StudyRole.objects.all()
        print("\t-Populating Study Roles")
        populate_available_roles(course_users, study_roles)

def save_image_course_seeder(encoded_image, image_id):
    image_format, base64_payload = encoded_image.split(';base64,')
    ext = image_format.split('/')[-1]
    data = ContentFile(b64decode(base64_payload),
                       name="")
    if imghdr.what(data) is not None:
        data.name = "u"+str(image_id)+"."+imghdr.what(data)
    else:
        return None

    return data
