# Generated by Django 4.2.4 on 2023-09-12 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stable_ai', '0004_alter_snsmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snsmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]