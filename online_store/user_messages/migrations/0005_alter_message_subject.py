# Generated by Django 5.0.3 on 2024-03-27 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0004_alter_message_body_alter_message_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
