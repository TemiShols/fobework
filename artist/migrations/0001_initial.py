# Generated by Django 4.2 on 2025-04-01 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('name', models.CharField(max_length=255)),
                ('genres', models.JSONField(default=list)),
                ('social_media', models.JSONField(default=dict)),
                ('base_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('requirements', models.TextField(blank=True)),
                ('portfolio_links', models.JSONField(default=list)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
