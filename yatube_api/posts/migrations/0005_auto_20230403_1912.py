# Generated by Django 3.2.16 on 2023-04-03 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20230403_1856'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_author_following',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'following'), name='unique_user_following'),
        ),
    ]
