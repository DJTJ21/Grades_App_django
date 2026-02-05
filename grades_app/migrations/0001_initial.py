# Generated migration file for grades_app models

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(blank=True, max_length=8, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('level', models.CharField(choices=[('L1', 'Licence 1'), ('L2', 'Licence 2'), ('L3', 'Licence 3'), ('M1', 'Master 1'), ('M2', 'Master 2')], max_length=2)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('coefficient', models.FloatField()),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='grades_app.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='grades_app.subject')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('student', 'subject', 'date')},
            },
        ),
    ]
