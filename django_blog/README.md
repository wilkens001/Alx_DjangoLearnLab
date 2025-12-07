# Django Blog Application

A full-featured blog application built with Django 5.0+, featuring user authentication, blog post management, and a complete comment system.

## Features

### 🔐 User Authentication
- **User Registration:** Custom registration form with email field
- **Login/Logout:** Secure authentication system with PBKDF2 password hashing
- **Profile Management:** Users can update their username and email
- **CSRF Protection:** All forms protected against Cross-Site Request Forgery
- **Session Management:** Secure session handling with Django's authentication system

### 📝 Blog Post Management
- **Create Posts:** Authenticated users can create new blog posts
- **View Posts:** Public listing of all posts with pagination (10 per page)
- **Edit Posts:** Authors can update their own posts
- **Delete Posts:** Authors can delete their own posts with confirmation
- **Post Detail View:** Full post content with author information and timestamps
- **Permission System:** Only post authors can edit or delete their posts

### 💬 Comment System
- **View Comments:** All users can view comments on posts
- **Create Comments:** Authenticated users can comment on posts
- **Edit Comments:** Comment authors can edit their comments
- **Delete Comments:** Comment authors can delete their comments with confirmation
- **Inline Form:** Quick comment submission directly on post detail page
- **Comment Count:** Display number of comments on each post
- **Timestamps:** Automatic tracking of creation and update times

### 🏷️ Tagging System
- **Tag Posts:** Categorize posts with multiple tags
- **Tag Management:** Create and manage tags through post forms
- **Tag Cloud:** Browse all tags with post counts
- **Filter by Tag:** View all posts associated with a specific tag
- **Auto-creation:** New tags are automatically created when needed
- **Many-to-Many:** Flexible tag-post relationships

### 🔍 Search Functionality
- **Multi-field Search:** Search across titles, content, and tags
- **Case-Insensitive:** Search works regardless of capitalization
- **Q Objects:** Complex query support for advanced searches
- **Quick Search:** Header search bar available on all pages
- **Full Search Page:** Dedicated search interface with tips
- **Result Display:** Clear results with post excerpts and metadata

### 🎨 User Interface
- **Responsive Design:** Mobile-friendly layout that works on all devices
- **Modern Styling:** Clean, professional CSS with hover effects and transitions
- **Dynamic Navigation:** Navigation menu updates based on authentication status
- **Form Validation:** Client-side and server-side validation with helpful error messages
- **Alert Messages:** Success and error messages for user actions
- **Pagination:** Easy navigation through multiple pages of posts
- **Tag Badges:** Visual tag display with interactive elements
- **Search Integration:** Seamless search experience across the site

## Installation

1. Ensure Django is installed:
## Technology Stack

- **Framework:** Django 5.0+
- **Database:** SQLite3 (development)
- **Authentication:** Django's built-in authentication system
- **Views:** Class-based generic views (ListView, DetailView, CreateView, UpdateView, DeleteView)
- **Forms:** Django ModelForms with custom validation
- **Templates:** Django template engine with template inheritance
- **Styling:** Custom CSS with responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Navigate to project directory:**
   ```bash
   cd django_blog
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install django
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set username, email, and password.

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Main site: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Project Structure

```
django_blog/
├── blog/                           # Main blog application
│   ├── migrations/                 # Database migrations
│   ├── static/blog/css/           # CSS stylesheets
│   │   └── style.css              # Main stylesheet
│   ├── templates/blog/            # HTML templates
│   │   ├── base.html              # Base template
│   │   ├── home.html              # Homepage
│   │   ├── register.html          # Registration page
│   │   ├── login.html             # Login page
│   │   ├── profile.html           # User profile page
│   │   ├── post_list.html         # Blog posts listing
│   │   ├── post_detail.html       # Individual post view
│   │   ├── post_form.html         # Create/edit post form
│   │   ├── post_confirm_delete.html   # Post deletion confirmation
│   │   ├── comment_form.html      # Comment create/edit form
│   │   ├── comment_confirm_delete.html # Comment deletion confirmation
│   │   ├── search_results.html    # Search results page
│   │   ├── posts_by_tag.html      # Posts filtered by tag
│   │   └── tags_list.html         # All tags cloud
│   ├── admin.py                   # Admin configuration
│   ├── forms.py                   # Form definitions
│   ├── models.py                  # Database models (Post, Comment, Tag)
│   ├── urls.py                    # URL routing
│   └── views.py                   # View logic
├── django_blog/                   # Project settings
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Main URL configuration
│   └── wsgi.py                    # WSGI configuration
├── db.sqlite3                     # SQLite database
├── manage.py                      # Django management script
├── README.md                      # This file
├── COMMENT_SYSTEM_DOCUMENTATION.md # Detailed comment system docs
└── TAG_AND_SEARCH_DOCUMENTATION.md # Tagging and search features docs
```

## Database Models

### Tag Model
```python
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
```

### Post Model
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
```

