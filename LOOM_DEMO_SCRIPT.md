# 🎥 Loom Demo Recording Script Guide

## ⏱️ Time Budget: 5 Minutes Maximum

**Recommended breakdown:**
- Introduction: 30 seconds
- Project Overview: 45 seconds
- Live Demo: 3 minutes
- Conclusion: 45 seconds

---

## 📝 Script Template

### 1. Introduction (30 seconds)

**Script:**
```
"Hi! My name is [YOUR NAME], and I'm excited to show you my capstone project 
for the ALX Backend Specialization program. 

Over the past 5 weeks, I've been building a comprehensive Social Media API 
from scratch using Django and Django REST Framework. 

Let me show you what I've created."
```

**What to show:**
- Your face/screen (you can choose)
- GitHub repository homepage (optional)

---

### 2. Project Overview (45 seconds)

**Script:**
```
"This Social Media API solves the problem of building complex social features 
for modern applications. It provides a complete backend that includes:

- User authentication and custom profiles
- A follow/unfollow system to build your network
- Posts and comments for content sharing
- A like system for engagement
- Real-time notifications
- And a personalized feed that shows posts from people you follow

The entire API is built with Django 5.2 and Django REST Framework, 
uses token-based authentication for security, and includes comprehensive 
tests for all features."
```

**What to show:**
- Briefly flash the project structure in VS Code
- Show the main features list in README

---

### 3. Live Demo (3 minutes) - THE MOST IMPORTANT PART

**Important: Have these ready BEFORE recording:**
- Development server running (`python manage.py runserver`)
- Postman/Thunder Client/Browser with saved requests
- At least 2 test users already created
- Sample data (posts, comments) in database

#### Demo Sequence:

**A. User Registration & Authentication (30 seconds)**

**Script:**
```
"Let me start by creating a new user account through the registration endpoint."
```

**Actions:**
- Show POST request to `/api/register/`
- Display request body with username, email, password
- Show successful response with user data and token
- **Brief comment:** "Notice we get back an authentication token immediately"

---

**B. User Profile & Following (30 seconds)**

**Script:**
```
"Now I'll log in as a different user and follow someone."
```

**Actions:**
- Show POST to `/api/login/` (or use existing token)
- Make POST request to `/api/follow/{user_id}/`
- Show successful response
- **Brief comment:** "The follow system is what makes the feed personalized"

---

**C. Creating Content - Posts (30 seconds)**

**Script:**
```
"Let's create a post."
```

**Actions:**
- Show POST to `/api/posts/`
- Request body: `{"title": "My First Post", "content": "This is awesome!"}`
- Show successful creation response
- **Optional:** Quickly show GET `/api/posts/` to see it in the list

---

**D. Engagement - Comments & Likes (40 seconds)**

**Script:**
```
"Other users can engage with posts through comments and likes."
```

**Actions:**
- Show POST to `/api/posts/{id}/like/`
- Show the like count increase
- Show POST to `/api/posts/{id}/comments/`
- Request body: `{"content": "Great post!"}`
- Show comment was created successfully

---

**E. Notifications (20 seconds)**

**Script:**
```
"The notification system automatically tracks these interactions."
```

**Actions:**
- Show GET to `/api/notifications/`
- Point out different notification types (follow, like, comment)
- Show unread count

---

**F. Personalized Feed (30 seconds)**

**Script:**
```
"Here's where it all comes together - the personalized feed."
```

**Actions:**
- Show GET to `/api/feed/`
- Explain: "This shows only posts from users I follow"
- Show pagination working (`?page=2`)
- **Optional bug moment:** "And yes, there might be some edge cases with empty feeds - that's part of the learning process!"

---

### 4. Conclusion (45 seconds)

**Script:**
```
"To wrap up, this project demonstrates:
- [Count on fingers] RESTful API design
- User authentication and authorization
- Complex database relationships with Django ORM
- And real-world social media features

While there are some features I'd still like to add - like real-time chat 
and better file handling - I'm really proud of what I've built in 5 weeks.

All the code is available on my GitHub, and I've included comprehensive 
documentation and tests. Thanks for watching!"
```

**What to show:**
- Quick scroll through the README
- Flash the test results (`python manage.py test` output)
- End on GitHub repository page

---

## 🎯 Demo Preparation Checklist

### Before Recording:

