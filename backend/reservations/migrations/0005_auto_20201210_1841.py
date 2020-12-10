# Generated by Django 3.1.3 on 2020-12-10 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0004_auto_20201201_0305"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reservation",
            options={
                "default_related_name": "reservations",
                "ordering": (
                    "room__building__name",
                    "room__name",
                    "event_date",
                    "start_time",
                ),
            },
        ),
    ]