from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    quantity = models.IntegerField()
    lib_author = models.CharField(max_length=100, default="Sara")
    category = models.CharField(max_length=50, default="Featured")
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=10)
    branch = models.CharField(max_length=3)
    contact_no = models.CharField(max_length=10)
    total_books_due = models.IntegerField(default=0)
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=8, default=1234)

    def __str__(self):
        return str(self.roll_no)


class Borrower(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.student.name + " borrowed " + self.book.title


class Reviews(models.Model):
    review = models.CharField(max_length=100, default="none")
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
