# Generated by Django 5.0.3 on 2024-03-27 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0002_alter_message_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='product',
        ),
    ]