### Comment Model
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## URL Routes

### Authentication
- `/` - Homepage with recent posts
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/profile/` - User profile management

### Blog Posts
- `/posts/` - List all blog posts
- `/post/<int:pk>/` - View individual post
- `/post/new/` - Create new post (requires login)
- `/post/<int:pk>/update/` - Edit post (requires ownership)
- `/post/<int:pk>/delete/` - Delete post (requires ownership)

### Comments
- `/post/<int:pk>/comments/new/` - Create comment (requires login)
- `/comment/<int:pk>/update/` - Edit comment (requires ownership)
- `/comment/<int:pk>/delete/` - Delete comment (requires ownership)

### Search and Tags
- `/search/` - Search posts by title, content, or tags
- `/tags/` - View all tags with post counts
- `/tags/<str:tag_name>/` - View posts filtered by specific tag

## Usage Guide

### For Visitors (Anonymous Users)
1. **View posts:** Browse all blog posts without logging in
2. **Read comments:** View all comments on posts
3. **Register:** Click "Register" to create an account
4. **Login:** Click "Login" to access full features

### For Registered Users
1. **Create posts:** Click "New Post" to write a blog post
2. **Add tags:** Enter comma-separated tags when creating posts
3. **Manage posts:** Edit or delete your own posts
4. **Add comments:** Comment on any post using the inline form
5. **Edit comments:** Update your comments anytime
6. **Delete comments:** Remove your comments with confirmation
7. **Search posts:** Use the search bar to find posts by keyword or tag
8. **Browse by tag:** Click any tag to view related posts
9. **Update profile:** Change your username and email in profile settings

### For Administrators
1. **Access admin panel:** Go to `/admin/` and login with superuser credentials
2. **Manage users:** Create, edit, or delete user accounts
3. **Manage tags:** View, edit, or merge tags
4. **Moderate content:** View, edit, or delete any posts or comments
5. **View analytics:** See post, comment, and tag statistics

## Form Validations

### Post Form
- **Title:** Required, minimum 5 characters
- **Content:** Required, minimum 20 characters
- **Tags:** Optional, comma-separated, 2-50 characters per tag

### Comment Form
- **Content:** Required, minimum 3 characters, maximum 1000 characters

### User Registration
- **Username:** Required, unique
- **Email:** Required, valid email format
- **Password:** Required, minimum 8 characters with complexity requirements
- **Password Confirmation:** Must match password

### Search Form
- **Query:** Optional, searches across titles, content, and tags

## Security Features

### Authentication Security
- Passwords hashed using PBKDF2 algorithm
- CSRF tokens on all forms
- Session-based authentication
- Login required decorators on protected views

### Permission System
- View-level permission checks
- Template-level permission rendering
- Author-only edit/delete permissions
- Database-level foreign key constraints

### Data Protection
- XSS prevention through template auto-escaping
- SQL injection prevention through Django ORM
- CSRF protection on all POST requests
- Secure password storage

## Documentation

For detailed information about specific features:
- [Comment System Documentation](COMMENT_SYSTEM_DOCUMENTATION.md) - Comprehensive guide to the comment system
- [Tag and Search Documentation](TAG_AND_SEARCH_DOCUMENTATION.md) - Complete guide to tagging and search features

## Troubleshooting

### Common Issues

**Issue:** `python: command not found`
- **Solution:** Use `python3` instead or add Python to PATH

**Issue:** Migration errors
- **Solution:** Delete `db.sqlite3` and all migration files except `__init__.py`, then run migrations again

**Issue:** Static files not loading
- **Solution:** Run `python manage.py collectstatic` and check `STATIC_URL` in settings

**Issue:** Admin CSS not loading
- **Solution:** Ensure `DEBUG = True` in development or properly configure static files for production

## Testing

### Manual Testing Checklist
- [ ] Register a new user account
- [ ] Login with credentials
- [ ] Create a new blog post
- [ ] View post detail page
- [ ] Edit your own post
- [ ] Delete your own post with confirmation
- [ ] Add a comment to a post
- [ ] Edit your comment
- [ ] Delete your comment
- [ ] Logout
- [ ] Try to create post without login (should redirect)
- [ ] View posts as anonymous user

## License

This project is developed as part of the ALX Django learning curriculum.

## Acknowledgments

- Django documentation and community
- ALX Africa for the project requirements
- Contributors and testers

---

**Built with ❤️ using Django**
