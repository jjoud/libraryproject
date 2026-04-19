from django.contrib import admin

from .models import Address, Book, Student


admin.site.register(Book)
admin.site.register(Address)
admin.site.register(Student)
