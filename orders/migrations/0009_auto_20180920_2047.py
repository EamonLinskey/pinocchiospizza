# Generated by Django 2.0.3 on 2018-09-20 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20180920_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='legalExtras',
            field=models.ManyToManyField(to='orders.Extra'),
        ),
    ]
