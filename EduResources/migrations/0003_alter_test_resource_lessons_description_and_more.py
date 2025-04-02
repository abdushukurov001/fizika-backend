# Generated by Django 5.1.7 on 2025-04-01 11:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EduResources', '0002_rename_quetion_test_question_alter_lessons_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EduResources.lessons'),
        ),
        migrations.AddField(
            model_name='lessons',
            name='description',
            field=models.TextField(default='No description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lessons',
            name='title',
            field=models.CharField(default='No description', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lessons',
            name='videoUrl',
            field=models.URLField(default='No description'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Resources',
        ),
    ]
