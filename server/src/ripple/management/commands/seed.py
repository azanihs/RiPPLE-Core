from django.core.management.base import BaseCommand
from questions.models import Topic, Question, Distractor, QuestionResponse, QuestionRating, Competency, CompetencyMap
from users.models import Course, User, CourseUser

from questions.services import QuestionService

from random import randint, randrange, sample, choice
from faker import Factory
fake = Factory.create()


def chance(n):
    return choice(range(n)) is n - 1


def make_questions(course_users, all_topics):
    img_url = "<img src='" + fake.image_url() + "' />" if chance(3) else ""
    answer_url = "<img src='" + fake.image_url() + "' />" if chance(3) else ""
    question = Question(
        content=img_url + "<p>" + fake.text() + "</p>",
        explanation=answer_url + "<p>" + fake.text() + "</p>",
        difficulty=randrange(0, 5),
        quality=randrange(0, 5),
        difficultyCount=randint(0, 100),
        qualityCount=randint(0, 100),
        author=choice(course_users)
    )

    question.save()
    question.topics.set(sample(all_topics, randrange(1, 5)))

    correct_index = randrange(0, 4)

    _d = []
    for i in range(0, 4):
        distractor = Distractor(
            content="<p>" + fake.text() + "</p>",
            response=chr(ord('A') + i),
            isCorrect=i == correct_index)
        distractor.question = question
        distractor.save()
        _d.append(distractor)

    return _d


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


class Command(BaseCommand):
    args = ''
    help = 'Populates the Questions database'

    def handle(self, *args, **options):
        def populate_course(topics, course, users):
            all_topics = [Topic.objects.create(
                name=x, course=course) for x in topics]
            print("\t-Enrolling Users")
            course_users = []
            for user in users:
                if chance(2):
                    course_users.append(
                        CourseUser.objects.create(user=user, course=course))

            print("\t-Making Questions")
            distractors = []
            for i in range(0, 50):
                distractors.extend(make_questions(course_users, all_topics))

            print("\t-Answering and Rating Questions")
            for user in course_users:
                for i in range(0, 10):
                    make_question_responses(user, distractors)

        courses = [
            {"courseCode": "SCIE1000", "courseName": "Intro to science"},
            {"courseCode": "CSSE1001", "courseName": "Intro to data systems"},
            {"courseCode": "INFS1200", "courseName": "Intro to software engineering"}
        ]
        unique_topics = ["Arrays", "Loops", "Recursion",
                         "Algorithms", "Data Structures", "Variables"]

        users = [User.objects.create(user_id=user_id, username=user_id, first_name=fake.first_name(), last_name=fake.last_name(), image=fake.image_url())
                 for user_id in range(50)]

        all_courses = [Course.objects.create(
            available=True,
            course_code=x["courseCode"], course_name=x["courseName"]) for x in courses]
        for course in all_courses:
            print("Populating Course: " + course.course_code)
            populate_course(unique_topics, course, users)
