# 🧪 Pre-Demo Testing Guide

## Quick Test Before Recording Your Loom Video

This guide helps you verify all key features work BEFORE you start recording.

---

## 🚀 Setup Steps

### 1. Start the Development Server

```powershell
cd social_media_api
python manage.py runserver
```

**Expected:** Server starts on `http://127.0.0.1:8000/`

**If migration errors:** Run migrations first
```powershell
python manage.py makemigrations
python manage.py migrate
```

---

### 2. Create Test Users (via Django Shell)

```powershell
python manage.py shell
```

In the shell:
```python
from accounts.models import CustomUser

# Create User 1
user1 = CustomUser.objects.create_user(
    username='alice',
    email='alice@example.com',
    password='TestPass123!',
    bio='Software developer and Django enthusiast'
)

# Create User 2
user2 = CustomUser.objects.create_user(
    username='bob',
    email='bob@example.com',
    password='TestPass123!',
    bio='Tech blogger and content creator'
)

# Create User 3 (optional)
user3 = CustomUser.objects.create_user(
    username='charlie',
    email='charlie@example.com',
    password='TestPass123!',
    bio='Full-stack developer'
)

print("Test users created!")
exit()
```

**Alternative: Use Admin Panel**
```powershell
python manage.py createsuperuser
```
Then create users via `http://127.0.0.1:8000/admin/`

---

## 🧪 Feature Testing Sequence

### Test 1: User Registration ✅

**Endpoint:** `POST http://127.0.0.1:8000/api/register/`

**Request Body:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123!",
  "bio": "New user testing the API"
}
```

**Expected Response:** `201 Created`
```json
{
  "id": 4,
  "username": "testuser",
  "email": "test@example.com",
  "bio": "New user testing the API",
  "token": "abc123..."
}
```

✅ **Pass if:** User created, token returned
❌ **Fail if:** Error 400/500

---

### Test 2: User Login ✅

**Endpoint:** `POST http://127.0.0.1:8000/api/login/`

**Request Body:**
```json
{
  "username": "alice",
  "password": "TestPass123!"
}
```

**Expected Response:** `200 OK`
```json
{
  "token": "xyz789...",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com"
  }
}
```

**Save this token!** You'll need it for authenticated requests.

✅ **Pass if:** Token returned
❌ **Fail if:** Invalid credentials error

---

### Test 3: View Profile ✅

**Endpoint:** `GET http://127.0.0.1:8000/api/profile/`

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
```

**Expected Response:** `200 OK`
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "bio": "Software developer and Django enthusiast",
  "followers_count": 0,
  "following_count": 0
}
```

✅ **Pass if:** Profile data returned
❌ **Fail if:** 401 Unauthorized

---

### Test 4: Create Post ✅

**Endpoint:** `POST http://127.0.0.1:8000/api/posts/`

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "My First Post",
  "content": "This is an amazing social media API I built with Django!"
}
```

**Expected Response:** `201 Created`
```json
{
  "id": 1,
  "title": "My First Post",
  "content": "This is an amazing social media API I built with Django!",
  "author": {
    "id": 1,
    "username": "alice"
  },
  "created_at": "2026-01-03T...",
  "updated_at": "2026-01-03T..."
}
```

✅ **Pass if:** Post created with ID
❌ **Fail if:** 400/401 error

---

### Test 5: List Posts ✅

**Endpoint:** `GET http://127.0.0.1:8000/api/posts/`

**Headers:** None required (public endpoint)

**Expected Response:** `200 OK`
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "My First Post",
      "content": "This is an amazing social media API...",
      "author": {
        "id": 1,
        "username": "alice"
      }
    }
  ]
}
```

✅ **Pass if:** Posts list returned with pagination
❌ **Fail if:** Error or no results

---

### Test 6: Follow User ✅

**Endpoint:** `POST http://127.0.0.1:8000/api/follow/2/`

**Headers:**
```
Authorization: Token ALICE_TOKEN
```

**Expected Response:** `200 OK`
```json
{
  "message": "You are now following bob",
  "following": true
}
```

**Verify:** Get alice's profile - `following_count` should be 1

✅ **Pass if:** Follow successful
❌ **Fail if:** 404 or error

---

### Test 7: View Feed ✅

**Endpoint:** `GET http://127.0.0.1:8000/api/feed/`

**Headers:**
```
Authorization: Token ALICE_TOKEN
```

**Expected Response:** `200 OK`
```json
{
  "count": 0,
  "results": []
}
```

**Note:** Feed will be empty until bob creates a post

**Create post as bob, then retest:**
- Login as bob
- Create a post
- Get alice's feed again
- Should now show bob's post

✅ **Pass if:** Feed returns (even if empty)
❌ **Fail if:** 500 error

---

### Test 8: Like Post ✅

**Endpoint:** `POST http://127.0.0.1:8000/api/posts/1/like/`

**Headers:**
```
Authorization: Token BOB_TOKEN
```

**Expected Response:** `200 OK`
```json
{
  "message": "Post liked successfully",
  "likes_count": 1
}
```

✅ **Pass if:** Like registered, count increased
❌ **Fail if:** Error

---

### Test 9: Comment on Post ✅

