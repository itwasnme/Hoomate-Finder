# Generated by Django 3.1.5 on 2021-04-09 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210409_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=18),
        ),
        migrations.AlterField(
            model_name='profile',
            name='budget_lower',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='budget_upper',
            field=models.IntegerField(default=800),
        ),
        migrations.AlterField(
            model_name='profile',
            name='car',
            field=models.CharField(choices=[('Have a car', 'Have a car'), ('Do not have a car', 'Do not have a car')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other/Prefer not to say', 'Other/Prefer not to say')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='grad_year',
            field=models.IntegerField(default=2021),
        ),
        migrations.AlterField(
            model_name='profile',
            name='personality',
            field=models.CharField(choices=[('Introvert', 'Introvert'), ('Extrovert', 'Extrovert')], default='', max_length=100),
        ),
    ]
