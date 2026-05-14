from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=50)
    grade = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    description = models.TextField()
    career_path = models.TextField()

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Course(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    name = models.CharField(max_length=100)
    credit = models.IntegerField()
    description = models.TextField()
    difficulty = models.IntegerField()

    def __str__(self):
        return self.name


class StudentInterest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    preference_level = models.IntegerField()

    def __str__(self):
        return f'{self.student.name} - {self.interest.name}'


class DepartmentInterest(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    relevance_level = models.IntegerField()

    def __str__(self):
        return f'{self.department.name} - {self.interest.name}'


class Recommendation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    score = models.IntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.name} → {self.department.name}'