from django.db import models
from django.core.validators import FileExtensionValidator


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50, blank=True)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
    pubdate = models.DateTimeField(null=True, blank=True)
    rating = models.SmallIntegerField(default=1)
    edition = models.SmallIntegerField(default=1)
    publisher = models.ForeignKey(
        Publisher,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    authors = models.ManyToManyField(Author, blank=True)

    def __str__(self):
        return self.title


class Address(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Address2(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.city} - {self.street}" if self.street else self.city


class Student2(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    addresses = models.ManyToManyField(Address2, blank=True)

    def __str__(self):
        return self.name


class StudentActivity(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.FileField(
        upload_to='student_activities/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
