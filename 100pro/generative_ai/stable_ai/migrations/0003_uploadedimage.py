# Generated by Django 4.2.4 on 2023-09-17 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stable_ai', '0002_rename_uploadedimage_re_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploaded_images/')),
            ],
        ),
    ]