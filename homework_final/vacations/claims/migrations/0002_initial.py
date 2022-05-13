# Generated by Django 3.2 on 2022-05-13 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('claims', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='agreed_with',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель'),
        ),
        migrations.AddField(
            model_name='claim',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник'),
        ),
    ]
