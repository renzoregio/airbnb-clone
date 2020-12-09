# Generated by Django 2.2.5 on 2020-11-17 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201117_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_method',
            field=models.CharField(choices=[('email', 'Email'), ('github', 'Github'), ('kakao', 'KakaoTalk')], default='email', max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_key',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
    ]
