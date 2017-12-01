# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import base64

from questions.models import Topic, Distractor, Question, QuestionResponse, QuestionScore, Competency
from users.services import UserService
from users.models import CourseUser

from .common import BootstrapTestCase

class QuestionTestCase(BootstrapTestCase):   
    def test_update_user_image(self):
        user = self._bootstrap_user()
        host = "//localhost:8000"
        with open("./users/tests/elephantJPG.png", "rb") as image_file:
            bad_encode = base64.b64encode(image_file.read())
            start = b"data:image/png;base64,"
            bad_encode = str(start+bad_encode)

        # Image is none
        res = UserService.update_user_image(user, host, None)
        self.assertEquals(res, {"error": "No image provided"})

        # Image type does not match file
        res = UserService.update_user_image(user, host, bad_encode)
        self.assertEquals(res, {"error": "Image is not of valid type"})