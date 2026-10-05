from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("add-request/", views.add_request, name="add_request"),
    path("update-status/<int:request_id>/", views.update_status, name="update_status"),
    path("assign-technician/<int:request_id>/", views.assign_technician, name="assign_technician"),
    path("delete-request/<int:request_id>/", views.delete_request, name="delete_request"),
    path("request/<int:request_id>/", views.request_detail, name="request_detail"),
    path("history/", views.history_list, name="history_list"),
    path("technicians/", views.technician_list, name="technician_list"),
    path("technicians/add/", views.technician_add, name="technician_add"),
    path("technicians/<int:technician_id>/edit/", views.technician_edit, name="technician_edit"),
    path("technicians/<int:technician_id>/delete/", views.technician_delete, name="technician_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_add, name="category_add"),
    path("categories/<int:category_id>/edit/", views.category_edit, name="category_edit"),
    path("categories/<int:category_id>/delete/", views.category_delete, name="category_delete"),
]
