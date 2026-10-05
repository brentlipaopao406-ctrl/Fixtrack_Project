from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, LoginForm, TechnicianForm
from .models import Category, RepairHistory, RepairRequest, Technician


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_authenticated and user.is_staff)(view_func)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html", {"form": form})


@login_required
def home(request):
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "")
    requests = RepairRequest.objects.select_related("reporter", "assigned_technician")
    if query:
        requests = requests.filter(
            Q(location__icontains=query)
            | Q(problem__icontains=query)
            | Q(category__icontains=query)
            | Q(status__icontains=query)
            | Q(priority__icontains=query)
            | Q(reporter__username__icontains=query)
            | Q(assigned_technician__name__icontains=query)
        )
    if sort == "priority":
        requests = requests.order_by("priority", "-created_at")
    stats = RepairRequest.objects.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status="Pending")),
        progress=Count("id", filter=Q(status="In Progress")),
        completed=Count("id", filter=Q(status="Completed")),
        cancelled=Count("id", filter=Q(status="Cancelled")),
    )
    context = {
        "requests": requests,
        "search_query": query,
        "technicians": Technician.objects.filter(is_active=True),
        "categories": Category.objects.filter(is_active=True),
        "total_requests": stats["total"],
        "pending_requests": stats["pending"],
        "in_progress_requests": stats["progress"],
        "completed_requests": stats["completed"],
        "cancelled_requests": stats["cancelled"],
    }
    return render(request, "dashboard.html", context)


@login_required
def add_request(request):
    if request.method != "POST":
        return redirect("home")
    category = request.POST.get("category", "").strip()
    priority = request.POST.get("priority", "").strip()
    location = request.POST.get("location", "").strip()
    problem = request.POST.get("problem", "").strip()
    valid_categories = set(Category.objects.filter(is_active=True).values_list("name", flat=True))
    if category not in valid_categories:
        messages.error(request, "Please select a valid category.")
        return redirect("home")
    if priority not in {"High", "Medium", "Low"} or not location or not problem:
        messages.error(request, "Please complete all required fields.")
        return redirect("home")
    obj = RepairRequest.objects.create(
        category=category,
        priority=priority,
        location=location,
        problem=problem,
        reporter=request.user,
        image=request.FILES.get("image"),
    )
    RepairHistory.objects.create(
        repair_request=obj,
        changed_by=request.user,
        old_status="",
        new_status="Pending",
        notes="Repair request created.",
    )
    messages.success(request, f"Repair ticket #{obj.id} created successfully.")
    return redirect("home")


@staff_required
def update_status(request, request_id):
    obj = get_object_or_404(RepairRequest, id=request_id)
    if request.method == "POST":
        new_status = request.POST.get("status", "").strip()
        notes = request.POST.get("notes", "").strip()
        valid = {choice[0] for choice in RepairRequest.STATUS_CHOICES}
        if new_status not in valid:
            messages.error(request, "Invalid status.")
            return redirect("home")
        old_status = obj.status
        obj.status = new_status
        obj.save(update_fields=["status"])
        if old_status != new_status or notes:
            RepairHistory.objects.create(
                repair_request=obj,
                changed_by=request.user,
                technician=obj.assigned_technician,
                old_status=old_status,
                new_status=new_status,
                notes=notes or f"Status changed from {old_status} to {new_status}.",
            )
        messages.success(request, f"Ticket #{obj.id} updated.")
    return redirect("home")


@staff_required
def assign_technician(request, request_id):
    obj = get_object_or_404(RepairRequest, id=request_id)
    if request.method == "POST":
        technician_id = request.POST.get("technician") or None
        technician = get_object_or_404(Technician, id=technician_id, is_active=True) if technician_id else None
        obj.assigned_technician = technician
        obj.save(update_fields=["assigned_technician"])
        label = technician.name if technician else "Unassigned"
        RepairHistory.objects.create(
            repair_request=obj,
            changed_by=request.user,
            technician=technician,
            old_status=obj.status,
            new_status=obj.status,
            notes=f"Technician assignment changed to {label}.",
        )
        messages.success(request, f"Ticket #{obj.id} assigned to {label}.")
    return redirect("home")


@staff_required
def delete_request(request, request_id):
    obj = get_object_or_404(RepairRequest, id=request_id)
    if request.method == "POST":
        ticket = obj.id
        obj.delete()
        messages.success(request, f"Ticket #{ticket} deleted.")
    return redirect("home")


@login_required
def request_detail(request, request_id):
    obj = get_object_or_404(RepairRequest.objects.select_related("reporter", "assigned_technician"), id=request_id)
    history = obj.history.select_related("changed_by", "technician")
    return render(request, "requests/request_detail.html", {"repair_request": obj, "history": history})


@staff_required
def history_list(request):
    entries = RepairHistory.objects.select_related("repair_request", "changed_by", "technician")
    return render(request, "requests/history_list.html", {"history": entries})


@staff_required
def technician_list(request):
    technicians = Technician.objects.annotate(request_count=Count("assigned_requests")).order_by("name")
    return render(request, "technicians/list.html", {"technicians": technicians})


@staff_required
def technician_add(request):
    form = TechnicianForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Technician added successfully.")
        return redirect("technician_list")
    return render(request, "technicians/form.html", {"form": form, "title": "Add Technician"})


@staff_required
def technician_edit(request, technician_id):
    obj = get_object_or_404(Technician, id=technician_id)
    form = TechnicianForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Technician updated successfully.")
        return redirect("technician_list")
    return render(request, "technicians/form.html", {"form": form, "title": "Edit Technician", "technician": obj})


@staff_required
def technician_delete(request, technician_id):
    obj = get_object_or_404(Technician, id=technician_id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Technician deleted.")
        return redirect("technician_list")
    return render(request, "technicians/confirm_delete.html", {"object": obj, "kind": "technician"})


@staff_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, "categories/list.html", {"categories": categories})


@staff_required
def category_add(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category added successfully.")
        return redirect("category_list")
    return render(request, "categories/form.html", {"form": form, "title": "Add Category"})


@staff_required
def category_edit(request, category_id):
    obj = get_object_or_404(Category, id=category_id)
    form = CategoryForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully.")
        return redirect("category_list")
    return render(request, "categories/form.html", {"form": form, "title": "Edit Category", "category": obj})


@staff_required
def category_delete(request, category_id):
    obj = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Category deleted.")
        return redirect("category_list")
    return render(request, "categories/confirm_delete.html", {"object": obj, "kind": "category"})
