# Generated by Django 4.0.3 on 2022-09-27 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_comments_bids'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
