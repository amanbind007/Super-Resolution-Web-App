# Generated by Django 4.0.4 on 2022-04-30 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_security_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='security_code',
            field=models.CharField(default='858382', max_length=6),
        ),
    ]
