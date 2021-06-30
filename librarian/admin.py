from django.contrib import admin

# Register your models here.

from .models import Book
from .models import Student
from .models import Borrower
from .models import Reviews

admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Borrower)
admin.site.register(Reviews)