**Endpoint:** `POST http://127.0.0.1:8000/api/posts/1/comments/`

**Headers:**
```
Authorization: Token BOB_TOKEN
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "Great post! Really helpful information."
}
```

**Expected Response:** `201 Created`
```json
{
  "id": 1,
  "content": "Great post! Really helpful information.",
  "author": {
    "id": 2,
    "username": "bob"
  },
  "post": 1,
  "created_at": "2026-01-03T..."
}
```

✅ **Pass if:** Comment created
❌ **Fail if:** 400/401 error

---

### Test 10: View Notifications ✅

**Endpoint:** `GET http://127.0.0.1:8000/api/notifications/`

**Headers:**
```
Authorization: Token ALICE_TOKEN
```

**Expected Response:** `200 OK`
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "type": "like",
      "message": "bob liked your post",
      "is_read": false,
      "created_at": "2026-01-03T..."
    },
    {
      "id": 2,
      "type": "comment",
      "message": "bob commented on your post",
      "is_read": false,
      "created_at": "2026-01-03T..."
    }
  ]
}
```

✅ **Pass if:** Notifications list returned
❌ **Fail if:** Error

---

## 🎯 Quick Test Checklist

Before recording your demo, verify:

- [ ] ✅ Server starts without errors
- [ ] ✅ User registration works
- [ ] ✅ User login returns token
- [ ] ✅ Profile endpoint works
- [ ] ✅ Can create posts
- [ ] ✅ Can list posts
- [ ] ✅ Can follow users
- [ ] ✅ Feed endpoint works (even if empty)
- [ ] ✅ Can like posts
- [ ] ✅ Can comment on posts
- [ ] ✅ Notifications are created

---

## 🛠️ Testing Tools

### Option 1: Postman (Recommended)
1. Download: https://www.postman.com/downloads/
2. Create new collection: "Social Media API"
3. Add all test requests
4. Save tokens in environment variables

### Option 2: Thunder Client (VS Code Extension)
1. Install extension in VS Code
2. Create requests in sidebar
3. Easy to use during demo

### Option 3: HTTPie (Command Line)
```powershell
pip install httpie

# Example: Login
http POST http://127.0.0.1:8000/api/login/ username=alice password=TestPass123!

# Example: Create post
http POST http://127.0.0.1:8000/api/posts/ "Authorization: Token YOUR_TOKEN" title="Test Post" content="Test content"
```

### Option 4: cURL
```powershell
# Login
curl -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -d "{\"username\":\"alice\",\"password\":\"TestPass123!\"}"

# Create post
curl -X POST http://127.0.0.1:8000/api/posts/ -H "Authorization: Token YOUR_TOKEN" -H "Content-Type: application/json" -d "{\"title\":\"Test\",\"content\":\"Test content\"}"
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'rest_framework'"
**Solution:**
```powershell
pip install -r requirements.txt
```

### Issue: Migration errors
**Solution:**
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Issue: 401 Unauthorized
**Solution:**
- Check token is correct
- Ensure token is in header: `Authorization: Token YOUR_TOKEN`
- Re-login to get fresh token

### Issue: 403 Forbidden
**Solution:**
- Check you're the author (for edit/delete)
- Verify permissions in views

### Issue: 404 Not Found
**Solution:**
- Check URL is correct
- Verify resource exists (post ID, user ID)

### Issue: Empty feed
**Solution:**
- This is normal if you haven't followed anyone
- Or if followed users have no posts
- Mention this in demo as expected behavior

---

## 📝 Sample Test Data Script

Create this file: `create_test_data.py`

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from accounts.models import CustomUser
from posts.models import Post, Comment

# Create users
alice = CustomUser.objects.create_user(
    username='alice',
    email='alice@example.com',
    password='TestPass123!',
    bio='Software developer'
)

bob = CustomUser.objects.create_user(
    username='bob',
    email='bob@example.com',
    password='TestPass123!',
    bio='Tech blogger'
)

# Alice follows Bob
alice.following.add(bob)

# Bob creates posts
post1 = Post.objects.create(
    author=bob,
    title='Django Best Practices',
    content='Here are my top 5 Django tips...'
)

post2 = Post.objects.create(
    author=bob,
    title='REST API Design',
    content='Building great APIs with DRF...'
)

# Alice creates a post
post3 = Post.objects.create(
    author=alice,
    title='My Django Journey',
    content='Just completed my social media API!'
)

# Alice comments on Bob's post
Comment.objects.create(
    post=post1,
    author=alice,
    content='Great tips! Thanks for sharing.'
)

# Bob likes Alice's post
post3.likes.add(bob)

print("✅ Test data created successfully!")
print(f"Users: {CustomUser.objects.count()}")
print(f"Posts: {Post.objects.count()}")
print(f"Comments: {Comment.objects.count()}")
```

**Run it:**
```powershell
python create_test_data.py
```

---

## ✅ Ready for Demo!

Once all tests pass, you're ready to:
1. ✅ Record your Loom video
2. ✅ Follow the LOOM_DEMO_SCRIPT.md
3. ✅ Show these working features
4. ✅ Submit with confidence!

**Good luck! 🚀**
