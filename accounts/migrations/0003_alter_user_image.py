# Generated by Django 4.1.7 on 2023-06-12 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='media/static/images/default.png', upload_to='media/static/images/'),
        ),
    ]