from django.shortcuts import render,redirect,get_object_or_404
from restaurantapp.models import CategoryDB,TableDB, MenuItemDB, OrderDB, OrderItem
from twilio.rest import Client
import os
# Create your views here.



def menu_view(request, table_uuid):

    table = get_object_or_404(TableDB, unique_id=table_uuid)
    menu = MenuItemDB.objects.all()
    categories = CategoryDB.objects.all()
    popular_items = MenuItemDB.objects.filter(Availability=True)[:4]
    return render(request, 'menudisp.html', {
        'table': table,'menu':menu,'categories':categories,'popular_items':popular_items})


def order_review(request, table_uuid):
    table = get_object_or_404(TableDB, unique_id=table_uuid)

    if request.method == "POST":
        item_ids = request.POST.getlist('item_ids')
        order = OrderDB.objects.create(Table=table, Status="Draft")
        total = 0

        for item_id in item_ids:

            qty = int(request.POST.get(f'qty_{item_id}', 0))
            item = MenuItemDB.objects.get(id=item_id)
            if qty > 0 and item.Availability:

                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=qty,
                    price_at_order=item.Price
                )
                total += item.Price * qty


        order.Total_price = total
        order.save()

        return redirect('order_summary', table_uuid=table_uuid, order_id=order.id)


def order_summary(request, table_uuid, order_id):

    order = get_object_or_404(OrderDB, id=order_id, Table__unique_id=table_uuid)


    items = order.items.all()

    return render(request, "OrderReview.html", {
        "order": order,
        "items": items,
        "table_uuid": table_uuid
    })


def final_place_order(request, table_uuid, order_id):
    order = get_object_or_404(OrderDB, id=order_id, Table__unique_id=table_uuid)

    if request.method == "POST":

        order.Note = request.POST.get("note")

        order.Status = "Pending"
        phone = request.POST.get("phone_number")
        if not phone:

            return redirect('order_summary', table_uuid=table_uuid, order_id=order.id)
        order.save()

        # WHATSAPP MESSAGE


        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"Order Confirmed!\nOrder ID: {order.id}\nTotal: ₹{order.Total_price}",
            from_='whatsapp:+14155238886',
            to=f"whatsapp:{phone}"
        )

        print(message.sid)
        return redirect('order_status', table_uuid=table_uuid, order_id=order.id)


def order_status(request, table_uuid, order_id):

    order = get_object_or_404(OrderDB, id=order_id, Table__unique_id=table_uuid)

    return render(request, "order_status.html", {
        "order": order
    })
