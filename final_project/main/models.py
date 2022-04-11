from final_project.accounts.models import AppUser, Profile
from django.contrib.auth import get_user_model
from django.db import models


UserModel = get_user_model()


class Courses(models.Model):
    COURSE_NAME_MAX_LENGTH = 50

    name = models.CharField(
        max_length=COURSE_NAME_MAX_LENGTH,
    )

    price = models.IntegerField()

    description = models.TextField()

    picture = models.URLField()

    duration = models.IntegerField()

    link_to_platform = models.URLField()

    coach = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    participants = models.ManyToManyField(
        Profile,
    )


class Equipment(models.Model):
    EQUIPMENT_NAME_MAX_LENGTH = 50

    name = models.CharField(
        max_length=EQUIPMENT_NAME_MAX_LENGTH,
    )

    picture = models.URLField()

    price = models.IntegerField()

    description = models.TextField()

    warranty = models.IntegerField()

    seller = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    owners = models.ManyToManyField(
        Profile,
    )


class StudyBook(models.Model):
    BOOK_NAME_MAX_LENGTH = 30

    name = models.CharField(
        max_length=BOOK_NAME_MAX_LENGTH,
    )

    price = models.IntegerField()

    cover = models.URLField()

    description = models.TextField()

    link_to_online_book = models.URLField()

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    owners = models.ManyToManyField(
        Profile,
    )


class Post(models.Model):
    TITLE_MAX_LENGTH = 50

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
    )

    picture = models.URLField()
    description = models.TextField()
    date_posted = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.IntegerField(
        default=0,
    )

    dislikes = models.IntegerField(
        default=0,
    )

    people_who_liked = {}

    people_who_disliked = []

    creator = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

