# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from questions.models import Question, QuestionImage, ExplanationImage, DistractorImage
from questions.services import AuthorService
from users.models import CourseUser
from django.db import IntegrityError
from mock import MagicMock, Mock, patch
from ripple.util import util

from .common import BootstrapTestCase

class QuestionRequestTest(BootstrapTestCase):
    def test_add_question(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        new_question = self._bootstrap_question_request()

        response = AuthorService.add_question(new_question, "/", author)
        self.assertEqual(response["state"], "Question Added")
        self.assertEqual(response["question"], Question.objects.all().first().toJSON())


    def test_none_field(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)

        attributes = ["question", "explanation", "responses", "topics"]

        for i in attributes:
            invalid_question = self._bootstrap_question_request()
            invalid_question[i] = None
            response = AuthorService.add_question(invalid_question, "/", author)
            self.assertEqual(response["state"], "Error")
            self.assertEqual(response["error"], "Invalid Question")

        invalid_question = self._bootstrap_question_request()
        distractor = next(iter(invalid_question["responses"]))
        invalid_question["responses"][distractor] = None
        response = AuthorService.add_question(invalid_question, "/", author)
        self.assertEqual(response["state"], "Error")
        self.assertEqual(response["error"], "Missing response " + distractor)


    def test_check_for_script_tags(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)

        attributes = ["question", "explanation"]

        script_tag = "<script> evil code </script>"

        for attribute in attributes:
            unsafe_question = self._bootstrap_question_request()
            unsafe_question[attribute]["content"] = script_tag
            response = AuthorService.add_question(unsafe_question, "/", author)
            self.assertEqual(response["state"], "Error")
            self.assertEqual(response["error"], "Invalid Question")

        unsafe_question = self._bootstrap_question_request()
        key = next(iter(unsafe_question["responses"]))
        unsafe_question["responses"][key]["content"] = script_tag
        response = AuthorService.add_question(unsafe_question, "/", author)
        self.assertEqual(response["state"], "Error")
        self.assertEqual(response["error"], "Invalid Distractor")


    def test_question_with_valid_image(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        image_question = self._bootstrap_question_request()

        image_test = Mock(name = "test")
        test = Mock(image = image_test)

        image_question["question"]["payloads"] = {"0": "data:image/jpeg;base64,..."}
        util.save_image = MagicMock(return_value = 1)
        QuestionImage.objects.create = MagicMock(return_value = test)
        image_question["question"]["content"] = "<img src = 'test'>"
        util.update_image_sources = MagicMock(return_value = True)
        response = AuthorService.add_question(image_question, "/", author)
        self.assertEqual(response["state"], "Question Added")
        self.assertEqual(response["question"], Question.objects.all()[0].toJSON())

        image_question["explanation"]["payloads"] = {"0": "data:image/jpeg;base64,..."}
        ExplanationImage.objects.create = MagicMock(return_value = test)
        response = AuthorService.add_question(image_question, "/", author)
        self.assertEqual(response["state"], "Question Added")
        self.assertEqual(response["question"], Question.objects.all()[1].toJSON())

        image_question["responses"]["A"]["payloads"] = {"0": "data:image/jpeg;base64,..."}
        DistractorImage.objects.create = MagicMock(return_value = test)
        response = AuthorService.add_question(image_question, "/", author)
        self.assertEqual(response["state"], "Question Added")
        self.assertEqual(response["question"], Question.objects.all()[2].toJSON())


    def test_question_with_invalid_image(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        image_question = self._bootstrap_question_request()

        util.save_image = MagicMock(return_value=None)

        image_question["question"]["payloads"] = {"0": "data:image/jpeg;base64,..."}
        response = AuthorService.add_question(image_question, "/", author)

        self.assertEqual(response["state"], "Error")
        self.assertEqual(response["error"], "Image is not of valid type")

    def test_new_source(self):
        urls = ["test"]
        content = "<img src='#:0'>"
        host = "/here/asfd/"
        result = util.update_image_sources(urls, content, host)
        self.assertTrue(urls[0] in result and host in result)

        content = "<img src='#:0' /><img src='//url_not_to_replace/' /><img src='#:1' />"
        urls = ["test", "test_2"]
        result = util.update_image_sources(urls, content, host)
        self.assertTrue(urls[0] in result and host in result)

    def test_empty_content(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        new_question = self._bootstrap_question_request()

        new_question["question"]["content"] = ""
        response = AuthorService.add_question(new_question, "/", author)
        self.assertEqual(response["state"], "Error")
        self.assertEqual(response["error"], "Invalid Question")


    @patch("ripple.util.util.extract_image_from_html")
    def test_general_exception_raised(self, mock_class):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        new_question = self._bootstrap_question_request()

        new_question["question"]["payloads"] = {"0": "data:image/jpeg;base64,..."}
        mock_class.side_effect = Exception("Exception Raised")
        response = AuthorService.add_question(new_question, "/", author)

        self.assertEqual(response["state"], "Error")
        self.assertEqual(response["error"], "Exception Raised")
