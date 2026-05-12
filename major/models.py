# Model 관련 fields, methods를 모아놓은 놈입니다
from django.db import models


class Major(models.Model):
    MName = models.CharField(max_length=100, primary_key=True)
    College = models.CharField(max_length=100)

    def __str__(self):
        return self.Mname


class User(models.Model):
    # ID : integer
    ID = models.IntegerField(primary_key=True)
    # Name:(
    name = models.CharField(max_length=50)
    interest = models.ForeignKey(
        Major, on_delete=models.SET_NULL, null=True, related_name="interested_users"
    )
    major_name = models.ForeignKey(
        Major, on_delete=models.SET_NULL, null=True, related_name="majored_users"
    )
    # level
    Level = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    Code = models.CharField(max_length=100, primary_key=True)
    LName = models.CharField(max_length=100)
    CourseLevel = models.IntegerField(default=0)
    Category = models.CharField(max_length=50, default="교양")

    major_name = models.ForeignKey(
        Major, on_delete=models.CASCADE, related_name="lectures"
    )

    def __str__(self):
        return self.Lname


class PreRequisiteRelation(models.Model):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="required_by"
    )
    pre_lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="prerequisite_for"
    )


class CourseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    major_name = models.ForeignKey(Major, on_delete=models.CASCADE)
