from django.shortcuts import render,get_object_or_404,redirect
from restaurantapp.models import *
from django.contrib.auth.models import User
# Create your views here.
from django.db.models import Q

def kitchen_dashboard(request):


    active_orders = OrderDB.objects.filter(
        Q(Status='Pending') | Q(Status='Cooking')
    ).order_by('Created_at')
    pending_cnt = OrderDB.objects.filter(Status="Pending").count()
    cooking_cnt = OrderDB.objects.filter(Status="Cooking").count()

    return render(request, "kitchen.html", {"orders": active_orders,
                                            "pending_cnt": pending_cnt,"cooking_cnt":cooking_cnt
                                            })


def update_status(request, order_id, new_status):
    if request.method == "POST":
        order = get_object_or_404(OrderDB, id=order_id)

        if new_status in ['Cooking', 'Done']:
            order.Status = new_status
            order.save()
    return redirect('kitchen_dashboard')