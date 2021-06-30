"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from librarian import views as lib_views
from users import views as users_views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django_filters.views import FilterView
from librarian.filters import BookFilter, StudentFilter
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', lib_views.about, name='about'),
    path('home/', lib_views.BookListView.as_view(), name='index'),
    path('book/<int:pk>/', lib_views.BookDetailView, name='book-detail'),
    # path('book/<int:pk>/',lib_views.BookDetailView, name='book-detail'),
    path('book/new/', lib_views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', lib_views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', lib_views.BookDeleteView.as_view(), name='book-delete'),
    url(r'^search/$', FilterView.as_view(filterset_class=BookFilter,
        template_name='librarian/search_book_list.html'), name='search_results'),
    
    url(r'^search_student/$', FilterView.as_view(filterset_class=StudentFilter,
        template_name='librarian/search_student_list.html'), name='search_student'),


    path('student/create/', lib_views.StudentCreate, name='student-create'),
    path('student/', lib_views.StudentList, name='student-list'),
    path('student/<int:pk>/', lib_views.StudentDetail, name='student-detail'),
    path('student<int:pk>/update/', lib_views.StudentUpdate, name='student-update'),
    path('student/<int:pk>/delete/', lib_views.StudentDelete, name='student-delete'),
    path('student/book_list', lib_views.student_BookListView, name='book-student'),
    path('book/<int:pk>/request_issue/', lib_views.student_request_issue, name='request-issue'),
    path('return/<int:pk>', lib_views.ret, name='ret'),

    path('rating/update/<int:pk>', lib_views.RatingUpdate, name='rating_update'),


    path('profile/', users_views.profile, name='profile'),

    path('register/', users_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
