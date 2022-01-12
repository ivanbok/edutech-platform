from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.ForeignKey(to='Levels', on_delete=models.CASCADE)

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Subjects(models.Model):
    subject = models.CharField(max_length=64)

class Levels(models.Model):
    level = models.CharField(max_length=64)

class QuestionTypes(models.Model):
    questiontype = models.CharField(max_length=64)

class Question(models.Model):
    questiontype = models.ForeignKey(to='QuestionTypes', on_delete=models.CASCADE, related_name='sourcequestion')
    subject = models.ForeignKey(to='Subjects', on_delete=models.CASCADE, related_name='questionsforsubject')
    level = models.ManyToManyField(Levels) # To allow for multiple levels
    tags = models.CharField(max_length=256)

class MultipleChoiceQuestion(models.Model):
    question = models.ForeignKey(to='Question', on_delete=models.CASCADE, related_name='MCQ')
    question_text = models.TextField(max_length=1000)
    option1 = models.TextField(max_length=1000)
    option2 = models.TextField(max_length=1000)
    option3 = models.TextField(max_length=1000)
    option4 = models.TextField(max_length=1000)
    correctAnswer = models.IntegerField()

class MultipleChoiceResponses(models.Model):
    student = models.ForeignKey(to='Student', on_delete=models.CASCADE, related_name='StudentMCQAnswers')
    questionid = models.ForeignKey(to='MultipleChoiceQuestion', on_delete=models.CASCADE, related_name='MCQAnswers')
    studentAnswer = models.IntegerField()
    is_correct = models.BooleanField(default=False)

class NumericResponseQuestion(models.Model):
    question = models.ForeignKey(to='Question', on_delete=models.CASCADE, related_name='NumericQuestions')
    question_text = models.TextField(max_length=1000)
    correctAnswer = models.DecimalField(max_digits=10, decimal_places=5)
    sigfigacceptable = models.IntegerField(default=2)