- [ ] **Start Django server:** `python manage.py runserver`
- [ ] **Create test users:** At least User A and User B
- [ ] **Prepare API client:** Postman/Thunder Client/HTTPie
- [ ] **Create saved requests:** All demo endpoints ready to go
- [ ] **Add sample data:** 2-3 posts, comments, likes
- [ ] **Test all endpoints:** Make sure everything works
- [ ] **Clear terminal:** Clean, professional appearance
- [ ] **Close unnecessary tabs/windows:** Focus on demo
- [ ] **Check audio:** Test microphone before recording
- [ ] **Practice once:** Do a dry run (don't need to record)

### API Requests to Prepare:

**Collection 1: Authentication**
```json
POST /api/register/
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123!"
}

POST /api/login/
{
  "username": "testuser",
  "password": "SecurePass123!"
}
```

**Collection 2: Social Features**
```json
POST /api/follow/2/
Headers: Authorization: Token YOUR_TOKEN

GET /api/feed/
Headers: Authorization: Token YOUR_TOKEN
```

**Collection 3: Posts**
```json
POST /api/posts/
Headers: Authorization: Token YOUR_TOKEN
{
  "title": "Amazing Django Features",
  "content": "Just learned how to build a social media API!"
}

GET /api/posts/
```

**Collection 4: Engagement**
```json
POST /api/posts/1/like/
Headers: Authorization: Token YOUR_TOKEN

POST /api/posts/1/comments/
Headers: Authorization: Token YOUR_TOKEN
{
  "content": "This is such a great post!"
}
```

**Collection 5: Notifications**
```json
GET /api/notifications/
Headers: Authorization: Token YOUR_TOKEN
```

---

## 🎬 Recording Tips

### Technical Setup:
1. **Use Loom Chrome Extension or Desktop App**
2. **Recording Mode:** Screen + Camera (or Screen only if you prefer)
3. **Resolution:** 1080p recommended
4. **Frame Rate:** 30fps is fine

### Presentation Tips:
1. **Speak Clearly:** Not too fast, not too slow
2. **Be Enthusiastic:** Show your passion for what you built
3. **Don't Read:** Use the script as a guide, not a word-for-word reading
4. **Handle Bugs Gracefully:** If something doesn't work, acknowledge it briefly
5. **Keep Moving:** Don't spend too long on one feature
6. **Watch the Time:** Practice to stay under 5 minutes

### What to Emphasize:
- ✅ **Working features** - show them in action
- ✅ **The problem you solved** - why this matters
- ✅ **Your learning journey** - what you built in 5 weeks
- ✅ **Technical skills** - Django, DRF, authentication, etc.

### What to Avoid:
- ❌ **Don't show code** - reviewers will check GitHub
- ❌ **Don't explain code** - focus on functionality
- ❌ **Don't apologize excessively** - bugs are normal
- ❌ **Don't rush** - speak at a natural pace
- ❌ **Don't go overtime** - 5 minutes maximum

---

## 🐛 Handling Bugs During Demo

**If something doesn't work:**

**Option 1: Acknowledge Briefly**
```
"Ah, looks like there's an edge case with empty results - 
that's on my list to fix. Let me move to the next feature..."
```

**Option 2: Skip Gracefully**
```
"This feature is still being refined, but I can show you 
the notification system which works great..."
```

**Option 3: Use Backup**
```
"Let me show you this with a different endpoint that 
demonstrates the same principle..."
```

**Remember:** The instructions say "Don't be scared to show bugs if they're still there — bugs are a normal part of building websites."

---

## ✅ Post-Recording Checklist

After recording your Loom video:

- [ ] **Watch it back:** Make sure audio and video are clear
- [ ] **Check length:** Under 5 minutes
- [ ] **Verify sharing settings:** Link is accessible
- [ ] **Test the link:** Open in incognito to ensure it works
- [ ] **Copy the link:** Have it ready for submission

---

## 📋 Quick Reference: Endpoint Summary

| Feature | Method | Endpoint | Auth Required |
|---------|--------|----------|---------------|
| Register | POST | `/api/register/` | No |
| Login | POST | `/api/login/` | No |
| Profile | GET | `/api/profile/` | Yes |
| Follow | POST | `/api/follow/<id>/` | Yes |
| Feed | GET | `/api/feed/` | Yes |
| List Posts | GET | `/api/posts/` | No |
| Create Post | POST | `/api/posts/` | Yes |
| Like Post | POST | `/api/posts/<id>/like/` | Yes |
| Comment | POST | `/api/posts/<id>/comments/` | Yes |
| Notifications | GET | `/api/notifications/` | Yes |

---

## 🎯 Example Opening Lines

Choose one that fits your personality:

**Confident:**
```
"Hi, I'm [Name], and I just spent 5 weeks building a production-ready 
social media API. Let me show you what it can do."
```

**Humble:**
```
"Hi, I'm [Name]. This is my first major Django project, and I'm excited 
to share what I learned while building a social media API."
```

**Enthusiastic:**
```
"Hey everyone! I'm [Name], and I'm so excited to show you the social media 
API I built from scratch. This has been an amazing learning journey!"
```

**Professional:**
```
"Hello, my name is [Name], and today I'll be demonstrating my capstone project: 
a comprehensive Social Media API built with Django and Django REST Framework."
```

---

## 🚀 You've Got This!

**Remember:**
- You built this from scratch in 5 weeks - that's impressive!
- The goal is to show what works, not perfection
- Reviewers want to see your learning and passion
- 5 minutes goes by quickly - practice helps
- Be yourself and have fun with it!

**Good luck with your recording! 🎬**
