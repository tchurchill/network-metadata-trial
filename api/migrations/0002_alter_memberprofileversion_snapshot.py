# Generated by Django 4.1 on 2022-11-01 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="memberprofileversion",
            name="snapshot",
            field=models.JSONField(max_length=1024),
        ),
    ]
