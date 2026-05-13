from django.contrib import admin

from .models import Address, Address2, Author, Book, Publisher, Student, Student2, StudentActivity


admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Address)
admin.site.register(Student)
admin.site.register(Address2)
admin.site.register(Student2)
admin.site.register(StudentActivity)
