# Permissions and Groups Setup Guide

## Overview

This document explains how permissions and groups are configured and used in the Django application to control access to various parts of the bookshelf app.

## Custom Permissions

Custom permissions have been added to the `Book` model in `bookshelf/models.py`:

- **can_view**: Allows users to view book details and lists
- **can_create**: Allows users to create new books
- **can_edit**: Allows users to edit existing books
- **can_delete**: Allows users to delete books

These permissions are defined in the `Book` model's Meta class:

```python
class Meta:
    permissions = [
        ("can_view", "Can view book"),
        ("can_create", "Can create book"),
        ("can_edit", "Can edit book"),
        ("can_delete", "Can delete book"),
    ]
```

## User Groups

Three user groups have been configured with different permission levels:

### 1. Viewers
- **Permissions**: `can_view`
- **Access Level**: Read-only access to books
- **Use Case**: Users who should only be able to browse and view book information

### 2. Editors
- **Permissions**: `can_view`, `can_create`, `can_edit`
- **Access Level**: Can view, create, and modify books (but not delete)
- **Use Case**: Content creators and moderators who manage book entries

### 3. Admins
- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Access Level**: Full access to all book operations
- **Use Case**: Administrators with complete control over book management

## Setup Instructions

### Step 1: Apply Migrations

After adding custom permissions to the model, create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Set Up Groups and Permissions

Run the custom management command to automatically create groups and assign permissions:

```bash
python manage.py setup_groups
```

This command will:
- Create the three groups (Viewers, Editors, Admins)
- Assign appropriate permissions to each group
- Display confirmation messages for each action

### Step 3: Assign Users to Groups

You can assign users to groups in two ways:

#### Option A: Using Django Admin Interface

1. Log in to Django admin at `/admin/`
2. Navigate to **Authentication and Authorization > Users**
3. Select a user to edit
4. In the **Permissions** section, scroll to **Groups**
5. Select one or more groups from the "Available groups" list
6. Click the arrow to move them to "Chosen groups"
7. Save the user

#### Option B: Using Django Shell

```python
python manage.py shell

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Get or create a user
user = User.objects.get(username='username')

# Get the group
viewers_group = Group.objects.get(name='Viewers')

# Add user to group
user.groups.add(viewers_group)
```

## Permission-Protected Views

The following views in `bookshelf/views.py` are protected by permissions:

### book_list (View all books)
- **Required Permission**: `bookshelf.can_view`
- **Decorator**: `@permission_required('bookshelf.can_view', raise_exception=True)`
- **Description**: Lists all books in the database

### book_detail (View specific book)
- **Required Permission**: `bookshelf.can_view`
- **Decorator**: `@permission_required('bookshelf.can_view', raise_exception=True)`
- **Description**: Displays details of a specific book

### book_create (Create new book)
- **Required Permission**: `bookshelf.can_create`
- **Decorator**: `@permission_required('bookshelf.can_create', raise_exception=True)`
- **Description**: Form to create a new book entry

### book_edit (Edit existing book)
- **Required Permission**: `bookshelf.can_edit`
- **Decorator**: `@permission_required('bookshelf.can_edit', raise_exception=True)`
- **Description**: Form to edit an existing book

### book_delete (Delete book)
- **Required Permission**: `bookshelf.can_delete`
- **Decorator**: `@permission_required('bookshelf.can_delete', raise_exception=True)`
- **Description**: Confirmation page and deletion of a book

## Testing Permissions

### Manual Testing Approach

1. **Create Test Users**:
   ```bash
   python manage.py createsuperuser  # For admin access
   python manage.py shell
   ```
   
   In the shell:
   ```python
   from django.contrib.auth import get_user_model
   User = get_user_model()
   
   # Create test users
   viewer_user = User.objects.create_user('viewer_test', password='testpass123')
   editor_user = User.objects.create_user('editor_test', password='testpass123')
   admin_user = User.objects.create_user('admin_test', password='testpass123')
   ```

2. **Assign Users to Groups**:
   ```python
   from django.contrib.auth.models import Group
   
   viewers = Group.objects.get(name='Viewers')
   editors = Group.objects.get(name='Editors')
   admins = Group.objects.get(name='Admins')
   
   viewer_user.groups.add(viewers)
   editor_user.groups.add(editors)
   admin_user.groups.add(admins)
   ```

3. **Test Access Levels**:
   - Log in as `viewer_test`: Should be able to view books only
   - Log in as `editor_test`: Should be able to view, create, and edit books
   - Log in as `admin_test`: Should have full access to all operations
   - Try accessing restricted views to verify 403 Forbidden errors

### Expected Behavior

| User Group | View Books | Create Books | Edit Books | Delete Books |
|------------|------------|--------------|------------|--------------|
| Viewers    | ✓          | ✗            | ✗          | ✗            |
| Editors    | ✓          | ✓            | ✓          | ✗            |
| Admins     | ✓          | ✓            | ✓          | ✓            |

## Security Features

- **raise_exception=True**: When a user lacks permission, they receive a 403 Forbidden error instead of being redirected to login
- **Permission Checks**: All CRUD operations are protected at the view level
- **Group-Based Access**: Permissions are managed through groups for easier administration
- **Granular Control**: Each operation (view, create, edit, delete) has its own permission

## Troubleshooting

### Permission Not Found Error
If you get an error that a permission doesn't exist:
1. Ensure migrations have been applied: `python manage.py migrate`
2. Check that the permission is defined in the model's Meta class
3. Verify the permission codename matches exactly (e.g., `can_view`, not `can_view_book`)

### User Can't Access View Despite Being in Group
1. Verify the user is actually in the group: Check in Django admin
2. Ensure the group has the required permission assigned
3. Try logging out and logging back in
4. Check that `raise_exception=True` is set in the decorator

### Groups Not Created
Run the setup command: `python manage.py setup_groups`

## File Structure

```
bookshelf/
├── models.py                    # Contains Book model with custom permissions
├── views.py                     # Contains permission-protected views
├── admin.py                     # Admin configuration
├── management/
│   └── commands/
│       └── setup_groups.py      # Management command to create groups
└── ...
```

## Additional Resources

- [Django Permissions Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization)
- [Django Groups Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#groups)
- [Permission Required Decorator](https://docs.djangoproject.com/en/stable/topics/auth/default/#the-permission-required-decorator)
