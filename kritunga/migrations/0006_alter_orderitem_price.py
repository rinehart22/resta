# Generated by Django 4.0.1 on 2022-05-05 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kritunga', '0005_orderitem_user_alter_orderitem_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]