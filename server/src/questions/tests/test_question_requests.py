# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from questions.models import Question, QuestionImage, ExplanationImage, DistractorImage, Distractor
from questions.services import AuthorService
from users.models import CourseUser
from django.db import IntegrityError
from mock import MagicMock, Mock, patch
from ripple.util import util

from .common import BootstrapTestCase

class QuestionRequestTest(BootstrapTestCase):
    def test_add_question(self):
        """Tests addittion of a new simple question without images"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        new_question = self._bootstrap_question_request()

        response = AuthorService.add_question(new_question, "/", author)
        self.assertEqual(response["state"], "Question Added")
        self.assertEqual(response["question"], Question.objects.all().first().toJSON())


    def test_none_field(self):
        """Tests an invalid question added that contains none fields in its attributes, including none fields in responses"""
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

    def test_no_true_answer(self):
        """Check that an Integrity Error is raised when none of the distractors have a true response"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        question = self._bootstrap_question_request()
        #Make all answers false
        for i in question["responses"]:
            question["responses"][i]["isCorrect"] = False
        response = AuthorService.add_question(question, "/", author)
        self.assertEqual(response["state"], "Error")
        self.assertEqual(response["error"], "No correct answer for question")


    def test_question_with_valid_image(self):
        """Checks that a question can be added that contains an image"""
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
        """Checks that a question addition fails when image is none type"""
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
        """Tests that the new source function creates a new path with the past path pieces"""
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
        """Check that a question addition fails when content on an attribute is empty"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)

        new_question = self._bootstrap_question_request()
        new_question["question"]["content"] = ""
        response = AuthorService.add_question(new_question, "/", author)
        self.assertEqual(response["state"], "Error")
        self.assertEqual(response["error"], "Question content is blank")

        new_question = self._bootstrap_question_request()
        new_question["explanation"]["content"] = ""
        response = AuthorService.add_question(new_question, "/", author)
        self.assertEqual(response["state"], "Error")
        self.assertEqual(response["error"], "Explanation content is blank")

        new_question = self._bootstrap_question_request()
        new_question["responses"]["A"]["content"] = ""
        response = AuthorService.add_question(new_question, "/", author)
        self.assertEqual(response["state"], "Error")
        self.assertEqual(response["error"], "Distractor content is blank")


    @patch("ripple.util.util.extract_image_from_html")
    def test_general_exception_raised(self, mock_class):
        """Tests that addition function behaves accordingly on a different exception that an IntegrityError"""
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


    def test_clean_content_function(self):
        """Tests that content on questions is properly cleansed"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)

        #Checking for element tags cleansing in question content
        unsafe_question = self._bootstrap_question_request()
        tag_tested = '<script>evil code</script>'
        unsafe_question["question"]["content"] = tag_tested
        response = AuthorService.add_question(unsafe_question, "/", author)
        added_question = Question.objects.all().first()
        self.assertEqual(response["state"], "Question Added")
        self.assertTrue(tag_tested not in added_question.content)

        #Checking for attribute tag cleansing in explanation content
        unsafe_question = self._bootstrap_question_request()
        tag_tested = '<p onclick="alert("you shall not pass");">evil code</script>'
        unsafe_question["explanation"]["content"] = tag_tested
        response = AuthorService.add_question(unsafe_question, "/", author)
        added_question = Question.objects.all().first()
        self.assertEqual(response["state"], "Question Added")
        self.assertTrue(tag_tested not in added_question.content)

        #Checking for style tag cleansing in response content
        unsafe_question = self._bootstrap_question_request()
        tag_tested = '<p style="position:absolute;">evil code</script>'
        unsafe_question["responses"]["A"]["content"] = tag_tested
        response = AuthorService.add_question(unsafe_question, "/", author)
        added_question = Question.objects.all().first()
        self.assertEqual(response["state"], "Question Added")
        self.assertTrue(tag_tested not in added_question.content)

    """The cleaning function sometimes modifies the string such as adding spaces on style tags so in order to
        test for equality the string must be exact
    """

    def test_allowed_cleaning_tags(self):
        """Tests that allowed tags pass trough the cleansing function"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)

        #Checking allowed element tags make it trough on question content
        unsafe_question = self._bootstrap_question_request()
        tag_tested = '<span>happy code</span>'
        unsafe_question["question"]["content"] = tag_tested
        response = AuthorService.add_question(unsafe_question, "/", author)
        added_question = Question.objects.all()[0]
        self.assertEqual(response["state"], "Question Added")
        self.assertTrue(tag_tested in added_question.content)

        #Checking allowed attributes make it trough on explanation content
        unsafe_question = self._bootstrap_question_request()
        tag_tested = '<a title="this aren\'t the droids you are looking for">happy code</a>'
        unsafe_question["explanation"]["content"] = tag_tested
        response = AuthorService.add_question(unsafe_question, "/", author)
        added_question = Question.objects.all()[1]
        self.assertEqual(response["state"], "Question Added")
        self.assertTrue(tag_tested in added_question.explanation)

    def test_allowed_cleaning_tags_responses(self):
        """Test that allowed style tags pass trough on response content, separated to avoid distractor overlap"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)

        #Checking for style tag cleansing in response content
        unsafe_question = self._bootstrap_question_request()
        tag_tested = '<p style="color: #339966;">happy code</p>'
        unsafe_question["responses"]["A"]["content"] = tag_tested
        response = AuthorService.add_question(unsafe_question, "/", author)
        added_distractor = Distractor.objects.all()[0]
        self.assertEqual(response["state"], "Question Added")
        self.assertTrue(tag_tested in added_distractor.content)

