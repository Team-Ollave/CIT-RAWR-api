# Generated by Django 3.1.3 on 2020-11-30 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0003_auto_20201130_0616"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reservation",
            options={
                "default_related_name": "reservations",
                "ordering": ("event_date", "start_time"),
            },
        ),
    ]
