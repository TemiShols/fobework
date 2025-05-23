# Generated by Django 4.2 on 2025-04-01 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('venue', '0001_initial'),
        ('artist', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_time', models.DateTimeField()),
                ('duration', models.PositiveIntegerField(help_text='Duration in minutes')),
                ('ticket_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_tickets', models.PositiveIntegerField()),
                ('available_tickets', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='draft', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='artist.artist')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='venue.venue')),
            ],
        ),
    ]
