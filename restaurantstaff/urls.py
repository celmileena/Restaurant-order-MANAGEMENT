from django.urls import path
from restaurantstaff import views

urlpatterns = [

# This will be accessed at /staff/dashboard/
    path('dashboard/', views.kitchen_dashboard, name='kitchen_dashboard'),

    # This will be accessed at /staff/complete/5/
    path('update-status/<int:order_id>/<str:new_status>/', views.update_status, name='update_status'),
    ]

