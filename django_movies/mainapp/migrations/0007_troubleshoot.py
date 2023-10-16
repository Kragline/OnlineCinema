# Generated by Django 4.2.5 on 2023-10-16 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0006_alter_movie_saga'),
    ]

    operations = [
        migrations.CreateModel(
            name='Troubleshoot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='troubleshoots', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
