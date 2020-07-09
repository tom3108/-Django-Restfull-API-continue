# Generated by Django 3.0.7 on 2020-07-02 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200702_1934'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actor',
            old_name='movie',
            new_name='movies',
        ),
        migrations.AlterField(
            model_name='extrainfo',
            name='kind',
            field=models.IntegerField(choices=[(3, 'drama'), (1, 'horror'), (0, 'unknown'), (2, 'comedy')], default=0),
        ),
    ]