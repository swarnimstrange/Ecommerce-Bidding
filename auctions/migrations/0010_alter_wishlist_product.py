# Generated by Django 4.0.3 on 2022-09-28 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_remove_wishlist_product_wishlist_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='auctions.listing'),
        ),
    ]
