from django.db import migrations, models
import django.db.models.deletion


def seed_categories(apps, schema_editor):
    Category = apps.get_model("repairs", "Category")
    defaults = [
        ("Technology", "Computer, printer, Wi-Fi and other IT equipment"),
        ("Furniture", "Desks, chairs, cabinets and other furniture"),
        ("Electrical", "Lights, outlets, switches and electrical equipment"),
        ("Plumbing", "Pipes, faucets, drains and water fixtures"),
        ("HVAC", "Air-conditioning and ventilation concerns"),
        ("General", "General building and facility repairs"),
    ]
    for name, description in defaults:
        Category.objects.get_or_create(name=name, defaults={"description": description})


class Migration(migrations.Migration):
    dependencies = [("repairs", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.CharField(blank=True, max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"], "verbose_name_plural": "Categories"},
        ),
        migrations.CreateModel(
            name="Technician",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("specialization", models.CharField(max_length=150)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="RepairHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("old_status", models.CharField(blank=True, max_length=30)),
                ("new_status", models.CharField(max_length=30)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("changed_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="auth.user")),
                ("repair_request", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="history", to="repairs.repairrequest")),
                ("technician", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="history_entries", to="repairs.technician")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="repairrequest",
            name="assigned_technician",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="assigned_requests", to="repairs.technician"),
        ),
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
