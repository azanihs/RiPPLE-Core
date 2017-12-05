# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import base64
from mock import MagicMock

from users.services import UserService
from users.models import CourseUser, UserImage, Token, Role, User
from questions.models import Topic, Course
from django.core.files import File as f
from django.test import Client
from django.utils import timezone
from datetime import datetime
import urllib
import json

from .common import BootstrapTestCase

class RequestMock:
    def __init__(self, request_dict):
        self._dict = request_dict

    @property
    def META(self):
        return self._dict

def mock_request_factory(request_dict):
    mocked_request = RequestMock(request_dict)
    return mocked_request

class UserTestCase(BootstrapTestCase):   
    def test_update_user_image(self):
        user = self._bootstrap_user()
        host = "//localhost:8000"
        with open("./users/tests/elephantJPG.png", "rb") as image_file:
            bad_encode = base64.b64encode(image_file.read())
            start = b"data:image/png;base64,"
            bad_encode = str(start+bad_encode)

        with open("./users/tests/elephant.jpeg", "rb") as image_file:
            good_encode = base64.b64encode(image_file.read())
            start = b"data:image/jpeg;base64,"
            good_encode = str(start+good_encode)

        # Image is none
        res = UserService.update_user_image(user, host, None)
        self.assertEqual(res, {"error": "No image provided"})

        # Image type does not match file
        res = UserService.update_user_image(user, host, bad_encode)
        self.assertEqual(res, {"error": "Image is not of valid type"})

        #Image update successful
        res = UserService.update_user_image(user, host, good_encode)
        self.assertEqual(res, {"name":user.first_name + " " + user.last_name,
                "image": user.image
            })
        
        image = UserImage.objects.filter(user=user)[0].image 
        encode = str(b"data:image/jpeg;base64,"+base64.b64encode(image.read()))
        self.assertEqual(good_encode, encode)

    
    def test_logged_in_user(self):
        user = self._bootstrap_course_user()
        
        # Request not none
        self.assertEqual(UserService.logged_in_user(None),
            {"error": "Request must be provided"})
        
        #Request not empty
        self.assertEqual(UserService.logged_in_user({}),
            {"error": "Request must be provided"})

        #No Token
        mocked_request = mock_request_factory({})
        with self.assertRaises(Exception) as e:
            UserService.logged_in_user(mocked_request)
        self.assertEqual(str(e.exception), "User not associated with token")

        #Token Given
        mocked_request = mock_request_factory({"HTTP_AUTHORIZATION": "secret_token"})
        UserService.token_to_user_course = MagicMock(return_value=None)

        UserService.logged_in_user(mocked_request)
        UserService.token_to_user_course.assert_called_with("secret_token")

    def test_user_courses(self):
        courses = [self._bootstrap_courses(x) for x in range(5)]
        users = [self._bootstrap_user() for x in range(5)]
        course_map = [
            [courses[0]],
            [courses[0], courses[1]],
            [courses[0], courses[1], courses[2]],
            [courses[3]],
            [courses[3], courses[4]]
        ]
        course_users = []
        for i in range(5):
            for c in course_map[i]:
                course_users.append(self._user_in_course(users[i], c))

        # No User
        self.assertEqual({"error": "CourseUser must be provided"} ,
                UserService.user_courses(None))


        # Valid        
        for c_u in course_users:
            u_id = c_u.user.id-1
            u_c = UserService.user_courses(c_u)
            c_list = [x.toJSON() for x in course_map[u_id]]

            self.assertEqual(u_c, c_list)
           


    def test_update_course(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user()
        course_user = self._user_in_course(user, course)

        # None inputs
        self.assertEqual(UserService.update_course(None, None),
                {"error": "Course user and update data must be provided"})

        # Empty inputs
        self.assertEqual(UserService.update_course({}, {}),
                {"error": "Course user and update data must be provided"})

        # New_Data invalid attributes
        # no topics
        self.assertEqual(UserService.update_course(course_user, {"test":"att"}), 
                {"error": "Course must have topics"})

        # Invalid topics
        self.assertEqual(UserService.update_course(course_user, 
                    {"topics": [{"invalid": "topic"}]}),
                {"error": "Topics must be JSON representations of Topics with, at minimum, attribute 'name'"})


        topics = self._bootstrap_topics(course)
        topics = [t.toJSON() for t in topics]
        
        # No course Code
        self.assertEqual(UserService.update_course(course_user, 
                    {"topics": topics}),
                {"error": "Missing course code"})

        # Course codes do not match
        self.assertEqual(UserService.update_course(course_user, {
                    "topics": topics,
                    "course": {
                        "courseCode": "invalid code"
                    }}),
                {"error": "Course not found"})

        # User role not defined
        self.assertEqual(UserService.update_course(course_user, {
                    "topics": topics,
                    "course": {
                        "courseCode": "test_course_1"
                    }}),
                {"error": "User does not have administrative permission for current context"})
        
        role = Role(role="Student")
        role.save()
        role = [role]
        course_user.roles.set(role)

        # User role is not instructor
        self.assertEqual(UserService.update_course(course_user, {
                    "topics": topics,
                    "course": {
                        "courseCode": "test_course_1"
                    }}),
                {"error": "User does not have administrative permission for current context"})

        role = Role(role="Instructor")
        role.save()
        role = [role]
        course_user.roles.set(role)

        # Invalid start
        self.assertEqual(UserService.update_course(course_user, {
                    "topics": topics,
                    "course": {
                        "courseCode": "test_course_1",
                        "start": "invalid start"
                    }}),
                {"error": "Given start timestamp is not valid: invalid start"})

        # Invalid end
        self.assertEqual(UserService.update_course(course_user, {
                    "topics": topics,
                    "course": {
                        "courseCode": "test_course_1",
                        "start": 100,
                        "end": "invalid end"
                    }}),
                {"error": "Given end timestamp is not valid: invalid end"})

        # Invalid topics
        # Invalid ID
        self.assertEqual(UserService.update_course(course_user, {
                    "topics": [{"id": "abc", "name": "def"}],
                    "course": {
                        "courseCode": "test_course_1",
                        "start": 100,
                        "end": 100
                    }}),
                {"error": "Invalid Topic ID"})
    
        
        #VALID TESTS
        self.assertEqual(UserService.update_course(course_user, {
                    "topics": [{"name": "topicA"}],
                    "course": {
                        "courseCode": "test_course_1",
                        "start": 100,
                        "end": 100
                    }}),
                {"course": {
                    "available": True,
                    "courseCode": "test_course_1",
                    "courseName": "course_name_1",
                    "end": 100,
                    "start": 100
                },
                "roles": ["Instructor"],
                "user": {
                    "image": "",
                    "name": "u_firstname u_lastname"
                }})


        topics = self._bootstrap_topics(course)
        topics = [t.toJSON() for t in topics]
        self.assertEqual(UserService.update_course(course_user, {
                    "topics": [
                        {"id": 8, "name": "topicA"},
                        {"name": "newTopic"},
                        {"id": 100, "name": "idNotExist"}    
                    ],
                    "course": {
                        "courseCode": "test_course_1",
                        "start": 100,
                        "end": 100
                    }}),
                {"course": {
                    "available": True,
                    "courseCode": "test_course_1",
                    "courseName": "course_name_1",
                    "end": 100,
                    "start": 100
                },
                "roles": ["Instructor"],
                "user": {
                    "image": "",
                    "name": "u_firstname u_lastname"
                }})


    def test_process_competencies(self):
        user = self._bootstrap_user()
        course = self._bootstrap_courses(1)
        course_user = self._user_in_course(user, course)
        topics = self._bootstrap_topics(course)
        competencies = []
        competencies.append(self._bootstrap_competencies(course_user, topics[0]))
        competencies.append(self._bootstrap_competencies(course_user, topics[1:4]))
        competencies.append(self._bootstrap_competencies(course_user, topics[5]))
        competencies.append(self._bootstrap_competencies(course_user, [topics[4],topics[5]]))

        #Competencies None
        self.assertEqual([], UserService._process_competencies(None))

        #Competencies < confidence
        competencies[0].confidence = -100
        self.assertEqual([], UserService._process_competencies([competencies[0]]))

        #More than 2 topics
        self.assertEqual([], UserService._process_competencies([competencies[1]]))

        #Topic 5 - OK
        self.assertEqual(UserService._process_competencies([competencies[2]]),
                [[{"id": 6, "name": "t6"}, {"id": 6, "name": "t6"}, 100, 100]])

        # Topic 4 and 5
        self.assertEqual(UserService._process_competencies([competencies[3]]),
                [[{"id": 5, "name": "t5"}, {"id": 6, "name": "t6"}, 100, 100]])


    def test_user_competencies(self):
        user = self._bootstrap_user()
        course = self._bootstrap_courses(1)
        course_user = self._user_in_course(user, course)
        topics = self._bootstrap_topics(course)
        

        self.assertEqual([], UserService.user_competencies(None))

        self.assertEqual([], UserService.user_competencies(CourseUser))

        self._bootstrap_competencies(course_user, topics[1:3])

        self.assertEqual(UserService.user_competencies(course_user),
                [[{"id": 2, "name": "t2"}, {"id": 3, "name": "t3"}, 100, 100]])



    def test_aggregate_competencies(self):
        user = self._bootstrap_user()
        course = self._bootstrap_courses(1)
        course_user = self._user_in_course(user, course)
        topics = self._bootstrap_topics(course)

        self.assertEqual([], UserService.aggregate_competencies(None, None))

        self.assertEqual([], UserService.aggregate_competencies(course_user, "peer"))

        self.assertEqual([], UserService.aggregate_competencies(course_user, "other"))

        self._bootstrap_competencies(course_user, topics[1:3])

        self.assertEqual(UserService.aggregate_competencies(course_user, "peer"),
                [[{"id": 2, "name": "t2"}, {"id": 3, "name": "t3"}, 100, 100]])

        self.assertEqual(UserService.aggregate_competencies(course_user, "other"),
                [[{"id": 2, "name": "t2"}, {"id": 3, "name": "t3"}, 100, 100]])


    def test_insert_course_if_not_exists(self):
        self.assertEqual(UserService.insert_course_if_not_exists(None),
                {"error": "Invalid Course Provided"})

        self.assertEqual(UserService.insert_course_if_not_exists({"invalid": "course"}),
                {"error": "Invalid Course Provided"})

        self.assertEqual(UserService.insert_course_if_not_exists(
                {"course_code": "test1", "course_name": "test1"}
        ), Course.objects.filter(course_code="test1")[0])

        c = Course(course_code="test2", course_name="test2")
        c.save()
        
        self.assertEqual(UserService.insert_course_if_not_exists(
                {"course_code": "test2", "course_name": "test2"}
        ), c)

    def test_insert_user_if_not_exists(self):
        self.assertEqual(UserService.insert_user_if_not_exists(None),
                {"error": "Invalid User Provided"})

        self.assertEqual(UserService.insert_user_if_not_exists({"invalid": "user"}),
                {"error": "Invalid User Provided"})

        self.assertEqual(UserService.insert_user_if_not_exists({"user_id": "u1"}),
                {"error": "Invalid User Provided"})

        self.assertEqual(UserService.insert_user_if_not_exists({"user_id": "test1", "first_name":"first_name", "last_name":"last_name", "image":""}), User.objects.filter(user_id="test1")[0])

        u = User(user_id="test2", first_name="first_name", last_name="last_name",
                image="")
        u.save()
        
        self.assertEqual(UserService.insert_user_if_not_exists(
                {"user_id": "test2", "first_name":"first_name", "last_name":"last_name",
                "image": ""}
        ), u)


    def test_insert_course_user_if_not_exists(self):
        user = self._bootstrap_user()
        course = self._bootstrap_courses(1)
        course2 = self._bootstrap_courses(2)

        self.assertEqual(UserService.insert_course_user_if_not_exists(None, user),
                {"error": "Invalid Course Provided"})

        self.assertEqual(UserService.insert_course_user_if_not_exists({}, user),
                {"error": "Invalid Course Provided"})

        self.assertEqual(UserService.insert_course_user_if_not_exists(course, None),
                {"error": "Invalid User Provided"})

        self.assertEqual(UserService.insert_course_user_if_not_exists(course, {}),
                {"error": "Invalid User Provided"})

        self.assertEqual(UserService.insert_course_user_if_not_exists(course, user), 
                CourseUser.objects.filter(course=course, user=user)[0])
        
        cu = CourseUser(course=course2, user=user)
        cu.save()

        self.assertEqual(UserService.insert_course_user_if_not_exists(
            course2, user), cu)

    
    def test_update_user_roles(self):
        user = self._bootstrap_user()
        course = self._bootstrap_courses(1)
        cu = CourseUser(course=course, user=user)
        cu.save()

        self.assertEqual(UserService.update_user_roles(None, "test_role"),
                {"error": "Invalid CourseUser Provided"})

        self.assertEqual(UserService.update_user_roles({}, "test_role"),
                {"error": "Invalid CourseUser Provided"})

        self.assertEqual(UserService.update_user_roles(cu, None),
                {"error": "Invalid Role Provided"})

        role1 = Role(role="role1")
        UserService.update_user_roles(cu, role1)
        self.assertTrue(role1.role in cu.roles.all().values_list("role", flat=True))

        UserService.update_user_roles(cu, "role2")
        self.assertTrue("role2" in cu.roles.all().values_list("role", flat=True))

