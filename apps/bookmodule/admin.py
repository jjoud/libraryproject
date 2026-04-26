from django.contrib import admin

from .models import Address, Author, Book, Publisher, Student


admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Address)
admin.site.register(Student)
