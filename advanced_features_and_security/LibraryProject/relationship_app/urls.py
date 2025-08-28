from django.urls import path
from . import views
from .views import list_books #added to match checker
from django.contrib.auth import views as auth_views

urlpatterns = [
    # function-based view: List all books
    path('books/', views.list_books, name='list_books'),

    # class-based view: Detail of a specific library
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # authentication views
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # rbac URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),

    # book mngmt URLs
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]