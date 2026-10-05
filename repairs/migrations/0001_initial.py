# Generated manually to mirror the original RepairRequest schema.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0012_alter_user_first_name_max_length")]
    operations = [
        migrations.CreateModel(
            name="RepairRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("category", models.CharField(choices=[("Technology", "Technology / IT"), ("Furniture", "Furniture"), ("Electrical", "Electrical"), ("Plumbing", "Plumbing"), ("HVAC", "HVAC / Air Conditioning"), ("General", "General Building")], max_length=50)),
                ("location", models.CharField(max_length=255)),
                ("problem", models.TextField()),
                ("priority", models.CharField(choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")], max_length=20)),
                ("status", models.CharField(choices=[("Pending", "Pending"), ("In Progress", "In Progress"), ("Completed", "Completed"), ("Cancelled", "Cancelled")], default="Pending", max_length=30)),
                ("image", models.ImageField(blank=True, null=True, upload_to="repair_images/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("reporter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="repair_requests", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        )
    ]
