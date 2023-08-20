from django.db import models
import re

EMAIL_REGEX =\
    re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        for key in postData:
            is_blank = False
            if postData[key] == "":
                is_blank = True
        if is_blank:
            errors['fields'] = "All fields required!"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        user = User.objects.filter(email=postData['email'])
        if user:
            errors['email'] = "Email already exists!"
        user = User.objects.filter(email=postData['username'])
        if user:
            errors['username'] = "Username already exists!"
        return errors

    def login_validator(self, postData):
        errors = {}
        for key in postData:
            is_blank = False
            if postData[key] == "":
                is_blank = True
        if is_blank:
            errors["fields"] = "All fields required!"
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address!"
        user = User.objects.filter(email=postData["email"])
        if not user:
            errors["email"] =\
                "User email does not exist - please sign up instead."
        # user = User.objects.filter(email=postData['username'])
        # if not user:
        #     errors['username'] = \
        #         "Username does not exist - please sign up instead."
        return errors


class User(models.Model):
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    record = {}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.username
