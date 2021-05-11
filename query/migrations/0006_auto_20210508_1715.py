# Generated by Django 3.2.1 on 2021-05-08 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('query', '0005_auto_20210507_0614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='report',
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('times_rated', models.IntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='query.posts')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]