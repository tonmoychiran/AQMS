# Generated by Django 4.1 on 2022-08-16 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aqms', '0004_delete_hdivision'),
    ]

    operations = [
        migrations.CreateModel(
            name='ivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(max_length=200)),
            ],
        ),
    ]
