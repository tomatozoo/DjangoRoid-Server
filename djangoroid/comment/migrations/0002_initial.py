# Generated by Django 4.1.7 on 2023-02-24 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("comment", "0001_initial"),
        ("note", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="note",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="note.note"
            ),
        ),
    ]
