# Generated migration for transitioning from custom Tag model to django-taggit

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_tag_post_tags'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        # First, remove the old many-to-many relationship
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        # Delete the old Tag model
        migrations.DeleteModel(
            name='Tag',
        ),
        # Add the new TaggableManager field
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(
                help_text='A comma-separated list of tags.',
                through='taggit.TaggedItem',
                to='taggit.Tag',
                verbose_name='Tags'
            ),
        ),
    ]
