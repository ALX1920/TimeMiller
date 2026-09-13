from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VisitCounter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("total", models.PositiveBigIntegerField(default=0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Contador de visitas",
                "verbose_name_plural": "Contador de visitas",
            },
        ),
        migrations.CreateModel(
            name="VisitLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("ip_hash", models.CharField(db_index=True, max_length=64)),
                ("date", models.DateField(db_index=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Registro de visita",
                "verbose_name_plural": "Registros de visitas",
            },
        ),
        migrations.AddConstraint(
            model_name="visitlog",
            constraint=models.UniqueConstraint(
                fields=("ip_hash", "date"), name="unique_visitor_per_day"
            ),
        ),
    ]
