from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .views import list_books, LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', CreateView.as_view(
        template_name='relationship_app/register.html',
        form_class=UserCreationForm,
        success_url='/relationship_app/books/'
    ), name='register'),

    # Book and Library URLs
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]