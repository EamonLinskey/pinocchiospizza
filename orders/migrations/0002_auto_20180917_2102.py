# Generated by Django 2.0.3 on 2018-09-17 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='style',
            old_name='style',
            new_name='PriceList',
        ),
        migrations.AddField(
            model_name='style',
            name='name',
            field=models.CharField(default='pricelist', max_length=32),
            preserve_default=False,
        ),
    ]