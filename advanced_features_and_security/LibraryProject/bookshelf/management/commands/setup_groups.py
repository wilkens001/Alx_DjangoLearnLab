"""
Django management command to set up user groups and permissions.

This command creates three groups (Viewers, Editors, Admins) and assigns
appropriate permissions to each group based on their role.

Usage:
    python manage.py setup_groups

Groups created:
- Viewers: Can only view books
- Editors: Can view, create, and edit books
- Admins: Can view, create, edit, and delete books
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Set up user groups with appropriate permissions for the bookshelf app'

    def handle(self, *args, **kwargs):
        """
        Main command handler that creates groups and assigns permissions.
        """
        self.stdout.write(self.style.MIGRATE_HEADING('Setting up groups and permissions...'))
        
        # Get the content type for the Book model
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get all custom permissions for the Book model
        can_view = Permission.objects.get(
            codename='can_view',
            content_type=book_content_type
        )
        can_create = Permission.objects.get(
            codename='can_create',
            content_type=book_content_type
        )
        can_edit = Permission.objects.get(
            codename='can_edit',
            content_type=book_content_type
        )
        can_delete = Permission.objects.get(
            codename='can_delete',
            content_type=book_content_type
        )
        
        # Create Viewers group
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created "Viewers" group'))
        else:
            self.stdout.write(self.style.WARNING('→ "Viewers" group already exists'))
        
        # Assign permissions to Viewers (can only view)
        viewers_group.permissions.clear()
        viewers_group.permissions.add(can_view)
        self.stdout.write(self.style.SUCCESS('  Assigned permissions: can_view'))
        
        # Create Editors group
        editors_group, created = Group.objects.get_or_create(name='Editors')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created "Editors" group'))
        else:
            self.stdout.write(self.style.WARNING('→ "Editors" group already exists'))
        
        # Assign permissions to Editors (can view, create, and edit)
        editors_group.permissions.clear()
        editors_group.permissions.add(can_view, can_create, can_edit)
        self.stdout.write(self.style.SUCCESS('  Assigned permissions: can_view, can_create, can_edit'))
        
        # Create Admins group
        admins_group, created = Group.objects.get_or_create(name='Admins')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created "Admins" group'))
        else:
            self.stdout.write(self.style.WARNING('→ "Admins" group already exists'))
        
        # Assign permissions to Admins (all permissions)
        admins_group.permissions.clear()
        admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
        self.stdout.write(self.style.SUCCESS('  Assigned permissions: can_view, can_create, can_edit, can_delete'))
        
        self.stdout.write(self.style.MIGRATE_HEADING('\nGroups setup completed successfully!'))
        self.stdout.write(self.style.SUCCESS('\nYou can now assign users to these groups via Django admin.'))
