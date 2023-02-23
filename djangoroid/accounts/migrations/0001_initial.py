# Generated by Django 4.1.7 on 2023-02-23 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("user_id", models.CharField(max_length=50)),
                ("password", models.CharField(max_length=20)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
