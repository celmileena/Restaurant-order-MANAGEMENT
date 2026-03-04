from django.urls import path
from qrmenuapp import views

urlpatterns = [
    path('menu/<uuid:table_uuid>/', views.menu_view, name='menu'),

path('review/<uuid:table_uuid>/', views.order_review, name='order_review'),


    path('summary/<uuid:table_uuid>/<int:order_id>/', views.order_summary, name='order_summary'),


    path('confirm/<uuid:table_uuid>/<int:order_id>/', views.final_place_order, name='final_place_order'),
path('status/<uuid:table_uuid>/<int:order_id>/', views.order_status, name='order_status'),
]
