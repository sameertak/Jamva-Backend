# Generated by Django 4.1.4 on 2022-12-21 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("userLogin", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="userModel",
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
                ("orders", models.CharField(max_length=20)),
                ("profile", models.ImageField(default="profile.png", upload_to="")),
                (
                    "name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="userLogin.phonemodel",
                    ),
                ),
            ],
        ),
    ]