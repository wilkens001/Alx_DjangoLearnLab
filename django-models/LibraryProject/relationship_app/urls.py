from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # URL pattern for function-based view that lists all books
    path('books/', views.list_books, name='list_books'),
    
    # URL pattern for class-based view that shows library details
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]