# Generated by Django 2.2.3 on 2019-07-25 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='auth_user_token', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
            },
        ),
    ]
