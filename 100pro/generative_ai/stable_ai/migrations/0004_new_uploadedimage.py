# Generated by Django 4.2.4 on 2023-09-17 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stable_ai', '0003_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='new_UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploaded_images/')),
            ],
        ),
    ]
