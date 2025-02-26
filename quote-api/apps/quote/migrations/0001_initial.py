# Generated by Django 5.1.6 on 2025-02-18 15:05

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('context', models.TextField(blank=True, default='', verbose_name='Text Content')),
                ('author', models.TextField(blank=True, default='', verbose_name='Author')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
