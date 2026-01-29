from django.db import models

# Create your models here.
class User(models.Model):
  email = models.CharField(max_length= 30)
  password = models.CharField(max_length= 20)
  phone = models.CharField(max_length= 10)
  name = models.CharField(max_length= 40)

  def __str__(self):
    return self.name

class Restaurant(models.Model):
  name = models.CharField(max_length = 20)
  picture = models.URLField(max_length = 200, default='/delivery/images/default.jpg')
  cuisine = models.CharField(max_length = 200)
  address = models.CharField(max_length= 200, default= "No address provided")
  location = models.URLField(max_length= 300, default='https://maps.app.goo.gl/s635cY4K5dwBSeog7')
  rating = models.FloatField()

class Item(models.Model):
  restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name = "items")
  name = models.CharField(max_length = 20)
  description = models.CharField(max_length = 200)
  price = models.FloatField()
  vegeterian = models.BooleanField(default=False)
  picture = models.URLField(max_length = 400, default='https://www.indiafilings.com/learn/wp-content/uploads/2024/08/How-to-Start-Food-Business.jpg')

class Cart(models.Model):
  customer = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="cart"
  )

  def total_price(self):
    return sum(
      ci.item.price * ci.quantity
      for ci in self.items.all()
    )


class CartItem(models.Model):
  cart = models.ForeignKey(
    Cart,
    related_name="items",
    on_delete=models.CASCADE
  )
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)

  @property
  def total_price(self):
    return self.item.price * self.quantity

  class Meta:
    unique_together = ("cart", "item")



class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.name
