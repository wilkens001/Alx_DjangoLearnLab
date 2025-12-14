My Django Social Media API - Progress Reflection

Name: wilkens001  
Date: December 14, 2025  
Repository: https://github.com/wilkens001/Alx_DjangoLearnLab  


What I've Built So Far

Getting Started - Repository Setup
First thing I did was set up my GitHub repo properly. Made sure it's public so anyone can check it out. I organized everything into folders that make sense and wrote a decent README explaining what the project does. I've been committing regularly (over 20 commits now) which has been helpful when I needed to go back and check what I changed.

Posts and Comments
This was the foundation of the API. Users can create posts with titles and content, and other users can comment on them. Pretty straightforward stuff, but getting it right took some time. I made sure only the person who wrote a post or comment can edit or delete it - seemed like common sense but needed custom permissions to enforce it.

I added search so you can find posts by keywords, and filtering by author. Also paginated everything so you don't get thousands of posts dumped on you at once. Wrote 13 tests to make sure everything works.

Follow System and Feed
This was more interesting. Users can follow each other (but not themselves - had to specifically prevent that). Once you follow people, you get a personalized feed showing only their posts. The feed shows newest posts first.

It's using Django's ManyToMany relationship which was new to me. Got 17 tests covering the follow/unfollow logic and the feed.

Likes and Notifications
Added a like button for posts. Made sure users can't like the same post twice (that would be weird). 

The notification system was probably the hardest part. I wanted notifications for different things - when someone follows you, likes your post, or comments on it. Used something called GenericForeignKey which lets one notification model handle different types of actions. Took me a while to wrap my head around it but it works well.

Users can mark notifications as read or mark everything as read at once. 20 tests for this feature.

Deployment Setup
Last task was getting everything ready for production. Set up environment variables so I'm not hardcoding passwords and secrets (learned that lesson). Added security headers, configured PostgreSQL for production (still using SQLite locally), and set up WhiteNoise to serve static files efficiently.

Wrote a bunch of guides because deployment can be confusing. Covered Heroku, VPS setups, and alternative platforms. Even wrote a guide for deploying without the Heroku CLI since I didn't have it installed.

The The Numbers
• 3 Django apps: accounts, posts, notifications
• 5 data models
• 15+ API endpoints
• 49 tests (all passing)
• About 5000 lines of code
• Way too much documentation (3000+ lines)


Challenges and How I Dealt With Them

Fighting with the Automated Checker
The automated checker was picky. Really picky. It wanted specific code patterns that weren't necessarily wrong, just different from what I wrote initially.

For example, I was checking if a like exists and then creating it separately. The checker wanted me to use `get_or_create()` instead. Fair enough - it's cleaner anyway. Also needed exact database field names in comments and specific URL patterns.

Basically learned to read the error messages super carefully and give the checker exactly what it wanted while keeping my code working.
Basically learned to read the error messages super carefully and give the checker exactly what it wanted while keeping my code working.

The GenericForeignKey Puzzleded notifications for different things - someone follows you, likes your post, comments, etc. But each notification points to a different type of thing (a User for follows, a Post for likes).

Normal foreign keys don't work for this. Had to learn about Django's ContentType framework and GenericForeignKey. It's basically a way to have one field that can point to any model. Took some reading and experimenting but I got it working.
Normal foreign keys don't work for this. Had to learn about Django's ContentType framework and GenericForeignKey. It's basically a way to have one field that can point to any model. Took some reading and experimenting but I got it working.

Deploying Without CLI Toolsidn't have their CLI installed. Instead of installing it, I just figured out how to do everything through their web dashboard. Actually wasn't that hard once I found the right buttons to click.

Also documented alternative deployment options (Render, Railway, etc.) since not everyone uses Heroku. Good learning experience in finding workarounds.
Also documented alternative deployment options (Render, Railway, etc.) since not everyone uses Heroku. Good learning experience in finding workarounds.

Keeping Tests Organizedy test file got messy fast. Tests were all over the place and some were basically duplicates.

Had to reorganize everything into separate test classes for each feature. Used setUp() to create test data once instead of repeating it everywhere. Added edge case tests like "what happens if someone tries to follow themselves" or "can you like the same post twice?"

Ended up with 49 tests that actually make sense and don't repeat each other.
Ended up with 49 tests that actually make sense and don't repeat each other.

Environment Variables and Securityet keys is obviously bad. I knew that but still had to figure out the right way to handle it.

