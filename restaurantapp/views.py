from django.shortcuts import render,redirect,get_object_or_404
from restaurantapp.models import CategoryDB,MenuItemDB,TableDB,OrderDB,OrderItem
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError


from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def dashboard(request):
    category = CategoryDB.objects.count()
    menu = MenuItemDB.objects.count()
    orders = OrderDB.objects.count()
    return render(request,"Dashboard.html",{"category":category,
                                            'menu':menu,"orders":orders})

def add_category(request):
    return render(request,"AddCategory.html")

def save_category(request):
    if request.method=="POST":
        category_name = request.POST.get("categoryname")
        description = request.POST.get("description")
        cat_img = request.FILES.get("image")
        is_active = True if request.POST.get("isactive") == "on" else False
        obj = CategoryDB(Category_Name=category_name,Description=description,
                         Image=cat_img,is_active=is_active)
        obj.save()
        messages.success(request, "Category saved successfully")
        return redirect(add_category)

def display_category(request):
    data = CategoryDB.objects.all()
    return render(request, "DisplayCategory.html",{'data':data})

def editcategory(request,c_id):
    data = CategoryDB.objects.get(id=c_id)
    return render(request,"EditCategory.html",{'data':data})

def updatecategory(request,cid):
    if request.method=="POST":
        category_name = request.POST.get("categoryname")
        description = request.POST.get("description")
        is_active = True if request.POST.get("isactive") == "on" else False
        try:
            img = request.FILES["image"]
            fs = FileSystemStorage()
            file = fs.save(img.name,img)
        except MultiValueDictKeyError:
            file = CategoryDB.objects.get(id=cid).Image
        CategoryDB.objects.filter(id=cid).update(Category_Name=category_name,Description=description,
                         Image=file,is_active=is_active)
        messages.success(request, "Category updated successfully")
        return redirect(display_category)


def deletecategory(request,cid):
    data = CategoryDB.objects.filter(id=cid)
    data.delete()
    messages.success(request, "Category deleted successfully")
    return redirect(display_category)
#----------------------MENU-------------------------------------------------------------
#-------------------------------------------------------------------------------------
def add_menu(request):
    categories = CategoryDB.objects.all()
    return render(request,"AddMenu.html",{'categories':categories})

def save_menu(request):
    if request.method=="POST":
        menu_name = request.POST.get("menuname")
        category = request.POST.get("menucategory")
        price = request.POST.get("price")
        description = request.POST.get("description")
        menu_img = request.FILES.get("menuimage")
        is_available= True if request.POST.get("available") == "on" else False
        obj = MenuItemDB(Name=menu_name,Category=category,Price=price,Short_Description=description,
                         Menu_Image=menu_img,Availability=is_available)
        obj.save()
        messages.success(request, "Menu Saved successfully")
        return redirect(add_menu)

def display_menu(request):
    data = MenuItemDB.objects.all()
    return render(request, "DisplayMenu.html",{'data':data})

def edit_menu(request,m_id):
    categories = CategoryDB.objects.all()
    data = MenuItemDB.objects.get(id=m_id)
    return render(request,"EditMenu.html",{'data':data,'categories':categories})

def update_menu(request,mid):
    if request.method=="POST":
        menu_name = request.POST.get("menuname")
        category = request.POST.get("menucategory")
        price = request.POST.get("price")
        description = request.POST.get("description")
        is_available = True if request.POST.get("available") == "on" else False
        try:
            img = request.FILES["menuimage"]
            fs = FileSystemStorage()
            file = fs.save(img.name,img)
        except MultiValueDictKeyError:
            file = MenuItemDB.objects.get(id=mid).Menu_Image
        MenuItemDB.objects.filter(id=mid).update(Name=menu_name,Category=category,Price=price,Short_Description=description,
                         Menu_Image=file,Availability=is_available)
        messages.success(request, "Menu updated successfully")
        return redirect(display_menu)

def deletemenu(request,mid):
    data = MenuItemDB.objects.filter(id=mid)
    data.delete()
    messages.success(request, "Menu Deleted successfully")
    return redirect(display_menu)

def add_table(request):
    return render(request,"AddTable.html")

def save_table(request):
    if request.method=="POST":
        table_number = request.POST.get("tableno")

        obj = TableDB(number=table_number)
        obj.save()
        messages.success(request, "Table Added!")
        return redirect(add_table)

def display_table(request):
    data = TableDB.objects.all()
    return render(request, "DisplayTable.html",{'data':data})

def edit_table(request,t_id):
    data = TableDB.objects.get(id=t_id)
    return render(request,"EditTable.html",{'data':data})

def update_table(request,tid):
    if request.method=="POST":
        table_number = request.POST.get("tableno")

        TableDB.objects.filter(id=tid).update(number=table_number)
        messages.success(request, "Table updated successfully")
        return redirect(display_table)

def delete_table(request,tid):
    data = TableDB.objects.filter(id=tid)
    data.delete()
    messages.success(request, "Table Deleted ")
    return redirect(display_table)


########################
#################KITCHEN


def kitchen_dashboard(request):
    # Get all orders that are actually placed (not drafts)
    # and sort by the oldest first
    active_orders = OrderDB.objects.filter(Status="Pending").order_by('id')

    return render(request, "kitchen.html", {"orders": active_orders})


def complete_order(request, order_id):
    order = get_object_or_404(OrderDB, id=order_id)
    order.Status = "Completed"
    order.save()
    return redirect('kitchen_dashboard')


def admin_login_page(request):
    return render(request,"Login.html")


def admin_login(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        pswd = request.POST.get("password")
        if not uname or not pswd:
            messages.error(request, "Username and Password are required")
            return redirect('login')
        user = authenticate(request, username=uname, password=pswd)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")

            if user.is_superuser or user.is_staff:
                return redirect('dashboard')
            elif user.groups.filter(name='Kitchen').exists():
                return redirect('kitchen_dashboard')

        else:
            messages.error(request, "Incorrect Username or Password")
            return redirect('login')

    return render(request, "login.html")


def add_staff(request):
    return render(request,"AddStaff.html")

def save_staff(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")

        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already exists")
            return redirect('add_staff')

        new_user = User.objects.create_user(username=u, password=p)
        kitchen_group = Group.objects.get(name='Kitchen')
        new_user.groups.add(kitchen_group)
        messages.success(request, "Staff added successfully")
        return redirect('dashboard')

def admin_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')

def order_display(request):
    data = OrderDB.objects.all().order_by('Created_at')
    price = OrderItem.objects.all()
    return render(request,"DisplayOrder.html",{"data": data,"price":price})

def display_staff(request):
    staff = User.objects.filter(groups__name='Kitchen')
    return render(request, "DisplayStaff.html",{'staff':staff})


def edit_staff(request, sid):
    staff = User.objects.get(id=sid)
    return render(request, "EditStaff.html",{'staff':staff})


def update_staff(request, sid):
    if request.method == "POST":
        staff = User.objects.get(id=sid)

        staff.username = request.POST.get("username")
        staff.is_active = True if request.POST.get("active") else False

        new_password = request.POST.get("password")
        if new_password:
            staff.set_password(new_password)

        staff.save()

        messages.success(request, "Staff updated successfully")
        return redirect(display_staff)

def delete_staff(request,s_id):
    data = User.objects.filter(id=s_id)
    data.delete()
    messages.success(request, "Staff Deleted successfully")
    return redirect(display_staff)
