# Generated by Django 2.0.3 on 2018-05-14 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20180511_0342'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'), ('catalog.can_see_borrowed', 'Can see borrowed'))},
        ),
    ]
