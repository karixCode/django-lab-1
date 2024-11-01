# Generated by Django 5.1.1 on 2024-10-21 20:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_votes',
        ),
        migrations.AddField(
            model_name='question',
            name='voted_by',
            field=models.ManyToManyField(blank=True, related_name='voted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='votes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.CharField(max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='short_description',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
