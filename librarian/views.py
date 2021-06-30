from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, Student, Borrower
import re
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
# from datetime import datetime,timedelta
from .forms import *
from .filters import BookFilter, StudentFilter


# Create your views here.

# HOME PAGE
def index(request):
    context = {
        'books': Book.objects.all()
    }
    return render(
        request, 'librarian/home.html', context
    )


def about(request):
    context = {
        'books_featured': Book.objects.filter(category="Featured"),
        'books_bestseller': Book.objects.filter(category="BestSeller"),
        'books_mostwished': Book.objects.filter(category="MostWished"),
        'books_education': Book.objects.filter(category="Education"),
        'page_name': 'about'
    }
    return render(
        request, 'librarian/about.html', context
    )


def search(request):
    book_list = Book.objects.all()
    book_filter = BookFilter(request.GET, queryset=book_list)
    return render(request, 'librarian/search_book_list.html', {'filter': book_filter})


def search_student(request):
    student_list = Student.objects.all()
    student_filter = StudentFilter(request.GET, queryset=student_list)
    return render(request, 'librarian/search_student_list.html', {'filter': student_filter})


# Book List Displayed
class BookListView(ListView):
    model = Book
    template_name = 'librarian/home.html'
    context_object_name = 'books'


# Book Detail Displayed
# class BookDetailView(DetailView):
#     model = Book


def BookDetailView(request, pk):
    book = get_object_or_404(Book, id=pk)
    reviews = Reviews.objects.filter(book=book).exclude(review="none")

    # stu = Student.objects.get(user=request.user)
    rr = Reviews.objects.filter(student__id=request.user.id)

    return render(request, 'librarian/book_detail.html', locals())


# Add a Book
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'quantity', 'category']
    template_name = 'librarian/book_form.html'

    def form_valid(self, form):
        form.instance.lib_author = self.request.user.username
        return super().form_valid(form)

    # Update a Book


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'quantity']

    def form_valid(self, form):
        form.instance.lib_author = self.request.user.username
        return super().form_valid(form)


class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'


@login_required
def StudentCreate(request):
    if not request.user.is_superuser:
        return redirect('index')

    # form() = StudentForm()

    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            s = form.cleaned_data['roll_no']
            form.save()
            messages.success(request, f'Student has been added to the database')
            return redirect('index')
    else:

        form = StudentForm()

    return render(request, 'librarian/student_form.html', {'form': form})


@login_required
def StudentList(request):
    context = {
        'students': Student.objects.all()
    }
    return render(request, 'librarian/student_list.html', context)


@login_required
def StudentDetail(request, pk):
    student = get_object_or_404(Student, id=pk)
    bor = Borrower.objects.filter(student=student)
    return render(request, 'librarian/student_detail.html', locals())


@login_required
def StudentUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Student.objects.get(id=pk)
    form = StudentForm(instance=obj)
    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('student-list')
    return render(request, 'librarian/student_form.html', locals())


@login_required
def StudentDelete(request, pk):
    obj = get_object_or_404(Student, pk=pk)
    obj.delete()
    return render(request, 'librarian/student_confirm_delete.html', locals())


@login_required
def student_BookListView(request):
    student = Student.objects.get(user=request.user)
    bor = Borrower.objects.filter(student=student)
    bor_list = []
    for b in bor:
        bor_list.append(b)
    return render(request, 'librarian/book_list.html', locals())


@login_required
def student_request_issue(request, pk):
    obj = Book.objects.get(id=pk)
    stu = Student.objects.get(user=request.user)
    # s = get_object_or_404(Student, roll_no=str(request.user))
    if stu.total_books_due < 4:
        message = "book has been isuued, You can collect book from library"
        a = Borrower()
        a.student = stu
        a.book = obj
        a.issue_date = datetime.datetime.now()
        a.return_date = datetime.datetime.now() + datetime.timedelta(days=30)
        print(a.return_date)
        obj.quantity = obj.quantity - 1
        obj.save()
        stu.total_books_due = stu.total_books_due + 1
        stu.save()
        a.save()
    else:
        message = "you have exceeded limit."
    return render(request, 'librarian/result.html', locals())


@login_required
def ret(request, pk):
    if not request.user.is_superuser:
        return redirect('index')

    obj = Borrower.objects.get(id=pk)
    book_pk = obj.book.id
    student_pk = obj.student.id

    student = Student.objects.get(id=student_pk)
    student.total_books_due = student.total_books_due - 1
    student.save()

    book = Book.objects.get(id=book_pk)
    book.quantity = book.quantity + 1
    book.save()
    obj.delete()
    return redirect('student-list')


@login_required
def RatingUpdate(request, pk):
    # obj = Reviews.objects.get(id=pk)
    stu = Student.objects.get(user=request.user)
    book = Book.objects.get(id=pk)
    print(stu)
    form = RatingForm()
    if request.method == 'POST':
        form = RatingForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj = Reviews()
            obj.student = stu
            obj.book = book
            print(obj)
            obj.save()
            return redirect('book-detail', pk=obj.book.id)

    return render(request, 'librarian/form.html', locals())
