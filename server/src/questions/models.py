# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from users.models import Course, CourseUser


class Topic(models.Model):
    name = models.CharField(max_length=128)

    course = models.ForeignKey(Course)

    def __str__(self):
        return self.name

    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Question(models.Model):
    content = models.TextField()
    explanation = models.TextField()
    difficulty = models.FloatField()
    quality = models.FloatField()
    difficultyCount = models.IntegerField()
    qualityCount = models.IntegerField()

    created_time = models.DateTimeField(auto_now_add=True)

    topics = models.ManyToManyField(Topic)
    author = models.ForeignKey(CourseUser)

    def __str__(self):
        return self.content[:20]

    def toJSON(self):
        return {
            "id": self.id,
            "content": self.content,
            "explanation": self.explanation,
            "difficulty": self.difficulty,
            "quality": self.quality,
            "difficultyCount": self.difficultyCount,
            "qualityCount": self.qualityCount,
            "topics": [x.toJSON() for x in self.topics.all()],
            "responses": [],
            "responseCount": sum((x.questionresponse_set.count() for x in self.distractor_set.all())),
            "distractors": [x.toJSON() for x in self.distractor_set.all()]
        }


class Distractor(models.Model):
    content = models.TextField()
    response = models.CharField(max_length=1)
    isCorrect = models.BooleanField()

    question = models.ForeignKey(Question, on_delete=None)

    def __str__(self):
        return self.content[:20]

    def toJSON(self):
        return {
            "id": self.id,
            "content": self.content,
            "response": self.response,
            "isCorrect": self.isCorrect
        }


class QuestionResponse(models.Model):
    response = models.ForeignKey(Distractor, on_delete=None)
    user = models.ForeignKey(CourseUser, on_delete=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "For user: " + str(self.user)


class QuestionRating(models.Model):
    quality = models.FloatField(null=True)
    difficulty = models.FloatField(null=True)

    user = models.ForeignKey(CourseUser, on_delete=None)
    response = models.ForeignKey(Distractor, on_delete=None)


class QuestionScore(models.Model):
    score = models.FloatField()
    number_answers = models.IntegerField()

    question = models.ForeignKey(Question)
    user = models.ForeignKey(CourseUser)

class Competency(models.Model):
    competency = models.FloatField()
    confidence = models.FloatField()

    topics = models.ManyToManyField(Topic)
    user = models.ForeignKey(CourseUser)

    def __str__(self):
        return str(self.competency)+" "+str(self.confidence)+" "+str(self.topics.all())

class QuestionImage(models.Model):
    image = models.ImageField(upload_to='question_photo')
    question = models.ForeignKey(Question, on_delete=None)


class ExplanationImage(models.Model):
    image = models.ImageField(upload_to='question_photo')
    question = models.ForeignKey(Question, on_delete=None)


class DistractorImage(models.Model):
    image = models.ImageField(upload_to='question_photo')
    distractor = models.ForeignKey(Distractor, on_delete=None)
