# Generated by Django 4.0.4 on 2022-05-07 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename__id_order_id_rename__id_orderitem_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='count',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]