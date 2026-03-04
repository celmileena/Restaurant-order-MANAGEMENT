from django.db import models
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

# Create your models here.
class CategoryDB(models.Model):
    Category_Name = models.CharField(max_length=100,blank=True ,null=True)
    Description = models.TextField(blank=True, null=True)
    Image = models.ImageField(upload_to='category_image/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

class MenuItemDB(models.Model):
    Name = models.CharField(max_length=100,blank=True ,null=True)
    Category = models.CharField(max_length=100,blank=True ,null=True)
    Price = models.DecimalField(max_digits=8, decimal_places=2)
    Short_Description = models.TextField(blank=True, null=True)
    Menu_Image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    Availability = models.BooleanField(default=True)


class TableDB(models.Model):
    number = models.IntegerField(unique=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr_data = f"http://192.168.29.192:8000/restaurantQR/menu/{self.unique_id}/"

            # 2. Generate the QR image
            qr = qrcode.make(qr_data).resize((298, 298))
            canvas = Image.new('RGB', (298, 298), 'white')
            canvas.paste(qr, (0, 0))

            buffer = BytesIO()
            canvas.save(buffer, 'PNG')

            fname = f'qr-{self.unique_id}.png'
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
        super().save(*args, **kwargs)


class OrderDB(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Cooking', 'Cooking'),
        ('Done', 'Done'),
    )
    Table = models.ForeignKey(TableDB, on_delete=models.CASCADE)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    Total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Added this
    Created_at = models.DateTimeField(auto_now_add=True)
    Note = models.CharField(max_length=200,blank=True,null=True)

    # We removed 'items' from here and moved it to the bridge table below


class OrderItem(models.Model):
    order = models.ForeignKey(OrderDB, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItemDB, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Crucial for multiple items
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)  # Keeps history accurate

