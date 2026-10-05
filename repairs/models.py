from django.contrib.auth.models import User
from django.db import models


class Technician(models.Model):
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=150)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class RepairRequest(models.Model):
    CATEGORY_CHOICES = [
        ("Technology", "Technology / IT"),
        ("Furniture", "Furniture"),
        ("Electrical", "Electrical"),
        ("Plumbing", "Plumbing"),
        ("HVAC", "HVAC / Air Conditioning"),
        ("General", "General Building"),
    ]
    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=255)
    problem = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")
    image = models.ImageField(upload_to="repair_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="repair_requests")
    assigned_technician = models.ForeignKey(
        Technician,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_requests",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Ticket #{self.id}"


class RepairHistory(models.Model):
    repair_request = models.ForeignKey(RepairRequest, on_delete=models.CASCADE, related_name="history")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, blank=True)
    old_status = models.CharField(max_length=30, blank=True)
    new_status = models.CharField(max_length=30)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"History for Ticket #{self.repair_request_id}"
