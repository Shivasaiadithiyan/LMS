from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.user.first_name} [{self.enrollment}]'

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    category_choices = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
    ]
    name = models.CharField(max_length=30)
    isbn = models.PositiveIntegerField()
    author = models.CharField(max_length=40)
    category = models.CharField(max_length=30, choices=category_choices, default='education')

    def __str__(self):
        return f'{self.name} [{self.isbn}]'


def get_expiry():
    return datetime.today() + timedelta(days=15)


class IssuedBook(models.Model):
    student = models.ForeignKey(StudentExtra, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issuedate = models.DateField(auto_now=True)
    expirydate = models.DateField(default=get_expiry)

    def __str__(self):
        return f'{self.student.get_name} - {self.book.name}'


class PendingFine(models.Model):
    student = models.OneToOneField(StudentExtra, on_delete=models.CASCADE)
    money = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.student.get_name} - Pending Fine: {self.money} INR'
