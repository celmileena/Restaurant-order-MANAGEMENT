from django.urls import path
from restaurantapp import views

urlpatterns = [
    path('dashboard/',views.dashboard,name="dashboard"),
    path('add_category/',views.add_category,name="add_category"),
    path('save_category/',views.save_category,name="save_category"),
    path('display_category/',views.display_category,name="display_category"),
    path('editcategory/<int:c_id>/',views.editcategory,name="editcategory"),
    path('updatecategory/<int:cid>/',views.updatecategory,name="updatecategory"),
    path('deletecategory/<int:cid>/',views.deletecategory,name="deletecategory"),

    path('add_menu/',views.add_menu,name="add_menu"),
    path('save_menu/',views.save_menu,name="save_menu"),
    path('display_menu/',views.display_menu,name="display_menu"),
    path('edit_menu/<int:m_id>/',views.edit_menu,name="edit_menu"),
    path('update_menu/<int:mid>/',views.update_menu,name="update_menu"),
    path('deletemenu/<int:mid>/',views.deletemenu,name="deletemenu"),
    path('addtable/',views.add_table,name="addtable"),
    path('savetable/',views.save_table,name="savetable"),
    path('displaytable/',views.display_table,name="displaytable"),

    path('edittable/<int:t_id>',views.edit_table,name="edittable"),
    path('updatetable/<int:tid>',views.update_table,name="updatetable"),
    path('deletetable/<int:tid>',views.delete_table,name="deletetable"),
    path('', views.admin_login_page, name='login'),
    path('loginview/', views.admin_login, name='loginview'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('save_staff/', views.save_staff, name='save_staff'),
    path('display_staff/', views.display_staff, name='display_staff'),
    path('edit_staff/<int:sid>/', views.edit_staff, name='edit_staff'),
    path('update_staff/<int:sid>/', views.update_staff, name='update_staff'),
    path('delete_staff/<int:s_id>/', views.delete_staff, name='delete_staff'),
path('logout/', views.admin_logout, name='logout'),
path('order_display/', views.order_display, name='order_display'),
]