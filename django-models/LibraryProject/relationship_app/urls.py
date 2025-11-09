from django.urls import path
from .views import list_books, LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    # URL pattern for function-based view that lists all books
    path('books/', list_books, name='list_books'),
    
    # URL pattern for class-based view that shows library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]