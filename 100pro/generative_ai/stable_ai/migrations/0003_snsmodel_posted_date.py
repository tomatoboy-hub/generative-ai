# Generated by Django 4.2.4 on 2023-09-12 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stable_ai', '0002_remove_snsmodel_content_remove_snsmodel_readtext_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='snsmodel',
            name='posted_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]