Used python-decouple to manage environment variables. Created a .env.example file showing what variables you need, and made sure .env itself is in .gitignore so secrets don't get committed. Set up defaults for development so it works out of the box but can be configured for production.

SQLite vs PostgreSQL
SQLite is great for development but not for production. Needed to support both without changing my code.

Used dj-database-url which reads a DATABASE_URL and configures everything automatically. In development it uses SQLite by default. In production you just set the DATABASE_URL to your PostgreSQL connection and it works.

Static Files Headache
Django's development server serves static files fine, but that doesn't work in production. You need a separate web server or CDN or something.

WhiteNoise solved this cleanly. It's a Python package that handles static files efficiently in production without needing Nginx or S3 or anything complicated. Just install it, add it to middleware, run collectstatic, and you're good.


What's Next

This Week

Get it Live
Priority one is actually deploying this thing. All the config is ready, just need to push it to Heroku through the web dashboard. Set up the PostgreSQL database, run migrations, create a superuser, and test everything actually works in production.

**Make it Faster**
Once it's live, I want to optimize the database queries. Right now I'm probably making way more queries than necessary. Need to use `select_related()` and `prefetch_related()` properly. Also should add some database indexes on fields I'm querying a lot.

**Better Documentation**
The README is decent but could use interactive API docs. Looking at drf-spectacular or Swagger. Would be nice to have a page where you can actually try the endpoints instead of just reading about them.

Maybe create a Postman collection too so people can easily test the API.
Maybe create a Postman collection too so people can easily test the API.

Nice-to-Have Features
If I have time, there are some features that would be cool to add:
• Search for users by username
• Add tags or categories to posts
• Password reset via email
• Rate limiting so people can't spam the API
• Better profile pages

Next Few Weeks

More Featuresding real-time notifications with WebSockets. Also direct messaging would be cool. Maybe image uploads for posts and profiles.

**Frontend**
Eventually want to build a simple React frontend. Nothing fancy, just something that actually uses the API so I can see it working end-to-end.

**DevOps Stuff**
DevOps Stuff
Should set up automated testing with GitHub Actions. Every time I push code, it runs all the tests automatically. Also want to add error tracking with something like Sentry.

Things I Want to Learn
• Django Channels for real-time features
• Better caching strategies (maybe Redis)
• OAuth2 for third-party login
• Docker to make deployment easier
• GraphQL as an alternative to REST


Looking Back

What Worked
Breaking the project into smaller tasks helped a lot. Wasn't as overwhelming when I could focus on one feature at a time. Writing tests as I went caught bugs early - way easier to fix them immediately than later.

Regular git commits were clutch. When something broke, I could easily see what changed and roll back if needed.

### What Didn't
Regular git commits were clutch. When something broke, I could easily see what changed and roll back if needed.

What Didn't
Also wish I'd planned the data models better upfront. Had to make some changes later that would have been easier if I'd thought them through more carefully.

Testing is good but I could use more integration tests. Right now I'm mostly testing individual pieces, not the whole workflow together.

Testing is good but I could use more integration tests. Right now I'm mostly testing individual pieces, not the whole workflow together.

Key Takeawaysation is actually really good. Whenever I was stuck, usually found the answer there. Just had to actually read it instead of skimming.

Tests are annoying to write but absolutely worth it. Saved me so many times.

Don't be afraid to search for help. Spent hours on some problems that had simple solutions I found on Stack Overflow.

Nothing has to be perfect the first time. Better to get something working and improve it than to overthink every detail upfront.

### What I Learned

Got way more comfortable with Django's ORM and querysets. Understanding foreign keys, ManyToMany relationships, and when to use them.

Django REST Framework makes building APIs pretty straightforward once you understand serializers and viewsets.

Deployment isn't as scary as I thought. There's a lot of moving pieces but it's mostly just configuration.

Writing good tests is a skill. It's not just about coverage - tests need to actually test meaningful things.

---

## Bottom Line

Built a working social media API with all the basic features you'd expect. It's not Facebook but it does what it's supposed to do. Got users, posts, comments, likes, follows, notifications, and a personalized feed. Everything has tests and it's ready to deploy.

Ran into some issues but figured them out. Learned a ton about Django, REST APIs, and deployment. Still lots to improve and features to add, but I have a solid foundation to build on.

Next step is getting it live and seeing how it performs with real use. Then I can optimize and add features based on what actually matters.

---

**Repository**: https://github.com/wilkens001/Alx_DjangoLearnLab  
**Status**: Ready to deploy  
**Tests**: 49/49 passing
