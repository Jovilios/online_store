# Generated by Django 5.0.3 on 2024-03-31 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0007_alter_message_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
