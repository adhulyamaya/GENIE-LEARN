# Generated by Django 4.2 on 2025-05-04 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0003_lesson_is_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='completed_lessons',
            field=models.ManyToManyField(blank=True, to='courses_app.lesson'),
        ),
    ]
