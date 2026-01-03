# ALX Django Learning Lab - Capstone Project

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-blue.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-ALX-orange.svg)](https://www.alxafrica.com/)

## 👋 About Me

**Name:** [Your Name Here]

**Program:** ALX Backend Specialization - Django Track

**Capstone Project:** Social Media API

---

## 🎯 Capstone Project: Social Media API

### What Problem Does It Solve?

The Social Media API provides a complete, production-ready backend for building modern social media platforms. It solves the challenge of implementing complex social features like user authentication, content management, social interactions (likes, follows, comments), and real-time notifications in a scalable and secure way.

This API can be used as the foundation for:
- Social networking applications
- Community platforms
- Content sharing websites
- Professional networking sites
- Team collaboration tools

### 🚀 Key Features

#### 1. **User Authentication & Profiles**
- Token-based authentication (secure and stateless)
- User registration with validation
- Custom user profiles with bio and profile pictures
- Profile management (view and update)

#### 2. **Social Interactions**
- **Follow/Unfollow System:** Build your network by following users
- **Personalized Feed:** See posts from people you follow
- **User Discovery:** Find and connect with other users

#### 3. **Content Management**
- **Posts:** Create, read, update, and delete posts
- **Comments:** Engage with posts through comments
- **Rich Text Support:** Full content creation capabilities
- **Author Permissions:** Only authors can edit/delete their content

#### 4. **Engagement Features**
- **Like/Unlike:** Show appreciation for posts
- **Like Counts:** Track engagement metrics
- **Comment Threads:** Build discussions around posts

#### 5. **Notifications System**
- Real-time notifications for:
  - New followers
  - Post likes
  - Post comments
- Mark notifications as read/unread
- Notification history

#### 6. **Advanced API Features**
- **Pagination:** Efficient data loading (10 items per page)
- **Search:** Find posts by title or content
- **Filtering:** Filter posts by author
- **Ordering:** Sort results by date or relevance

### 📁 Project Structure

```
social_media_api/
├── accounts/              # User authentication and profiles
│   ├── models.py         # Custom User model with social features
│   ├── serializers.py    # User data serialization
│   ├── views.py          # Authentication endpoints
│   └── tests.py          # Comprehensive test suite
├── posts/                 # Posts and comments
│   ├── models.py         # Post and Comment models
│   ├── serializers.py    # Post/Comment serialization
│   ├── views.py          # CRUD operations
│   └── tests.py          # Post feature tests
├── notifications/         # Notification system
│   ├── models.py         # Notification model
│   ├── serializers.py    # Notification serialization
│   ├── views.py          # Notification endpoints
│   └── tests.py          # Notification tests
├── social_media_api/     # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL routing
│   └── wsgi.py           # Production server config
├── requirements.txt       # Python dependencies
├── manage.py             # Django management
└── README.md             # Detailed documentation
```

### 🛠️ Technology Stack

- **Framework:** Django 5.2
- **API:** Django REST Framework 3.14+
- **Database:** SQLite (development) / PostgreSQL (production-ready)
- **Authentication:** Token-based authentication
- **Python:** 3.13

### 📚 API Endpoints

#### Authentication
- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `GET /api/profile/` - View profile
- `PUT /api/profile/` - Update profile

#### Social Features
- `POST /api/follow/<user_id>/` - Follow a user
- `POST /api/unfollow/<user_id>/` - Unfollow a user
- `GET /api/feed/` - Personalized feed

#### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create a post
- `GET /api/posts/<id>/` - View post details
- `PUT /api/posts/<id>/` - Update post
- `DELETE /api/posts/<id>/` - Delete post

#### Comments
- `POST /api/posts/<id>/comments/` - Add comment
- `GET /api/comments/<id>/` - View comment
- `PUT /api/comments/<id>/` - Update comment
- `DELETE /api/comments/<id>/` - Delete comment

#### Likes
- `POST /api/posts/<id>/like/` - Like a post
- `POST /api/posts/<id>/unlike/` - Unlike a post

#### Notifications
- `GET /api/notifications/` - List notifications
- `PATCH /api/notifications/<id>/read/` - Mark as read

### 🎥 Demo Video

**Watch the full demo:** [Loom Video Link]

The demo showcases:
1. User registration and authentication
2. Creating and managing posts
3. Following users and viewing personalized feed
4. Liking and commenting on posts
5. Receiving and managing notifications

### 🚀 Quick Start

#### Prerequisites
- Python 3.13+
- pip (Python package manager)
- Virtual environment (recommended)

#### Installation

```bash
# Clone the repository
git clone https://github.com/wilkens001/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

#### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts
python manage.py test posts
python manage.py test notifications
```

### 📖 Documentation

For detailed API documentation, see:
- [Social Media API README](./social_media_api/README.md)
- [API Documentation](./social_media_api/API_DOCUMENTATION.md)
- [Posts API Documentation](./social_media_api/POSTS_API_DOCUMENTATION.md)
- [Follow & Feed Documentation](./social_media_api/FOLLOW_AND_FEED_DOCUMENTATION.md)
- [Likes & Notifications Documentation](./social_media_api/LIKES_AND_NOTIFICATIONS_DOCUMENTATION.md)

### 🧪 Testing & Quality

- ✅ Comprehensive test coverage for all features
- ✅ Unit tests for models, serializers, and views
- ✅ Integration tests for complex workflows
- ✅ Token authentication security
- ✅ Permission-based access control
- ✅ Input validation and error handling

### 🐛 Known Issues & Future Enhancements

#### Current Limitations
- File uploads use local storage (can be migrated to cloud storage)
- SQLite database (production-ready for PostgreSQL/MySQL)
- Basic notification system (can be enhanced with WebSockets)

#### Future Enhancements
- Real-time chat messaging
- Story/status updates
- Video post support
- Advanced search with filters
- Analytics dashboard
- Email notifications
- Mobile app integration

### 🎓 Learning Outcomes

Through this project, I gained hands-on experience with:
- Building RESTful APIs with Django REST Framework
- Implementing token-based authentication
- Designing complex database relationships
- Writing comprehensive tests
- Creating user-friendly API documentation
- Managing project requirements and dependencies
- Git version control and GitHub workflows

---

## 📂 Additional Projects (Weekly Tasks)

This repository also contains weekly learning projects:

### 1. Introduction to Django
Basic Django setup and Library Project foundation

### 2. Django Models
Working with Django ORM and database models

### 3. Advanced API Project
Learning advanced DRF features (filtering, searching, ordering)

### 4. Django Blog
Full-featured blog with authentication and comments

### 5. Advanced Features & Security
Security best practices and advanced Django features

---

## 🤝 Contributing

This is a capstone project for ALX. While it's not open for contributions, feel free to:
- Fork the repository for your own learning
- Open issues if you find bugs
- Use it as a reference for your projects

## 📝 License

This project was created as part of the ALX Backend Specialization program.

## 🙏 Acknowledgments

- **ALX Africa** for the comprehensive Django curriculum
- **Django & DRF Communities** for excellent documentation
- **Fellow Learners** for peer support and collaboration

---

## 📧 Contact

**GitHub:** [@wilkens001](https://github.com/wilkens001)

**Project Link:** [https://github.com/wilkens001/Alx_DjangoLearnLab](https://github.com/wilkens001/Alx_DjangoLearnLab)

---

**Built with ❤️ during ALX Backend Specialization - December 2025 to January 2026**
